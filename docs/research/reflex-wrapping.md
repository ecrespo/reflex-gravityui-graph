# Research · Wrapping React/JS in Reflex + publishing

Sources: Reflex docs — Wrapping React, Custom Components (overview /
prerequisites / command reference).

## Custom-component layout

This repo was scaffolded with `reflex component init` (Reflex ≤ 0.9; the command
was removed in 0.10 in favour of the
[component template](https://github.com/reflex-dev/component-template)). The
layout it produced — PyPI package name `reflex-<folder>` — is kept as-is:

```
pyproject.toml
README.md
custom_components/reflex_gravityui_graph/   # importable package (shipped)
  ├─ __init__.py        # re-exports the public API
  └─ <component>.py      # the wrapper(s)
<name>_demo/            # a normal Reflex app that imports the component
```

`[tool.setuptools.packages.find] where = ["custom_components"]` makes the inner
package the distributable. The `reflex-` prefix and the
`reflex-custom-components` keyword aid PyPI/gallery discovery.

## Wrapping a React component

- A wrapper subclasses `rx.Component` (or `NoSSRComponent` for browser-only libs).
- `library` = npm import specifier; `tag` = export name; `is_default` selects
  default vs named export.
- `lib_dependencies` pins the real npm package(s) into `package.json`.
- Props are class attrs typed as `rx.Var[...]`; Reflex renames snake_case →
  camelCase automatically (override via `_rename_props`).
- Events are `rx.EventHandler[spec]`; the spec maps JS callback args → handler
  args. Returning `(payload,)` forwards a single serializable dict.
- Stylesheets: `add_imports` with an empty key (`{"": "pkg/styles.css"}`).
- Custom JS / hooks: `add_custom_code` (page-level code) and `add_hooks`
  (component hooks, optionally ordered with `VarData.position`).

## Wrapping a hook-based / imperative library

Reflex components can't call React hooks. The robust pattern is to ship a local
`.jsx` **bridge** that encapsulates the hooks/imperative lifecycle and exposes
flat props, then wrap the bridge:

- `path = rx.asset("./bridge.jsx", shared=True)` copies it into the frontend
  public dir.
- `library = f"$/public{path}"`, `tag = "Bridge"`, `is_default = False`.
- `lib_dependencies = ["the-real-pkg@x.y.z"]`; the bridge imports the real lib.

This component uses exactly that approach for `@gravity-ui/graph` (`useGraph` +
imperative `setEntities`/`start`/`zoomTo`). See `docs/sdd/02-architecture.md`.

## Publishing (with `uv`)

Prerequisites: a PyPI account + API token.

```bash
uv sync --extra dev
uv run pytest -q
uv run --with ruff python -m reflex_base.utils.pyi_generator custom_components/reflex_gravityui_graph/graph.py   # refresh the .pyi stub
uv build                            # builds .tar.gz + .whl into dist/
uv publish                          # uploads to PyPI (token via env/CLI)
```

Reflex 0.10 removed the `reflex component` CLI (`init`/`build`/`publish`/`share`);
the official replacement is the
[component template](https://github.com/reflex-dev/component-template). This repo
keeps its setuptools layout: the stub is generated with Reflex's
`reflex_base.utils.pyi_generator`, committed, and shipped via package-data, and
`uv build` runs at the project root (where `pyproject.toml` lives). Keep `version` in `pyproject.toml`
bumped for each release. `twine check dist/*` validates metadata before upload.

## Checklist mapped to this repo

- ✅ custom-component layout (`custom_components/reflex_gravityui_graph/` + demo).
- ✅ `pyproject.toml` with name `reflex-gravityui-graph`, `reflex-custom-components`
  keyword, Apache-2.0, `dev` extras, `*.pyi`/`*.jsx` package-data.
- ✅ NoSSR wrapper + JSX bridge + pinned `lib_dependencies`.
- ✅ README with install + `uv` build/publish instructions.
- ✅ `.pyi` stub generated with the Reflex 0.10 `pyi_generator`; `uv build` +
  `uv publish` on Python 3.11–3.13 (0.1.0 and 0.2.0 published).
