# Video documentation projects

`docs/videos/` stores source projects for workspace-level video documentation.

## Commit policy

Track source inputs that are needed to reproduce a video:

- `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `storyboard*.md`
- `hyperframes.json`, `meta.json`, `index.html`, composition HTML, and lightweight source assets

Do not commit generated render outputs by default:

- `renders/` MP4/PNG outputs
- `.thumbnails/` local preview thumbnails

Generated outputs may be attached to releases or shared through external storage when needed, but they should not be mixed into root bootstrap commits unless explicitly approved.

## Current project

- `subproject-intros/` is a HyperFrames source project for Korean subproject introduction content.
- Its `renders/` and `.thumbnails/` directories are local/generated outputs and are ignored by the root `.gitignore`.
