"""Connections: live toggles for bezier/straight, direction, arrows, labels.

Reproduces the Storybook "Main/GraphEditor" connection controls and the
"VerticalGraph" story, driven by interactive switches.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import colored_connections, graph_canvas

from ..layout import page
from ..state import GraphState

_FRAME = {
    "width": "100%",
    "height": "520px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_DATA = colored_connections()


def _switch(label: str, checked, handler) -> rx.Component:
    return rx.hstack(
        rx.switch(checked=checked, on_change=handler),
        rx.text(label, size="2"),
        align="center",
        spacing="2",
    )


def connections_page() -> rx.Component:
    return page(
        "Connections",
        "Toggle how edges render. These map to @gravity-ui/graph "
        "`settings`: useBezierConnections, bezierConnectionDirection, "
        "showConnectionArrows and showConnectionLabels.",
        rx.card(
            rx.hstack(
                _switch("Bezier", GraphState.use_bezier, GraphState.toggle_bezier),
                _switch("Arrows", GraphState.show_arrows, GraphState.toggle_arrows),
                _switch("Labels", GraphState.show_labels, GraphState.toggle_labels),
                rx.hstack(
                    rx.text("Direction", size="2"),
                    rx.select(
                        ["horizontal", "vertical"],
                        value=GraphState.bezier_direction,
                        on_change=GraphState.set_direction,
                    ),
                    align="center",
                    spacing="2",
                ),
                spacing="5",
                wrap="wrap",
                align="center",
            ),
        ),
        rx.box(
            graph_canvas(
                blocks=_DATA.blocks_payload(),
                connections=_DATA.connections_payload(),
                settings=GraphState.settings,
                zoom_padding=200,
                width="100%",
                height="520px",
            ),
            style=_FRAME,
        ),
    )
