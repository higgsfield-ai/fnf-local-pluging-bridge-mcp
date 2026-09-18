# Bridge migration

| Former bridge workflow | Local equivalent |
| --- | --- |
| `AE_get_skills` / skill retrieval | `ae_get_skill` with no name for index, name for entry, reference for one module |
| Individual cloud layer/property tools | `ae_catalog` then `ae_do` with the documented operation |
| Host connection status | Offline CLI doctor, then `ae_project_info` for live AE |
| Screenshot / frame proof | `ae_render_frame`, inspect returned image |
| Cloud identity / relay | Not required for local stdio; OS and Adobe requirements still apply |
| HTML-to-scene, cloud preview, Lottie converter | Not provided by this runtime; build a native scene plan or add a separately tested adapter |
| Image/video generation | A separately available provider, if requested |
| Blender / Premiere tools | Separate integrations; not available in this server |

`ae_project_export_json` / `ae_project_import_json` use this runtime's own project schema. They do not accept or produce Lottie JSON. Do not imply that the historical archived instructions are executable locally. The active skill corpus is adapted; the archive preserves the original material for future migration.
