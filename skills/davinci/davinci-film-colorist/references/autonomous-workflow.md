# Application Access and Recovery

## Establish the session

Discover the available Resolve tools and read the current schemas for the required actions. A registered server, historical configuration, or saved success does not establish a usable connection. If the documented connection route is unavailable, use another existing supported route; do not invent API calls or silently require installation or an application update.

Select the project and material specified by the user. For an open-project request, verify the actual project, timeline, selected clip, timecode, and current grade version. Resolve ambiguous targets before a write. An offline source or empty Viewer cannot support grading from substitute footage or a similar thumbnail. Keep reads and writes within the requested material and the Color workflow.

## Operation ownership

Pending and timed-out operations may still be running. Retain ownership of the operation until it finishes or its own client is safely stopped after identity checks. Stopping that client does not cancel a command already delivered to Resolve. Do not issue a duplicate command or concurrent SDK and GUI action while completion is unknown. Record the last confirmed state and uncertainty, then recheck project, timeline, clip, timecode, version, and transport before proceeding.

Inspect the full behavior of each wrapper before a write. A compound version operation may also archive a timeline; unchanged selection does not prove that no copy was created. If extra actions exceed the request, use a documented route with the required scope and recovery behavior. Do not invent bypass flags or assume a granular interface inherits compound backups. Read back the actual affected state after the action.

## Recoverable grading

Record the active grade and timecode and preserve a control frame. Create a distinct usable grade version when needed, verify that it is active, and confirm that its initial image matches the baseline. An existing suitable backup can satisfy recovery requirements; do not make redundant copies automatically.

For a correction to one clip, keep selection limited to it. When converting a remote grade to a local grade, distinguish the individual version's Copy to Local operation from timeline-wide grade commands. Local versions do not isolate Shared, Group, or Timeline nodes. Keep those areas unchanged unless their modification is requested and their recovery is established. Converting a selected Shared node to a normal Corrector is different from globally deleting its shared source.

Before replacing a grade through DRX, establish the exact target, graph scope, layer, dependency contract, and a verified return path for the replaced content. A PNG, a list of names, an API success flag, or a confirmation token is not a restorable grade. A neutral CDL is not undo. Getter addressing does not automatically establish a setter's target or layer.

## Verify and recover from errors

After a state-changing operation, read back the affected objects and inspect the actual image. A file path does not prove that its image was viewed. Confirm timeline copies when the wrapper is expected to create them. Separate successful parameter storage, visual response, restoration, and saved output.

If a menu action unexpectedly starts playback, inspect the new state before trying another route. A confirmed stop does not restore the original frame. Repeated identical failures without new evidence are a stopping condition for that route. Continue independent permitted work and report the precise limitation.

Before returning control, restore expected Viewer and diagnostic modes, verify the chosen version and transport state, and save the authorized result. Supply the current project context and visual intent when a future task needs to continue the work; do not promise memory or application access across sessions.
