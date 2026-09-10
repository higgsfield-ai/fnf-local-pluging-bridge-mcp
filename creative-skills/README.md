# FNF Creative Apps Skills

Skill sources for the `fnf-local-pluging-bridge-mcp` repository, adapted from FNF bridge skills. The `skills/` directory is the active corpus; `archive/bridge-ae/` preserves the original source and is never served or installed. No license to redistribute the archived source is assumed; keep this repository private until ownership and licensing are settled.

## Install

From the repository root, `python3 creative-skills/scripts/install.py` installs the `use-after-effects` entry skill into `~/.agents/skills/use-after-effects` as a symlink. It refuses to overwrite an unrelated skill. The runtime serves all companion skills through `ae_get_skill`; installing ten overlapping global skills is unnecessary.

## Maintain

From the repository root, edit active skills, run `python3 creative-skills/scripts/validate.py`, commit the result, then run `node scripts/sync-skills.mjs ./creative-skills`. Review and commit its pinned snapshot. Runtime lookup never reads the sibling checkout or fetches the network.

See [migration notes](MIGRATION.md) and [source provenance](provenance.json).
