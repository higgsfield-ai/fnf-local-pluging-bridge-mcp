#!/usr/bin/env node
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { stat } from "node:fs/promises";
import { isAbsolute } from "node:path";
import { BlenderTransport, discover } from "./transport.js";

const root = new URL("../", import.meta.url);
const usage = `Higgsfield use Blender
  fnf-blender doctor                         Discover bridges and verify live bpy execution
  fnf-blender config [--format json|toml]    Print local MCP configuration
  fnf-blender launch --blender PATH          Open Blender with the bundled bridge
  fnf-blender install-addon --blender PATH   Install the add-on for that Blender version
  fnf-blender serve                          Run the stdio MCP server

Requires Node.js 24+ and Blender 4.2+. BLENDER_MCP_PID selects an instance.
BLENDER_MCP_RUNTIME_DIR overrides local bridge discovery on both processes.
No WebSocket or cloud account is required. npm package: fnf-blender-mcp.`;

async function main(): Promise<void> {
  const [command = "help", ...args] = process.argv.slice(2);
  if (["help", "--help", "-h"].includes(command)) { console.log(usage); return; }
  if (command === "serve") { await import("./index.js"); return; }
  if (command === "config") {
    if (args.length && (args[0] !== "--format" || args.length !== 2 || !["json", "toml"].includes(args[1]))) throw new Error(usage);
    const entry = { command: process.execPath, args: [fileURLToPath(new URL("dist/index.js", root))] };
    if (args[1] === "toml") {
      console.log(`[mcp_servers.higgsfield-use-blender]\ncommand = ${JSON.stringify(entry.command)}\nargs = ${JSON.stringify(entry.args)}`);
    } else console.log(JSON.stringify({ mcpServers: { "higgsfield-use-blender": entry } }, null, 2));
    return;
  }
  if (command === "doctor") {
    const connections = await discover();
    console.log(JSON.stringify({ node: process.version, bridges: connections.map(({ pid, port }) => ({ pid, port })) }));
    const job = await new BlenderTransport().execute("import bpy\nresult = {'version': bpy.app.version_string, 'file': bpy.data.filepath, 'scene': bpy.context.scene.name}", 5);
    if (!job.ok) throw new Error(job.error || "Blender execution failed");
    console.log(JSON.stringify(job.result));
    return;
  }
  if (command === "install-addon" || command === "launch") {
    if (args[0] !== "--blender" || args.length !== 2) throw new Error("Pass --blender with the absolute Blender executable path.");
    const executable = args[1];
    if (!isAbsolute(executable) || !(await stat(executable)).isFile()) throw new Error("--blender must point to an absolute executable file, not the .app directory.");
    const script = fileURLToPath(new URL(command === "launch" ? "scripts/launch.py" : "scripts/install_addon.py", root));
    const launchArgs = command === "launch" ? ["--python", script] : ["--background", "--factory-startup", "--python-exit-code", "1", "--python", script];
    const child = spawn(executable, launchArgs, { stdio: command === "launch" ? "ignore" : "inherit", detached: command === "launch" });
    await new Promise<void>((resolve, reject) => {
      child.once("error", reject);
      if (command === "launch") child.once("spawn", () => { child.unref(); resolve(); });
      else child.once("exit", code => code === 0 ? resolve() : reject(new Error(`Blender installer exited ${code}`)));
    });
    if (command === "launch") console.log("Blender launched with the bridge bootstrap. Run doctor after startup to verify the connection.");
    return;
  }
  throw new Error(usage);
}

main().catch(error => { console.error(error instanceof Error ? error.message : String(error)); process.exitCode = 1; });
