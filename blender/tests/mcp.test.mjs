import assert from 'node:assert/strict';
import test from 'node:test';
import { spawn, execFileSync } from 'node:child_process';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { once } from 'node:events';
import { setTimeout as delay } from 'node:timers/promises';
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
import { BlenderTransport } from '../dist/transport.js';
import { BL_TOOLS } from '../dist/tools.js';

const root = new URL('../', import.meta.url);
const python = process.env.PYTHON || 'python3';

async function startHarness(directory) {
  const child = spawn(python, [new URL('tests/bridge_harness.py', root).pathname], {
    env: { ...process.env, BLENDER_MCP_RUNTIME_DIR: directory }, stdio: ['ignore', 'pipe', 'inherit'],
  });
  await Promise.race([once(child.stdout, 'data'), once(child, 'exit').then(() => { throw new Error('Bridge harness exited'); })]);
  return child;
}

test('stdio MCP reaches authenticated Python bridge and preserves errors/images', { timeout: 20000 }, async () => {
  const directory = await mkdtemp(join(tmpdir(), 'fnf-blender-test-'));
  const bridge = await startHarness(directory);
  const client = new Client({ name: 'test', version: '1' });
  try {
    await client.connect(new StdioClientTransport({ command: process.execPath, args: [new URL('dist/index.js', root).pathname], env: { BLENDER_MCP_RUNTIME_DIR: directory }, stderr: 'pipe' }));
    const listed = await client.listTools();
    assert.equal(listed.tools.length, BL_TOOLS.length + 2);
    assert.equal(listed.tools.find(t => t.name === 'bl_execute').annotations.readOnlyHint, false);
    assert.equal(listed.tools.find(t => t.name === 'bl_health').annotations.readOnlyHint, true);
    const health = await client.callTool({ name: 'bl_health', arguments: {} });
    assert.equal(health.structuredContent.result.version, 'fixture-4.2');
    const result = await client.callTool({ name: 'bl_execute', arguments: { code: "print('hello')\nresult = {'answer': 6 * 7}" } });
    assert.deepEqual(result.structuredContent.result, { answer: 42 });
    const polled = await client.callTool({ name: 'bl_job_status', arguments: { job_id: result.structuredContent.job_id } });
    assert.deepEqual(polled.structuredContent.result, { answer: 42 });
    const failure = await client.callTool({ name: 'bl_execute', arguments: { code: "raise ValueError('expected')" } });
    assert.equal(failure.isError, true);
    assert.match(failure.structuredContent.error, /expected/);
    const unknownArg = await client.callTool({ name: 'bl_health', arguments: { unexpected: true } });
    assert.equal(unknownArg.isError, true);
    const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aP9sAAAAASUVORK5CYII=';
    const image = await client.callTool({ name: 'bl_execute', arguments: { code: `result = {'pngBase64': '${png}', 'width': 1, 'height': 1}` } });
    assert.equal(image.content.find(c => c.type === 'image').data, png);
    assert.equal(image.structuredContent.result.pngBase64, undefined);
    const skill = await client.callTool({ name: 'bl_get_skill', arguments: { name: 'modeling' } });
    assert.match(skill.content[0].text, /Modeling/);
  } finally {
    await client.close();
    bridge.kill();
    await once(bridge, 'exit');
    await rm(directory, { recursive: true, force: true });
  }
});

test('discovery rejects ambiguity; timeout recovers the same job without resubmission', { timeout: 20000 }, async () => {
  const directory = await mkdtemp(join(tmpdir(), 'fnf-blender-select-'));
  const a = await startHarness(directory);
  const b = await startHarness(directory);
  const previousDir = process.env.BLENDER_MCP_RUNTIME_DIR;
  const previousPid = process.env.BLENDER_MCP_PID;
  process.env.BLENDER_MCP_RUNTIME_DIR = directory;
  delete process.env.BLENDER_MCP_PID;
  try {
    const transport = new BlenderTransport();
    await assert.rejects(transport.connection(), /Multiple Blender/);
    process.env.BLENDER_MCP_PID = String(a.pid);
    const marker = join(directory, 'executions.txt');
    const code = `import time\nwith open(${JSON.stringify(marker)}, 'a') as f: f.write('once\\n')\ntime.sleep(1.5)\nresult = 42`;
    let job;
    try { await transport.execute(code, 1); assert.fail('Expected a timeout'); }
    catch (error) { job = /job_id=([a-f0-9]{32})/.exec(error.message)?.[1]; assert.ok(job, error.message); }
    await delay(800);
    assert.equal((await transport.status(job)).result, 42);
    const { readFile } = await import('node:fs/promises');
    assert.equal(await readFile(marker, 'utf8'), 'once\n');
  } finally {
    if (previousDir === undefined) delete process.env.BLENDER_MCP_RUNTIME_DIR; else process.env.BLENDER_MCP_RUNTIME_DIR = previousDir;
    if (previousPid === undefined) delete process.env.BLENDER_MCP_PID; else process.env.BLENDER_MCP_PID = previousPid;
    a.kill(); b.kill();
    await Promise.all([once(a, 'exit'), once(b, 'exit')]);
    await rm(directory, { recursive: true, force: true });
  }
});

test('typed bpy scripts compile, including unicode and hostile-looking argument strings', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'fnf-blender-compile-'));
  try {
    const scripts = BL_TOOLS.map(tool => tool.code({ name: '"\\\nБлендер ${danger}', code: 'result = 42', path: '/tmp/test.blend' }));
    const path = join(directory, 'scripts.json');
    await writeFile(path, JSON.stringify(scripts));
    execFileSync(python, ['-c', 'import json,sys\nfor code in json.load(open(sys.argv[1])): compile(code, "<test>", "exec")', path]);
  } finally { await rm(directory, { recursive: true, force: true }); }
});

test('CLI config uses persistent absolute paths and missing Blender is actionable', async () => {
  const config = JSON.parse(execFileSync(process.execPath, ['dist/cli.js', 'config'], { cwd: root, encoding: 'utf8' }));
  assert.equal(config.mcpServers['higgsfield-use-blender'].command, process.execPath);
  assert.match(config.mcpServers['higgsfield-use-blender'].args[0], /\/dist\/index.js$/);
  const directory = await mkdtemp(join(tmpdir(), 'fnf-blender-missing-'));
  try {
    assert.throws(() => execFileSync(process.execPath, ['dist/cli.js', 'doctor'], { cwd: root, env: { ...process.env, BLENDER_MCP_RUNTIME_DIR: directory }, stdio: 'pipe' }), error => {
      assert.match(error.stderr.toString(), /No live Blender bridge/);
      return true;
    });
  } finally { await rm(directory, { recursive: true, force: true }); }
});

test('a failed render restores scene settings and respects existing output files', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'fnf-blender-render-'));
  try {
    const output = join(directory, 'render.png');
    const tool = BL_TOOLS.find(t => t.name === 'bl_render');
    const source = tool.code({ output_path: output, resolution: [128, 128], engine: 'CYCLES', samples: 8 });
    const file = join(directory, 'render.py');
    await writeFile(file, source);
    execFileSync(python, ['-c', `
import sys, types
from pathlib import Path
S = types.SimpleNamespace
render = S(engine='BLENDER_EEVEE_NEXT', resolution_x=1920, resolution_y=1080, resolution_percentage=50, filepath='original', image_settings=S(file_format='JPEG'))
scene = S(camera=object(), render=render, cycles=S(samples=64))
calls = []
def fail(**kwargs):
    calls.append(1)
    assert render.engine == 'CYCLES' and render.resolution_percentage == 100 and scene.cycles.samples == 8
    raise RuntimeError('render failed')
bpy = types.ModuleType('bpy')
bpy.context = S(scene=scene)
bpy.ops = S(render=S(render=fail))
sys.modules['bpy'] = bpy
code = Path(sys.argv[1]).read_text()
try: exec(code)
except RuntimeError as error: assert str(error) == 'render failed'
else: raise AssertionError('Expected render failure')
assert (render.engine, render.resolution_x, render.resolution_y, render.resolution_percentage, render.filepath, render.image_settings.file_format, scene.cycles.samples) == ('BLENDER_EEVEE_NEXT', 1920, 1080, 50, 'original', 'JPEG', 64)
output = Path(sys.argv[2])
output.write_text('preserve')
try: exec(code)
except ValueError as error: assert 'exists' in str(error)
else: raise AssertionError('Expected overwrite guard')
assert output.read_text() == 'preserve' and len(calls) == 1
`, file, output]);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
