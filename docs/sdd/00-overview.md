# 00 · Overview

## Problem

Reflex developers building flowcharts, node editors, pipeline visualizations or
large diagrams in pure Python have no high-performance graph component.
`@gravity-ui/graph` solves the performance/interactivity trade-off on the web
(Canvas when zoomed out, HTML/React when zoomed in), but it is a TypeScript +
React, hook-driven, imperative library — not usable from Reflex out of the box.

## Goal

Ship a publish-ready Reflex **custom component** that wraps `@gravity-ui/graph`
and exposes its full feature set declaratively from Python, with a demo app that
reproduces the upstream Storybook examples, full SDD documentation, and a
`uv`-based build/publish workflow.

## In scope

- A `GravityGraph` / `graph_canvas` component covering blocks, connections,
  settings, colors, constants, camera/zoom, and the principal events.
- DDD value objects (`Block`, `Connection`, `Anchor`, `GraphData`) that build and
  validate entity payloads in Python.
- Recipe helpers that reproduce the Storybook stories (basics, anchors, colored
  edges, grouping, and the hundred/thousand/five-thousand performance graphs).
- A multi-page demo app, one page per example category.
- SDD artifacts + research notes, packaged for PyPI per the Reflex
  custom-component prerequisites.

## Out of scope (v0.1, see roadmap in 04-plan)

- The optional plugin layers that pull extra npm packages: ELK / layered
  auto-layout (`elkjs`), MiniMap, DevTools, CSS-variables layer. These are
  documented as a follow-up because they require additional dependencies and a
  per-layer bridge.
- Fully custom canvas block classes registered via `settings.blockComponents`
  (functions/classes can't cross the Python↔JS boundary as plain props).

## Phases

1. **Phase 0 — Foundations.** Repo scaffold, packaging, JSX bridge, core
   component, NoSSR wiring, smoke demo.
2. **Phase 1 — Data & domain.** `Block`/`Connection`/`Anchor`/`GraphData` value
   objects with validation; snake→camel contract.
3. **Phase 2 — Examples & demo.** Recipe helpers + multi-page demo covering all
   example categories; live settings/theming controls.
4. **Phase 3 — Events & interaction.** Selection / connection-created / camera
   events; optional HTML blocks.
5. **Phase 4 — Packaging & publish.** Stub generation, tests, CI, README, build
   with `uv`, GitHub repo, PyPI.

## Success criteria

- `graph_canvas(...)` renders a working graph in a Reflex page.
- The demo runs and reproduces every example category from Storybook.
- `pytest` passes; `uv run reflex component build` produces a valid wheel/sdist
  and `twine check` passes.
- The package installs from PyPI and imports cleanly.
