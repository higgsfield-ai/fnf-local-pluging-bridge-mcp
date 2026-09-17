#!/usr/bin/env python3
"""Verify/install bundled bundled HF-Astra-Looks using only Python stdlib.

Dry-run is the default. --apply requires an explicit --lut-dir and never
overwrites different files. This script does not launch or connect to Resolve.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sys

PACKAGE_NAME = "HF-Astra-Looks"
DCTL_NAME = "HF-Astra-Looks.dctl"
DATA_NAME = "ASTRA_LookMixer_Data"
LUT_NAMES = ("ektachrome.cube", "portra.cube", "vision2.cube", "vision3d.cube", "vision3t.cube")
BUNDLED_DCTL_SHA256 = "1b2736d56567274708a0ff10156c93a34521e4955f776612a2f10fa6d0fe4603"
DEFAULT_SOURCE = Path(__file__).resolve().parents[1] / "assets" / PACKAGE_NAME
INSTALL_PATHS = ("DCTL/" + DCTL_NAME,) + tuple("DCTL/" + DATA_NAME + "/" + name for name in LUT_NAMES)


class InstallError(Exception):
    """Expected package, path or conflict error; no silent overwrite."""


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_relative(value):
    if not isinstance(value, str) or "\\" in value or ":" in value:
        raise InstallError("Invalid manifest relative path: " + repr(value))
    relative = PurePosixPath(value)
    if relative.is_absolute() or not relative.parts or any(p in (".", "..") for p in relative.parts):
        raise InstallError("Unsafe manifest relative path: " + value)
    if str(relative) != value:
        raise InstallError("Noncanonical manifest relative path: " + value)
    return relative


def reject_child_symlinks(root, relative):
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise InstallError("Refusing symlink inside source/destination: " + str(current))


def verify_source(source):
    source = Path(source).expanduser().resolve()
    manifest_path = source / "manifest.json"
    if not source.is_dir() or not manifest_path.is_file():
        raise InstallError("Missing bundled source or manifest: " + str(source))
    if manifest_path.is_symlink():
        raise InstallError("Manifest must be a regular nonsymlink file")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise InstallError("Invalid manifest JSON: " + str(exc)) from exc
    if not isinstance(manifest, dict) or manifest.get("name") != PACKAGE_NAME:
        raise InstallError("Manifest is not the bundled HF-Astra-Looks package")
    if manifest.get("dctl") != "DCTL/" + DCTL_NAME or manifest.get("required_luts") != 5:
        raise InstallError("Unexpected bundled DCTL/dependency contract")
    if manifest.get("source_dctl_sha256") != BUNDLED_DCTL_SHA256:
        raise InstallError("Manifest does not identify the supplied bundled DCTL")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise InstallError("Manifest has no payload file records")
    verified = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise InstallError("Invalid manifest file record")
        relative = safe_relative(entry.get("path"))
        name = str(relative)
        if name in verified:
            raise InstallError("Duplicate manifest path: " + name)
        expected_hash = entry.get("sha256")
        expected_bytes = entry.get("bytes")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise InstallError("Invalid SHA-256 record: " + name)
        if type(expected_bytes) is not int or expected_bytes < 0:
            raise InstallError("Invalid byte-size record: " + name)
        reject_child_symlinks(source, relative)
        file = source.joinpath(*relative.parts)
        if not file.is_file():
            raise InstallError("Missing source payload: " + str(file))
        if file.stat().st_size != expected_bytes or sha256(file) != expected_hash:
            raise InstallError("Source manifest verification failed: " + name)
        verified[name] = entry
    missing = set(INSTALL_PATHS) - set(verified)
    if missing:
        raise InstallError("Manifest lacks required bundled payload: " + ", ".join(sorted(missing)))
    if verified["DCTL/" + DCTL_NAME]["sha256"] != BUNDLED_DCTL_SHA256:
        raise InstallError("Bundled DCTL payload hash differs")
    # Verify every manifest file, including parameters/SUMMARY, but install only
    # the DCTL and its five declared sibling LUT dependencies.
    return source, verified


def destination_state(destination, entry):
    if not destination.exists():
        return "create"
    if not destination.is_file():
        raise InstallError("Destination conflict (not a regular file): " + str(destination))
    if destination.stat().st_size != entry["bytes"] or sha256(destination) != entry["sha256"]:
        raise InstallError("Destination conflict; refusing overwrite: " + str(destination))
    return "identical"


def install(source, lut_dir, apply=False):
    source, verified = verify_source(source)
    lut_root = Path(lut_dir).expanduser().resolve()
    if lut_root.exists() and not lut_root.is_dir():
        raise InstallError("Selected LUT root is not a directory: " + str(lut_root))
    target = lut_root / PACKAGE_NAME
    planned = []
    # All known conflicts are checked before creating directories or files.
    for name in INSTALL_PATHS:
        relative = PurePosixPath(PACKAGE_NAME) / PurePosixPath(name).relative_to("DCTL")
        reject_child_symlinks(lut_root, relative)
        destination = lut_root.joinpath(*relative.parts)
        for parent in destination.parents:
            if parent == lut_root:
                break
            if parent.exists() and not parent.is_dir():
                raise InstallError("Destination parent is not a directory: " + str(parent))
        state = destination_state(destination, verified[name])
        planned.append((name, destination, state))
    written = 0
    result_files = []
    for name, destination, state in planned:
        if apply:
            relative = destination.relative_to(lut_root)
            reject_child_symlinks(lut_root, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Recheck an existing file rather than trusting a stale plan.
            if destination.exists():
                state = destination_state(destination, verified[name])
            else:
                try:
                    with destination.open("xb") as output, (source / name).open("rb") as input_file:
                        shutil.copyfileobj(input_file, output, 1024 * 1024)
                except FileExistsError:
                    # A concurrent identical installation is harmless; a
                    # different file remains a conflict and is never replaced.
                    state = destination_state(destination, verified[name])
                else:
                    if destination_state(destination, verified[name]) != "identical":
                        raise InstallError("Written file failed verification: " + str(destination))
                    state = "installed"
                    written += 1
        result_files.append({"source": name, "destination": str(destination), "status": state,
                             "sha256": verified[name]["sha256"]})
    return {"mode": "apply" if apply else "dry-run", "source": str(source),
            "lut_root": str(lut_root), "install_directory": str(target),
            "manifest_payloads_verified": len(verified), "files_written": written,
            "files": result_files,
            "resolve_action": "None. Refresh the LUT list and native-test the DCTL separately."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lut-dir", type=Path, required=True,
                        help="Explicit Resolve LUT root. Installs in its HF-Astra-Looks subdirectory.")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE,
                        help="Bundled source package; defaults to bundled assets/HF-Astra-Looks.")
    parser.add_argument("--apply", action="store_true", help="Write verified missing files. Default is dry-run.")
    args = parser.parse_args(argv)
    try:
        result = install(args.source_dir, args.lut_dir, apply=args.apply)
    except (InstallError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
