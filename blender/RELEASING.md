# Release fnf-blender-mcp

Run commands from this `blender/` directory. Its package.json and package-lock.json are independent of the root After Effects package.

1. Run `npm ci`, `npm test`, `npm run typecheck`, and `npm run test:package`.
2. For a new release, bump the version here with `npm version patch --no-git-tag-version` (or the intended version). npm versions are immutable; `0.1.0` is already published.
3. Update the version in README.md and skills/use-blender/references/installation.md, and synchronize that skill with fnf-mcp-server’s use-blender command bundle. Commit the version, lockfile and instructions together.
4. Run `npm pack --json` and review its file list. Publish the reviewed archive with `npm publish ./fnf-blender-mcp-<version>.tgz --access public --registry=https://registry.npmjs.org/` when release publication is authorized.
5. Verify the registry version and checksum, then install it into an isolated directory and check the MCP tools and offline skill. Report live Blender validation separately.

The source migration does not republish version 0.1.0. Its existing npm archive remains usable; repository.directory metadata takes effect in the next release.
