# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-10-24

Compatibility release for **Reflex 0.10**.

### Changed
- Require `reflex>=0.10.0` (was `>=0.8.0`); verified against Reflex 0.10.0
  (React 19, Vite 8, react-router 8).
- Require Python `>=3.11` (Reflex 0.10 dropped Python 3.10); CI matrix is now
  3.11 / 3.12 / 3.13.
- Build requirement bumped to `setuptools>=78.1.1`.
- Regenerated `graph.pyi` with the Reflex 0.10 stub generator (PEP 604
  `X | None` event-handler annotations).
- Demo app: declare `rx.plugins.RadixThemesPlugin()` explicitly (implicit Radix
  enablement is deprecated) and require `reflex>=0.10.0`.

### Docs & tooling
- README, SDD and research notes updated: `reflex component build/share` no
  longer exist in Reflex 0.10 — build with `uv build` and regenerate the stub
  with `python -m reflex_base.utils.pyi_generator`.
- CI gains a job that compiles the demo app against the component.

## [0.1.0] - 2026-06-24

First release. A publish-ready Reflex custom component wrapping
`@gravity-ui/graph@1.11.0`.

### Added (Component)
- `GravityGraph` / `graph_canvas` wrapper rendered through a local JSX bridge
  (`graph_canvas.jsx`) that drives the upstream `useGraph` hook + imperative API
  (`setEntities`, `start`, `zoomTo`) behind a flat, declarative prop surface.
- Client-only rendering via `NoSSRComponent`; npm dependency
  `@gravity-ui/graph@1.11.0` pinned through `lib_dependencies`.
- Props: `blocks`, `connections`, `settings`, `colors`, `constants`,
  `config_name`, `auto_start`, `zoom_on_start`, `zoom_target`, `zoom_padding`,
  `render_html_blocks`.
- Events: `on_block_selection_change`, `on_connection_created`,
  `on_connection_selection_change`, `on_camera_change`, `on_block_drag_end`,
  `on_state_change` — each forwarding a plain serializable payload.

### Added (Domain — DDD)
- `Block`, `Connection`, `Anchor`, `EAnchorType` value objects that serialize to
  the upstream camelCase entity shapes and validate their invariants.
- `GraphData` aggregate with duplicate-id and dangling-edge validation.

### Added (Recipes)
- Example builders reproducing the Storybook stories: `one_block`,
  `two_connected_blocks`, `colored_connections`, `block_with_anchors`,
  `grouped_graph`, and `generate_layered_blocks` (hundred / thousand /
  five-thousand block performance graphs).
- `default_settings` and the `THEMES` (light/dark) color presets.

### Added (Demo)
- Multi-page Reflex demo app with one page per example category: Basics,
  Connections, Scale, Grouping, Camera & Zoom, Theming, Interaction & Events.

### Added (Docs & tooling)
- Spec-Driven Design artifacts under `docs/sdd/` (overview, PRD, architecture,
  component spec, plan, tasks) and research notes under `docs/research/`.
- `uv`-based developer/publishing workflow, pytest suite (domain, recipes,
  public API, render contract) and a GitHub Actions CI workflow.
