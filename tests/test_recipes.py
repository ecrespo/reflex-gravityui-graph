"""Unit tests for the example/recipe helpers (pure Python, no Reflex needed)."""

import pytest

from reflex_gravityui_graph import recipes


def test_default_settings_keys_are_camelcase():
    s = recipes.default_settings()
    assert s["useBezierConnections"] is True
    assert s["canDragCamera"] is True
    assert s["showConnectionArrows"] is True
    assert "bezierConnectionDirection" in s


def test_default_settings_enables_block_drag_by_default():
    # @gravity-ui/graph defaults canDrag to NONE (blocks immovable); the recipe
    # must opt into draggable nodes so the component is interactive out of the box.
    assert recipes.default_settings()["canDrag"] == "all"


def test_default_settings_can_restrict_block_drag():
    assert recipes.default_settings(can_drag_blocks=False)["canDrag"] == "none"
    assert (
        recipes.default_settings(can_drag_blocks="onlySelected")["canDrag"]
        == "onlySelected"
    )


def test_one_block():
    data = recipes.one_block()
    assert len(data.blocks) == 1
    assert data.connections == []


def test_two_connected_blocks_has_anchored_edge():
    data = recipes.two_connected_blocks()
    payload = data.connections_payload()[0]
    assert payload["sourceAnchorId"] == "out1"
    assert payload["targetAnchorId"] == "in1"


def test_colored_connections_have_styles():
    data = recipes.colored_connections()
    assert data.connections, "expected at least one connection"
    assert all("styles" in c.to_dict() for c in data.connections)


def test_block_with_anchors_counts():
    data = recipes.block_with_anchors(n_in=3, n_out=2)
    anchors = data.blocks[0].anchors
    ins = [a for a in anchors if a.type.value == "IN"]
    outs = [a for a in anchors if a.type.value == "OUT"]
    assert len(ins) == 3 and len(outs) == 2


def test_generate_layered_blocks_is_reproducible():
    a = recipes.generate_layered_blocks(layers_count=5, connections_per_layer=5)
    b = recipes.generate_layered_blocks(layers_count=5, connections_per_layer=5)
    assert a.blocks_payload() == b.blocks_payload()
    assert a.connections_payload() == b.connections_payload()


def test_generate_layered_blocks_referential_integrity():
    # GraphData construction validates every edge endpoint exists.
    data = recipes.generate_layered_blocks(layers_count=8, connections_per_layer=12)
    assert len(data.blocks) == 8 * 12


def test_generate_layered_blocks_rejects_bad_args():
    with pytest.raises(ValueError):
        recipes.generate_layered_blocks(layers_count=0, connections_per_layer=5)


def test_grouped_graph_assigns_groups():
    data = recipes.grouped_graph(groups=3, per_group=4)
    groups = {b.group for b in data.blocks}
    assert groups == {"group_0", "group_1", "group_2"}


def test_themes_have_light_and_dark():
    assert set(recipes.THEMES) == {"light", "dark"}
    assert "block" in recipes.THEMES["light"]
