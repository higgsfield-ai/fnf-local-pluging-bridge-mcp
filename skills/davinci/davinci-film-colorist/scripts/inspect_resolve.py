#!/usr/bin/env python3
"""Read the current Resolve context without changing the application or project.

Uses only the vendor's documented getters. The CLI supervises one child with a
timeout, using temporary transport/phase files and an optional new JSON output.
No GUI interaction, preference changes, app launch,
version switching, media import, grading, or network setup occurs.
"""

import argparse
import importlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone


SETTINGS = (
    "colorScienceMode", "isAutoColorManage", "separateColorSpaceAndGamma",
    "colorSpaceInput", "colorSpaceInputGamma",
    "colorSpaceTimeline", "colorSpaceTimelineGamma",
    "colorSpaceOutput", "colorSpaceOutputGamma",
    "inputDRT", "outputDRT", "colorAcesIDT", "colorAcesODT",
    "colorAcesGamutCompressType", "colorSpaceOutputToneMapping",
    "colorSpaceOutputGamutMapping", "colorSpaceOutputToneLuminanceMax",
    "timelineWorkingLuminance", "timelineWorkingLuminanceMode",
    "useColorSpaceAwareGradingTools", "videoDataLevels", "nodeStackLayers",
)
CLIP_PROPERTIES = (
    "Camera Manufacturer", "Camera Type", "Color Space Notes", "Gamma Notes",
    "Input Color Space", "Input Gamma", "Video Codec", "Format", "Bit Depth",
    "Resolution", "FPS", "Data Level", "RAW", "ISO",
    "White Point (Kelvin)", "White Balance Tint",
)
METADATA = (
    "Camera Manufacturer", "Camera Type", "Color Space Notes", "Gamma Notes",
    "ISO", "White Point (Kelvin)", "White Balance Tint",
)


class SnapshotError(Exception):
    def __init__(self, code, stage, message):
        super().__init__(message)
        self.code = code
        self.stage = stage


def runtime_preflight():
    """Check SDK prerequisites, without claiming native library compatibility."""
    if sys.version_info[:2] < (3, 6):
        raise SnapshotError("PYTHON_UNSUPPORTED", "runtime",
                            "Для helper требуется Python 3.6 или новее.")
    bits = struct.calcsize("P") * 8
    if bits != 64:
        raise SnapshotError("PYTHON_BITNESS_UNSUPPORTED", "runtime",
                            f"Интерпретатор {bits}-битный; SDK требует 64-битный Python.")


def output_preflight(output):
    """Validate the requested report path before any vendor import."""
    if output is None:
        return
    if output.suffix.lower() != ".json":
        raise SnapshotError("OUTPUT_SUFFIX_INVALID", "output_preflight",
                            "Укажите новый файл с расширением .json.")
    try:
        parent_info = output.parent.stat()
    except FileNotFoundError as exc:
        raise SnapshotError("OUTPUT_PARENT_MISSING", "output_preflight",
                            "Папка отчёта не найдена; выберите существующую папку или stdout.") from exc
    except NotADirectoryError as exc:
        raise SnapshotError("OUTPUT_PARENT_NOT_DIRECTORY", "output_preflight",
                            "Родительский путь отчёта не является папкой.") from exc
    except OSError as exc:
        raise SnapshotError("OUTPUT_PRECHECK_FAILED", "output_preflight",
                            "Не удалось проверить папку отчёта.") from exc
    if not stat.S_ISDIR(parent_info.st_mode):
        raise SnapshotError("OUTPUT_PARENT_NOT_DIRECTORY", "output_preflight",
                            "Родительский путь отчёта не является папкой.")
    try:
        output.lstat()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise SnapshotError("OUTPUT_PRECHECK_FAILED", "output_preflight",
                            "Не удалось проверить путь отчёта.") from exc
    else:
        raise SnapshotError("OUTPUT_EXISTS", "output_preflight",
                            "Путь отчёта уже существует; укажите новое имя.")


def module_roots():
    """Locate configured or standard vendor directories without changing them."""
    roots = []
    if os.environ.get("RESOLVE_SCRIPT_API"):
        roots.append(Path(os.environ["RESOLVE_SCRIPT_API"]).expanduser())
    if sys.platform == "darwin":
        roots.append(Path("/Library/Application Support/Blackmagic Design/"
                          "DaVinci Resolve/Developer/Scripting"))
    elif sys.platform.startswith("win"):
        roots.append(Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) /
                     "Blackmagic Design" / "DaVinci Resolve" / "Support" /
                     "Developer" / "Scripting")
    elif sys.platform.startswith("linux"):
        roots.extend((Path("/opt/resolve/Developer/Scripting"),
                      Path("/home/resolve/Developer/Scripting")))
    return roots


def load_resolve_module():
    """Find the installed official wrapper; never copy or install vendor code."""
    runtime_preflight()
    try:
        roots = module_roots()
    except Exception as exc:
        raise SnapshotError("WRAPPER_DISCOVERY_FAILED", "wrapper_discovery",
                            "Не удалось определить каталоги официального wrapper.") from exc
    # Process-local module discovery only. Do not write .pyc into vendor folders.
    sys.dont_write_bytecode = True
    for root in roots:
        for modules in (root / "Modules", root):
            try:
                found = (modules / "DaVinciResolveScript.py").is_file()
            except OSError as exc:
                raise SnapshotError("WRAPPER_DISCOVERY_FAILED", "wrapper_discovery",
                                    "Не удалось проверить каталог официального wrapper.") from exc
            if found:
                sys.path.insert(0, str(modules))
                try:
                    return importlib.import_module("DaVinciResolveScript")
                except Exception as exc:
                    raise SnapshotError(
                        "WRAPPER_IMPORT_FAILED", "wrapper_import",
                        "Файл wrapper найден, но импорт не выполнен; причина совместимости не установлена."
                    ) from exc
    # Also support an interpreter whose official module path is already configured.
    try:
        return importlib.import_module("DaVinciResolveScript")
    except ModuleNotFoundError as exc:
        if exc.name != "DaVinciResolveScript":
            raise SnapshotError("WRAPPER_IMPORT_FAILED", "wrapper_import",
                                "Импорт wrapper не выполнен; отсутствующий компонент не определяет совместимость SDK.") from exc
        raise SnapshotError(
            "WRAPPER_NOT_FOUND", "wrapper_import",
            "Wrapper не найден в проверенных каталогах и пути импорта. Проверьте RESOLVE_SCRIPT_API официальной установки."
        ) from exc
    except Exception as exc:
        raise SnapshotError("WRAPPER_IMPORT_FAILED", "wrapper_import",
                            "Импорт wrapper не выполнен; причина совместимости не установлена.") from exc


def simple(value):
    """Reject unexpected bulk objects instead of serializing their contents."""
    return value if value is None or isinstance(value, (str, int, float, bool)) else None


def read(obj, method, *args):
    if obj is None:
        return None
    try:
        return getattr(obj, method)(*args)
    except Exception:
        return None


def checked_read(obj, method, *args):
    """Keep a failed getter distinct from a successful result of None."""
    if obj is None:
        return False, None, "missing_context"
    try:
        getter = getattr(obj, method)
    except Exception:
        return False, None, "method_unavailable"
    if not callable(getter):
        return False, None, "method_unavailable"
    try:
        return True, getter(*args), None
    except Exception:
        return False, None, "getter_failed"


def fields(obj, method, keys):
    return {key: simple(read(obj, method, key)) for key in keys}


def basename_only(value):
    if not isinstance(value, str) or not value:
        return None
    return value.replace("\\", "/").rsplit("/", 1)[-1]


def empty_graph(status, reason):
    return {"status": status, "reason": reason, "node_count": None, "nodes": None}


def graph_snapshot(graph):
    count_ok, count, error = checked_read(graph, "GetNumNodes")
    if not count_ok:
        return empty_graph("unknown", error)
    # bool is an int subclass in Python, but is not a node count.
    if type(count) is not int or count < 0:
        return empty_graph("unknown", "invalid_node_count")
    nodes = []
    details_known = True
    for index in range(1, count + 1):
        lut_ok, lut, _ = checked_read(graph, "GetLUT", index)
        tools_ok, tools, _ = checked_read(graph, "GetToolsInNode", index)
        lut_known = lut_ok and isinstance(lut, str)
        tools_known = (tools_ok and isinstance(tools, list)
                       and all(isinstance(name, str) for name in tools))
        details_known = details_known and lut_known and tools_known
        nodes.append({
            "index": index,
            "lut_filename": basename_only(lut),
            "lut_status": ("none_reported" if lut == "" else
                           "reported" if isinstance(lut, str) and lut else
                           "unavailable_or_none"),
            "lut_path_omitted": isinstance(lut, str) and ("/" in lut or "\\" in lut),
            "tool_names": ([name for name in tools if isinstance(name, str)]
                           if isinstance(tools, list) else None),
            "tools_status": "ok" if tools_known else "unknown",
        })
    return {"status": "ok" if details_known else "unknown",
            "reason": None if details_known else "node_details_unavailable",
            "node_count": count, "nodes": nodes}


def scoped_graph_snapshot(owner, method, *args, missing_reason="missing_context"):
    if owner is None:
        return empty_graph("unknown", missing_reason)
    ok, graph, error = checked_read(owner, method, *args)
    if not ok:
        return empty_graph("unknown", error)
    if graph is None:
        return empty_graph("unknown", "graph_not_returned")
    return graph_snapshot(graph)


def color_group_snapshot(item, missing_reason="no_current_video_item"):
    """Inspect only the current item's group; never assign or switch a group."""
    result = {
        "status": "unknown",
        "reason": missing_reason,
        "name": None,
        "name_status": "unknown",
        "pre_clip_node_graph": empty_graph("unknown", missing_reason),
        "post_clip_node_graph": empty_graph("unknown", missing_reason),
    }
    if item is None:
        return result
    ok, group, error = checked_read(item, "GetColorGroup")
    if not ok:
        result["reason"] = error
        result["pre_clip_node_graph"] = empty_graph("unknown", error)
        result["post_clip_node_graph"] = empty_graph("unknown", error)
        return result
    if group is None:
        # This status requires an actual successful GetColorGroup call.
        result.update(status="not_applicable", reason="no_group_returned",
                      name_status="not_applicable")
        result["pre_clip_node_graph"] = empty_graph("not_applicable", "no_group_returned")
        result["post_clip_node_graph"] = empty_graph("not_applicable", "no_group_returned")
        return result
    if isinstance(group, (str, bytes, int, float, bool, list, tuple, dict, set)):
        result["reason"] = "invalid_group_returned"
        result["pre_clip_node_graph"] = empty_graph("unknown", "invalid_group_returned")
        result["post_clip_node_graph"] = empty_graph("unknown", "invalid_group_returned")
        return result
    name_ok, name, _ = checked_read(group, "GetName")
    result.update(status="ok", reason=None,
                  name=name if name_ok and isinstance(name, str) else None,
                  name_status="ok" if name_ok and isinstance(name, str) else "unknown")
    result["pre_clip_node_graph"] = scoped_graph_snapshot(group, "GetPreClipNodeGraph")
    result["post_clip_node_graph"] = scoped_graph_snapshot(group, "GetPostClipNodeGraph")
    return result


def current_context(resolve):
    """Preserve unknown reads separately from a successful absent context."""
    context = dict.fromkeys(("project_manager", "project", "timeline", "item"))
    context.update(status="ok", reason=None)
    owner = resolve
    for stage, getter, absent_status in (
        ("project_manager", "GetProjectManager", "unknown"),
        ("project", "GetCurrentProject", "no_current_project"),
        ("timeline", "GetCurrentTimeline", "no_current_timeline"),
        ("item", "GetCurrentVideoItem", "no_current_video_item"),
    ):
        ok, value, error = checked_read(owner, getter)
        if not ok:
            context.update(status="unknown", reason=f"{stage}.{getter}:{error}")
            break
        if value is None:
            context.update(status=absent_status,
                           reason="project_manager_not_returned" if stage == "project_manager"
                           else absent_status)
            break
        if isinstance(value, (str, bytes, int, float, bool, list, tuple, dict, set)):
            context.update(status="unknown", reason=f"{stage}.{getter}:invalid_context_returned")
            break
        context[stage] = value
        owner = value
    return context


def snapshot(resolve):
    # This review copy is scoped to the Color page by the current task.
    page_ok, page, page_error = checked_read(resolve, "GetCurrentPage")
    if not page_ok or not isinstance(page, str) or not page or page != "color":
        available_page = page_ok and isinstance(page, str) and bool(page)
        return {
            "schema": "film-colorist-readonly-snapshot-2",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "not_color_page" if available_page else "page_unavailable",
            "current_page": page if available_page else None,
            "reason": "color_page_required" if available_page else page_error or "page_not_returned",
            "limitations": [
                "This review copy only reads Color context. No project context was queried "
                "because the current page could not be confirmed as color.",
            ],
        }
    context = current_context(resolve)
    project, timeline, item = (context[key] for key in ("project", "timeline", "item"))
    media = read(item, "GetMediaPoolItem")
    project_settings = fields(project, "GetSetting", SETTINGS) if project else None
    data = {
        "schema": "film-colorist-readonly-snapshot-2",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": context["status"],
        "reason": context["reason"],
        "current_page": page,
        "project_name": simple(read(project, "GetName")),
        "timeline_name": simple(read(timeline, "GetName")),
        "current_clip_name": basename_only(read(item, "GetName")),
        "current_timecode": simple(read(timeline, "GetCurrentTimecode")),
        "project_color_settings": project_settings,
        "timeline_color_settings": fields(timeline, "GetSetting", SETTINGS) if timeline else None,
        "clip_properties": fields(media, "GetClipProperty", CLIP_PROPERTIES) if media else None,
        "camera_metadata": fields(media, "GetMetadata", METADATA) if media else None,
        "raw_decode_output": {
            "status": "unknown",
            "reason": "No documented effective Camera RAW decode-output getter "
                      "is used by this helper. Source metadata and assigned input "
                      "color space do not establish the signal entering a CST node.",
        },
        "grade_versions": None,
        "clip_node_graphs": [],
        "timeline_node_graph": scoped_graph_snapshot(
            timeline, "GetNodeGraph", missing_reason=context["reason"]),
        "color_group": color_group_snapshot(item, missing_reason=context["reason"]),
        "limitations": [
            "Read-only API snapshot; no application page, preference, or project was changed.",
            "Null means unavailable, unsupported, or no value; it does not mean zero or disabled.",
            "Current-context status no_current_* requires a successful getter returning None. "
            "Failed, unavailable, or invalid context getters remain unknown; reason identifies "
            "the upstream stage. Available earlier context and its graphs are still read.",
            "Setting values may include inactive controls. Interpret them with colorScienceMode "
            "and separateColorSpaceAndGamma; do not combine them into an invented pipeline.",
            "Clip layers, the current timeline graph, and the current clip's group pre/post "
            "graphs are queried. Graph connections, node enabled state, monitor transforms, "
            "and arbitrary OFX parameters are not fully described; absent LUTs do not prove "
            "the absence of color transforms.",
            "Graph status is unknown if its object, count, or LUT/tool details cannot be read "
            "as documented. Known partial values are retained. A color-group status of "
            "not_applicable requires a successful GetColorGroup call returning None; "
            "failed or unavailable getters remain unknown. Group ok means a group object "
            "was returned, while its name and each graph have separate statuses.",
            "LUT paths, media paths, camera serials, and bulk private metadata are omitted.",
            "This snapshot does not prove CST accuracy, display calibration, or image quality.",
        ],
    }
    if item:
        current = read(item, "GetCurrentVersion")
        names = read(item, "GetVersionNameList", 0)
        data["grade_versions"] = {
            "current": ({"name": simple(current.get("versionName")),
                         "type": simple(current.get("versionType"))}
                        if isinstance(current, dict) else None),
            "local_names": ([name for name in names if isinstance(name, str)]
                            if isinstance(names, list) else None),
            "type_key": {"0": "local grade", "1": "remote grade"},
        }
        try:
            layers = int(project_settings.get("nodeStackLayers"))
        except (TypeError, ValueError):
            layers = 0
        if layers > 0:
            for layer in range(1, layers + 1):
                graph_data = scoped_graph_snapshot(item, "GetNodeGraph", layer)
                data["clip_node_graphs"].append({"layer": layer, **graph_data})
        else:
            graph_data = scoped_graph_snapshot(item, "GetNodeGraph")
            data["clip_node_graphs"].append({"layer": 1, **graph_data})
            data["limitations"].append(
                "Node-stack layer count unavailable; only the documented default first layer was read."
            )
    return data


def main(phase=None):
    # Kept callable for existing offline tests; process protection is in cli().
    phase = phase or (lambda name: None)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON to this file instead of stdout.")
    args = parser.parse_args()
    try:
        output_preflight(args.output)
        phase("before_wrapper_import")
        module = load_resolve_module()
        phase("after_wrapper_import")
        try:
            phase("before_scriptapp")
            resolve = module.scriptapp("Resolve")
            phase("after_scriptapp")
        except Exception as exc:
            raise SnapshotError("SESSION_CONNECTION_FAILED", "session_connect",
                                "Не удалось получить scripting-сессию Resolve; ошибка вызова подключения.") from exc
        if resolve is None:
            raise SnapshotError(
                "SESSION_UNAVAILABLE", "session_connect",
                "scriptapp вернул None: доступная scripting-сессия не получена. Helper не запускает приложение и не меняет доступ."
            )
        try:
            phase("before_snapshot")
            data = snapshot(resolve)
            phase("after_snapshot")
        except Exception as exc:
            raise SnapshotError("SNAPSHOT_READ_FAILED", "snapshot_read",
                                "Не удалось завершить чтение контекста Color.") from exc
        try:
            phase("before_json_serialize")
            result = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
            phase("after_json_serialize")
        except Exception as exc:
            raise SnapshotError("SNAPSHOT_SERIALIZE_FAILED", "json_serialize",
                                "Не удалось сформировать JSON из прочитанного контекста.") from exc
        try:
            if args.output:
                # Exclusive creation also protects against a race after prevalidation.
                with args.output.open("x", encoding="utf-8") as stream:
                    stream.write(result)
            else:
                print(result, end="")
        except FileExistsError as exc:
            raise SnapshotError("OUTPUT_EXISTS", "output_write",
                                "Путь отчёта уже существует; файл не перезаписан.") from exc
        except Exception as exc:
            code = "OUTPUT_WRITE_FAILED" if args.output else "STDOUT_WRITE_FAILED"
            message = "Не удалось записать файл отчёта." if args.output else "Не удалось вывести отчёт в stdout."
            raise SnapshotError(code, "output_write", message) from exc
    except SnapshotError as exc:
        error = {"status": "error", "code": exc.code, "stage": exc.stage, "message": str(exc)}
        # ASCII transport preserves the Russian message on legacy stderr encodings.
        print(json.JSONEncoder(ensure_ascii=True).encode(error), file=sys.stderr)
        return 2
    return 0


DEFAULT_TIMEOUT = 60.0
CLEANUP_WAIT = 2.0


def stop_child(child):
    """Signal only this Popen child; never Resolve, a parent, or a process group."""
    errors = []
    for action in ("terminate", "kill"):
        try:
            if child.poll() is not None:
                break
            getattr(child, action)()
            child.wait(timeout=CLEANUP_WAIT)
        except subprocess.TimeoutExpired:
            pass
        except (OSError, KeyboardInterrupt) as exc:
            errors.append(type(exc).__name__ + ": " + str(exc))
    return {"cleanup_completed": child.returncode is not None,
            "child_returncode": child.returncode, "cleanup_errors": errors}


def supervise(command, timeout, phase_path):
    """Parent owns one child. Temp files avoid pipe backpressure during native waits."""
    started = time.monotonic()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=out,
                                 stderr=err, env=env, shell=False)
        timed_out = False
        interrupted = False
        supervisor_error = None
        cleanup = None
        try:
            child.wait(timeout=max(0.001, timeout - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            timed_out = True
        except KeyboardInterrupt:
            interrupted = True
        except OSError as exc:
            supervisor_error = str(exc)
        finally:
            # Also runs if the parent is interrupted or wait itself raises.
            cleanup = stop_child(child)
        out.seek(0)
        stdout = out.read().decode("utf-8", errors="replace")
        err.seek(0)
        stderr = err.read().decode("utf-8", errors="replace")
    phases = []
    try:
        for line in phase_path.read_text(encoding="utf-8").splitlines():
            try:
                phases.append(json.loads(line))
            except ValueError:
                pass  # A terminated write may leave an incomplete last line.
    except OSError:
        pass
    return {"stdout": stdout, "stderr": stderr, "timed_out": timed_out,
            "interrupted": interrupted, "supervisor_error": supervisor_error,
            "child_pid": child.pid, "elapsed_seconds": time.monotonic() - started,
            "last_phase": phases[-1] if phases else None, **cleanup}


def emit_error(code, stage, message, **details):
    error = {"status": "error", "code": code, "stage": stage, "message": message}
    error.update(details)
    print(json.dumps(error, ensure_ascii=True), file=sys.stderr)
    return 2


def relay_stderr(text):
    """Keep vendor diagnostics even when the parent has a legacy ASCII stream."""
    try:
        sys.stderr.write(text)
    except UnicodeEncodeError:
        sys.stderr.write(text.encode("ascii", errors="backslashreplace").decode("ascii"))


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON to a new file instead of stdout.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help="Child inspection budget in seconds (default 60); cleanup adds at most 4 seconds of waits.")
    args = parser.parse_args(argv)
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        return emit_error("TIMEOUT_INVALID", "runtime", "Timeout must be a finite positive number.")
    try:
        # No SDK is imported in the parent; reject bad destinations before spawn.
        output_preflight(args.output)
        runtime_preflight()
        folder = tempfile.mkdtemp(prefix="resolve-inspect-")
        transport_cleanup_error = None
        try:
            phase_path = Path(folder) / "phases.jsonl"
            command = [sys.executable, "-B", "-u", str(Path(__file__).resolve()),
                       "--_inspect_worker", str(phase_path)]
            outcome = supervise(command, args.timeout, phase_path)
        finally:
            try:
                shutil.rmtree(folder)
            except OSError as exc:
                # In particular, a surviving Windows child may retain a handle.
                # Never replace the timeout/interruption diagnostic with this.
                transport_cleanup_error = str(exc)
        phase = outcome["last_phase"]
        details = {key: outcome[key] for key in (
            "child_pid", "elapsed_seconds", "last_phase", "cleanup_completed",
            "child_returncode", "cleanup_errors")}
        details["child_stderr"] = outcome["stderr"][-16384:]
        details["transport_cleanup_error"] = transport_cleanup_error
        if transport_cleanup_error:
            details["retained_temporary_directory"] = folder
        if outcome["timed_out"]:
            return emit_error(
                "INSPECT_TIMEOUT", phase["phase"] if phase else "child_start",
                "Inspection exceeded its budget; no snapshot was accepted. No automatic retry.",
                timeout_seconds=args.timeout, **details)
        if outcome["interrupted"]:
            return emit_error("INSPECT_INTERRUPTED", phase["phase"] if phase else "child_start",
                              "Inspection interrupted; no snapshot accepted. See own-child cleanup result.",
                              **details)
        if outcome["supervisor_error"]:
            return emit_error("INSPECT_SUPERVISOR_FAILED", "parent_wait",
                              outcome["supervisor_error"], **details)
        if outcome["child_returncode"] != 0:
            # Vendor warnings may precede the helper's own ASCII JSON error.
            diagnostics = []
            for line in outcome["stderr"].splitlines():
                try:
                    diagnostics.append(json.loads(line))
                except ValueError:
                    pass
            if any(isinstance(d, dict) and d.get("status") == "error"
                   and all(k in d for k in ("code", "stage", "message")) for d in diagnostics):
                relay_stderr(outcome["stderr"])
                if transport_cleanup_error:
                    emit_error("INSPECT_TRANSPORT_CLEANUP_FAILED", "parent_cleanup",
                               transport_cleanup_error, **details)
                return 2
            return emit_error("INSPECT_CHILD_FAILED", "child_exit",
                              "Inspection child exited without a complete snapshot.",
                              **details)
        if transport_cleanup_error:
            return emit_error("INSPECT_TRANSPORT_CLEANUP_FAILED", "parent_cleanup",
                              transport_cleanup_error, **details)
        if outcome["stderr"]:
            relay_stderr(outcome["stderr"])
        result = outcome["stdout"]
        try:
            if not isinstance(json.loads(result), dict):
                raise ValueError("Expected a JSON object")
        except ValueError as exc:
            raise SnapshotError("SNAPSHOT_SERIALIZE_FAILED", "json_serialize",
                                "Child did not return one valid JSON snapshot.") from exc
        try:
            if args.output:
                with args.output.open("x", encoding="utf-8") as stream:
                    stream.write(result)
            else:
                print(result, end="")
        except FileExistsError as exc:
            raise SnapshotError("OUTPUT_EXISTS", "output_write",
                                "Путь отчёта уже существует; файл не перезаписан.") from exc
        except Exception as exc:
            raise SnapshotError("OUTPUT_WRITE_FAILED" if args.output else "STDOUT_WRITE_FAILED",
                                "output_write", "Не удалось записать файл отчёта." if args.output
                                else "Не удалось вывести отчёт в stdout.") from exc
        return 0
    except SnapshotError as exc:
        return emit_error(exc.code, exc.stage, str(exc))
    except KeyboardInterrupt:
        return emit_error("INSPECT_INTERRUPTED", "parent_wait", "Inspection interrupted; own-child cleanup attempted.")
    except OSError as exc:
        return emit_error("INSPECT_SUPERVISOR_FAILED", "parent", str(exc))


def worker(phase_path):
    def phase(name):
        with phase_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"phase": name, "pid": os.getpid(),
                                     "utc": datetime.now(timezone.utc).isoformat(),
                                     "monotonic": time.monotonic()}) + "\n")
            stream.flush()
    sys.argv = [sys.argv[0]]  # Worker always uses stdout; only the parent writes --output.
    phase("worker_started")
    return main(phase=phase)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--_inspect_worker":
        raise SystemExit(worker(Path(sys.argv[2])))
    raise SystemExit(cli())
