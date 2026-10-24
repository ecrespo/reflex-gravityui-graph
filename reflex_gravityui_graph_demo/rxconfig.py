import reflex as rx

config = rx.Config(
    app_name="reflex_gravityui_graph_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
