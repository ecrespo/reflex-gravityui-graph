"""Grouping: blocks assigned to groups (Storybook "Canvas/Groups" stories)."""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import default_settings, graph_canvas, grouped_graph

from ..layout import page

_FRAME = {
    "width": "100%",
    "height": "560px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_DATA = grouped_graph(groups=3, per_group=5)


def grouping_page() -> rx.Component:
    return page(
        "Grouping",
        "Each block carries a `group` id; the graph lays out and visually "
        "clusters blocks by group. This mirrors the Canvas/Groups stories.",
        rx.box(
            graph_canvas(
                blocks=_DATA.blocks_payload(),
                connections=_DATA.connections_payload(),
                settings=default_settings(),
                zoom_padding=120,
                width="100%",
                height="560px",
            ),
            style=_FRAME,
        ),
    )
