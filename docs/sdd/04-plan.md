# 04 · Implementation Plan

## Milestones

### M0 — Foundations  ✅
- Repo scaffold in the Reflex custom-component layout.
- `pyproject.toml` (setuptools + `uv` workflow), LICENSE, `.gitignore`, CI.
- JSX bridge (`graph_canvas.jsx`) + `GravityGraph` (`NoSSRComponent`, `$/public`
  bridge import, pinned `lib_dependencies`).

### M1 — Data & domain  ✅
- `Anchor` / `Block` / `Connection` / `GraphData` value objects + validation.
- snake→camel render contract; public API re-exports.

### M2 — Examples & demo  ✅
- `recipes.py`: basics, anchors, colored edges, grouping, layered generator,
  settings + theme presets.
- Multi-page demo: Basics, Connections, Scale, Grouping, Camera, Theming,
  Interaction — with live controls and a shared `GraphState`.

### M3 — Events & interaction  ✅
- Selection / connection-created / connection-selection / camera / drag-end /
  state-change events; serializable payloads; optional HTML blocks.

### M4 — Packaging & publish  ✅ (build/publish steps require credentials)
- Tests (domain, recipes, public API, render contract) + GitHub Actions CI.
- README with `uv` build/publish instructions.
- `uv run reflex component build` → generates `*.pyi` stub + wheel/sdist.
- `git` repo on `main`; public GitHub repo; `uv publish` to PyPI.

## Roadmap (post-0.1)

- **Plugin layers (M5).** Per-layer bridges + optional extras for MiniMap,
  DevTools, CSS-variables, and ELK / layered auto-layout (`elkjs`).
- **Custom canvas blocks (M6).** A registration mechanism for
  `settings.blockComponents` (custom `is` → React/Canvas renderer).
- **Imperative API surface (M7).** Expose `zoomToBlocks`, `updateEntities`,
  selection-bucket APIs as Reflex special events / refs.
- **Connection-creation UX (M8).** Wrap `ConnectionLayer` / `NewBlockLayer` /
  `PortConnectionLayer` examples.

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Hook API can't be wrapped directly | Local JSX bridge (ADR-1). |
| Event payloads non-serializable | Reduce to ids/coords in the bridge (ADR-5). |
| Large graphs janky | Straight edges + no arrows at scale; canvas LOD. |
| Upstream breaking changes | Pin npm version; bump deliberately (ADR-3). |
| `.pyi` drift | Generate via `reflex component build`, ship in wheel. |

## Definition of done

- Demo reproduces every example category and runs via `reflex run`.
- `pytest -q` green locally and in CI on 3.10–3.12.
- Wheel/sdist build clean; `twine check` passes; package published & importable.
