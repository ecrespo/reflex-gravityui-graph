"""Theming: switch the graph color scheme at runtime.

Mirrors the "Theme" / "updateGraphColors" stories by passing a `colors` dict
(RecursivePartial<TGraphColors>) to the component.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import THEMES, default_settings, graph_canvas, two_connected_blocks

from ..layout import page
from ..state import GraphState

_FRAME = {
    "width": "100%",
    "height": "520px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

_DATA = two_connected_blocks(bezier=True)
_BLOCKS = _DATA.blocks_payload()
_CONNS = _DATA.connections_payload()


def theming_page() -> rx.Component:
    return page(
        "Theming",
        "Pass a `colors` dict to recolor the canvas, blocks, anchors and "
        "connections. Switch between the bundled light and dark themes.",
        rx.card(
            rx.hstack(
                rx.text("Theme", size="2"),
                rx.select(
                    list(THEMES.keys()),
                    value=GraphState.theme_name,
                    on_change=GraphState.set_theme,
                ),
                align="center",
                spacing="3",
            ),
        ),
        rx.box(
            rx.match(
                GraphState.theme_name,
                *[
                    (
                        name,
                        graph_canvas(
                            blocks=_BLOCKS,
                            connections=_CONNS,
                            settings=default_settings(),
                            colors=colors,
                            zoom_padding=220,
                            width="100%",
                            height="520px",
                        ),
                    )
                    for name, colors in THEMES.items()
                ],
                graph_canvas(
                    blocks=_BLOCKS,
                    connections=_CONNS,
                    settings=default_settings(),
                    colors=THEMES["light"],
                    width="100%",
                    height="520px",
                ),
            ),
            style=_FRAME,
        ),
    )
