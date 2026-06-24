"""Interaction & events: HTML blocks, selection, connection creation.

Demonstrates the event surface (on_block_selection_change, on_connection_created,
on_camera_change) and the optional rich HTML block rendering at detailed zoom.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import default_settings, graph_canvas, two_connected_blocks

from ..layout import page
from ..state import GraphState

_FRAME = {
    "width": "100%",
    "height": "480px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_DATA = two_connected_blocks(bezier=True)
_BLOCKS = _DATA.blocks_payload()
_CONNS = _DATA.connections_payload()


def interaction_page() -> rx.Component:
    return page(
        "Interaction & events",
        "Create new connections by dragging from an OUT anchor to an IN "
        "anchor, select blocks, and watch the event log. Events cross back "
        "to Reflex as plain dicts.",
        rx.hstack(
            rx.box(
                graph_canvas(
                    blocks=_BLOCKS,
                    connections=_CONNS,
                    settings=default_settings(can_create_new_connections=True),
                    render_html_blocks=True,
                    zoom_padding=220,
                    on_block_selection_change=GraphState.log_event,
                    on_connection_created=GraphState.log_event,
                    on_camera_change=GraphState.log_event,
                    width="100%",
                    height="480px",
                ),
                style=_FRAME,
                flex="1",
            ),
            rx.vstack(
                rx.hstack(
                    rx.heading("Event log", size="4"),
                    rx.spacer(),
                    rx.button("Clear", size="1", variant="soft",
                              on_click=GraphState.clear_events),
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.cond(
                    GraphState.events,
                    rx.vstack(
                        rx.foreach(
                            GraphState.events,
                            lambda e: rx.code(e, size="1", width="100%"),
                        ),
                        spacing="1",
                        width="100%",
                        overflow_y="auto",
                        max_height="400px",
                    ),
                    rx.text("Interact with the graph to see events…",
                            color_scheme="gray", size="2"),
                ),
                width="340px",
                align="start",
            ),
            spacing="4",
            width="100%",
            align="start",
        ),
    )
