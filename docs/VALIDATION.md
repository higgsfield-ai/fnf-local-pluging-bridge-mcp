# Validation of the FNF local fork

Tested on macOS with Node 24.14.0 and Adobe After Effects 2026 on 2026-09-10.

## Automated checks

- Offline Vitest suite (276 tests): operation schemas, transport behavior, errors, policy, JSX compatibility, bundled skills and real MCP stdio discovery.
- TypeScript source and test typechecks, lint, formatting, generated tool documentation drift check.
- Skill frontmatter validations and all active local Markdown reference links.
- Package verification: extract the npm tarball to a temporary directory, start its server from an unrelated working directory, discover 12 tools and read a bundled reference. Dependencies are linked from the installed runtime; this checks packaged content, not a fresh network dependency installation.
- Codex registration and entry-skill installation are idempotent on this Mac.

## Live AE smoke test

A real `ae_project_info` call succeeded in 333 ms. The project was empty, clean and unsaved before the demo. The catalog exposed 197 native operations with the default policy.

`scripts/live-smoke.mjs` created one 1280×720 composition at 30 fps, seven editable native shape/text layers, opacity keyframes with easing, and rendered frames at 0, 0.3 and 1 second. All three PNGs were visually inspected: the initial hidden title/subtitle, partial reveal and settled state behaved as intended. The project was saved to `runtime/local-smoke/fnf-local-smoke.aep`; a structured execution report and PNGs accompany it. These generated files are ignored by Git.

The live demo intentionally refuses to run against an existing or dirty project. It leaves its own saved demonstration project open for review. Run it explicitly with `node scripts/live-smoke.mjs`; it is not part of routine tests.

## Limits

Windows runtime and installation have not been tested on this machine. The full destructive upstream E2E suite was not run. The smoke test verifies native construction, keys, rendering and saving; it does not establish that every native operation or specialized glass/depth recipe works in every AE version. The ten read-only evaluation questions in `evaluations/skills.xml` are prepared cases, not an independent model evaluation result.
