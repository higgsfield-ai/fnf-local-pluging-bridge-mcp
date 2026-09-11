---
name: use-blender
description: Install and connect the local Higgsfield use Blender MCP, or use it to edit native Blender scenes.
---

# Higgsfield use Blender

Connect a desktop MCP client to Blender on the same computer:

Desktop client → stdio → local fnf-blender-mcp → authenticated localhost HTTP → Blender Python add-on.

Use **Higgsfield use Blender** as the display name and `higgsfield-use-blender` as the server identifier. No WebSocket, cloud bridge login or Higgsfield account is needed for local scene operations. Cloud asset generation uses a separate service.

The runtime is distributed as the public npm package `fnf-blender-mcp`; installation requires no source checkout or build.

This is a local setup command, not a generation preset. A cloud sandbox cannot install into the user's desktop Blender. First discover available local `bl_*` tools and check an existing connection before reinstalling.

For setup, read [installation](references/installation.md). For connection diagnosis and edits, read [verification](references/verification.md). When these files are served by get_preset_instructions, load them with `/use-blender/references/installation` and `/use-blender/references/verification` respectively.
