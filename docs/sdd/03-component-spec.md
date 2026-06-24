# 03 · Component Specification

The exact contract for `GravityGraph` / `graph_canvas`.

## Props

| Python prop | JS prop | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `blocks` | `blocks` | `list[dict]` | `[]` | Node list (see Block shape). |
| `connections` | `connections` | `list[dict]` | `[]` | Edge list (see Connection shape). |
| `settings` | `settings` | `dict` | `{}` | `TGraphSettingsConfig`. |
| `colors` | `colors` | `dict` | – | `RecursivePartial<TGraphColors>`. |
| `constants` | `constants` | `dict` | – | `RecursivePartial<TGraphConstants>`. |
| `config_name` | `configName` | `str` | `"reflex-gravityui-graph"` | Graph configuration name. |
| `auto_start` | `autoStart` | `bool` | `True` | `start()` on attach. |
| `zoom_on_start` | `zoomOnStart` | `bool` | `True` | `zoomTo` on attach. |
| `zoom_target` | `zoomTarget` | `str \| list` | `"center"` | `"center"`, rect, or block-id list. |
| `zoom_padding` | `zoomPadding` | `int` | `100` | Fit padding (px). |
| `render_html_blocks` | `renderHtmlBlocks` | `bool` | `False` | Rich HTML blocks at detailed zoom. |

Reflex auto-renames snake_case → camelCase; no `_rename_props` entries are
required. The component subclasses `NoSSRComponent`.

## Events

Each event handler receives a single plain dict.

| Python event | Payload |
| --- | --- |
| `on_block_selection_change` | `{"added": [id…], "removed": [id…]}` |
| `on_connection_created` | `{"sourceBlockId", "targetBlockId", "sourceAnchorId", "targetAnchorId"}` |
| `on_connection_selection_change` | `{"added": [id…], "removed": [id…]}` |
| `on_camera_change` | `{"x", "y", "scale"}` |
| `on_block_drag_end` | `{"blockId", "x", "y"}` |
| `on_state_change` | `{"state"}` (e.g. `"ATTACHED"`) |

## Data shapes

### Block (`TBlock`)

```jsonc
{
  "id": "a",            // required, string|number, unique
  "is": "block-action", // discriminator; unregistered → default canvas block
  "x": 0, "y": 0,        // required position
  "width": 200, "height": 160, // required, > 0
  "name": "A",          // label
  "selected": false,     // optional
  "group": "group_0",   // optional group id
  "anchors": [ /* Anchor */ ],
  "meta": { /* arbitrary */ }
}
```

### Anchor (`TAnchor`)

```jsonc
{ "id": "out1", "blockId": "a", "type": "OUT", "index": 0 }  // type: "IN" | "OUT"
```

### Connection (`TConnection`)

```jsonc
{
  "sourceBlockId": "a", "targetBlockId": "b",     // required
  "sourceAnchorId": "out1", "targetAnchorId": "in1", // optional
  "id": 1, "label": "edge",                       // optional
  "dashed": true, "selected": false,               // optional
  "styles": { "background": "#f00", "selectedBackground": "#f00", "dashes": [6,4] }
}
```

## Python builders (`domain.py`)

- `Anchor(id, block_id, type=EAnchorType.OUT, index=0).to_dict()`
- `Block(id, x, y, name, is_, width, height, selected, group, anchors, meta).to_dict()`
- `Connection(source_block_id, target_block_id, source_anchor_id, target_anchor_id, id, label, dashed, selected, styles).to_dict()`
- `GraphData(blocks, connections)` → `.blocks_payload()`, `.connections_payload()`
  with duplicate-id and dangling-edge validation.

## Settings keys commonly used (`TGraphSettingsConfig`)

`canDragCamera`, `canZoomCamera`, `canDrag` (`ECanDrag`:
`"all"`/`"onlySelected"`/`"none"` — move nodes with the mouse; upstream default
is `"none"`), `canCreateNewConnections`, `useBezierConnections`,
`bezierConnectionDirection` (`"horizontal"`/`"vertical"`), `showConnectionArrows`,
`showConnectionLabels`, `useBlocksAnchors`, `scaleFontSize`. Build them with
`recipes.default_settings(...)`, whose `can_drag_blocks` arg defaults to `True`
(`canDrag="all"`) so nodes are draggable out of the box.

## Invariants

- Block `width`/`height` must be positive; ids unique within a graph.
- Every connection endpoint must reference an existing block (validated by
  `GraphData`).
- The component must be given an explicit height (canvas fills its container).
