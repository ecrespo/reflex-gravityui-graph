"""reflex-gravityui-graph: a Reflex wrapper for @gravity-ui/graph.

Public API::

    from reflex_gravityui_graph import graph_canvas, GravityGraph

    # DDD value objects for building graph data:
    from reflex_gravityui_graph import Block, Connection, Anchor, EAnchorType, GraphData

    # Example/recipe helpers (reproduce the upstream Storybook stories):
    from reflex_gravityui_graph import (
        one_block, two_connected_blocks, colored_connections, block_with_anchors,
        generate_layered_blocks, grouped_graph, default_settings, THEMES,
    )
"""

from typing import TYPE_CHECKING, Any

from .domain import (
    DEFAULT_BLOCK_HEIGHT,
    DEFAULT_BLOCK_IS,
    DEFAULT_BLOCK_WIDTH,
    Anchor,
    Block,
    Connection,
    EAnchorType,
    GraphData,
)
from .recipes import (
    DARK_THEME,
    LIGHT_THEME,
    THEMES,
    block_with_anchors,
    colored_connections,
    default_settings,
    generate_layered_blocks,
    grouped_graph,
    one_block,
    two_connected_blocks,
)

# The component layer (``graph.py``) imports Reflex. We expose it lazily via
# PEP 562 ``__getattr__`` so the pure-Python domain/recipe API stays importable
# and unit-testable without Reflex installed (NFR5). Reflex is only imported
# when one of these symbols is actually accessed.
_LAZY_COMPONENT_EXPORTS = {"GravityGraph", "graph_canvas", "GRAVITY_GRAPH_VERSION"}

if TYPE_CHECKING:  # pragma: no cover - typing/IDE only
    from .graph import (  # noqa: F401
        GRAVITY_GRAPH_VERSION,
        GravityGraph,
        graph_canvas,
    )


def __getattr__(name: str) -> Any:
    """Lazily resolve the Reflex-dependent component exports (PEP 562)."""
    if name in _LAZY_COMPONENT_EXPORTS:
        from . import graph

        return getattr(graph, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__version__ = "0.1.0"

__all__ = [
    # Component
    "GravityGraph",
    "graph_canvas",
    "GRAVITY_GRAPH_VERSION",
    # Domain
    "Anchor",
    "Block",
    "Connection",
    "EAnchorType",
    "GraphData",
    "DEFAULT_BLOCK_IS",
    "DEFAULT_BLOCK_WIDTH",
    "DEFAULT_BLOCK_HEIGHT",
    # Recipes
    "default_settings",
    "one_block",
    "two_connected_blocks",
    "colored_connections",
    "block_with_anchors",
    "generate_layered_blocks",
    "grouped_graph",
    "THEMES",
    "LIGHT_THEME",
    "DARK_THEME",
    "__version__",
]
