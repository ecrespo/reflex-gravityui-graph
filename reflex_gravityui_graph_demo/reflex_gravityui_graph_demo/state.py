"""Shared state for the demo: live-editable settings + event log."""

from __future__ import annotations

import reflex as rx

from reflex_gravityui_graph import default_settings


class GraphState(rx.State):
    """Drives the interactive controls shared across demo pages."""

    # --- connections page toggles ---
    use_bezier: bool = True
    bezier_direction: str = "horizontal"
    show_arrows: bool = True
    show_labels: bool = False
    can_create_connections: bool = False

    # --- camera page toggles ---
    can_drag_camera: bool = True
    can_zoom_camera: bool = True

    # --- scale page selector ---
    scale_preset: str = "Hundred (10×10)"

    # --- theming page ---
    theme_name: str = "light"

    # --- event log (interaction page) ---
    events: list[str] = []

    @rx.var
    def settings(self) -> dict:
        """Compose the live settings dict from the toggles."""
        return default_settings(
            can_drag_camera=self.can_drag_camera,
            can_zoom_camera=self.can_zoom_camera,
            can_create_new_connections=self.can_create_connections,
            use_bezier_connections=self.use_bezier,
            bezier_direction=self.bezier_direction,
            show_connection_arrows=self.show_arrows,
            show_connection_labels=self.show_labels,
        )

    def toggle_bezier(self, value: bool):
        self.use_bezier = value

    def set_direction(self, value: str):
        self.bezier_direction = value

    def toggle_arrows(self, value: bool):
        self.show_arrows = value

    def toggle_labels(self, value: bool):
        self.show_labels = value

    def toggle_create(self, value: bool):
        self.can_create_connections = value

    def toggle_drag(self, value: bool):
        self.can_drag_camera = value

    def toggle_zoom(self, value: bool):
        self.can_zoom_camera = value

    def set_scale_preset(self, value: str):
        self.scale_preset = value

    def set_theme(self, value: str):
        self.theme_name = value

    def log_event(self, payload: dict):
        """Append an event payload to the on-screen log (newest first)."""
        self.events = [str(payload)] + self.events[:24]

    def clear_events(self):
        self.events = []
