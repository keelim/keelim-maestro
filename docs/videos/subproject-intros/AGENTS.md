# Workspace introduction video

Own local scenes, assets, and timing, not current child capabilities or registration. This video reflects an earlier workspace; reconcile optional and archived projects before using it as a current introduction.

- Scene edits do not authorize child-repository changes or reactivation.
- Timed elements need `data-start`, `data-duration`, and `data-track-index`. Keep visible `clip` elements and timeline registration aligned.
- Create paused GSAP timelines and register them in `window.__timelines`. Frames must not depend on wall-clock time, randomness, or live data.
- Existing GSAP scripts load from a CDN; do not claim fully offline rendering or add live requests.
- Distinguish muted video from separate audio tracks. When duration changes, verify the next scene's start and total length.
- Renders and thumbnails are generated output. Do not automatically add large outputs in place of source HTML/assets.

With HyperFrames installed, use `npx hyperframes preview`, `npx hyperframes lint`, and `npx hyperframes render` from this directory. After HTML changes, run lint, resolve its errors, and inspect scene boundaries and the final frame in a preview or render. If tooling is absent, report the prerequisite instead of installing a skill/package merely because this guide names it. Keep `CLAUDE.md` linked to this file.
