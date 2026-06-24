"""Basics: hello-world block, two connected blocks, anchors, colored edges.

Reproduces the Storybook "Main/GraphEditor" stories: OneBlock,
OneStraightConnection / OneBezierConnection, WithAnchors, ColoredConnections.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import (
    block_with_anchors,
    colored_connections,
    default_settings,
    graph_canvas,
    one_block,
    two_connected_blocks,
)

from ..layout import page

_FRAME = {
    "width": "100%",
    "height": "420px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_ONE = one_block()
_TWO = two_connected_blocks(bezier=True)
_ANCHORS = block_with_anchors(n_in=3, n_out=2)
_COLORED = colored_connections()


def _demo(title: str, data, **settings_kwargs) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="4"),
        rx.box(
            graph_canvas(
                blocks=data.blocks_payload(),
                connections=data.connections_payload(),
                settings=default_settings(**settings_kwargs),
                zoom_padding=200,
                width="100%",
                height="420px",
            ),
            style=_FRAME,
        ),
        spacing="2",
        width="100%",
    )


def basics_page() -> rx.Component:
    return page(
        "Basics",
        "The smallest possible graphs — a single block, an anchored "
        "connection, multiple anchors, and per-edge colors.",
        _demo("One block", _ONE),
        _demo("Two blocks · bezier connection", _TWO),
        _demo("Block with multiple anchors", _ANCHORS),
        _demo("Colored & dashed connections", _COLORED, show_connection_labels=True),
    )
