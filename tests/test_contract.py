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
