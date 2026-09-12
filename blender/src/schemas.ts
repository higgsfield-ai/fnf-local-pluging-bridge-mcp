import { z } from "zod";


const vec3 = z.tuple([z.number(), z.number(), z.number()]);

export const executeShape = {
  code: z
    .string().min(1).max(1_000_000)
    .describe(
      "Python source executed inside the connected Blender with full `bpy` "
      + "access. To return data, assign a JSON-serialisable value to a variable "
      + "named `result`.",
    ),
};

export const sceneSummaryShape = {};

export const addPrimitiveShape = {
  kind: z
    .enum(["cube", "uv_sphere", "ico_sphere", "cylinder", "cone", "plane", "torus", "monkey"])
    .describe("Primitive type to add."),
  name: z.string().optional().describe("Rename the created object to this."),
  location: vec3.optional().describe("World position [x, y, z] in metres (Z up). Default [0,0,0]."),
};

export const deleteObjectShape = {
  name: z.string().describe("Exact name of the object to delete."),
};

export const setTransformShape = {
  name: z.string().describe("Exact object name to transform."),
  location: vec3.optional().describe("Parent-relative location [x, y, z] in scene units."),
  rotation_euler: vec3.optional().describe("Euler rotation [x, y, z] in RADIANS (XYZ)."),
  scale: vec3.optional().describe("Scale factors [x, y, z] (1 = unchanged)."),
};

export const setMaterialShape = {
  object: z.string().describe("Exact object name to receive the material."),
  color: z
    .tuple([z.number(), z.number(), z.number(), z.number()])
    .optional()
    .describe("Base colour RGBA, each 0-1. Default opaque mid-grey."),
  metallic: z.number().min(0).max(1).optional().describe("Metallic 0-1."),
  roughness: z.number().min(0).max(1).optional().describe("Roughness 0-1."),
  material_name: z.string().optional().describe("Name for the created material."),
};

export const importModelShape = {
  path: z.string().min(1).describe("Absolute local file path to import instead of a URL."),
  location: vec3.optional().describe("Move the imported root to this world position."),
};

export const addLightShape = {
  type: z.enum(["POINT", "SUN", "SPOT", "AREA"]).describe("Light type."),
  location: vec3.optional().describe("World position [x, y, z]. Default [0,0,5]."),
  energy: z.number().optional().describe("Light power/energy (watts). Default 1000 for POINT/SPOT/AREA, 5 for SUN."),
  name: z.string().optional().describe("Rename the created light."),
};

export const addCameraShape = {
  location: vec3.optional().describe("World position [x, y, z]. Default [7.36, -6.93, 4.96]."),
  rotation_euler: vec3.optional().describe("Euler rotation [x, y, z] in RADIANS. Default a 3/4 view."),
  set_active: z.boolean().optional().describe("Make this the active scene camera. Default true."),
  name: z.string().optional().describe("Rename the created camera."),
};

export const setActiveCameraShape = {
  name: z.string().describe("Exact camera object name to make active."),
};

export const setFrameShape = {
  frame: z.number().int().describe("Frame number to set as current."),
};

export const renderShape = {
  output_path: z.string().min(1).describe("Absolute path for the PNG. Default a temp file."),
  resolution: z
    .tuple([z.number().int().min(1).max(16384), z.number().int().min(1).max(16384)])
    .optional()
    .describe("Render [width, height] in pixels. Default the scene's current setting."),
  engine: z.enum(["BLENDER_EEVEE_NEXT", "CYCLES", "BLENDER_WORKBENCH"]).optional()
    .describe("Render engine. Default the scene's current engine."),
  samples: z.number().int().min(1).max(65536).optional().describe("Cycles sample count; requires the CYCLES engine."),
};

export const screenshotShape = {
  max_size: z
    .number()
    .int()
    .min(64).max(2048)
    .optional()
    .describe("Longest-edge pixel cap for the capture (keeps it under the 1MB message limit). Default 1280."),
  shading: z
    .enum(["SOLID", "MATERIAL", "RENDERED", "WIREFRAME"])
    .optional()
    .describe("Viewport shading to capture with. Default keeps the current viewport shading."),
};

export const getObjectShape = {
  name: z.string().describe("Exact object name to inspect."),
};
