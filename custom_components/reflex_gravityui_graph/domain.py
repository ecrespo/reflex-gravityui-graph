"""Domain value objects for @gravity-ui/graph entities (DDD).

These are framework-agnostic, immutable Python value objects that capture the
upstream entity shapes (``TBlock``, ``TConnection``, ``TAnchor``) and validate
their invariants in Python, so a misconfigured graph fails fast with a clear
message instead of silently rendering broken on Canvas. Each value object knows
how to serialize itself to the exact camelCase dict the library expects.

Typical use::

    from reflex_gravityui_graph import Block, Connection, Anchor, EAnchorType

    a = Block(id="a", x=0, y=0, name="A",
              anchors=[Anchor(id="out", block_id="a", type=EAnchorType.OUT)])
    b = Block(id="b", x=300, y=200, name="B",
              anchors=[Anchor(id="in", block_id="b", type=EAnchorType.IN)])
    edge = Connection(source_block_id="a", source_anchor_id="out",
                      target_block_id="b", target_anchor_id="in")

    blocks = [a.to_dict(), b.to_dict()]
    connections = [edge.to_dict()]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union

BlockId = Union[str, int]

# Default block discriminator. @gravity-ui/graph renders blocks whose ``is`` is
# not registered in ``settings.blockComponents`` with its built-in canvas block,
# so this default "just works" without registering a custom component.
DEFAULT_BLOCK_IS = "block-action"

# Library defaults for block geometry (constants.block.WIDTH / HEIGHT).
DEFAULT_BLOCK_WIDTH = 200
DEFAULT_BLOCK_HEIGHT = 160


class EAnchorType(str, Enum):
    """Anchor direction, mirroring the upstream ``EAnchorType`` enum."""

    IN = "IN"
    OUT = "OUT"


@dataclass(frozen=True)
class Anchor:
    """A connection point on a block (``TAnchor``).

    ``index`` orders multiple anchors of the same ``type`` on a block (the
    library auto-positions IN anchors on the left, OUT anchors on the right).
    """

    id: str
    block_id: BlockId
    type: Union[EAnchorType, str] = EAnchorType.OUT
    index: int = 0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Anchor.id must be a non-empty string")
        if self.index < 0:
            raise ValueError(f"Anchor.index must be >= 0, got {self.index}")

    def to_dict(self) -> dict[str, Any]:
        anchor_type = (
            self.type.value if isinstance(self.type, EAnchorType) else self.type
        )
        return {
            "id": self.id,
            "blockId": self.block_id,
            "type": anchor_type,
            "index": self.index,
        }


@dataclass(frozen=True)
class Block:
    """A graph node (``TBlock``).

    The library requires ``id``, ``is``, ``x``, ``y``, ``width``, ``height`` and
    ``name``; everything else is optional. ``is_`` maps to the upstream ``is``
    discriminator (``is`` is a Python keyword, hence the trailing underscore).
    """

    id: BlockId
    x: int = 0
    y: int = 0
    name: str = ""
    is_: str = DEFAULT_BLOCK_IS
    width: int = DEFAULT_BLOCK_WIDTH
    height: int = DEFAULT_BLOCK_HEIGHT
    selected: bool = False
    group: str | None = None
    anchors: list[Anchor] = field(default_factory=list)
    meta: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.id is None or self.id == "":
            raise ValueError("Block.id must be a non-empty id")
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                f"Block {self.id!r} must have positive width/height, "
                f"got {self.width}x{self.height}"
            )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "is": self.is_,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "name": self.name or str(self.id),
            "selected": self.selected,
            "anchors": [a.to_dict() for a in self.anchors],
        }
        if self.group is not None:
            data["group"] = self.group
        if self.meta is not None:
            data["meta"] = self.meta
        return data


@dataclass(frozen=True)
class Connection:
    """A graph edge (``TConnection``).

    Connect blocks directly (``source_block_id`` -> ``target_block_id``) or via
    named anchors (``source_anchor_id`` / ``target_anchor_id``). Optional
    ``label``, ``dashed`` and ``styles`` (e.g. ``{"selectedBackground": ...,
    "dashes": [6, 4]}``) customize the rendered edge.
    """

    source_block_id: BlockId
    target_block_id: BlockId
    source_anchor_id: str | None = None
    target_anchor_id: str | None = None
    id: Union[str, int, None] = None
    label: str | None = None
    dashed: bool = False
    selected: bool = False
    styles: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.source_block_id is None or self.target_block_id is None:
            raise ValueError(
                "Connection requires both source_block_id and target_block_id"
            )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "sourceBlockId": self.source_block_id,
            "targetBlockId": self.target_block_id,
        }
        if self.source_anchor_id is not None:
            data["sourceAnchorId"] = self.source_anchor_id
        if self.target_anchor_id is not None:
            data["targetAnchorId"] = self.target_anchor_id
        if self.id is not None:
            data["id"] = self.id
        if self.label is not None:
            data["label"] = self.label
        if self.dashed:
            data["dashed"] = True
        if self.selected:
            data["selected"] = True
        if self.styles is not None:
            data["styles"] = self.styles
        return data


@dataclass(frozen=True)
class GraphData:
    """An aggregate of blocks + connections with validated referential integrity.

    Use it to build a whole graph and emit the two props in one step::

        data = GraphData(blocks=[...], connections=[...])
        graph_canvas(blocks=data.blocks_payload(), connections=data.connections_payload())
    """

    blocks: list[Block] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)

    def __post_init__(self) -> None:
        ids = [b.id for b in self.blocks]
        duplicates = {i for i in ids if ids.count(i) > 1}
        if duplicates:
            raise ValueError(f"Duplicate block ids: {sorted(map(str, duplicates))}")
        known = set(ids)
        for c in self.connections:
            if c.source_block_id not in known:
                raise ValueError(
                    f"Connection source {c.source_block_id!r} is not a known block"
                )
            if c.target_block_id not in known:
                raise ValueError(
                    f"Connection target {c.target_block_id!r} is not a known block"
                )

    def blocks_payload(self) -> list[dict[str, Any]]:
        return [b.to_dict() for b in self.blocks]

    def connections_payload(self) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self.connections]
