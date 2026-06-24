"""Unit tests for the DDD value objects (pure Python, no Reflex needed)."""

import pytest

from reflex_gravityui_graph.domain import (
    Anchor,
    Block,
    Connection,
    EAnchorType,
    GraphData,
)


def test_block_to_dict_uses_upstream_keys():
    b = Block(id="a", x=1, y=2, name="A", width=120, height=90)
    d = b.to_dict()
    assert d["id"] == "a"
    assert d["is"] == "block-action"  # default discriminator
    assert (d["x"], d["y"], d["width"], d["height"]) == (1, 2, 120, 90)
    assert d["name"] == "A"
    assert d["anchors"] == []


def test_block_name_defaults_to_id():
    assert Block(id="x").to_dict()["name"] == "x"


def test_block_rejects_non_positive_size():
    with pytest.raises(ValueError):
        Block(id="a", width=0)


def test_anchor_serialization_and_enum():
    a = Anchor(id="out", block_id="a", type=EAnchorType.OUT, index=1)
    d = a.to_dict()
    assert d == {"id": "out", "blockId": "a", "type": "OUT", "index": 1}


def test_anchor_rejects_negative_index():
    with pytest.raises(ValueError):
        Anchor(id="o", block_id="a", index=-1)


def test_connection_optional_fields_omitted():
    c = Connection(source_block_id="a", target_block_id="b")
    d = c.to_dict()
    assert d == {"sourceBlockId": "a", "targetBlockId": "b"}


def test_connection_full_payload():
    c = Connection(
        source_block_id="a", source_anchor_id="o",
        target_block_id="b", target_anchor_id="i",
        id=7, label="edge", dashed=True, selected=True,
        styles={"background": "#f00"},
    )
    d = c.to_dict()
    assert d["sourceAnchorId"] == "o"
    assert d["targetAnchorId"] == "i"
    assert d["id"] == 7
    assert d["label"] == "edge"
    assert d["dashed"] is True
    assert d["selected"] is True
    assert d["styles"] == {"background": "#f00"}


def test_connection_requires_both_endpoints():
    with pytest.raises(ValueError):
        Connection(source_block_id=None, target_block_id="b")


def test_graphdata_detects_duplicate_block_ids():
    with pytest.raises(ValueError):
        GraphData(blocks=[Block(id="a"), Block(id="a")])


def test_graphdata_validates_connection_endpoints():
    with pytest.raises(ValueError):
        GraphData(
            blocks=[Block(id="a")],
            connections=[Connection(source_block_id="a", target_block_id="ghost")],
        )


def test_graphdata_payload_roundtrip():
    data = GraphData(
        blocks=[Block(id="a"), Block(id="b")],
        connections=[Connection(source_block_id="a", target_block_id="b")],
    )
    assert len(data.blocks_payload()) == 2
    assert data.connections_payload()[0]["targetBlockId"] == "b"
