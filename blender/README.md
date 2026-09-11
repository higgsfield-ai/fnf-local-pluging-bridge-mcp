# Higgsfield use Blender

The independent Blender package in `fnf-local-pluging-bridge-mcp/blender`, for editing native Blender scenes. No WebSocket, Cloudflare Worker, R2 bucket or cloud bridge account is required.

```text
Desktop MCP client ── stdio ── Node MCP server
                                  │
                     authenticated HTTP on 127.0.0.1
                                  │
                        Blender Python add-on
                                  │
                       main-thread timer → bpy
```

Install the public [fnf-blender-mcp](https://www.npmjs.com/package/fnf-blender-mcp) package, published by `arsu_higgsfield_ai`. No source checkout or build is needed for installation.

## Quick start

Requires Node.js 24+ with npm and Blender 4.2+. Blender supplies the add-on's Python runtime; a separate Python installation is only needed for development tests.

Install into a persistent user directory (macOS/Linux):

```sh
bridgeDir="$HOME/.higgsfield/blender-mcp"
npm install --prefix "$bridgeDir" --registry=https://registry.npmjs.org/ fnf-blender-mcp@0.1.0
bridgeCli="$bridgeDir/node_modules/fnf-blender-mcp/dist/cli.js"
node "$bridgeCli" launch --blender "/absolute/path/to/blender"
node "$bridgeCli" doctor
node "$bridgeCli" config --format json
```

For Windows PowerShell, use `$bridgeDir = Join-Path $env:LOCALAPPDATA 'Higgsfield/blender-mcp'`, install with `npm.cmd install --prefix $bridgeDir --registry=https://registry.npmjs.org/ fnf-blender-mcp@0.1.0`, then set `$bridgeCli = Join-Path $bridgeDir 'node_modules/fnf-blender-mcp/dist/cli.js'` and invoke `node $bridgeCli` with the commands above. The [installation skill](skills/use-blender/references/installation.md) contains the full setup procedure.

`launch` opens a **new** Blender process with the bundled bridge. It does not attach to an existing process or change saved preferences. Wait for startup before running `doctor`. Use the actual executable, such as `Blender.app/Contents/MacOS/Blender` on macOS or `blender.exe` on Windows.

For an existing installation and automatic startup:

```sh
node "$bridgeCli" install-addon --blender "/absolute/path/to/blender"
```

Enable **Higgsfield use Blender** in Blender's Preferences → Add-ons, then save preferences if desired. The installer only copies the add-on into that version's user scripts directory. It never saves or resets preferences, and refuses to overwrite an unrecognized add-on directory. An already-running instance may need refreshing or restarting; preserve unsaved work.

Merge the generated JSON entry into the desktop client's MCP configuration. For Codex use `node "$bridgeCli" config --format toml`. This helper prints configuration; it does not register or enable a client connection. Both formats use absolute Node and server paths. Keep the installed package at that persistent location. Refresh the client's MCP connection, then call `bl_health` and `bl_get_scene_summary` from the conversation. A shell `doctor` success alone does not establish conversation tool availability.

## Tools

| Area | Tools |
| --- | --- |
| Inspect | `bl_health`, `bl_get_scene_summary`, `bl_get_object` |
| Scene | `bl_add_primitive`, `bl_delete_object`, `bl_set_transform`, `bl_set_material`, `bl_import_model` |
| Camera/light | `bl_add_camera`, `bl_set_active_camera`, `bl_add_light` |
| Animation | `bl_set_frame`, `bl_insert_keyframe` |
| Files | `bl_save_project`, `bl_open_project` |
| Evidence | `bl_screenshot`, `bl_render` |
| Python/status | `bl_execute`, `bl_job_status` |
| Offline guidance | `bl_get_skill` |

Start with `bl_get_skill(name: "blender-scene")`. It routes to modeling, materials, lighting/camera and animation guidance. Use `bl_execute` for bpy operations beyond the typed tools; assign a JSON-compatible value to `result`. stdout and stderr are returned with a 64 KiB cap each. Results are limited to 4 MiB; return a file path for larger data.

Screenshots return inline MCP images without cloud uploads and need a VIEW_3D area. Camera renders write a local PNG and include a preview for files up to 4 MiB. Render overrides are restored afterward; an explicit sample override currently requires Cycles. Saving or rendering over an existing file requires `overwrite: true`. Opening a project refuses unsaved changes unless `discard_unsaved: true`.

This package does not bundle cloud generation, offline Blender API/manual search, or the original connector's model-generation and motion-import handlers. Use a separate Higgsfield MCP for generation, download finished assets, and import an absolute local path. Local Python has the full permissions of the Blender process; it is not a sandbox.

## Connection and timeout behavior

- The add-on binds an ephemeral loopback port and generates a random bearer token. Discovery files live in `~/.higgsfield/blender/bridge-<pid>.json`, with owner-only file permissions on POSIX. Windows uses the user's profile-directory ACLs.
- Browser-origin requests, incorrect Host headers and missing/incorrect tokens are rejected. Do not expose the endpoint or share its token.
- The server refuses ambiguous multi-instance discovery. Set `BLENDER_MCP_PID` in the MCP server environment to select the intended instance.
- Override `BLENDER_MCP_RUNTIME_DIR` on **both** the Blender process and MCP process when a custom directory is needed. `config` does not include these environment overrides automatically.
- HTTP only queues work. A persistent Blender timer executes Python on the main thread. Rendering or long scripts can block Blender's UI.
- Commands are accepted once and receive a job ID. Pending jobs expire before execution after their deadline. A running script cannot be safely interrupted; timeout does not mean cancellation or rollback.
- After a timeout, use `bl_job_status` on the original PID before retrying. A script exception can leave partial changes. If submission failed before the job ID was received, inspect the scene first.
- Up to 128 job records are retained in memory, with old completed jobs evicted as new jobs arrive. Restarting Blender loses history. A client-side MCP timeout may occur before the tool returns its job ID; set tool timeouts above 300 seconds for long renders and inspect state before retrying.

## Development and verification

From a source checkout, run `cd blender` and `npm ci` first. Development checks:

```sh
npm test
npm run typecheck
npm run test:package
```

The automated tests cover a real stdio MCP subprocess talking to the real Python HTTP bridge, authenticated discovery, multiple instances, execution errors, result images, input validation, queue overload, expiration, timeouts and status recovery. A minimal bpy fixture supplies metadata in those tests. Every typed Python script is syntax-compiled. `test:package` builds a local `.tgz`, installs it in an isolated directory, and checks the shipped runtime, skills and setup files; it does not publish anything.

**These tests do not prove live Blender behavior.** Blender was not found on the development Mac, so real geometry, viewport rendering, installer behavior inside Blender and Windows/Linux integration remain unverified. For a live check, run `doctor`, inspect a disposable scene, create a primitive, set a material and camera, render/view a small PNG, save/reopen a temporary `.blend`, and confirm unsaved-file guards. Never use an existing unsaved project as the test fixture.

## Slash command

The matching `/use-blender` bundle is added to `fnf-mcp-server` under `src/tools/preset-instructions/resources/commands/use-blender`. It returns installation and verification instructions before any remote preset lookup. The standalone source lives in `skills/use-blender`; keep their bodies synchronized when editing setup instructions. The server command adds a `title` frontmatter field for its catalog.

See [UPSTREAM.md](UPSTREAM.md) for provenance and [LICENSE](LICENSE) for the MIT license.

The source was imported from standalone revision `2517549`; npm installation paths and the `/use-blender` command are unchanged. See [RELEASING.md](RELEASING.md) for package releases.
