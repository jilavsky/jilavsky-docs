# Documentation screenshots: shot list

One row per screenshot in `docs/`. The ID is `<page>-<nn>-<what>`, where `<page>` is the page's
file name; the image lives next to the page at `<page dir>/img/<page>/<id>.png`.

- **automated: yes**: `python scripts/make_doc_screenshots.py --only <id>` makes it.
- **automated: no**: needs judgment (real data, a tricky state, an OS dialog). The page holds an
  invisible `% SCREENSHOT <id>: …` comment until the image exists; then replace the comment with
  a `figure` that has alt text and a caption, and set the status to `done`.
- **status**: `done` (image committed and shown), `todo` (placeholder only).

`tests/test_doc_screenshots.py` checks that this list, the pages, the images and the
`@shot` functions agree.

Column order: ID · page · dataset · state to set up · must show · automated? · status.

## <page>

| ID | page | dataset | state to set up | must show | automated? | status |
|---|---|---|---|---|---|---|
