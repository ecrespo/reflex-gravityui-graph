"""Scale: hundred / thousand / five-thousand block layered graphs.

Reproduces the Storybook "HundredBlocks", "ThousandBlocks" and
"FiveThousandsBlocks" performance stories via `generate_layered_blocks`.
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import default_settings, generate_layered_blocks, graph_canvas

from ..layout import page
from ..state import GraphState

_FRAME = {
    "width": "100%",
    "height": "560px",
    "border": f"1px solid {rx.color('gray', 5)}",
    "border_radius": "12px",
    "overflow": "hidden",
}

# Pre-generate each preset once at import time (reproducible via a fixed seed).
_PRESETS: dict[str, object] = {
    "Hundred (10×10)": generate_layered_blocks(layers_count=10, connections_per_layer=10),
    "Thousand (25×40)": generate_layered_blocks(layers_count=25, connections_per_layer=40),
    "Five thousand (40×125)": generate_layered_blocks(
        layers_count=40, connections_per_layer=125, dashed=False
    ),
}

_BLOCKS = {name: data.blocks_payload() for name, data in _PRESETS.items()}
_CONNS = {name: data.connections_payload() for name, data in _PRESETS.items()}

# Bezier is heavy at 5k nodes; straight edges keep large graphs smooth.
_BIG_SETTINGS = default_settings(use_bezier_connections=False, show_connection_arrows=False)


def scale_page() -> rx.Component:
    return page(
        "Scale & performance",
        "@gravity-ui/graph renders the full graph on Canvas when zoomed out, "
        "so it stays smooth with thousands of nodes. Pick a preset to load it.",
        rx.card(
            rx.hstack(
                rx.text("Preset", size="2"),
                rx.select(
                    list(_PRESETS.keys()),
                    value=GraphState.scale_preset,
                    on_change=GraphState.set_scale_preset,
                ),
                rx.badge(
                    rx.match(
                        GraphState.scale_preset,
                        ("Hundred (10×10)", "~100 blocks"),
                        ("Thousand (25×40)", "~1,000 blocks"),
                        ("Five thousand (40×125)", "~5,000 blocks"),
                        "",
                    ),
                    color_scheme="amber",
                ),
                align="center",
                spacing="3",
            ),
        ),
        rx.box(
            rx.match(
                GraphState.scale_preset,
                *[
                    (
                        name,
                        graph_canvas(
                            blocks=_BLOCKS[name],
                            connections=_CONNS[name],
                            settings=_BIG_SETTINGS,
                            zoom_padding=80,
                            width="100%",
                            height="560px",
                        ),
                    )
                    for name in _PRESETS
                ],
                graph_canvas(
                    blocks=_BLOCKS["Hundred (10×10)"],
                    connections=_CONNS["Hundred (10×10)"],
                    settings=_BIG_SETTINGS,
                    width="100%",
                    height="560px",
                ),
            ),
            style=_FRAME,
        ),
    )
