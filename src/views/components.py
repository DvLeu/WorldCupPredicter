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
                className=f"score-row{' score-row-primary' if indice == 0 else ''}",
                children=[
                    html.Span(
                        marcador,
                        className="score-name",
                        style={"color": COLORS["accent"] if indice == 0 else COLORS["txt"]},
                    ),
                    html.Span(
                        f"{probabilidad:.1%}",
                        className="score-prob",
                    ),
                ],
            )
        )

    return html.Div(
        className="score-list",
        children=items,
    )
