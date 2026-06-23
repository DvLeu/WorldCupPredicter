from dash import dash_table, dcc, html

from config import COLORS, INTERVALO_MS

INDEX_STRING = """
<!DOCTYPE html><html><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  body{margin:0;background:#f8fafc;color:#0f172a;font-family:Inter,system-ui,sans-serif;}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px 60px;}
  .hero{background:linear-gradient(120deg,#1e3a8a 0%,#6d28d9 60%,#22c55e 140%);
        padding:34px 20px;text-align:center;margin-bottom:26px;}
  .hero h1{margin:0;font-size:30px;font-weight:800;color:#fff;}
  .hero p{margin:6px 0 0;color:#dbeafe;font-size:14px;}
  .card{background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;
        padding:22px;margin-bottom:22px;box-shadow:0 2px 12px rgba(0,0,0,.06);}
  .card h2{margin:0 0 4px;font-size:19px;font-weight:700;color:#0f172a;}
  .card .sub{color:#64748b;font-size:13px;margin:0 0 18px;}
  label{font-size:13px;color:#64748b;font-weight:500;display:block;margin-bottom:6px;}
  .row{display:flex;gap:16px;flex-wrap:wrap;align-items:end;}
  .col{flex:1;min-width:200px;}
  .metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(135px,1fr));
           gap:12px;margin:6px 0 18px;}
  .metric{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;
          padding:14px 12px;text-align:center;}
  .metric-val{font-size:24px;font-weight:800;line-height:1.1;}
  .metric-lbl{font-size:11px;color:#64748b;margin-top:5px;text-transform:uppercase;
              letter-spacing:.4px;}
  .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;}
  @media(max-width:900px){.grid3{grid-template-columns:1fr 1fr;}}
  @media(max-width:760px){.grid3{grid-template-columns:1fr;}}
  .disclaimer{color:#94a3b8;font-size:12px;text-align:center;margin-top:8px;}
  .Select-control,.Select-menu-outer,.VirtualizedSelectOption{
    background:#fff!important;color:#0f172a!important;border-color:#e2e8f0!important;}
  .Select-value-label,.Select-placeholder,.Select--single>.Select-control .Select-value{color:#0f172a!important;}
  .VirtualizedSelectFocusedOption{background:#f1f5f9!important;}
</style></head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>
"""


def crear_layout():
    return html.Div(
        [
            html.Div(
                className="hero",
                children=[
                    html.H1("Parlay Builder - Dvleu"),
                    html.P(id="ultima-actualizacion"),
                ],
            ),
            html.Div(
                className="wrap",
                children=[
                    seccion_partidos_pendientes(),
                    seccion_simulador(),
                    html.P(
                        "Solo orientativo - no es consejo financiero.",
                        className="disclaimer",
                    ),
                ],
            ),
            dcc.Store(id="store-pend"),
            dcc.Store(id="store-modelo"),
            dcc.Interval(id="intervalo", interval=INTERVALO_MS, n_intervals=0),
        ]
    )


def seccion_partidos_pendientes():
    return html.Div(
        className="card",
        children=[
            html.H2("Partidos no se han jugado"),
            html.P(
                "Probabilidades 1X2 y mercados de goles. Filtra por torneo para ver solo los que te interesan.",
                className="sub",
            ),
            html.Div(
                className="row",
                style={"marginBottom": "10px"},
                children=[
                    html.Div(
                        className="col",
                        children=[
                            html.Label("Filtrar por torneo"),
                            dcc.Dropdown(
                                id="filtro-torneo",
                                placeholder="Todos",
                                clearable=True,
                            ),
                        ],
                    )
                ],
            ),
            dcc.Graph(id="g-pend", config={"displayModeBar": False}),
            tabla_partidos_pendientes(),
        ],
    )


def tabla_partidos_pendientes():
    return dash_table.DataTable(
        id="t-pend",
        page_size=12,
        style_as_list_view=True,
        style_cell={
            "textAlign": "left",
            "padding": "10px 12px",
            "fontFamily": "Inter",
            "backgroundColor": COLORS["card"],
            "color": COLORS["txt"],
            "border": "none",
            "borderBottom": f"1px solid {COLORS['border']}",
            "fontSize": "13px",
        },
        style_header={
            "fontWeight": "700",
            "backgroundColor": COLORS["card2"],
            "color": COLORS["txt"],
            "border": "none",
            "borderBottom": f"1px solid {COLORS['border']}",
        },
    )


def seccion_simulador():
    return html.Div(
        className="card",
        children=[
            html.H2("Simulador de partido"),
            html.P(
                "Elige dos selecciones y ve como queda el analisis: quien gana, que marcador esperar y si conviene Over o BTTS.",
                className="sub",
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col",
                        children=[html.Label("Local"), dcc.Dropdown(id="sel-local")],
                    ),
                    html.Div(
                        className="col",
                        children=[html.Label("Visitante"), dcc.Dropdown(id="sel-visit")],
                    ),
                ],
            ),
            html.Div(id="metric-box"),
            html.Div(
                className="grid3",
                children=[
                    html.Div([html.Label("Marcadores mas probables"), html.Div(id="top5-box")]),
                    html.Div(
                        [
                            html.Label("Probabilidad por marcador exacto (%)"),
                            dcc.Graph(id="g-heat", config={"displayModeBar": False}),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Cuantos goles en total"),
                            dcc.Graph(id="g-total", config={"displayModeBar": False}),
                        ]
                    ),
                ],
            ),
        ],
    )
