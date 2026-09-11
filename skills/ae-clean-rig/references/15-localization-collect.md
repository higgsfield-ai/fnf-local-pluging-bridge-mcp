# Dependencies, cleanup and handover packages

## Dependency audit

Distinguish missing effects, installed but inactive licenses, effects disabled by the user, expression errors, and output obscured by other layers. An effect inventory does not establish visibility or activation.

Identify the actual vendor and package from the installed effect, its matchName, and official documentation. Record the composition, layer, layer and effect enablement, relevant parameters, masks and occlusion, and visible interval in the final composition. Trace start time, stretch, Time Remap, and repeated nesting before selecting diagnostic frames. Do not identify a plugin family from appearance alone or reuse an earlier project's licensing status.

Verify product identity, compatibility, and any requested purchase information against the vendor's current official source. Purchase, installation, activation, and enabling an effect are distinct actions; approval for analysis does not authorize them. Check application and license-manager state separately. An empty account or license list is insufficient reason to reinstall software or switch accounts. Do not repeatedly reopen deferred licensing decisions without new relevant evidence.

When asked to restore disabled effects, identify the specific instances from reliable history or current evidence. Ask if the affected instances cannot be determined; never enable every effect in the project. Do not disable effects or conceal watermarks to obtain a clean result without authorization. Mark a render affected by unresolved dependencies as DRAFT and identify the remaining dependency.

## Cleanup on copies

Identify the current language projects and final compositions. Check external drives, missing footage, and available space. Preserve unsaved work and perform cleanup only on new copies.

Trace every layer source, including disabled references, nested compositions, proxies, and image sequences. Include expression dependencies that reference other compositions or footage, dynamically constructed names, and externally loaded data. Retain uncertain dependencies and report why. An invisible item is not necessarily unused. Adobe documents that [Reduce Project can remove compositions referenced only by expressions](https://helpx.adobe.com/after-effects/desktop/work-with-footage-items/manage-footage-items/footage-items.html); retain those dependencies explicitly before reduction.

Remove only proven unused items and empty folders from the copy. Do not consolidate superficially similar footage items without checking interpretation and proxies. Record excluded items and their recovery source. Preserve original media, user archives, older projects, and global caches.

## Collection and destination

Use File > Dependencies > Collect Files. On an already cleaned copy, the All option collects remaining sources and proxies without requiring another reduction; inspect proxy options to retain the files needed by the requested package. Native collection handles more than copying the first image of a sequence. [Adobe's collection documentation](https://helpx.adobe.com/after-effects/desktop/render-and-export/basics-of-rendering-and-exporting/basics-rendering-exporting.html) describes the source and proxy options and the generated dependency report.

Create a clearly named parent directory with independent language folders. Select the destination directory separately from the filename and verify the actual created path. After moving a newly collected package, reopen and save its collected project from the final location. Subsequent edits to the original project do not update the collected copy automatically.

## Package verification

Check that required media and proxies resolve inside each collection, with no missing files or new expression errors. Compare retained composition structure, keys, text, and timing against the baseline. Compare copied file sizes and SHA-256 hashes, hashing shared source files once when practical. Footage-item counts need not equal unique-file counts.

If requested, copy existing rendered videos into a Renders folder. Identify them as existing renders and do not imply they reflect later AEP edits without verification.

Collection does not install fonts, plugins, or licenses on another computer. Include exact dependency information and native collection reports. Bundle fonts only when needed and permitted by their licenses; do not redistribute paid or system fonts automatically. Mark incomplete languages as pending. Report cleanup, collection, reopening, and verification as separate completion states.
