"""Functional guards for the demo app (reflex_gravityui_graph_demo).

The demo lives in a sibling package, so these tests build its pages in an
isolated interpreter with the demo on the path. They validate that the demo
keeps exercising the component contract (here: the full event surface, FR6).
"""

import os
import subprocess
import sys
import textwrap

import pytest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = ROOT / "custom_components"
DEMO_ROOT = ROOT / "reflex_gravityui_graph_demo"

pytest.importorskip("reflex")

if not (DEMO_ROOT / "reflex_gravityui_graph_demo").is_dir():
    pytest.skip("demo package not present", allow_module_level=True)


def _build_page_and_collect_events(module: str, factory: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(PKG_ROOT), str(DEMO_ROOT), env.get("PYTHONPATH", "")]
    )
    code = textwrap.dedent(
        f"""
        import importlib
        mod = importlib.import_module("{module}")
        comp = getattr(mod, "{factory}")()

        def find_gravity(node):
            if type(node).__name__ == "GravityGraph":
                return node
            for child in getattr(node, "children", []) or []:
                found = find_gravity(child)
                if found is not None:
                    return found
            return None

        graph = find_gravity(comp)
        assert graph is not None, "no GravityGraph found in page"
        print("EVENTS:" + ",".join(sorted(graph.event_triggers)))
        """
    )
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env
    )


def test_sidebar_uses_only_valid_icons():
    """Building a page must not trip Reflex's invalid-icon-tag fallback."""
    result = _build_page_and_collect_events(
        "reflex_gravityui_graph_demo.reflex_gravityui_graph_demo", "index"
    )
    combined = result.stdout + result.stderr
    assert "Invalid icon tag" not in combined, combined


def test_interaction_page_wires_full_event_surface():
    result = _build_page_and_collect_events(
        "reflex_gravityui_graph_demo.pages.interaction", "interaction_page"
    )
    assert result.returncode == 0, result.stderr
    line = next(ln for ln in result.stdout.splitlines() if ln.startswith("EVENTS:"))
    wired = set(line[len("EVENTS:"):].split(",")) if line[len("EVENTS:"):] else set()
    expected = {
        "on_block_selection_change",
        "on_connection_created",
        "on_connection_selection_change",
        "on_camera_change",
        "on_block_drag_end",
        "on_state_change",
    }
    assert expected <= wired, f"interaction demo missing events: {sorted(expected - wired)}"
