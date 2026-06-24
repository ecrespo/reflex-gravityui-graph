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
from .graph import (
    GRAVITY_GRAPH_VERSION,
    GravityGraph,
    graph_canvas,
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
