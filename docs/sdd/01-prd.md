# 01 · Product Requirements (PRD)

## Users

- **Reflex app developers** who need an interactive graph/flowchart/node-editor
  without writing TypeScript or React.
- **Data/ML engineers** visualizing pipelines or DAGs from Python data.
- **Tool builders** embedding editable node graphs in internal tools.

## User stories

1. *As a Reflex developer*, I can render a graph by passing Python lists of
   blocks and connections, so I never touch JavaScript.
2. *As a developer*, I can build entities with typed, validated Python objects,
   so misconfiguration fails fast with a clear error.
3. *As a developer*, I can toggle rendering options (bezier/straight edges,
   arrows, labels, drag, zoom) from Reflex state and see the graph update live.
4. *As a developer*, I can recolor the graph (theme) by passing a colors dict.
5. *As a developer*, I can render hundreds to thousands of nodes and still pan/
   zoom smoothly.
6. *As a developer*, I can react to user interaction (selection, new
   connections, camera moves) in my Reflex event handlers.
7. *As a maintainer*, I can build and publish the package to PyPI with `uv`.

## Functional requirements

- **FR1** Expose a `graph_canvas` / `GravityGraph` component.
- **FR2** Accept `blocks` and `connections` as JSON-serializable lists of dicts.
- **FR3** Accept `settings`, `colors`, `constants` dicts passed through to the
  library unchanged (snake/camel-agnostic at the data level).
- **FR4** Provide `Block`, `Connection`, `Anchor`, `EAnchorType`, `GraphData`
  value objects that emit the correct camelCase payloads and validate inputs.
- **FR5** Provide camera controls: `auto_start`, `zoom_on_start`, `zoom_target`,
  `zoom_padding`.
- **FR6** Emit events: block selection, connection created, connection selection,
  camera change, block drag end, graph state change — each as a plain dict.
- **FR7** Optionally render rich HTML/React block bodies at detailed zoom.
- **FR8** Ship recipe helpers reproducing the upstream Storybook examples.
- **FR9** Ship a multi-page demo app covering every example category.

## Non-functional requirements

- **NFR1 (SSR safety)** The engine touches `window`/Canvas → client-only render
  via `NoSSRComponent`.
- **NFR2 (Performance)** Large graphs (5k nodes) must remain interactive; use
  straight edges and disable arrows at scale in the demo presets.
- **NFR3 (Reproducibility)** Pin the npm version (`@gravity-ui/graph@1.11.0`);
  the layered-graph generator uses a fixed seed.
- **NFR4 (Packaging)** Conform to the Reflex custom-component layout and the
  PyPI publishing prerequisites; build with `uv`.
- **NFR5 (Quality)** Pure-Python domain/recipe logic is unit-tested without a
  running frontend; component wiring is contract-tested with Reflex installed.
- **NFR6 (Compatibility)** Python ≥ 3.10; Reflex ≥ 0.8; React 17/18 (the
  library's peer range).

## Acceptance criteria

- A minimal `graph_canvas(blocks=[...], connections=[...])` renders.
- Demo pages load and reproduce: basics, anchors, colored/dashed edges,
  bezier/straight, vertical direction, grouping, scale presets, theming,
  camera toggles, and interaction events.
- `pytest -q` green; `reflex component build` + `twine check` green.
