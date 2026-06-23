import io
from datetime import datetime

import pandas as pd
from dash import Input, Output, html

from config import COLORS
from models.predictor import (
    analizar_goles,
    cargar_y_entrenar,
    matriz_marcadores,
    mezclar_elo,
    prob_1x2_de_matriz,
)
from views.components import metric_card, top5_marcadores
from views.figures import fig_heatmap, fig_pendientes, fig_total, fig_vacia


def registrar_callbacks(app):
    """Registra todos los callbacks de Dash."""

    @app.callback(
        Output("store-pend", "data"),
        Output("store-modelo", "data"),
        Output("filtro-torneo", "options"),
        Output("sel-local", "options"),
        Output("sel-visit", "options"),
        Output("ultima-actualizacion", "children"),
        Input("intervalo", "n_intervals"),
    )
    def refrescar(_):
        df_pendientes, modelo = cargar_y_entrenar()

        if df_pendientes.empty:
            torneos = []
            pendientes_json = "{}"
            cantidad = 0
        else:
            torneos = [
                {"label": torneo, "value": torneo}
                for torneo in sorted(df_pendientes["torneo"].unique())
            ]
            pendientes_json = df_pendientes.to_json(date_format="iso")
            cantidad = len(df_pendientes)

        equipos = [{"label": equipo, "value": equipo} for equipo in sorted(modelo["fuerza"].keys())]
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        return (
            pendientes_json,
            modelo,
            torneos,
            equipos,
            equipos,
            f"Actualizado {fecha} - {cantidad} partidos pendientes",
        )

    @app.callback(
        Output("g-pend", "figure"),
        Output("t-pend", "data"),
        Output("t-pend", "columns"),
        Input("store-pend", "data"),
        Input("filtro-torneo", "value"),
    )
    def pintar_pendientes(pendientes_json, torneo):
        if not pendientes_json or pendientes_json == "{}":
            return fig_pendientes(pd.DataFrame()), [], []

        df = pd.read_json(io.StringIO(pendientes_json))
        df["fecha"] = pd.to_datetime(df["fecha"])

        if torneo:
            df = df[df["torneo"] == torneo]

        tabla = preparar_tabla_pendientes(df)
        columnas = [{"name": columna, "id": columna} for columna in tabla.columns]
        return fig_pendientes(df), tabla.to_dict("records"), columnas

    @app.callback(
        Output("metric-box", "children"),
        Output("top5-box", "children"),
        Output("g-heat", "figure"),
        Output("g-total", "figure"),
        Input("store-modelo", "data"),
        Input("sel-local", "value"),
        Input("sel-visit", "value"),
    )
    def explorar(modelo, local, visitante):
        vacio = fig_vacia("Elige dos selecciones")
        placeholder = html.Div("Selecciona equipos para calcular marcadores.", className="empty-state")

        if not modelo or not local or not visitante or local == visitante:
            mensaje = html.Div(
                "Elige local y visitante para ver el analisis.",
                className="empty-state",
            )
            return mensaje, placeholder, vacio, vacio

        matriz, lambda_local, lambda_visitante = matriz_marcadores(
            modelo,
            local,
            visitante,
            neutral=True,
        )
        prob_local, prob_empate, prob_visitante = prob_1x2_de_matriz(matriz)
        prob_local, prob_empate, prob_visitante = mezclar_elo(
            modelo.get("elo", {}), local, visitante, prob_local, prob_empate, prob_visitante
        )
        goles = analizar_goles(matriz)

        metricas = html.Div(
            className="metrics",
            children=[
                metric_card(f"{prob_local:.0%}", f"Gana {local}", COLORS["local"]),
                metric_card(f"{prob_empate:.0%}", "Empate", COLORS["empate"]),
                metric_card(f"{prob_visitante:.0%}", f"Gana {visitante}", COLORS["visit"]),
                metric_card(f"{lambda_local:.2f}-{lambda_visitante:.2f}", "Goles esperados", COLORS["txt2"]),
                metric_card(f"{goles['o15']:.0%}", "Over 1.5", COLORS["accent2"]),
                metric_card(f"{goles['o25']:.0%}", "Over 2.5", COLORS["accent2"]),
                metric_card(f"{goles['o35']:.0%}", "Over 3.5", COLORS["accent2"]),
                metric_card(f"{goles['btts']:.0%}", "Ambos anotan", COLORS["accent2"]),
            ],
        )

        return (
            metricas,
            top5_marcadores(goles["top5"]),
            fig_heatmap(matriz, local, visitante),
            fig_total(goles["dist_total"]),
        )


def preparar_tabla_pendientes(df):
    """Transforma el DataFrame del modelo en columnas amigables para la tabla."""
    tabla = df.copy()
    tabla["Fecha"] = tabla["fecha"].dt.strftime("%d/%m")
    tabla["Partido"] = tabla["local"] + " vs " + tabla["visitante"]
    tabla["Local"] = porcentaje(tabla["prob_local"])
    tabla["Empate"] = porcentaje(tabla["prob_empate"])
    tabla["Visitante"] = porcentaje(tabla["prob_visitante"])
    tabla["Resultado prob."] = tabla["marcador"] + "  (" + porcentaje(tabla["p_marcador"]) + ")"
    tabla["Goles (L-V)"] = (
        tabla["goles_local"].map(lambda valor: f"{valor:.2f}")
        + "-"
        + tabla["goles_visit"].map(lambda valor: f"{valor:.2f}")
    )
    tabla["Over 1.5"] = porcentaje(tabla["o15"])
    tabla["Over 2.5"] = porcentaje(tabla["o25"])
    tabla["Ambos anotan"] = porcentaje(tabla["btts"])

    columnas = [
        "Fecha",
        "Partido",
        "Local",
        "Empate",
        "Visitante",
        "Resultado prob.",
        "Goles (L-V)",
        "Over 1.5",
        "Over 2.5",
        "Ambos anotan",
    ]
    return tabla[columnas]


def porcentaje(serie):
    return (serie * 100).round(0).astype(int).astype(str) + "%"
