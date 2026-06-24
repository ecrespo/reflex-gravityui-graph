// Local React bridge for @gravity-ui/graph.
//
// @gravity-ui/graph is hook + imperative driven: you create a `Graph` instance
// with the `useGraph` hook, push entities through `setEntities`, and start the
// render loop once the canvas is ATTACHED. Reflex components cannot call React
// hooks directly, so this thin bridge encapsulates the whole lifecycle and
// exposes a flat, declarative prop surface that the Python wrapper drives.
//
// Everything below is plain, JSON-serializable data (blocks, connections,
// settings, colors, constants) plus a handful of event callbacks, which is
// exactly what Reflex can pass across the Python <-> JS boundary.
//
// Requires the npm dependency `@gravity-ui/graph` (declared as a
// `lib_dependency` on the Python side so Reflex installs it).
import React, { useEffect, useMemo } from "react";
import { GraphState } from "@gravity-ui/graph";
import {
  GraphCanvas,
  GraphBlock,
  useGraph,
  useGraphEvents,
} from "@gravity-ui/graph/react";

// Pull the `.id` off a list of canvas component instances (defensively, since
// the exact shape of an event payload's component objects is internal).
function idsOf(list) {
  if (!Array.isArray(list)) return [];
  return list
    .map((item) => {
      if (item == null) return null;
      if (typeof item === "object") {
        if ("id" in item) return item.id;
        if (item.state && "id" in item.state) return item.state.id;
      }
      return item;
    })
    .filter((id) => id !== null && id !== undefined);
}

export function GravityGraph(props) {
  const {
    blocks = [],
    connections = [],
    settings = {},
    colors = null,
    constants = null,
    configName = "reflex-gravityui-graph",
    autoStart = true,
    zoomOnStart = true,
    zoomTarget = "center",
    zoomPadding = 100,
    renderHtmlBlocks = false,
    onBlockSelectionChange = null,
    onConnectionCreated = null,
    onConnectionSelectionChange = null,
    onCameraChange = null,
    onBlockDragEnd = null,
    onStateChange = null,
    style = null,
    className = null,
  } = props;

  // Assemble the optional view configuration (colors + constants) only when at
  // least one of them is supplied, so we never clobber library defaults.
  const viewConfiguration = useMemo(() => {
    const view = {};
    if (colors) view.colors = colors;
    if (constants) view.constants = constants;
    return view;
  }, [JSON.stringify(colors), JSON.stringify(constants)]);

  const { graph, setEntities, start } = useGraph({
    name: configName,
    settings,
    viewConfiguration,
  });

  // Push the entity set whenever blocks/connections change. We stringify for
  // the dependency array so structurally-equal updates don't thrash the canvas.
  const blocksKey = JSON.stringify(blocks);
  const connectionsKey = JSON.stringify(connections);
  useEffect(() => {
    if (!graph) return;
    setEntities({ blocks, connections });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graph, setEntities, blocksKey, connectionsKey]);

  // Live-apply settings changes after the first mount.
  const settingsKey = JSON.stringify(settings);
  useEffect(() => {
    if (graph && graph.updateSettings) graph.updateSettings(settings);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graph, settingsKey]);

  // Live-apply color / constant changes.
  useEffect(() => {
    if (!graph) return;
    if (colors && graph.setColors) graph.setColors(colors);
    if (constants && graph.setConstants) graph.setConstants(constants);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graph, JSON.stringify(colors), JSON.stringify(constants)]);

  // Subscribe to the graph events the Python wrapper cares about. Each payload
  // is reduced to plain, serializable data before crossing back to Reflex.
  useGraphEvents(graph, {
    "blocks-selection-change": (detail) => {
      if (!onBlockSelectionChange) return;
      const changes = (detail && detail.changes) || {};
      onBlockSelectionChange({
        added: idsOf(changes.add),
        removed: idsOf(changes.removed),
      });
    },
    "connection-created": (detail) => {
      if (!onConnectionCreated) return;
      onConnectionCreated({
        sourceBlockId: detail?.sourceBlockId ?? null,
        targetBlockId: detail?.targetBlockId ?? null,
        sourceAnchorId: detail?.sourceAnchorId ?? null,
        targetAnchorId: detail?.targetAnchorId ?? null,
      });
    },
    "connection-selection-change": (detail) => {
      if (!onConnectionSelectionChange) return;
      const changes = (detail && detail.changes) || {};
      onConnectionSelectionChange({
        added: idsOf(changes.add),
        removed: idsOf(changes.removed),
      });
    },
    "camera-change": (detail) => {
      if (!onCameraChange) return;
      onCameraChange({
        x: detail?.x ?? null,
        y: detail?.y ?? null,
        scale: detail?.scale ?? null,
      });
    },
    "block-drag-end": (detail) => {
      if (!onBlockDragEnd) return;
      onBlockDragEnd({
        blockId: detail?.blockId ?? detail?.block?.id ?? null,
        x: detail?.x ?? null,
        y: detail?.y ?? null,
      });
    },
  });

  // When requested, render rich HTML/React blocks at detailed zoom levels. The
  // default (canvas-only) path is the most robust and needs no registration.
  const renderBlock = renderHtmlBlocks
    ? (g, block) => (
        <GraphBlock graph={g} block={block}>
          {block.name ?? block.id}
        </GraphBlock>
      )
    : undefined;

  const wrapperStyle = style || { width: "100%", height: "600px" };

  return (
    <GraphCanvas
      className={className}
      style={wrapperStyle}
      graph={graph}
      renderBlock={renderBlock}
      onStateChanged={({ state }) => {
        if (onStateChange) onStateChange({ state });
        if (state === GraphState.ATTACHED) {
          if (autoStart) start();
          if (zoomOnStart && graph) {
            graph.zoomTo(zoomTarget, { padding: zoomPadding });
          }
        }
      }}
    />
  );
}
