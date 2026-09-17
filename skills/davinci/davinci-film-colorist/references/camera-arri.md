# ARRI Source Profiles

ARRIRAW contains sensor data that a decoder develops into RGB. Neither ARRIRAW nor an MXF container establishes camera model or the gamma entering a Color node. Read the effective decoder output and earlier processing before selecting a transform.

The original ALEXA Mini and Mini LF encoding uses ARRI Wide Gamut 3 and LogC3; the LF designation alone does not imply LogC4. ALEXA 35's original REVEAL processing uses ARRI Wide Gamut 4 and LogC4. Reprocessing compatible older ARRIRAW through REVEAL can produce AWG4/LogC4 despite older camera notes. That possibility does not apply automatically to already developed ProRes or another RGB transcode.

Read Decode Using and the effective Camera Raw settings. With project inheritance, inspect the project's ARRI decoder controls. An active Decode as LogC4 changes the decoded output contract; an inactive unchecked control does not establish the inherited value. Preserve an explicitly accepted decode unless a change is requested.

For ProRes or another processed source, establish the saved gamma, gamut, baked look, and output transformation. A RAW control cannot restore the original sensor data. If managed processing or an earlier transform already converted the source, the next CST receives that new signal rather than camera LogC.

A manufacturer display LUT requires its declared input and output contract. A CST with matching space labels is not automatically visually equivalent to the manufacturer's rendering. Evaluate mapping separately and use the display target agreed for the task.

Use the current official camera encoding and RAW workflow documentation when exact model or decoder behavior is uncertain. These mappings were carried from the supplied reference material; they do not constitute a new camera, decoder, or Resolve runtime test.
