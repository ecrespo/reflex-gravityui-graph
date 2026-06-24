# 02 · Architecture

## High-level picture

```
Reflex app (Python)
  └─ graph_canvas(blocks, connections, settings, colors, constants, events…)
        │  (Reflex compiles props → React props, snake_case → camelCase)
        ▼
  graph_canvas.jsx  ──────────────── local JSX bridge (shipped in the package)
        │  useGraph(config) → Graph instance
        │  setEntities({blocks, connections})
        │  useGraphEvents(graph, {...})  → serialize → Reflex event handlers
        │  <GraphCanvas graph=… renderBlock=… onStateChanged=start+zoomTo/>
        ▼
  @gravity-ui/graph  ─────────────── npm dependency (Canvas + React engine)
```

## Key decision: a local JSX bridge

`@gravity-ui/graph`'s React surface is **hook-driven and imperative**:

- `const { graph, setEntities, start } = useGraph(config)` creates the instance.
- entities are pushed imperatively via `setEntities` / `updateEntities`.
- the render loop must be `start()`-ed once the canvas reaches
  `GraphState.ATTACHED` (typically inside `onStateChanged`).
- camera is positioned imperatively (`graph.zoomTo("center", {padding})`).

Reflex components map Python classes to React elements, but they **cannot call
React hooks** or run imperative lifecycle code. The idiomatic Reflex solution
(also used elsewhere in this author's component fleet, e.g. the maplibre
`useControl` bridges) is to ship a small **local `.jsx` bridge** that:

1. calls `useGraph` internally,
2. syncs `blocks`/`connections`/`settings`/`colors`/`constants` via effects,
3. subscribes to events and reduces each payload to plain serializable data,
4. starts the loop and fits the camera on `ATTACHED`,
5. exposes everything as flat props.

The Python `GravityGraph` then wraps **the bridge**, not the library directly.

### Wiring

- `_BRIDGE_PATH = rx.asset("./graph_canvas.jsx", shared=True)` copies the bridge
  into the compiled frontend's public dir.
- `library = f"$/public{_BRIDGE_PATH}"`, `tag = "GravityGraph"`,
  `is_default = False` → Reflex imports the named export from the bridge.
- `lib_dependencies = ["@gravity-ui/graph@1.11.0"]` ensures the real npm package
  is installed and pinned. The bridge imports `@gravity-ui/graph/react`
  (the React subpath export) and `@gravity-ui/graph` (for `GraphState`).
- `NoSSRComponent` base → the import is dynamic and SSR-disabled.

## Data flow

- **Props down:** Python builds plain dicts (optionally via `Block`/`Connection`
  value objects). Reflex serializes them and renames snake_case props to
  camelCase. The bridge diffs `JSON.stringify(blocks/connections/settings)` so
  structurally-equal updates don't thrash the canvas.
- **Events up:** the bridge maps each upstream event payload (which may contain
  internal component instances) to a small `{...}` of ids/coords/scale before
  calling the Reflex callback, keeping the boundary serializable.

## Modules

| Module | Responsibility |
| --- | --- |
| `graph.py` | The Reflex `GravityGraph` component + `graph_canvas` factory. |
| `graph_canvas.jsx` | The React bridge (hooks, effects, events, lifecycle). |
| `domain.py` | DDD value objects + validation (framework-agnostic). |
| `recipes.py` | Example builders + settings/theme presets. |
| `__init__.py` | Public API surface. |

## Architecture Decision Records

- **ADR-1 — Local JSX bridge over direct wrap.** A hook-based imperative API
  can't be driven from a plain Reflex component; the bridge is the only robust
  option. *Consequence:* one extra JS file shipped in the wheel.
- **ADR-2 — `NoSSRComponent`.** Canvas/`window` access forbids SSR.
- **ADR-3 — Pin npm to `@gravity-ui/graph@1.11.0`.** Reproducible builds; bump
  deliberately.
- **ADR-4 — Pass settings/colors/constants as opaque dicts.** They are already
  JSON-serializable; we don't model every key in Python, so upstream additions
  work without a wrapper change. Typed ergonomics live in `recipes.py`.
- **ADR-5 — Reduce event payloads in the bridge.** Upstream payloads embed
  component instances; we extract ids/coords so handlers receive plain dicts.
- **ADR-6 — Defer plugin layers (ELK/MiniMap/DevTools/CSS-vars).** They need
  extra npm deps and per-layer bridges; tracked as roadmap.
- **ADR-7 — Default to canvas-only blocks.** `render_html_blocks` is opt-in;
  the default path needs no `blockComponents` registration and always works.
