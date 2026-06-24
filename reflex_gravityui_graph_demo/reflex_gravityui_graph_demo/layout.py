"""Shared page shell: a sidebar of example links + content area."""

from __future__ import annotations

import reflex as rx

NAV: list[tuple[str, str, str]] = [
    ("Overview", "/", "home"),
    ("Basics", "/basics", "circle-dot"),
    ("Connections", "/connections", "spline"),
    ("Scale", "/scale", "layers"),
    ("Grouping", "/grouping", "group"),
    ("Camera & Zoom", "/camera", "move"),
    ("Theming", "/theming", "palette"),
    ("Interaction & Events", "/interaction", "mouse-pointer-click"),
]


def _nav_link(label: str, href: str, icon: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(label, size="2"),
            align="center",
            spacing="2",
            padding="0.4rem 0.6rem",
            border_radius="8px",
            _hover={"background": rx.color("gray", 4)},
            width="100%",
        ),
        href=href,
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("git-fork", size=20),
            rx.heading("gravity-ui/graph", size="4"),
            align="center",
            spacing="2",
        ),
        rx.text("Reflex custom component", size="1", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            *[_nav_link(label, href, icon) for label, href, icon in NAV],
            spacing="1",
            width="100%",
        ),
        rx.spacer(),
        rx.link(
            rx.hstack(rx.icon("github", size=14), rx.text("Source", size="1")),
            href="https://github.com/ecrespo/reflex-gravityui-graph",
            is_external=True,
        ),
        spacing="3",
        padding="1rem",
        width="260px",
        height="100vh",
        position="sticky",
        top="0",
        border_right=f"1px solid {rx.color('gray', 5)}",
    )


def page(title: str, description: str, *content: rx.Component) -> rx.Component:
    """Wrap page content with the sidebar and a title block."""
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.heading(title, size="7"),
            rx.text(description, color_scheme="gray", size="3"),
            rx.divider(),
            *content,
            spacing="4",
            padding="2rem",
            width="100%",
            max_width="1100px",
        ),
        align="start",
        spacing="0",
        width="100%",
    )
