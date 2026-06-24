"""Camera & zoom: drag / zoom toggles and fit-on-start behavior.

Mirrors the camera-related Storybook controls (canDragCamera, canZoomCamera)
and the zoomTo / zoom-on-attach API usage.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import generate_layered_blocks, graph_canvas

from ..layout import page
from ..state import GraphState

_FRAME = {
    "width": "100%",
    "height": "560px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_DATA = generate_layered_blocks(layers_count=6, connections_per_layer=6)
_BLOCKS = _DATA.blocks_payload()
_CONNS = _DATA.connections_payload()


def _switch(label: str, checked, handler) -> rx.Component:
    return rx.hstack(
        rx.switch(checked=checked, on_change=handler),
        rx.text(label, size="2"),
        align="center",
        spacing="2",
    )


def camera_page() -> rx.Component:
    return page(
        "Camera & zoom",
        "The graph fits to view on attach (graph.zoomTo('center')). Toggle "
        "whether the user can pan (canDragCamera), zoom (canZoomCamera), move "
        "nodes by dragging them (canDrag), or draw links by dragging from an OUT "
        "anchor to an IN anchor (canCreateNewConnections). Drag a node to move "
        "it; with 'Create links' on, drag between anchors to add a connection.",
        rx.card(
            rx.hstack(
                _switch("Drag camera", GraphState.can_drag_camera, GraphState.toggle_drag),
                _switch("Zoom camera", GraphState.can_zoom_camera, GraphState.toggle_zoom),
                _switch("Drag nodes", GraphState.can_drag_blocks, GraphState.toggle_drag_blocks),
                _switch("Create links", GraphState.can_create_connections, GraphState.toggle_create),
                spacing="5",
                align="center",
            ),
        ),
        rx.box(
            graph_canvas(
                blocks=_BLOCKS,
                connections=_CONNS,
                settings=GraphState.settings,
                zoom_on_start=True,
                zoom_target="center",
                zoom_padding=160,
                width="100%",
                height="560px",
            ),
            style=_FRAME,
        ),
    )
