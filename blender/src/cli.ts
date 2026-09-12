#!/usr/bin/env node
import { fileURLToPath } from "node:url";
import { BlenderTransport, resolveExecutable } from "./transport.js";

const usage = `Higgsfield use Blender
  fnf-blender doctor [--blender PATH]                    Verify a new background Blender process
  fnf-blender config [--blender PATH] [--format json|toml] Print local MCP configuration
  fnf-blender serve                                      Run the stdio MCP server

Requires Node.js 24+ and Blender 4.2+. BLENDER_EXECUTABLE selects the executable.
Each MCP session owns a background Blender process. Save .blend files before reconnecting.
No add-on, HTTP listener, WebSocket or open Blender window is required.`;

async function main(): Promise<void> {
  const [command = "help", ...args] = process.argv.slice(2);
  if (["help", "--help", "-h"].includes(command)) { console.log(usage); return; }
  if (command === "serve" && args.length === 0) { await import("./index.js"); return; }
  if (!["config", "doctor"].includes(command)) throw new Error(usage);
  let executable: string | undefined, format = "json";
  const seen = new Set<string>();
  for (let index = 0; index < args.length; index += 2) {
    const key = args[index], value = args[index + 1];
    if (!value || seen.has(key)) throw new Error(usage);
    seen.add(key);
    if (key === "--blender") executable = value;
    else if (key === "--format" && command === "config" && ["json", "toml"].includes(value)) format = value;
    else throw new Error(usage);
  }
  executable = await resolveExecutable(executable);
  if (command === "config") {
    const entry = { command: process.execPath, args: [fileURLToPath(new URL("./index.js", import.meta.url))], env: { BLENDER_EXECUTABLE: executable } };
    if (format === "toml") console.log(`[mcp_servers.higgsfield-use-blender]\ncommand = ${JSON.stringify(entry.command)}\nargs = ${JSON.stringify(entry.args)}\n[mcp_servers.higgsfield-use-blender.env]\nBLENDER_EXECUTABLE = ${JSON.stringify(executable)}`);
    else console.log(JSON.stringify({ mcpServers: { "higgsfield-use-blender": entry } }, null, 2));
    return;
  }
  const transport = new BlenderTransport({ executable });
  try {
    const job = await transport.execute("import bpy, os\nresult = {'version': bpy.app.version_string, 'background': bpy.app.background, 'pid': os.getpid(), 'file': bpy.data.filepath}", 15);
    if (!job.ok) throw new Error(job.error || "Blender execution failed");
    console.log(JSON.stringify({ executable, ...job }));
  } finally { await transport.close(); }
}
main().catch(error => { console.error(error instanceof Error ? error.message : String(error)); process.exitCode = 1; });
