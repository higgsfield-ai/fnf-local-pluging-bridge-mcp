# Publishing the npm package

The package name is `fnf-after-effects-mcp`. Publishing needs an authorized npm account; users installing the public package do not need one. Keep upstream attribution in `LICENSE` and the separate skill provenance in `UPSTREAM.md`.

## Prepare

Use Node 24+ and a clean release branch. If skill sources changed, commit them, run `npm run sync:skills -- ./creative-skills` and commit the pinned bundle first.

```sh
npm ci --ignore-scripts
npm run check
npm run test:offline
npm run test:package
npm publish --dry-run --access public
```

`prepack` compiles the server before packing. Consumers install prebuilt files with scripts disabled; no development dependencies are needed. Package verification installs the tarball and its production dependencies into a fresh temporary prefix, then exercises its CLI and MCP tools from outside the checkout.

## Publish

```sh
npm login --auth-type=web --registry=https://registry.npmjs.org/
npm whoami --registry=https://registry.npmjs.org/
npm publish --access public
npm view fnf-after-effects-mcp@0.1.0 version dist.integrity
```

Complete login and any publish verification in npm's browser flow. Never put account credentials or tokens in repository files or chat. npm may require two-factor verification. A dry run does not establish publishing permission or reserve the name.

After publication, test the registry version in a fresh prefix, update the server's `/use-after-effects` setup instructions. Only then describe the npm installation as available. Use a new version for subsequent releases and update pinned setup examples together.
