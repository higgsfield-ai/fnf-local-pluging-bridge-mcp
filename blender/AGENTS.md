# Development

- Keep this package independent of the cloud Adobe connector and sibling checkouts.
- Use stdio for MCP and authenticated loopback HTTP for Blender; execute bpy only on its main thread.
- Never automatically retry a submitted mutation after uncertain completion; preserve the job ID for status recovery.
- Run `npm test` and `npm run typecheck`. Python fixtures do not count as live Blender validation.
- Keep `skills/use-blender` synchronized with its command bundle in `fnf-mcp-server`.
- Use concise Conventional Commit messages. Do not publish or deploy without user authorization.
