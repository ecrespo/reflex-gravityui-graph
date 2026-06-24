"""Contract tests for the Reflex component wiring.

These require ``reflex`` to be importable; they are skipped otherwise so the
pure-domain suite still runs on minimal environments.
"""

import pytest

reflex = pytest.importorskip("reflex")


def test_public_api_exports():
    import reflex_gravityui_graph as pkg

    for name in [
        "GravityGraph", "graph_canvas", "GRAVITY_GRAPH_VERSION",
        "Block", "Connection", "Anchor", "EAnchorType", "GraphData",
        "default_settings", "generate_layered_blocks", "THEMES",
    ]:
        assert hasattr(pkg, name), f"missing public export: {name}"


def test_component_library_pins_gravity_version():
    from reflex_gravityui_graph.graph import GRAVITY_GRAPH_VERSION

    assert GRAVITY_GRAPH_VERSION == "@gravity-ui/graph@1.11.0"


def test_component_is_nossr_and_named_export():
    from reflex.components.component import NoSSRComponent

    from reflex_gravityui_graph import GravityGraph

    assert issubclass(GravityGraph, NoSSRComponent)
    assert GravityGraph.tag == "GravityGraph"
    assert GravityGraph.is_default is False


def test_component_creates_with_snake_to_camel_props():
    from reflex_gravityui_graph import graph_canvas

    comp = graph_canvas(
        blocks=[{"id": "a", "is": "block-action", "x": 0, "y": 0,
                 "width": 100, "height": 100, "name": "A"}],
        connections=[],
        config_name="demo",
        render_html_blocks=True,
    )
    rendered = str(comp.render())
    # Reflex converts snake_case prop names to camelCase in the output.
    assert "configName" in rendered
    assert "renderHtmlBlocks" in rendered


# The six events the component contract (docs/sdd/03-component-spec.md, FR6)
# promises. They must stay exposed and wireable so handlers keep receiving data.
EXPECTED_EVENTS = {
    "on_block_selection_change",
    "on_connection_created",
    "on_connection_selection_change",
    "on_camera_change",
    "on_block_drag_end",
    "on_state_change",
}


def test_component_exposes_all_six_event_triggers():
    from reflex_gravityui_graph import graph_canvas

    triggers = set(graph_canvas(blocks=[], connections=[]).get_event_triggers())
    assert EXPECTED_EVENTS <= triggers, (
        "missing event triggers: " f"{sorted(EXPECTED_EVENTS - triggers)}"
    )


def test_all_event_handlers_are_wireable():
    import reflex as rx

    from reflex_gravityui_graph import graph_canvas

    class _Sink(rx.State):
        def on_event(self, payload: dict):
            ...

    comp = graph_canvas(
        blocks=[],
        connections=[],
        on_block_selection_change=_Sink.on_event,
        on_connection_created=_Sink.on_event,
        on_connection_selection_change=_Sink.on_event,
        on_camera_change=_Sink.on_event,
        on_block_drag_end=_Sink.on_event,
        on_state_change=_Sink.on_event,
    )
    # Every wired event must register on the instance, and render must succeed.
    assert EXPECTED_EVENTS <= set(comp.event_triggers)
    assert str(comp.render())
