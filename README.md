# reflex-gravityui-graph

A [Reflex](https://reflex.dev) custom component that wraps
[`@gravity-ui/graph`](https://github.com/gravity-ui/graph) — a high-performance
graph / flowchart / node-editor visualization library that renders the full
graph on **Canvas** when zoomed out (smooth with thousands of nodes) and swaps
to **HTML/React** for rich interactions when zoomed in.

It exposes the whole graph declaratively from Python: pass `blocks`,
`connections`, `settings`, `colors` and `constants` as plain data, and receive
selection / connection / camera events back into your Reflex state.

> Status: **0.1.0 (beta).** Wraps `@gravity-ui/graph@1.11.0`.

---

## Installation

```bash
uv add reflex-gravityui-graph
# or
pip install reflex-gravityui-graph
```

The first time the demo (or your app) runs, Reflex installs the npm dependency
`@gravity-ui/graph` automatically.

## Quick start

```python
import reflex as rx
from reflex_gravityui_graph import graph_canvas, Block, Connection, Anchor, EAnchorType

a = Block(id="a", x=0, y=0, name="Start",
          anchors=[Anchor(id="out", block_id="a", type=EAnchorType.OUT)])
b = Block(id="b", x=320, y=180, name="End",
          anchors=[Anchor(id="in", block_id="b", type=EAnchorType.IN)])
edge = Connection(source_block_id="a", source_anchor_id="out",
                  target_block_id="b", target_anchor_id="in")


def index() -> rx.Component:
    return graph_canvas(
        blocks=[a.to_dict(), b.to_dict()],
        connections=[edge.to_dict()],
        width="100%",
        height="600px",
    )


app = rx.App()
app.add_page(index)
```

`GraphCanvas` fills its container, so always give the component an explicit
height (`height="600px"`) or a sized parent.

## Why a JSX bridge?

`@gravity-ui/graph`'s React API is **hook + imperative**: you create a `Graph`
with the `useGraph` hook, push entities with `setEntities`, and `start()` the
render loop once the canvas is attached. Reflex components can't call React hooks
directly, so this package ships a tiny local bridge (`graph_canvas.jsx`) that
encapsulates that lifecycle and presents a flat, declarative, JSON-serializable
prop surface. See [`docs/sdd/02-architecture.md`](docs/sdd/02-architecture.md).

## API

### `graph_canvas(...)` / `GravityGraph`

| Prop | Type | Description |
| --- | --- | --- |
| `blocks` | `list[dict]` | Nodes (`id`, `is`, `x`, `y`, `width`, `height`, `name`, optional `anchors`, `selected`, `group`, `meta`). |
| `connections` | `list[dict]` | Edges (`sourceBlockId`/`targetBlockId`, optional anchor ids, `label`, `styles`, `dashed`, `selected`). |
| `settings` | `dict` | `TGraphSettingsConfig` (bezier, arrows, labels, drag/zoom, anchors, …). |
| `colors` | `dict` | `RecursivePartial<TGraphColors>` view colors. |
| `constants` | `dict` | `RecursivePartial<TGraphConstants>` view constants. |
| `config_name` | `str` | Underlying graph configuration name. |
| `auto_start` | `bool` | Start the render loop on attach (default `True`). |
| `zoom_on_start` | `bool` | Fit camera to graph on attach (default `True`). |
| `zoom_target` | `str` \| list | `"center"`, a rect, or a list of block ids. |
| `zoom_padding` | `int` | Padding (px) when fitting on start. |
| `render_html_blocks` | `bool` | Render rich HTML/React blocks at detailed zoom. |

**Events** (each delivers one plain dict to your handler):

`on_block_selection_change`, `on_connection_created`,
`on_connection_selection_change`, `on_camera_change`, `on_block_drag_end`,
`on_state_change`.

### Domain value objects

`Block`, `Connection`, `Anchor`, `EAnchorType`, `GraphData` build and validate
the entity payloads in Python (duplicate-id and dangling-edge checks included).

### Recipe helpers (reproduce the upstream Storybook stories)

`one_block`, `two_connected_blocks`, `colored_connections`, `block_with_anchors`,
`generate_layered_blocks` (hundred / thousand / five-thousand block graphs),
`grouped_graph`, `default_settings`, and the `THEMES` color presets.

## Demo app

A full demo with one page per example category lives in
`reflex_gravityui_graph_demo/`:

```bash
uv pip install -e .
cd reflex_gravityui_graph_demo
reflex run
```

Pages: Basics · Connections · Scale · Grouping · Camera & Zoom · Theming ·
Interaction & Events.

## Development

This project uses [`uv`](https://docs.astral.sh/uv/).

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uv run pytest -q                  # run the test suite
uv run reflex component build     # build wheel/sdist + generate the .pyi stub
uv publish                        # publish to PyPI (needs an API token)
```

See [`docs/sdd/`](docs/sdd/) for the full Spec-Driven Design artifacts
(overview, PRD, architecture, component spec, plan, tasks) and
[`docs/research/`](docs/research/) for the upstream research notes.

## Credits

- [`@gravity-ui/graph`](https://github.com/gravity-ui/graph) by Gravity UI (MIT).
- Built as a [Reflex custom component](https://reflex.dev/docs/custom-components/overview/).

## License

Apache-2.0 © Ernesto Crespo. `@gravity-ui/graph` is MIT © YANDEX LLC.
