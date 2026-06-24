# Spec-Driven Design (SDD) artifacts

This directory holds the design artifacts for **reflex-gravityui-graph**, a
Reflex custom component wrapping [`@gravity-ui/graph`](https://github.com/gravity-ui/graph).
Specifications are the primary artifact: they were written before and alongside
the implementation, and they remain the source of truth for *why* the component
is shaped the way it is.

Read them in order:

| # | Document | Purpose |
| --- | --- | --- |
| 00 | [Overview](00-overview.md) | Problem, goals, scope, phases, success criteria. |
| 01 | [PRD](01-prd.md) | Product requirements: users, user stories, functional & non-functional requirements. |
| 02 | [Architecture](02-architecture.md) | System design, the JSX-bridge decision, data flow, ADRs. |
| 03 | [Component spec](03-component-spec.md) | The exact prop / event / data contract. |
| 04 | [Plan](04-plan.md) | Phased implementation plan and milestones. |
| 05 | [Tasks](05-tasks.md) | Concrete task breakdown with status. |

Supporting research lives in [`../research/`](../research/):
- [`gravity-ui-graph.md`](../research/gravity-ui-graph.md) — upstream API & examples.
- [`reflex-wrapping.md`](../research/reflex-wrapping.md) — how Reflex wraps React/JS.
