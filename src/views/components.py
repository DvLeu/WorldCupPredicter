from dash import html

from config import COLORS


def metric_card(valor, etiqueta, color=None):
    return html.Div(
        className="metric",
        children=[
            html.Div(
                valor,
                className="metric-val",
                style={"color": color or COLORS["accent"]},
            ),
            html.Div(etiqueta, className="metric-lbl"),
        ],
    )


def top5_marcadores(top5):
    items = []

    for indice, (marcador, probabilidad) in enumerate(top5):
        items.append(
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "padding": "6px 10px",
                    "background": COLORS["card2"] if indice == 0 else "transparent",
                    "borderRadius": "8px",
                    "marginBottom": "4px",
                },
                children=[
                    html.Span(
                        marcador,
                        style={
                            "fontWeight": "700" if indice == 0 else "400",
                            "fontSize": "15px",
                            "color": COLORS["accent"] if indice == 0 else COLORS["txt"],
                        },
                    ),
                    html.Span(
                        f"{probabilidad:.1%}",
                        style={"fontSize": "13px", "color": COLORS["txt2"]},
                    ),
                ],
            )
        )

    return html.Div(
        [
            html.Div(
                "Marcadores mas probables",
                style={
                    "fontSize": "11px",
                    "color": COLORS["txt2"],
                    "textTransform": "uppercase",
                    "letterSpacing": ".4px",
                    "marginBottom": "8px",
                    "fontWeight": "600",
                },
            ),
            *items,
        ],
        style={
            "background": COLORS["card"],
            "border": f"1px solid {COLORS['border']}",
            "borderRadius": "12px",
            "padding": "14px",
        },
    )
