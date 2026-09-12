# Install the local Blender MCP

Requirements: Node.js 24+ with npm, and Blender 4.2 or newer on the user's own computer. Package: [fnf-blender-mcp](https://www.npmjs.com/package/fnf-blender-mcp), publisher `arsu_higgsfield_ai`. Install version `0.1.0` from the public npm registry. No npm account, GitHub login, source checkout, TypeScript build or separate Python installation is needed to use the package.

First check `node --version` and `npm --version` and locate the intended Blender executable. Common discovery hints are `/Applications/Blender.app/Contents/MacOS/Blender`, Windows `C:/Program Files/Blender Foundation/Blender <version>/blender.exe`, or `blender` on Linux PATH. On Windows use `npm.cmd` when PowerShell blocks `npm.ps1`; try resolved absolute executable paths before concluding dependencies are missing. A failed default-path check does not prove Blender is uninstalled. Do not install Blender itself unless requested.

## Install into a persistent user directory

Use a user-owned installation prefix so global administrator permissions are unnecessary. Preserve an existing working installation and client configuration when diagnosing a connection. Do not install or register from a cloud sandbox, temporary directory or npx cache.

macOS / Linux:

```sh
bridgeDir="$HOME/.higgsfield/blender-mcp"
npm install --prefix "$bridgeDir" --registry=https://registry.npmjs.org/ --no-audit --no-fund fnf-blender-mcp@0.1.0
bridgeCli="$bridgeDir/node_modules/fnf-blender-mcp/dist/cli.js"
node "$bridgeCli" --help
```

Windows PowerShell:

```powershell
$bridgeDir = Join-Path $env:LOCALAPPDATA 'Higgsfield/blender-mcp'
npm.cmd install --prefix $bridgeDir --registry=https://registry.npmjs.org/ --no-audit --no-fund fnf-blender-mcp@0.1.0
$bridgeCli = Join-Path $bridgeDir 'node_modules/fnf-blender-mcp/dist/cli.js'
node $bridgeCli --help
```

Use the discovered persistent Node/npm paths if they are not on PATH. A registry authentication error for this public package is not a reason to ask the user to create an npm account; inspect the failing registry/configuration without exposing saved tokens or changing unrelated private-registry settings.

## Connect Blender

1. Set `blenderExe` to the verified absolute Blender executable path (not the `.app` directory). To open a **new** Blender process with the bundled bridge, run `node "$bridgeCli" launch --blender "$blenderExe"` on macOS/Linux, or `node $bridgeCli launch --blender $blenderExe` in PowerShell. This leaves preferences unchanged and does not attach to an already-open instance.
2. For regular startup in an existing installation, use `install-addon --blender` with the same executable. It copies the add-on into that Blender version's user scripts directory without saving or resetting preferences. Enable **Higgsfield use Blender** in Preferences → Add-ons in the intended instance; save preferences if automatic startup is wanted. A running instance may need refreshing/restarting. Preserve unsaved work.
3. After startup, run the installed CLI with `doctor` to verify a real bpy round trip.
4. Run the installed CLI with `config --format json` for JSON MCP clients or `config --format toml` for Codex. Merge only this server entry into the intended desktop client's supported configuration, preserving other servers, environment and tool policies. Generated paths are absolute; keep the installed package and Node at those locations. The helper prints configuration; it does not register or enable a connection.
5. Refresh the MCP connection and load `/use-blender/references/verification` (or the bundled verification reference).

`BLENDER_MCP_PID` selects one of several live Blender processes. `BLENDER_MCP_RUNTIME_DIR` must match between the add-on process and MCP server if overridden; default `~/.higgsfield/blender`. Add these overrides to client configuration when needed; `config` does not include them automatically. Never paste bridge tokens into chat or logs.
