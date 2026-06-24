# 05 · Task Breakdown

Status legend: ✅ done · 🔜 roadmap.

## Phase 0 — Foundations
- ✅ T0.1 Scaffold repo in the Reflex custom-component layout.
- ✅ T0.2 `pyproject.toml` with package metadata, `uv`/setuptools, `dev` extras.
- ✅ T0.3 LICENSE (Apache-2.0), `.gitignore`, CHANGELOG, GitHub Actions CI.
- ✅ T0.4 `graph_canvas.jsx` bridge: `useGraph`, `setEntities`, `useGraphEvents`,
  `onStateChanged` → `start` + `zoomTo`.
- ✅ T0.5 `GravityGraph` component: `NoSSRComponent`, `$/public` bridge import,
  `lib_dependencies = ["@gravity-ui/graph@1.11.0"]`, prop surface.

## Phase 1 — Data & domain
- ✅ T1.1 `EAnchorType`, `Anchor`, `Block`, `Connection` value objects.
- ✅ T1.2 `GraphData` aggregate with duplicate-id + dangling-edge validation.
- ✅ T1.3 camelCase `to_dict()` serialization matching `TBlock`/`TConnection`.
- ✅ T1.4 Public API re-exports in `__init__.py`.

## Phase 2 — Examples & demo
- ✅ T2.1 `default_settings`, `THEMES` (light/dark) presets.
- ✅ T2.2 `one_block`, `two_connected_blocks`, `colored_connections`,
  `block_with_anchors`.
- ✅ T2.3 `generate_layered_blocks` (hundred/thousand/five-thousand) + seed.
- ✅ T2.4 `grouped_graph`.
- ✅ T2.5 Demo shell (sidebar + layout) and shared `GraphState`.
- ✅ T2.6 Pages: Basics, Connections, Scale, Grouping, Camera, Theming,
  Interaction.

## Phase 3 — Events & interaction
- ✅ T3.1 Event props + serializable payload reduction in the bridge.
- ✅ T3.2 Interaction demo page with live event log.
- ✅ T3.3 Optional `render_html_blocks` (HTML/React blocks at detailed zoom).

## Phase 4 — Packaging & publish
- ✅ T4.1 Tests: `test_domain`, `test_recipes`, `test_contract` (render +
  public API). Pure-Python suite verified (21/21).
- ✅ T4.2 README with `uv` build/publish workflow.
- ✅ T4.3 SDD artifacts + research notes.
- ✅ T4.4 `git init`, commit on `main`, public GitHub repo.
- ⏳ T4.5 `uv run reflex component build` (generates `*.pyi` + dist) — run with a
  Reflex-supported Python (3.10–3.12).
- ⏳ T4.6 `uv publish` to PyPI (requires an API token).

## Roadmap tasks
- 🔜 T5.x Plugin layers: MiniMap, DevTools, CSS-variables, ELK/layered layout.
- 🔜 T6.x Custom canvas block registration (`settings.blockComponents`).
- 🔜 T7.x Imperative API as Reflex special events (zoomToBlocks, updateEntities).
- 🔜 T8.x Connection-creation layers (ConnectionLayer/NewBlockLayer/Port…).
