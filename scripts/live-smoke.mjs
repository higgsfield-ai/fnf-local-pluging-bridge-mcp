import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
const root = resolve(import.meta.dirname, "..");
const output = resolve(root, "runtime/local-smoke");
const client = new Client({ name: "fnf-live-smoke", version: "1.0.0" });
await client.connect(
  new StdioClientTransport({
    command: process.execPath,
    args: [resolve(root, "dist/index.js")],
    stderr: "pipe",
  }),
);
async function call(name, args = {}) {
  const response = await client.callTool({ name, arguments: args }, undefined, { timeout: 120000 });
  if (response.isError)
    throw new Error(JSON.stringify(response.structuredContent ?? response.content));
  return (
    response.structuredContent ?? JSON.parse(response.content.find((x) => x.type === "text").text)
  );
}
try {
  const initial = await call("ae_project_info");
  if (initial.result.numItems !== 0 || initial.result.dirty || initial.result.file)
    throw new Error(
      "Live demo requires an empty, clean, unsaved AE project. Existing work was not changed.",
    );
  await call("ae_get_skill", { name: "ae-clean-rig" });
  const catalog = await call("ae_catalog");
  for (const category of ["comp", "layer", "shape", "text", "property", "keyframe", "batch"])
    await call("ae_catalog", { category });
  const comp = "FNF Local MCP — Smoke Test";
  const ops = [];
  const add = (operation, args) => ops.push({ operation, args });
  const position = (layer, value) =>
    add("property.set", {
      comp,
      layer,
      property: ["ADBE Transform Group", "ADBE Position"],
      value,
    });
  add("comp.create", { name: comp, width: 1280, height: 720, fps: 30, duration: 2 });
  for (const [layer, size, color, at, roundness] of [
    ["Background", [1280, 720], [0.035, 0.045, 0.055, 1], [640, 360], 0],
    ["Card", [1120, 550], [0.08, 0.1, 0.12, 1], [640, 360], 32],
    ["Accent", [80, 8], [0.55, 0.98, 0.65, 1], [200, 240], 4],
  ]) {
    add("layer.create_shape", { comp, name: layer });
    add("shape.add_group", { comp, layer, name: "Surface" });
    add("shape.add_rect", { comp, layer, groupIndex: 1, size, roundness });
    add("shape.add_fill", { comp, layer, groupIndex: 1, color });
    position(layer, at);
  }
  for (const [name, text, fontSize, at, color] of [
    ["Eyebrow", "FNF / AFTER EFFECTS", 20, [160, 194], [0.55, 0.98, 0.65]],
    ["Title", "Connected.", 88, [154, 370], [0.96, 0.98, 1]],
    [
      "Subtitle",
      "Native layers. Local control. Offline skills.",
      28,
      [160, 432],
      [0.64, 0.7, 0.74],
    ],
    ["Footer", "MCP  →  EXTENDSCRIPT  →  AFTER EFFECTS", 16, [160, 554], [0.46, 0.53, 0.59]],
  ]) {
    add("layer.create_text", { comp, name, text });
    add("text.set_style", {
      comp,
      layer: name,
      font: "ArialMT",
      fontSize,
      fillColor: color,
      applyFill: true,
      applyStroke: false,
      justification: "left",
    });
    position(name, at);
  }
  for (const [layer, delay] of [
    ["Title", 0],
    ["Subtitle", 0.15],
  ]) {
    const property = ["ADBE Transform Group", "ADBE Opacity"];
    add("keyframe.add", { comp, layer, property, time: delay, value: 0 });
    add("keyframe.add", { comp, layer, property, time: delay + 0.5, value: 100 });
    for (const keyIndex of [1, 2])
      add("keyframe.set_easing", { comp, layer, property, keyIndex, preset: "ease" });
  }
  const built = await call("ae_do", { operation: "batch.run", args: { ops, stopOnError: true } });
  mkdirSync(output, { recursive: true });
  const frames = [];
  for (const time of [0, 0.3, 1]) {
    const outPath = resolve(output, `frame-${time}.png`);
    const rendered = await call("ae_render_frame", { compNameOrId: comp, time, outPath });
    frames.push({ time, outPath, result: rendered });
  }
  const project = await call("ae_save_project", { path: resolve(output, "fnf-local-smoke.aep") });
  const info = await call("ae_project_info");
  writeFileSync(
    resolve(output, "report.json"),
    JSON.stringify(
      {
        date: new Date().toISOString(),
        catalogOperationCount: catalog.totalOperations,
        built,
        frames,
        project,
        info,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    JSON.stringify(
      {
        ok: true,
        output,
        operationCount: catalog.totalOperations,
        frames: frames.map((x) => x.outPath),
        project: project.result,
      },
      null,
      2,
    ),
  );
} finally {
  await client.close();
}
