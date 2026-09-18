# Add-on Installation

## Bundled dependency

Use the bundled [Blockstage 0.3.0 installation-unlocked variant](../assets/Blockstage-0.3.0.zip), resolved relative to this skill. Its installation version threshold has been relaxed; functional code, the license, character library, and thumbnails are preserved. The relaxed installer metadata does not establish compatibility with every Blender release. Its manifest identifies blockstage version 0.3.0. No separate Cast installation is needed.

## Automatic setup

Perform dependency setup as part of the requested Blockstage workflow, without asking the user to install it manually or seeking redundant confirmation. Use the user's installed Blender through the existing connection or native interface. This skill imposes no specific Blender version; establish compatibility through the native installer's result, extension registration, and asset loading. Discover the actual extension repository and registered module in that Blender installation; do not assume a user directory or module prefix.

When installation is needed, use Blender's native Install from Disk operation in Edit, Preferences, Get Extensions. Select the bundled ZIP directly and enable the installed extension. The native operation is also exposed as extensions.package_install_files for tools that provide Blender API access. Save the enabled preference in the same Blender session. Do not create or require a separate installer script.

If 0.3.0 is already installed but disabled, enable it. If another version or a legacy copy conflicts, preserve its recoverable files and settings, disable only the conflicting Blockstage registration, and install the bundled version through Blender's extension manager. Do not enable duplicate copies. Preserve unsaved scene work before any necessary restart. Avoid changing preferences through a background Blender process while the user's Blender is open.

Confirm the registered version and the Blockstage sidebar in the 3D View. Confirm that Room Builder and Man, Woman, Heavy Man, and Heavy Woman are available, including the cast library and thumbnails. Copying an archive alone is not a completed installation. Existing characters in older scenes are not automatically replaced by installing the extension.

If Blender access, the archive, or a required permission is unavailable, state the exact missing requirement and request only what is needed. If Blender rejects the extension or its character library, report the actual compatibility error without bypassing installation checks or claiming unsupported compatibility. Do not report installation success or substitute another asset system. Skill instructions cannot bypass tool permissions or create a Blender connection themselves.
