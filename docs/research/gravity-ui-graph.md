# Research · @gravity-ui/graph

Source: <https://github.com/gravity-ui/graph> · Storybook:
<https://preview.gravity-ui.com/graph/>

## Package facts

- npm: `@gravity-ui/graph`, version **1.11.0**, license **MIT**.
- Peer deps: `react` and `react-dom` `^17 || ^18`.
- Runtime deps: `@preact/signals-core`, `intersects`, `lodash`, `rbush`,
  `style-observer`.
- Exports map: `"."` → core (`Graph`, types), `"./react"` → React bindings,
  `"./plugins"` → optional layers.

## Core idea

Renders the whole graph on **Canvas** when zoomed out (fast for thousands of
nodes), then switches to **HTML/React** components for visible blocks when zoomed
in. Three level-of-detail bands (minimalistic / schematic / detailed) via
`constants.block.SCALES = [0.125, 0.225, 0.7]`.

## React API (the part we wrap)

- `useGraph(config: HookGraphParams)` → `{ graph, setEntities, updateEntities,
  start, stop, setSettings, setViewConfiguration, addLayer, zoomTo, api }`.
  - `HookGraphParams = Pick<TGraphConfig,"settings"|"layers"> & { graph?, name?,
    viewConfiguration?: { colors?, constants? } }`.
- `<GraphCanvas graph renderBlock onStateChanged className blockListClassName
  reactLayerRef {...eventCallbacks} />`.
- `useGraphEvent(graph, name, handler)` / `useGraphEvents(graph, {name: handler})`.
- `<GraphBlock graph block>` — HTML block wrapper (syncs to canvas coords; CSS
  vars like `--graph-block-geometry-x/y/width/height`).
- `<GraphBlockAnchor graph anchor position>` — anchor render point.
- `<GraphLayer>`, `<GraphPortal>` — declarative layers/overlays.
- Canonical start pattern: in `onStateChanged`, when `state ===
  GraphState.ATTACHED`, call `start()` then `graph.zoomTo("center", {padding})`.

## Config / settings (`TGraphSettingsConfig`)

`canDragCamera`, `canZoomCamera`, `canDrag` (`ECanDrag`), `dragThreshold`,
`canCreateNewConnections`, `scaleFontSize`, `showConnectionArrows`,
`useBezierConnections`, `bezierConnectionDirection` (`horizontal`/`vertical`),
`useBlocksAnchors`, `showConnectionLabels`, `blockComponents` (custom canvas
classes keyed by `is`), `connection`, `background`, `resolveWheelIntent`,
`getCameraBlockScaleLevel`.

`viewConfiguration.colors` (`TGraphColors`: canvas/block/anchor/connection/
selection groups) and `viewConfiguration.constants` (`TGraphConstants`:
system/camera/block/connection/text) recolor and re-scale the view.

## Entity shapes

- **TBlock**: `id`, `is`, `x`, `y`, `width`, `height`, `name`, optional
  `anchors`, `selected`, `group`, `meta`.
- **TAnchor**: `id`, `blockId`, `type` (`EAnchorType.IN`/`OUT`), `index`.
- **TConnection**: `sourceBlockId`/`targetBlockId` (+ optional `sourceAnchorId`/
  `targetAnchorId` or port ids), `id`, `label`, `styles` (colors + `dashes`),
  `dashed`, `selected`.

`setEntities` replaces the entity set; `updateEntities` merges/updates.

## Events

`camera-change`, `state-change`, `colors-changed`, `constants-changed`,
`block-change`, `block-drag-start/drag/drag-end`, `blocks-selection-change`
(`{changes:{add,removed}}`), `blocks-geometry-change`,
`block-anchor-selection-change`, `connection-created` (cancelable,
`{sourceBlockId,targetBlockId,sourceAnchorId,targetAnchorId}`),
`connection-create-start/hover/drop`, `connection-selection-change`,
`group-collapse-change`, `groups-selection-change`,
`block-add-start-from-shadow`/`block-added-from-shadow`, generic `click`.

## Zoom API

`graph.zoomTo(target, {transition?, padding?})` where target is `"center"`, a
rect, a block-id list, or component list. Also `api.zoomToBlocks/zoomToElements/
zoomToRect/zoomToViewPort`.

## Storybook examples (porting checklist)

- **Main/GraphEditor:** OneBlock, OneStraightConnection, OneBezierConnection,
  ColoredConnections, WithAnchors, HundredBlocks, ThousandBlocks,
  FiveThousandsBlocks, GraphStressTest, NirvanaMaxGraphTest,
  CustomSchematicBlock, CustomLayer, VerticalGraph, SnappingGraph, EmptyGraph.
- **Api/*:** startStop, updateBlock, updateConnection, updateGraphColors,
  Connection Selection (bucket / react-state), zoomSpeed, zoomToBlocks,
  zoomToElements, zoomToRect, zoomToViewPort.
- **Canvas/Groups:** default, extended, large, manual, collapsible, transfer.
- **Examples/*:** ConnectionLayer, PortConnectionLayer, NewBlockLayer,
  CustomConnectionLabel, ImageByBlocks, ImageInsteadBlock,
  MouseWheelBehaviorScroll, Theme, ViewportInsets.
- **Plugins/*:** MiniMap, DevTools, CSS Variables (basic/advanced), ELK
  (Box/Layered/Disco/Radial/MrTree/Force/Stress/Random/SporeOverlap/
  SporeCompaction), Layered.
- **Playground:** kitchen-sink editor (Monaco schema, toolbox, custom blocks).

### Coverage in this component (v0.1)

Covered: basics (one/two/anchors/colored/bezier/straight/vertical/labels/
arrows), scale (hundred/thousand/five-thousand), grouping, theming (colors),
camera (drag/zoom/zoomTo-on-start), interaction (selection, connection-created,
camera events, HTML blocks).

Roadmap (need extra deps / per-layer bridges): plugin layers (MiniMap,
DevTools, CSS-variables, ELK/Layered auto-layout), custom canvas block classes,
the dedicated connection-creation layers, and the Playground.
