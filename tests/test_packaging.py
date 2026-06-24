"""Packaging / import-surface contracts.

These guard the design promises in the SDD that aren't about runtime behavior:

* NFR5: the pure-Python domain/recipe logic must be importable and unit-testable
  *without* Reflex installed (so the pure suite runs on minimal environments).
* The JSX bridge ships in the package and its event contract stays in sync with
  the documented payloads.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = ROOT / "custom_components"
JSX = PKG_ROOT / "reflex_gravityui_graph" / "graph_canvas.jsx"


def _run_without_reflex(code: str) -> subprocess.CompletedProcess:
    """Run *code* in a fresh interpreter where ``import reflex`` fails."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(PKG_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    prelude = textwrap.dedent(
        """
        import sys
        # Make any `import reflex` (or submodule) raise ImportError, simulating a
        # minimal environment without Reflex installed.
        class _Blocker:
            def find_spec(self, name, path=None, target=None):
                if name == "reflex" or name.startswith("reflex."):
                    raise ImportError("reflex is blocked for this test")
                return None
        sys.meta_path.insert(0, _Blocker())
        """
    )
    return subprocess.run(
        [sys.executable, "-c", prelude + textwrap.dedent(code)],
        capture_output=True,
        text=True,
        env=env,
    )


def test_domain_and_recipes_import_without_reflex():
    result = _run_without_reflex(
        """
        from reflex_gravityui_graph import domain, recipes
        from reflex_gravityui_graph import Block, Connection, GraphData
        from reflex_gravityui_graph import one_block, generate_layered_blocks

        b = Block(id="a")
        assert b.to_dict()["id"] == "a"
        assert one_block().blocks[0].id == "block_1"
        assert len(generate_layered_blocks(layers_count=3, connections_per_layer=3).blocks) == 9
        print("PURE-IMPORT-OK")
        """
    )
    assert result.returncode == 0, (
        "domain/recipes must import without Reflex (NFR5).\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "PURE-IMPORT-OK" in result.stdout


def test_jsx_bridge_is_shipped_in_package():
    assert JSX.is_file(), f"JSX bridge must ship in the package at {JSX}"


def test_jsx_bridge_subscribes_to_documented_events():
    """The bridge must wire every upstream event name the Python API promises.

    Names/payloads are documented in docs/research/gravity-ui-graph.md and the
    component spec; a silent rename upstream would make events never fire.
    """
    src = JSX.read_text()
    for event_name in (
        "blocks-selection-change",
        "connection-created",
        "connection-selection-change",
        "camera-change",
        "block-drag-end",
    ):
        assert event_name in src, f"bridge no longer subscribes to {event_name!r}"
    # Reduced, serializable payload keys the Python handlers rely on.
    for payload_key in ("sourceBlockId", "targetBlockId", "scale", "blockId"):
        assert payload_key in src, f"bridge dropped payload key {payload_key!r}"
