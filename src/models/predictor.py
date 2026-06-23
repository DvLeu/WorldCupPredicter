import io
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from scipy.stats import poisson

from config import (
    ANIOS_HISTORIAL,
    ELO_K,
    ELO_PESO,
    HALF_LIFE_ANIOS,
    MAX_G,
    RAW_URL,
    RHO,
    SHRINKAGE,
)


def peso_torneo(nombre):
    """Da mas peso a partidos competitivos que a amistosos."""
    nombre = str(nombre).lower()

    if "friendly" in nombre:
        return 0.35
    if "world cup" in nombre and "qualif" in nombre:
        return 1.4
    if "world cup" in nombre:
        return 1.6
    if any(
        palabra in nombre
        for palabra in (
            "nations league",
            "copa",
            "euro",
            "africa cup",
            "asian cup",
            "gold cup",
            "continental",
        )
    ):
        return 1.2

    return 1.0


def dc_tau(goles_local, goles_visitante, lambda_local, lambda_visitante):
    """Correccion Dixon-Coles para marcadores bajos."""
    if goles_local == 0 and goles_visitante == 0:
        return max(0.01, 1 - lambda_local * lambda_visitante * RHO)
    if goles_local == 1 and goles_visitante == 0:
        return 1 + lambda_visitante * RHO
    if goles_local == 0 and goles_visitante == 1:
        return 1 + lambda_local * RHO
    if goles_local == 1 and goles_visitante == 1:
        return max(0.01, 1 - RHO)

    return 1.0


def matriz_marcadores(modelo, local, visitante, neutral=True, max_goles=MAX_G):
    """Crea la matriz de probabilidades de todos los marcadores posibles."""
    fuerzas = modelo["fuerza"]
    fuerza_local = fuerzas[local]
    fuerza_visitante = fuerzas[visitante]

    if neutral:
        base_local = modelo["liga_avg"]
        base_visitante = modelo["liga_avg"]
    else:
        base_local = modelo["liga_home"]
        base_visitante = modelo["liga_away"]

    lambda_local = fuerza_local["attack"] * fuerza_visitante["defense"] * base_local
    lambda_visitante = fuerza_visitante["attack"] * fuerza_local["defense"] * base_visitante

    prob_local = poisson.pmf(np.arange(max_goles + 1), lambda_local)
    prob_visitante = poisson.pmf(np.arange(max_goles + 1), lambda_visitante)
    matriz = np.outer(prob_local, prob_visitante)

    for goles_local in range(2):
        for goles_visitante in range(2):
            matriz[goles_local, goles_visitante] *= dc_tau(
                goles_local,
                goles_visitante,
                lambda_local,
                lambda_visitante,
            )

    matriz /= matriz.sum()
    return matriz, lambda_local, lambda_visitante


def prob_1x2_de_matriz(matriz):
    """Devuelve probabilidades de local, empate y visitante."""
    gana_local = float(np.tril(matriz, -1).sum())
    empate = float(np.trace(matriz))
    gana_visitante = float(np.triu(matriz, 1).sum())
    return gana_local, empate, gana_visitante


def analizar_goles(matriz, max_goles=MAX_G):
    """Resume mercados de goles y marcadores mas probables."""
    mejor_local, mejor_visitante = np.unravel_index(matriz.argmax(), matriz.shape)

    total_goles = np.zeros(2 * max_goles + 1)
    for goles_local in range(max_goles + 1):
        for goles_visitante in range(max_goles + 1):
            total_goles[goles_local + goles_visitante] += matriz[goles_local, goles_visitante]

    total_mas_probable = int(total_goles.argmax())

    def over(linea):
        return float(sum(prob for goles, prob in enumerate(total_goles) if goles > linea))

    ambos_anotan = float(matriz[1:, 1:].sum())
    marcadores = [
        ((goles_local, goles_visitante), matriz[goles_local, goles_visitante])
        for goles_local in range(max_goles + 1)
        for goles_visitante in range(max_goles + 1)
    ]
    top5 = sorted(marcadores, key=lambda item: -item[1])[:5]

    return {
        "marcador": f"{mejor_local}-{mejor_visitante}",
        "p_marcador": float(matriz[mejor_local, mejor_visitante]),
        "total": total_mas_probable,
        "p_total": float(total_goles[total_mas_probable]),
        "o15": over(1.5),
        "o25": over(2.5),
        "o35": over(3.5),
        "btts": ambos_anotan,
        "top5": [(f"{local}-{visitante}", float(prob)) for (local, visitante), prob in top5],
        "dist_total": total_goles,
    }


def calcular_elo(df_jugados):
    """Calcula ELO iterativo para todos los equipos usando el historial completo."""
    elo = {}
    for _, p in df_jugados.sort_values("date").iterrows():
        local = p["home_team"]
        visit = p["away_team"]
        k = ELO_K * peso_torneo(p["tournament"])

        e_l = elo.get(local, 1000.0)
        e_v = elo.get(visit, 1000.0)
        p_l = 1.0 / (1.0 + 10.0 ** ((e_v - e_l) / 400.0))

        gd = abs(p["home_score"] - p["away_score"])
        mult = 1.0 if gd <= 1 else (1.5 if gd == 2 else (1.75 + max(0, gd - 3) / 8.0))

        if p["home_score"] > p["away_score"]:
            s_l = 1.0
        elif p["home_score"] == p["away_score"]:
            s_l = 0.5
        else:
            s_l = 0.0

        delta = k * mult * (s_l - p_l)
        elo[local] = e_l + delta
        elo[visit] = e_v - delta

    return elo


def mezclar_elo(elo, local, visitante, p_local_dc, p_draw_dc, p_visit_dc):
    """Mezcla probabilidades Dixon-Coles con probabilidad ELO.

    Usa el score esperado ELO para descomponer win/loss, manteniendo
    el empate del modelo DC como ancla estructural.
    """
    if not elo or local not in elo or visitante not in elo:
        return p_local_dc, p_draw_dc, p_visit_dc

    e_local = 1.0 / (1.0 + 10.0 ** ((elo[visitante] - elo[local]) / 400.0))

    # Descomponer score ELO en win/draw/loss usando DC draw como ancla
    p_win_elo = max(0.0, e_local - 0.5 * p_draw_dc)
    p_loss_elo = max(0.0, (1.0 - e_local) - 0.5 * p_draw_dc)
    p_draw_elo = 1.0 - p_win_elo - p_loss_elo

    p_l = (1 - ELO_PESO) * p_local_dc + ELO_PESO * p_win_elo
    p_d = (1 - ELO_PESO) * p_draw_dc + ELO_PESO * p_draw_elo
    p_v = (1 - ELO_PESO) * p_visit_dc + ELO_PESO * p_loss_elo

    total = p_l + p_d + p_v
    return p_l / total, p_d / total, p_v / total


def cargar_y_entrenar():
    """Descarga datos historicos, entrena el modelo y predice partidos pendientes."""
    url = f"{RAW_URL}?t={int(datetime.now().timestamp())}"
    respuesta = requests.get(url, timeout=20)
    respuesta.raise_for_status()

    df = pd.read_csv(io.StringIO(respuesta.text))
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    jugados = df[df["home_score"].notna()].copy()
    jugados["home_score"] = jugados["home_score"].astype(float)
    jugados["away_score"] = jugados["away_score"].astype(float)

    fecha_mas_reciente = df["date"].max()
    entrenamiento = jugados[
        jugados["date"] >= fecha_mas_reciente - pd.Timedelta(days=365 * ANIOS_HISTORIAL)
    ].copy()
    entrenamiento["w"] = (
        0.5
        ** (
            (fecha_mas_reciente - entrenamiento["date"]).dt.days
            / (365 * HALF_LIFE_ANIOS)
        )
        * entrenamiento["tournament"].map(peso_torneo).fillna(1.0)
    )

    no_neutrales = entrenamiento[entrenamiento["neutral"] == False]
    liga_home = float(np.average(no_neutrales["home_score"], weights=no_neutrales["w"]))
    liga_away = float(np.average(no_neutrales["away_score"], weights=no_neutrales["w"]))
    liga_avg = float(
        np.average(
            pd.concat([entrenamiento["home_score"], entrenamiento["away_score"]]),
            weights=pd.concat([entrenamiento["w"], entrenamiento["w"]]),
        )
    )

    local = entrenamiento[["home_team", "home_score", "away_score", "w"]].rename(
        columns={"home_team": "team", "home_score": "gf", "away_score": "ga"}
    )
    visitante = entrenamiento[["away_team", "away_score", "home_score", "w"]].rename(
        columns={"away_team": "team", "away_score": "gf", "home_score": "ga"}
    )

    equipos = pd.concat([local, visitante], ignore_index=True)
    equipos["gfw"] = equipos["gf"] * equipos["w"]
    equipos["gaw"] = equipos["ga"] * equipos["w"]

    resumen = (
        equipos.groupby("team")
        .agg(gfw=("gfw", "sum"), gaw=("gaw", "sum"), n=("w", "sum"))
        .reset_index()
    )
    resumen["gf"] = resumen["gfw"] / resumen["n"]
    resumen["ga"] = resumen["gaw"] / resumen["n"]

    k = SHRINKAGE
    resumen["attack"] = (
        (resumen["gf"] * resumen["n"] + liga_avg * k) / (resumen["n"] + k)
    ) / liga_avg
    resumen["defense"] = (
        (resumen["ga"] * resumen["n"] + liga_avg * k) / (resumen["n"] + k)
    ) / liga_avg

    fuerza = resumen.set_index("team")[["attack", "defense"]].to_dict("index")
    elo = calcular_elo(jugados)
    modelo = {
        "fuerza": fuerza,
        "liga_avg": liga_avg,
        "liga_home": liga_home,
        "liga_away": liga_away,
        "elo": elo,
    }

    pendientes = df[df["home_score"].isna()].copy()
    predicciones = []

    for _, partido in pendientes.iterrows():
        local = partido["home_team"]
        visitante = partido["away_team"]

        if local not in fuerza or visitante not in fuerza:
            continue

        matriz, lambda_local, lambda_visitante = matriz_marcadores(
            modelo,
            local,
            visitante,
            bool(partido["neutral"]),
        )
        prob_local, prob_empate, prob_visitante = prob_1x2_de_matriz(matriz)
        prob_local, prob_empate, prob_visitante = mezclar_elo(
            elo, local, visitante, prob_local, prob_empate, prob_visitante
        )
        goles = analizar_goles(matriz)

        predicciones.append(
            {
                "fecha": partido["date"],
                "torneo": partido["tournament"],
                "local": local,
                "visitante": visitante,
                "sede": partido.get("city", ""),
                "prob_local": prob_local,
                "prob_empate": prob_empate,
                "prob_visitante": prob_visitante,
                "marcador": goles["marcador"],
                "p_marcador": goles["p_marcador"],
                "total": goles["total"],
                "goles_local": float(f"{lambda_local:.2f}"),
                "goles_visit": float(f"{lambda_visitante:.2f}"),
                "o15": goles["o15"],
                "o25": goles["o25"],
                "o35": goles["o35"],
                "btts": goles["btts"],
            }
        )

    df_pendientes = pd.DataFrame(predicciones)
    if not df_pendientes.empty:
        df_pendientes = df_pendientes.sort_values("fecha")

    return df_pendientes, modelo
