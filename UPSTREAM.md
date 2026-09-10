# Upstream and provenance

This local fork is based on [kumo.productions/mcp-aftereffects](https://github.com/kumoproductions/mcp-aftereffects), version 0.2.0 at commit `11f6ca4` (full history retained). Its MIT license and copyright notice remain in LICENSE. The upstream author's identity is retained as attribution, not a claim of authorship of FNF changes.

FNF changes add offline AE skill delivery, a pinned skill corpus, local setup diagnostics, installation support and validation. `skills/manifest.json` identifies the source commit and SHA-256 of every served document. Source instructions originate in the private FNF bridge project and are maintained under `creative-skills/` in this repository (originally `fnf-creative-apps-skills`). They are not covered by the upstream runtime's MIT grant; no additional redistribution license is granted here.

The upstream automated publishing workflow and registry entry are removed. The FNF distribution uses its own npm package name, `fnf-after-effects-mcp`; it is not a release by the upstream author and is not registered in the MCP Registry. Existing operation/transport documentation and historical release notes describe upstream behavior unless explicitly updated here.
