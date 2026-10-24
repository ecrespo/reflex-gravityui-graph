# 05 · Task Breakdown

Status legend: ✅ done · ⏳ pending (env/credentials) · 🔜 roadmap.

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
  public API), plus `test_packaging` (import surface / bridge contract) and
  `test_demo` (demo functional guards). Suite verified (32/32).
- ✅ T4.2 README with `uv` build/publish workflow.
- ✅ T4.3 SDD artifacts + research notes.
- ✅ T4.4 `git init`, commit on `main`, public GitHub repo.
- ✅ T4.5 `.pyi` stub + dist — stub via `reflex_base.utils.pyi_generator`,
  dist via `uv build` (Python 3.11–3.13, Reflex ≥ 0.10).
- ✅ T4.6 `uv publish` to PyPI.

## Roadmap tasks
- 🔜 T5.x Plugin layers: MiniMap, DevTools, CSS-variables, ELK/layered layout.
- 🔜 T6.x Custom canvas block registration (`settings.blockComponents`).
- 🔜 T7.x Imperative API as Reflex special events (zoomToBlocks, updateEntities).
- 🔜 T8.x Connection-creation layers (ConnectionLayer/NewBlockLayer/Port…).

## Validation pass (post-implementation review)

A code-vs-spec review surfaced gaps the original ✅ marks hid. Each was fixed
test-first (RED → GREEN); the suite grew 25 → 34.

- ✅ T-G1 NFR5 — make `domain`/`recipes` importable without Reflex. `__init__`
  eagerly imported `graph.py` (→ Reflex), so the "pure" suite couldn't run on a
  minimal env. Fixed with a PEP 562 `__getattr__` that defers the component
  exports. Guard: `test_packaging.py::test_domain_and_recipes_import_without_reflex`.
- ✅ T-G2 FR6 — lock the event/bridge contract. Added guards that all six event
  triggers are exposed and wireable, that the JSX bridge ships, and that it still
  subscribes to the documented upstream event names + payload keys
  (`test_contract.py`, `test_packaging.py`).
- ✅ T-G3 Demo — wire the full event surface on the Interaction page (was 3/6;
  added `on_connection_selection_change`, `on_block_drag_end`, `on_state_change`).
  Guard: `test_demo.py::test_interaction_page_wires_full_event_surface`.
- ✅ T-G4 Demo — replace the invalid `github` lucide icon (silently downgraded to
  `circle_help`) with `code`. Guard: `test_demo.py::test_sidebar_uses_only_valid_icons`.
- ✅ T-G5 Interactivity — nodes were immovable: `@gravity-ui/graph`'s runtime
  `DefaultSettings.canDrag` is `ECanDrag.NONE`, and neither the component nor
  `default_settings` emitted `canDrag`. Added a `can_drag_blocks` arg to
  `default_settings` (default `True` -> `canDrag="all"`) and a "Drag nodes"
  toggle on the Camera demo page. Guards:
  `test_recipes.py::test_default_settings_enables_block_drag_by_default`,
  `test_default_settings_can_restrict_block_drag`.
- ✅ T-G6 Connection interactivity — clarified the model: `BlockConnection`
  geometry is derived from block positions, so links follow their nodes and are
  not free-draggable by design. The supported edit is drawing connections by
  dragging anchors (OUT→IN) or Shift+block→block, via `ConnectionLayer` /
  `canCreateNewConnections`. Exposed a "Create links" toggle on the Camera demo
  page (reuses `default_settings(can_create_new_connections=…)`). Free-line drag
  and interactive multipoint waypoints remain roadmap (need a custom layer).
- ✅ T4.5 `.pyi` stub — generated and committed (`graph.pyi`), shipped via
  package-data.
- ✅ T4.6 `uv publish` — 0.1.0 published.
- ✅ T4.7 Reflex 0.10 upgrade (0.2.0): `reflex>=0.10.0`, Python ≥ 3.11, stub
  regenerated, demo compiled and verified in dev + prod (React 19).
