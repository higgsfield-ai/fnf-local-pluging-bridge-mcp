---
name: ae-mcp-realities
description: Companion module of ae-clean-rig, loaded on demand through ae_get_skill. Not an entry point: do not select it directly and do not use it to start After Effects work — ae-clean-rig decides when this module is needed. Covers local MCP capabilities, operation discovery, policy restrictions, error recovery and differences from the cloud bridge.
---

# Local MCP realities

Use the local `higgsfield-use-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

## Connection and scope

The desktop client launches a stdio MCP process. On macOS it asks AE to run the bundled dispatcher through AppleScript; on Windows it launches AfterFX with `-r`. The dispatcher reads a per-request local mailbox file and writes a correlated response. This is executable scripting, not simulated mouse input. No panel is installed in AE. Node, AE, OS permissions and AE scripting preferences are required independently.

Skill lookup and `ae_catalog` work without launching AE. `ae_project_info` tests the actual connection. A successful MCP handshake alone does not prove AE is reachable. This server controls After Effects only, not Blender or Premiere.

## Discover, then execute

`ae_catalog({})` lists categories and operation names. `ae_catalog({category: "layer"})` gives parameter schemas; execute with `ae_do({operation: "layer.create_text", args: {...}})`. Native cameras and 3D layers are available through cataloged operations; the old bridge's blanket no-3D restriction does not apply. Installed effects and renderer capabilities still need inspection.

Layer indices are mutable and one-based. Prefer stable identifiers where accepted, or resolve uniquely named layers again after insertions, deletion and precomposition. AE effect match names are more reliable than localized labels. Reacquire property groups after structural edits.

## Policy and errors

`AE_MCP_READONLY=1` limits mutation; `AE_MCP_ALLOW_CATEGORIES` filters operations; arbitrary scripting requires `AE_MCP_ENABLE_EVAL=1`. Do not enable eval to bypass an unsupported operation without the user's request. Respect application-configuration confirmations separately from project edits.

A batch uses one undo group but is not a database transaction: earlier operations may already have succeeded when a later operation fails. Inspect partial results before retrying. A timeout after request consumption means completion is uncertain; inspect project state before replaying a mutation. Call undo alone if appropriate, never nested in a batch.

Errors use `{ok:false,error:{code,message,retryable,...}}`. Even a retryable transport error does not mean a project mutation is safe to repeat. Fix schema errors before dispatch, distinguish operation-returned errors from transport completion, and preserve meaningful failure details.

Read [bridge migration](references/bridge-mapping.md) for capability boundaries.
