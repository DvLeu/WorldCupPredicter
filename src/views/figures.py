import numpy as np
import plotly.graph_objects as go

from config import COLORS, MAX_G, PLOTLY_BASE


def fig_vacia(mensaje):
    return go.Figure().update_layout(
        **PLOTLY_BASE,
        height=300,
        annotations=[
            {
                "text": mensaje,
                "showarrow": False,
                "font": {"color": COLORS["txt2"], "size": 13},
            }
        ],
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
    )


def fig_pendientes(df):
    if df.empty:
        return fig_vacia("Sin partidos para este filtro")

    etiquetas = df["local"] + "  vs  " + df["visitante"]
    fig = go.Figure()

    barras = [
        ("prob_local", "Gana local", COLORS["local"]),
        ("prob_empate", "Empate", COLORS["empate"]),
        ("prob_visitante", "Gana visitante", COLORS["visit"]),
    ]

    for columna, nombre, color in barras:
        fig.add_bar(
            y=etiquetas,
            x=df[columna] * 100,
            name=nombre,
            orientation="h",
            marker_color=color,
            text=[f"{valor:.0%}" for valor in df[columna]],
            textposition="auto",
            insidetextanchor="middle",
            textfont={"color": "#ffffff", "size": 12},
            hovertemplate="%{y}<br>" + nombre + ": %{x:.1f}%<extra></extra>",
        )

    fig.update_layout(
        **PLOTLY_BASE,
        barmode="stack",
        xaxis={
            "title": "Probabilidad (%)",
            "range": [0, 100],
            "gridcolor": COLORS["border"],
        },
        yaxis={"gridcolor": "rgba(0,0,0,0)", "automargin": True},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        margin={"l": 10, "r": 10, "t": 40, "b": 40},
        height=max(320, 56 * len(df)),
        bargap=0.35,
        uniformtext={"mode": "hide", "minsize": 10},
    )
    return fig


def fig_heatmap(matriz, local, visitante, vista=6):
    submatriz = matriz[: vista + 1, : vista + 1] * 100

    fig = go.Figure(
        go.Heatmap(
            z=submatriz,
            x=list(range(vista + 1)),
            y=list(range(vista + 1)),
            colorscale=[
                [0.0, "#f8fafc"],
                [0.35, "#c7d2fe"],
                [0.7, "#60a5fa"],
                [1.0, "#047857"],
            ],
            showscale=True,
            colorbar={"title": "%", "thickness": 12},
            text=[[f"{valor:.1f}" for valor in fila] for fila in submatriz],
            texttemplate="%{text}",
            textfont={"size": 10, "color": COLORS["txt"]},
            hovertemplate=(
                f"{local} %{{y}} - {visitante} %{{x}}"
                "<br>Probabilidad: %{z:.2f}%<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        **PLOTLY_BASE,
        height=380,
        xaxis={"title": f"Goles {visitante}", "dtick": 1, "gridcolor": COLORS["border"]},
        yaxis={
            "title": f"Goles {local}",
            "dtick": 1,
            "autorange": "reversed",
            "gridcolor": COLORS["border"],
        },
        margin={"l": 10, "r": 10, "t": 30, "b": 40},
    )
    return fig


def fig_total(distribucion, vista=8):
    datos = distribucion[: vista + 1] * 100
    pico = int(np.argmax(datos))
    colores = [COLORS["accent"] if indice == pico else "#dbe4ee" for indice in range(len(datos))]

    fig = go.Figure(
        go.Bar(
            x=list(range(len(datos))),
            y=datos,
            marker_color=colores,
            text=[f"{valor:.0f}%" for valor in datos],
            textposition="outside",
            textfont={"color": COLORS["txt2"], "size": 11},
            hovertemplate="Total %{x} goles<br>Probabilidad: %{y:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_BASE,
        height=300,
        xaxis={"title": "Total de goles en el partido", "dtick": 1},
        yaxis={"title": "Probabilidad (%)", "gridcolor": COLORS["border"], "gridwidth": 1},
        margin={"l": 10, "r": 10, "t": 30, "b": 40},
        uniformtext={"mode": "hide", "minsize": 10},
    )
    return fig
