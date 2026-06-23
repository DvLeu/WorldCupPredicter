"""
Configuracion general de la aplicacion.
"""

RAW_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

ANIOS_HISTORIAL = 10
HALF_LIFE_ANIOS = 2.5
SHRINKAGE = 10
RHO = 0.10
INTERVALO_MS = 300_000
MAX_G = 10
ELO_K = 40
ELO_PESO = 0.45

COLORS = {
    "bg": "#f4f7fb",
    "card": "#ffffff",
    "card2": "#eef3f8",
    "txt": "#132238",
    "txt2": "#66758a",
    "border": "#d8e1ec",
    "local": "#1d4ed8",
    "empate": "#6b7280",
    "visit": "#b45309",
    "accent": "#047857",
    "accent2": "#4f46e5",
}

PLOTLY_BASE = {
    "template": "plotly_white",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": COLORS["txt"], "family": "Inter"},
}
