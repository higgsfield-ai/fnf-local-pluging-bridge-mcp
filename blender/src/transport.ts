import { readdir, readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { z } from "zod";

export const runtimeDirectory = () => process.env.BLENDER_MCP_RUNTIME_DIR || join(homedir(), ".higgsfield", "blender");
const connectionSchema = z.object({
  protocol: z.literal("higgsfield-blender/1"), pid: z.number().int().positive(),
  port: z.number().int().min(1).max(65535), token: z.string().regex(/^[a-f0-9]{64}$/),
});
export type Connection = z.infer<typeof connectionSchema>;
const jobSchema = z.object({
  job_id: z.string(), state: z.enum(["queued", "running", "completed", "expired"]),
  ok: z.boolean().optional(), result: z.unknown().optional(), error: z.string().optional(),
  stdout: z.string().optional(), stderr: z.string().optional(),
});
export type JobResult = z.infer<typeof jobSchema>;

async function request(connection: Connection, path: string, body?: unknown): Promise<unknown> {
  const response = await fetch(`http://127.0.0.1:${connection.port}${path}`, {
    method: body === undefined ? "GET" : "POST", redirect: "error",
    headers: { Authorization: `Bearer ${connection.token}`, "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(5000),
  });
  if (!response.ok) throw new Error(`Blender bridge HTTP ${response.status}: ${(await response.text()).slice(0, 1000)}`);
  return response.json();
}

export async function discover(directory = runtimeDirectory()): Promise<Connection[]> {
  const names = await readdir(directory).catch((error: NodeJS.ErrnoException) => {
    if (error.code === "ENOENT") return [];
    throw error;
  });
  const candidates = await Promise.all(names.filter(name => /^bridge-\d+\.json$/.test(name)).map(async name => {
    try {
      const connection = connectionSchema.parse(JSON.parse(await readFile(join(directory, name), "utf8")));
      const health = z.object({ protocol: z.literal("higgsfield-blender/1"), pid: z.number() }).parse(await request(connection, "/health"));
      return health.pid === connection.pid ? connection : undefined;
    } catch { return undefined; }
  }));
  return candidates.filter((value): value is Connection => value !== undefined);
}

export class BlenderTransport {
  async connection(): Promise<Connection> {
    const connections = await discover();
    const selected = process.env.BLENDER_MCP_PID;
    const matches = selected ? connections.filter(item => String(item.pid) === selected) : connections;
    if (!matches.length) throw new Error("No live Blender bridge found. Open Blender with the Higgsfield use Blender add-on enabled; run fnf-blender doctor on this computer.");
    if (matches.length > 1) throw new Error(`Multiple Blender instances: ${matches.map(item => item.pid).join(", ")}. Set BLENDER_MCP_PID to choose one before editing.`);
    return matches[0];
  }

  async status(jobId: string, connection?: Connection): Promise<JobResult> {
    return jobSchema.parse(await request(connection ?? await this.connection(), `/jobs/${encodeURIComponent(jobId)}`));
  }

  async execute(code: string, timeoutSeconds = 120): Promise<JobResult> {
    const connection = await this.connection();
    let accepted: JobResult;
    try {
      accepted = jobSchema.parse(await request(connection, "/execute", { code, timeout_seconds: timeoutSeconds }));
    } catch (error) {
      throw new Error(`Submission failed; execution may have been accepted. Inspect scene state before retrying. ${String(error)}`);
    }
    const deadline = Date.now() + timeoutSeconds * 1000;
    try {
      while (Date.now() < deadline) {
        const result = await this.status(accepted.job_id, connection);
        if (result.state === "completed" || result.state === "expired") return result;
        await delay(100);
      }
    } catch (error) {
      throw new Error(`Lost contact with Blender; job_id=${accepted.job_id}, pid=${connection.pid}. Use bl_job_status before retrying. ${String(error)}`);
    }
    throw new Error(`Blender is still busy; job_id=${accepted.job_id}, pid=${connection.pid}. Execution may continue. Use bl_job_status before retrying; no automatic retry was sent.`);
  }
}
