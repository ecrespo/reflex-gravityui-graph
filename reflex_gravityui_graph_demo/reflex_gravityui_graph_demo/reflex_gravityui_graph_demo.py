"""Demo Reflex app for reflex-gravityui-graph.

Each page reproduces a category of @gravity-ui/graph Storybook examples:

* Basics      - one block, anchored connection, multiple anchors, colored edges
* Connections - live bezier/straight, direction, arrows, labels toggles
* Scale       - hundred / thousand / five-thousand block performance graphs
* Grouping    - blocks clustered by `group` id
* Camera      - pan/zoom toggles and fit-on-attach
* Theming     - light / dark color schemes via the `colors` prop
* Interaction - HTML blocks, selection, connection creation, event log

Run from the repo root::

    uv pip install -e .
    cd reflex_gravityui_graph_demo
    reflex run
"""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import (
    default_settings,
    graph_canvas,
    two_connected_blocks,
)

from .layout import page
from .pages.basics import basics_page
from .pages.camera import camera_page
from .pages.connections import connections_page
from .pages.grouping import grouping_page
from .pages.interaction import interaction_page
from .pages.scale import scale_page
from .pages.theming import theming_page

_HERO = two_connected_blocks(bezier=True)


def _feature(icon: str, title: str, body: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.icon(icon, size=20),
            rx.heading(title, size="3"),
            rx.text(body, size="2", color_scheme="gray"),
            spacing="2",
            align="start",
        ),
        width="100%",
    )


def index() -> rx.Component:
    return page(
        "reflex-gravityui-graph",
        "A Reflex custom component wrapping @gravity-ui/graph — a "
        "high-performance Canvas + React graph / flowchart / node-editor library.",
        rx.box(
            graph_canvas(
                blocks=_HERO.blocks_payload(),
                connections=_HERO.connections_payload(),
                settings=default_settings(),
                zoom_padding=220,
                width="100%",
                height="380px",
            ),
            style={
                "width": "100%",
                "height": "380px",
                "border": f"1px solid {rx.color('gray', 5)}",
                "border_radius": "12px",
                "overflow": "hidden",
            },
        ),
        rx.grid(
            _feature("circle-dot", "Declarative data",
                     "Pass blocks & connections as plain Python dicts or build "
                     "them with the typed Block / Connection value objects."),
            _feature("gauge", "Canvas performance",
                     "Renders thousands of nodes on Canvas when zoomed out, "
                     "HTML/React when zoomed in."),
            _feature("settings-2", "Fully configurable",
                     "settings, colors and constants are passed straight "
                     "through — bezier edges, arrows, labels, themes and more."),
            _feature("mouse-pointer-click", "Events",
                     "Selection, connection-created and camera changes flow "
                     "back to your Reflex state as plain dicts."),
            columns="2",
            spacing="3",
            width="100%",
        ),
        rx.callout(
            "Use the sidebar to explore each example category.",
            icon="info",
        ),
    )


app = rx.App()
app.add_page(index, route="/", title="reflex-gravityui-graph")
app.add_page(basics_page, route="/basics", title="Basics · gravity-ui graph")
app.add_page(connections_page, route="/connections", title="Connections · gravity-ui graph")
app.add_page(scale_page, route="/scale", title="Scale · gravity-ui graph")
app.add_page(grouping_page, route="/grouping", title="Grouping · gravity-ui graph")
app.add_page(camera_page, route="/camera", title="Camera · gravity-ui graph")
app.add_page(theming_page, route="/theming", title="Theming · gravity-ui graph")
app.add_page(interaction_page, route="/interaction", title="Interaction · gravity-ui graph")
