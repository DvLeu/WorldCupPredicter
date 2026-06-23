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

COLORS = {
    "bg": "#f8fafc",
    "card": "#ffffff",
    "card2": "#f1f5f9",
    "txt": "#0f172a",
    "txt2": "#64748b",
    "border": "#e2e8f0",
    "local": "#2563eb",
    "empate": "#64748b",
    "visit": "#ea580c",
    "accent": "#16a34a",
    "accent2": "#7c3aed",
}

PLOTLY_BASE = {
    "template": "plotly_white",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": COLORS["txt"], "family": "Inter"},
}
