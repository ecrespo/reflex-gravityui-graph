"""A Reflex wrapper around @gravity-ui/graph.

`@gravity-ui/graph` (https://github.com/gravity-ui/graph) is a high-performance
graph / flowchart / node-editor visualization library. It renders the whole
graph on Canvas when zoomed out (fast for thousands of nodes) and swaps to
HTML/React for rich interactions when zoomed in.

The upstream React API is hook + imperative driven (``useGraph`` creates a
``Graph`` instance, ``setEntities`` pushes nodes/edges, ``start`` runs the render
loop once attached). Reflex components cannot call React hooks directly, so this
package ships a small local JSX bridge (``graph_canvas.jsx``) that encapsulates
that lifecycle and exposes a flat, declarative prop surface. This module is the
Python side of that bridge.

Public API::

    from reflex_gravityui_graph import graph_canvas

    graph_canvas(
        blocks=[{"id": "a", "is": "block-action", "x": 0, "y": 0,
                 "width": 120, "height": 120, "name": "A"}],
        connections=[],
    )
"""

from __future__ import annotations

from typing import Any

import reflex as rx
from reflex.components.component import NoSSRComponent

# Pinned npm version for reproducible builds. Bump deliberately.
GRAVITY_GRAPH_VERSION = "@gravity-ui/graph@1.11.0"

# Copy the local JSX bridge into the compiled frontend's public dir, then import
# the bridge from there (same mechanism used for other JSX-bridge components).
_BRIDGE_PATH = rx.asset("./graph_canvas.jsx", shared=True)


def _payload_event_spec(payload: rx.Var[dict]) -> tuple[rx.Var[dict]]:
    """Forward a single serializable payload dict to the event handler."""
    return (payload,)


class GravityGraph(NoSSRComponent):
    """A @gravity-ui/graph canvas, driven declaratively from Reflex.

    The component is client-only: the engine touches ``window``/Canvas, so it is
    a ``NoSSRComponent`` (Reflex emits a dynamic, SSR-disabled import). See
    ``docs/sdd/02-architecture.md``.

    Sizing: ``GraphCanvas`` fills its container, so give the component an
    explicit height (e.g. ``height="600px"``) or pass ``style``.
    """

    # Import the local JSX bridge from the frontend public dir.
    library = f"$/public{_BRIDGE_PATH}"

    # Named export from the bridge.
    tag = "GravityGraph"
    is_default = False

    # Ensure the real npm package lands in package.json with a pinned version.
    lib_dependencies: list[str] = [GRAVITY_GRAPH_VERSION]

    # ------------------------------------------------------------------ #
    # Data props (plain, JSON-serializable)
    # ------------------------------------------------------------------ #

    # Blocks (nodes). Each dict uses upstream camelCase keys:
    # ``id``, ``is``, ``x``, ``y``, ``width``, ``height``, ``name`` and the
    # optional ``anchors``, ``selected``, ``group``, ``meta``.
    blocks: rx.Var[list[dict[str, Any]]]

    # Connections (edges). Each dict: ``sourceBlockId`` / ``targetBlockId`` and
    # optional ``sourceAnchorId`` / ``targetAnchorId`` / ``id`` / ``label`` /
    # ``styles`` / ``dashed`` / ``selected``.
    connections: rx.Var[list[dict[str, Any]]]

    # Graph settings (``TGraphSettingsConfig``): ``canDragCamera``,
    # ``canZoomCamera``, ``canCreateNewConnections``, ``useBezierConnections``,
    # ``bezierConnectionDirection``, ``showConnectionArrows``,
    # ``showConnectionLabels``, ``useBlocksAnchors``, ``scaleFontSize``, ...
    settings: rx.Var[dict[str, Any]]

    # View colors (``RecursivePartial<TGraphColors>``): ``canvas``, ``block``,
    # ``anchor``, ``connection``, ``selection``, ...
    colors: rx.Var[dict[str, Any]]

    # View constants (``RecursivePartial<TGraphConstants>``): ``system``,
    # ``camera``, ``block``, ``connection``, ``text``.
    constants: rx.Var[dict[str, Any]]

    # Configuration name passed to the underlying graph instance.
    config_name: rx.Var[str]  # -> configName

    # ------------------------------------------------------------------ #
    # Lifecycle / camera props
    # ------------------------------------------------------------------ #

    # Start the render loop automatically once the canvas is attached.
    auto_start: rx.Var[bool]  # -> autoStart

    # Fit the camera to the graph once attached.
    zoom_on_start: rx.Var[bool]  # -> zoomOnStart

    # Zoom target: ``"center"``, a rect, or a list of block ids.
    zoom_target: rx.Var[Any]  # -> zoomTarget

    # Padding (px) used when fitting the camera on start.
    zoom_padding: rx.Var[int]  # -> zoomPadding

    # Render rich HTML/React block bodies at detailed zoom (default canvas-only).
    render_html_blocks: rx.Var[bool]  # -> renderHtmlBlocks

    # ------------------------------------------------------------------ #
    # Events (each forwards one serializable payload dict)
    # ------------------------------------------------------------------ #

    # ``{"added": [ids], "removed": [ids]}`` when the block selection changes.
    on_block_selection_change: rx.EventHandler[_payload_event_spec]

    # ``{"sourceBlockId", "targetBlockId", "sourceAnchorId", "targetAnchorId"}``
    # when a new connection is drawn (requires ``canCreateNewConnections``).
    on_connection_created: rx.EventHandler[_payload_event_spec]

    # ``{"added": [ids], "removed": [ids]}`` when the connection selection changes.
    on_connection_selection_change: rx.EventHandler[_payload_event_spec]

    # ``{"x", "y", "scale"}`` whenever the camera pans/zooms.
    on_camera_change: rx.EventHandler[_payload_event_spec]

    # ``{"blockId", "x", "y"}`` when a block drag finishes.
    on_block_drag_end: rx.EventHandler[_payload_event_spec]

    # ``{"state"}`` on graph state transitions (e.g. ``"ATTACHED"``).
    on_state_change: rx.EventHandler[_payload_event_spec]

    # Reflex auto-converts snake_case prop names to camelCase, covering every
    # prop above. Add entries only for names the heuristic would get wrong.
    _rename_props: dict[str, str] = {}


# Convenience factory: ``graph_canvas(blocks=[...], connections=[...])``.
graph_canvas = GravityGraph.create
