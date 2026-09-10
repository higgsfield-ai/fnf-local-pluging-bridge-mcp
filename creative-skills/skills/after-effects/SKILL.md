---
name: after-effects
description: Set up and use the local FNF After Effects MCP when the user asks to connect After Effects, install its local integration, or create and edit native AE projects.
---

# Local After Effects

Connect the desktop MCP client to the local Node server, which runs bundled ExtendScript inside After Effects through OS scripting and a local file mailbox. No cloud bridge, Higgsfield login, or installed AE panel is required. Adobe licensing and OS Automation permissions remain separate requirements.

## Setup

1. Use the user's local computer, with macOS or Windows and After Effects installed. Check `node --version` and `npm --version`; require Node 24+. If either command is missing, guide installation of Node.js 24 LTS with npm from https://nodejs.org/en/download, then reopen the terminal and check again. npm/npx cannot bootstrap themselves without Node/npm. Do not install into a remote sandbox.
2. Install the published package with `npm install --global --ignore-scripts fnf-after-effects-mcp@0.1.0`, then run `fnf-after-effects doctor`. If the version is unavailable, report that publication is pending; do not substitute an unrelated npm package. If macOS reports EACCES, use `npm install --global --ignore-scripts --prefix "$HOME/.local" fnf-after-effects-mcp@0.1.0` and invoke `"$HOME/.local/bin/fnf-after-effects"`. No Git, build step, Python or AE panel is required. Doctor checks installation without launching AE; it does not prove live connectivity.
3. For Codex with its CLI available, run `fnf-after-effects install-codex`. It registers the absolute Node and server paths as `fnf-after-effects`; a conflicting existing entry must be reviewed before replacement. For another desktop MCP client or when the CLI is unavailable, use the configuration printed by `fnf-after-effects config`. Use the permanently installed helper, never an npx cache path. A remote web client cannot directly launch this local stdio process.
4. Refresh the client's MCP connection if needed. Call `ae_get_skill` with no arguments, then with `name: "ae-clean-rig"`. These calls work even with AE closed.
5. Call `ae_project_info` to test real communication. Let the OS present any Automation permission prompt. If AE reports file/network scripting disabled, enable the corresponding AE Scripting & Expressions preference as part of the requested installation. Do not silently modify unrelated preferences or close an unsaved project.
6. Only report connected after a successful live response. Distinguish missing app, permission denial, startup timeout and a working MCP with disconnected AE.

## Work

Discover categories with `ae_catalog`, inspect the current project, load only relevant companion skills through `ae_get_skill`, and execute documented operations through `ae_do`. Preserve existing work. Use a small isolated comp for a user-authorized smoke test. Check returned errors and rendered frames before claiming success. A skill supplies instructions; it cannot create an unavailable MCP tool in the current session.
