"""Ergonomic helpers that reproduce the upstream @gravity-ui/graph examples.

The library's Storybook ships many stories: hello-world blocks, anchored
connections, bezier vs straight edges, colored/dashed connections, and large
"layered" graphs with hundreds to thousands of nodes. These helpers build the
equivalent ``blocks``/``connections``/``settings``/``colors`` payloads from a
plain-Python API so the Reflex demo (and consumers) never hand-write the data.

All functions return JSON-serializable structures ready to pass straight to
``graph_canvas(...)``.
"""

from __future__ import annotations

import math
import random
from typing import Any

from .domain import (
    DEFAULT_BLOCK_IS,
    Anchor,
    Block,
    Connection,
    EAnchorType,
    GraphData,
)

# --------------------------------------------------------------------------- #
# Settings presets (mirror the Storybook argTypes / story configs)
# --------------------------------------------------------------------------- #


# Valid @gravity-ui/graph ``canDrag`` (ECanDrag) values: which blocks the user
# can move with the mouse. The library default is ``"none"`` (blocks immovable).
_CAN_DRAG_VALUES = {"all", "onlySelected", "none"}


def _normalize_can_drag(value: bool | str) -> str:
    """Map an ergonomic ``can_drag_blocks`` flag to an ECanDrag string."""
    if isinstance(value, bool):
        return "all" if value else "none"
    if value not in _CAN_DRAG_VALUES:
        raise ValueError(
            f"can_drag_blocks must be a bool or one of {sorted(_CAN_DRAG_VALUES)}, "
            f"got {value!r}"
        )
    return value


def default_settings(
    *,
    can_drag_camera: bool = True,
    can_zoom_camera: bool = True,
    can_drag_blocks: bool | str = True,
    can_create_new_connections: bool = False,
    use_bezier_connections: bool = True,
    bezier_direction: str = "horizontal",
    show_connection_arrows: bool = True,
    show_connection_labels: bool = False,
    use_blocks_anchors: bool = True,
    scale_font_size: float = 1.0,
) -> dict[str, Any]:
    """Build a ``settings`` dict from the most common Storybook controls.

    ``can_drag_blocks`` controls whether nodes can be moved with the mouse
    (``canDrag``). The upstream default is ``"none"`` (immovable), so this
    defaults to ``True`` -> ``"all"`` to keep the component interactive. Pass
    ``False`` for ``"none"`` or ``"onlySelected"`` to restrict it.
    """
    return {
        "canDragCamera": can_drag_camera,
        "canZoomCamera": can_zoom_camera,
        "canDrag": _normalize_can_drag(can_drag_blocks),
        "canCreateNewConnections": can_create_new_connections,
        "useBezierConnections": use_bezier_connections,
        "bezierConnectionDirection": bezier_direction,
        "showConnectionArrows": show_connection_arrows,
        "showConnectionLabels": show_connection_labels,
        "useBlocksAnchors": use_blocks_anchors,
        "scaleFontSize": scale_font_size,
    }


# --------------------------------------------------------------------------- #
# Color themes (mirror the "Theme" / "updateGraphColors" stories)
# --------------------------------------------------------------------------- #

LIGHT_THEME: dict[str, Any] = {
    "canvas": {"layerBackground": "#f9f9f9", "belowLayerBackground": "#eaeaea",
               "dots": "#d0d2ce", "border": "#EAEAEAFF"},
    "block": {"background": "#e0e0e0", "border": "#dfdfdf", "text": "#272727",
              "selectedBorder": "#FFCC00"},
    "anchor": {"background": "#4a4a4a", "selectedBorder": "#FFCC00"},
    "connection": {"background": "#272727", "selectedBackground": "#ecc113"},
    "selection": {"background": "rgba(0,0,0,0.051)", "border": "#ecc113"},
}

DARK_THEME: dict[str, Any] = {
    "canvas": {"layerBackground": "#1f1f1f", "belowLayerBackground": "#161616",
               "dots": "#3a3a3a", "border": "#2a2a2aFF"},
    "block": {"background": "#2c2c2c", "border": "#3a3a3a", "text": "#ffffff",
              "selectedBorder": "#FFCC00"},
    "anchor": {"background": "#c0c0c0", "selectedBorder": "#FFCC00"},
    "connection": {"background": "#d0d0d0", "selectedBackground": "#ecc113"},
    "selection": {"background": "rgba(255,255,255,0.08)", "border": "#ecc113"},
}

THEMES: dict[str, dict[str, Any]] = {"light": LIGHT_THEME, "dark": DARK_THEME}


# --------------------------------------------------------------------------- #
# Small, hand-built example graphs (the "Main/GraphEditor" basic stories)
# --------------------------------------------------------------------------- #


def one_block() -> GraphData:
    """The hello-world story: a single block."""
    return GraphData(
        blocks=[Block(id="block_1", x=0, y=0, width=160, height=160,
                      name="Block #1")],
        connections=[],
    )


def two_connected_blocks(*, bezier: bool = True) -> GraphData:
    """Two anchored blocks joined by one connection (straight or bezier)."""
    a = Block(
        id="action_1", x=-200, y=-120, width=160, height=160, name="Block #1",
        anchors=[Anchor(id="out1", block_id="action_1", type=EAnchorType.OUT)],
    )
    b = Block(
        id="action_2", x=220, y=140, width=160, height=160, name="Block #2",
        anchors=[Anchor(id="in1", block_id="action_2", type=EAnchorType.IN)],
    )
    edge = Connection(
        source_block_id="action_1", source_anchor_id="out1",
        target_block_id="action_2", target_anchor_id="in1",
    )
    return GraphData(blocks=[a, b], connections=[edge])


def colored_connections() -> GraphData:
    """Mirrors the "ColoredConnections" story: per-edge colored/dashed styles."""
    palette = ["#e74c3c", "#27ae60", "#2980b9", "#8e44ad"]
    blocks: list[Block] = []
    connections: list[Connection] = []
    hub = Block(id="hub", x=0, y=0, width=160, height=120, name="Hub",
                anchors=[Anchor(id="hub_out", block_id="hub",
                                type=EAnchorType.OUT)])
    blocks.append(hub)
    for i, color in enumerate(palette):
        angle = (i / len(palette)) * 2 * math.pi
        leaf_id = f"leaf_{i}"
        blocks.append(
            Block(
                id=leaf_id, x=int(360 * math.cos(angle)),
                y=int(260 * math.sin(angle)), width=140, height=110,
                name=f"Leaf {i + 1}",
                anchors=[Anchor(id=f"{leaf_id}_in", block_id=leaf_id,
                                type=EAnchorType.IN)],
            )
        )
        connections.append(
            Connection(
                source_block_id="hub", source_anchor_id="hub_out",
                target_block_id=leaf_id, target_anchor_id=f"{leaf_id}_in",
                label=f"edge {i + 1}", dashed=(i % 2 == 1),
                styles={"background": color, "selectedBackground": color},
            )
        )
    return GraphData(blocks=blocks, connections=connections)


def block_with_anchors(n_in: int = 2, n_out: int = 2) -> GraphData:
    """Mirrors the "WithAnchors" story: a block exposing several IN/OUT anchors."""
    anchors = [
        Anchor(id=f"in_{i}", block_id="anchored", type=EAnchorType.IN, index=i)
        for i in range(n_in)
    ] + [
        Anchor(id=f"out_{i}", block_id="anchored", type=EAnchorType.OUT, index=i)
        for i in range(n_out)
    ]
    return GraphData(
        blocks=[Block(id="anchored", x=0, y=0, width=200, height=200,
                      name="Anchored block", anchors=anchors)],
        connections=[],
    )


# --------------------------------------------------------------------------- #
# Large "layered" graph generator (Hundred/Thousand/FiveThousand stories)
# --------------------------------------------------------------------------- #


def generate_layered_blocks(
    *,
    layers_count: int = 10,
    connections_per_layer: int = 20,
    dashed: bool = False,
    block_is: str = DEFAULT_BLOCK_IS,
    seed: int | None = 42,
    h_gap: int = 360,
    v_gap: int = 220,
) -> GraphData:
    """Reproduce the upstream ``generatePrettyBlocks`` layered graphs.

    Creates ``layers_count`` columns of nodes wired left-to-right, where each
    layer holds roughly ``connections_per_layer`` nodes. Use it for the
    "HundredBlocks" (10x100), "ThousandBlocks" (25x200) and "FiveThousandsBlocks"
    (40x300) demos. A fixed ``seed`` keeps the layout reproducible.
    """
    if layers_count <= 0 or connections_per_layer <= 0:
        raise ValueError("layers_count and connections_per_layer must be > 0")
    rng = random.Random(seed)
    nodes_per_layer = max(1, connections_per_layer)

    blocks: list[Block] = []
    layer_ids: list[list[str]] = []
    for layer in range(layers_count):
        ids: list[str] = []
        for n in range(nodes_per_layer):
            bid = f"l{layer}_n{n}"
            blocks.append(
                Block(
                    id=bid, is_=block_is,
                    x=layer * h_gap,
                    y=int((n - nodes_per_layer / 2) * v_gap),
                    width=150, height=90, name=bid,
                    anchors=[
                        Anchor(id=f"{bid}_in", block_id=bid, type=EAnchorType.IN),
                        Anchor(id=f"{bid}_out", block_id=bid, type=EAnchorType.OUT),
                    ],
                )
            )
            ids.append(bid)
        layer_ids.append(ids)

    connections: list[Connection] = []
    for layer in range(layers_count - 1):
        src_ids = layer_ids[layer]
        dst_ids = layer_ids[layer + 1]
        for _ in range(connections_per_layer):
            s = rng.choice(src_ids)
            t = rng.choice(dst_ids)
            connections.append(
                Connection(
                    source_block_id=s, source_anchor_id=f"{s}_out",
                    target_block_id=t, target_anchor_id=f"{t}_in",
                    dashed=dashed,
                )
            )
    return GraphData(blocks=blocks, connections=connections)


# --------------------------------------------------------------------------- #
# Grouping example (the "Canvas/Groups" stories)
# --------------------------------------------------------------------------- #


def grouped_graph(groups: int = 3, per_group: int = 4) -> GraphData:
    """Build a grouped graph by assigning blocks to ``group`` ids."""
    blocks: list[Block] = []
    connections: list[Connection] = []
    for g in range(groups):
        prev: str | None = None
        for i in range(per_group):
            bid = f"g{g}_b{i}"
            blocks.append(
                Block(
                    id=bid, group=f"group_{g}",
                    x=g * 420, y=i * 160, width=150, height=90,
                    name=f"G{g} · {i}",
                    anchors=[
                        Anchor(id=f"{bid}_in", block_id=bid, type=EAnchorType.IN),
                        Anchor(id=f"{bid}_out", block_id=bid, type=EAnchorType.OUT),
                    ],
                )
            )
            if prev is not None:
                connections.append(
                    Connection(
                        source_block_id=prev, source_anchor_id=f"{prev}_out",
                        target_block_id=bid, target_anchor_id=f"{bid}_in",
                    )
                )
            prev = bid
    return GraphData(blocks=blocks, connections=connections)
