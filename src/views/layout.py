from dash import dash_table, dcc, html

from config import COLORS, INTERVALO_MS

INDEX_STRING = """
<!DOCTYPE html><html><head>{%metas%}<meta name="viewport" content="width=device-width, initial-scale=1"><title>{%title%}</title>{%favicon%}{%css%}
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f4f7fb;--surface:#ffffff;--surface-soft:#eef3f8;--text:#132238;
    --muted:#66758a;--line:#d8e1ec;--blue:#1d4ed8;--green:#047857;
    --indigo:#4f46e5;--shadow:0 12px 30px rgba(19,34,56,.07);
  }
  *{box-sizing:border-box;}
  html{min-height:100%;}
  body{
    margin:0;background:var(--bg);color:var(--text);
    font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;
  }
  button,input,.Select-control{font:inherit;}
  .app-shell{min-height:100vh;}
  .hero{background:var(--surface);border-bottom:1px solid var(--line);}
  .hero-inner{
    max-width:1180px;margin:0 auto;padding:30px 24px 24px;
    display:flex;align-items:flex-end;justify-content:space-between;gap:24px;
  }
  .brand-block{max-width:720px;}
  .eyebrow{
    margin:0 0 8px;color:var(--green);font-size:12px;font-weight:800;
    letter-spacing:.08em;text-transform:uppercase;
  }
  .hero h1{margin:0;font-size:32px;line-height:1.15;font-weight:800;color:var(--text);}
  .status-pill{
    margin:0;color:var(--muted);font-size:13px;line-height:1.4;
    background:var(--surface-soft);border:1px solid var(--line);border-radius:999px;
    padding:8px 12px;white-space:nowrap;
  }
  .wrap{max-width:1180px;margin:0 auto;padding:28px 24px 64px;}
  .card{padding:0 0 30px;margin-bottom:34px;border-bottom:1px solid var(--line);}
  .card:last-of-type{border-bottom:0;margin-bottom:18px;}
  .card h2{margin:0 0 6px;font-size:21px;line-height:1.25;font-weight:800;color:var(--text);}
  .card .sub{color:var(--muted);font-size:14px;line-height:1.55;margin:0 0 20px;max-width:760px;}
  label,.panel-title{
    font-size:12px;color:var(--muted);font-weight:800;display:block;margin-bottom:8px;
    letter-spacing:.04em;text-transform:uppercase;
  }
  .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;align-items:end;margin-bottom:18px;}
  .col{min-width:0;}
  .chart-shell,.table-shell,.analysis-panel{
    background:var(--surface);border:1px solid var(--line);border-radius:8px;box-shadow:var(--shadow);
  }
  .chart-shell{padding:8px 8px 2px;margin-bottom:18px;overflow:hidden;}
  .table-shell{overflow:hidden;}
  .metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;margin:20px 0 18px;}
  .metric{
    min-height:92px;background:var(--surface);border:1px solid var(--line);border-radius:8px;
    padding:15px 12px;text-align:left;display:flex;flex-direction:column;justify-content:center;
    box-shadow:0 8px 20px rgba(19,34,56,.045);
  }
  .metric-val{font-size:25px;font-weight:800;line-height:1.05;overflow-wrap:anywhere;}
  .metric-lbl{font-size:11px;color:var(--muted);margin-top:7px;text-transform:uppercase;letter-spacing:.04em;font-weight:700;}
  .grid3{display:grid;grid-template-columns:minmax(210px,.9fr) minmax(280px,1.35fr) minmax(260px,1fr);gap:16px;align-items:stretch;}
  .analysis-panel{padding:16px;min-width:0;overflow:hidden;}
  .analysis-panel .dash-graph{min-height:280px;}
  .score-list{display:flex;flex-direction:column;gap:8px;}
  .score-row{
    display:flex;justify-content:space-between;align-items:center;gap:12px;
    padding:10px 0;border-bottom:1px solid var(--line);
  }
  .score-row:last-child{border-bottom:0;}
  .score-row-primary{padding:10px 12px;border:1px solid #c9e5d9;background:#eef8f3;border-radius:8px;}
  .score-name{font-size:15px;font-weight:700;}
  .score-prob{font-size:13px;color:var(--muted);font-weight:700;}
  .empty-state{color:var(--muted);font-size:14px;padding:18px 0;}
  .disclaimer{color:#8795a8;font-size:12px;text-align:center;margin:22px 0 0;}
  .dash-graph{width:100%;}
  .Select-control,.Select-menu-outer,.VirtualizedSelectOption{
    background:#fff!important;color:var(--text)!important;border-color:var(--line)!important;}
  .Select-control{border-radius:8px!important;min-height:42px!important;box-shadow:none!important;}
  .is-focused:not(.is-open)>.Select-control{border-color:var(--blue)!important;box-shadow:0 0 0 3px rgba(29,78,216,.12)!important;}
  .Select-placeholder,.Select--single>.Select-control .Select-value{line-height:40px!important;}
  .Select-value-label,.Select-placeholder,.Select--single>.Select-control .Select-value{color:var(--text)!important;}
  .Select-menu-outer{border-radius:8px!important;box-shadow:0 18px 36px rgba(19,34,56,.14)!important;overflow:hidden!important;}
  .VirtualizedSelectFocusedOption{background:#eef3f8!important;}
  @media(max-width:980px){
    .grid3{grid-template-columns:1fr 1fr;}
    .grid3 .analysis-panel:first-child{grid-column:1/-1;}
  }
  @media(max-width:720px){
    .hero-inner{padding:24px 18px 20px;display:block;}
    .hero h1{font-size:27px;}
    .status-pill{display:inline-block;margin-top:14px;white-space:normal;}
    .wrap{padding:22px 18px 52px;}
    .card{margin-bottom:28px;padding-bottom:26px;}
    .grid3{grid-template-columns:1fr;}
    .metrics{grid-template-columns:repeat(2,minmax(0,1fr));}
  }
  @media(max-width:460px){
    .hero h1{font-size:24px;}
    .metrics{grid-template-columns:1fr;}
    .metric{min-height:82px;}
  }
</style></head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>
"""


def crear_layout():
    return html.Div(
        className="app-shell",
        children=[
            html.Div(
                className="hero",
                children=[
                    html.Div(
                        className="hero-inner",
                        children=[
                            html.Div(
                                className="brand-block",
                                children=[
                                    html.P("Mundial 2026", className="eyebrow"),
                                    html.H1("Predicciones de partidos internacionales"),
                                ],
                            ),
                            html.P(id="ultima-actualizacion", className="status-pill"),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="wrap",
                children=[
                    seccion_partidos_pendientes(),
                    seccion_simulador(),
                    html.P(
                        "Predicciones orientativas. No garantizan resultados reales.",
                        className="disclaimer",
                    ),
                ],
            ),
            dcc.Store(id="store-pend"),
            dcc.Store(id="store-modelo"),
            dcc.Interval(id="intervalo", interval=INTERVALO_MS, n_intervals=0),
        ],
    )


def seccion_partidos_pendientes():
    return html.Div(
        className="card",
        children=[
            html.H2("Partidos pendientes"),
            html.P(
                "Calendario internacional con probabilidades 1X2 y mercados de goles.",
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
                                persistence=True,
                            ),
                        ],
                    )
                ],
            ),
            dcc.Loading(
                type="dot",
                children=[
                    html.Div(
                        className="chart-shell",
                        children=dcc.Graph(
                            id="g-pend",
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ),
                    html.Div(className="table-shell", children=tabla_partidos_pendientes()),
                ],
            ),
        ],
    )


def tabla_partidos_pendientes():
    return dash_table.DataTable(
        id="t-pend",
        page_size=12,
        style_as_list_view=True,
        fill_width=True,
        style_table={
            "overflowX": "auto",
            "minWidth": "100%",
        },
        style_cell={
            "textAlign": "left",
            "padding": "10px 12px",
            "fontFamily": "Inter",
            "backgroundColor": COLORS["card"],
            "color": COLORS["txt"],
            "border": "none",
            "borderBottom": f"1px solid {COLORS['border']}",
            "fontSize": "13px",
            "minWidth": "110px",
            "width": "120px",
            "maxWidth": "220px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_header={
            "fontWeight": "700",
            "backgroundColor": COLORS["card2"],
            "color": COLORS["txt"],
            "border": "none",
            "borderBottom": f"1px solid {COLORS['border']}",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fbfdff",
            },
            {
                "if": {"column_id": "Partido"},
                "fontWeight": "700",
                "color": COLORS["txt"],
                "minWidth": "190px",
            },
            {
                "if": {"column_id": "Local"},
                "color": COLORS["local"],
                "fontWeight": "700",
            },
            {
                "if": {"column_id": "Empate"},
                "color": COLORS["empate"],
                "fontWeight": "700",
            },
            {
                "if": {"column_id": "Visitante"},
                "color": COLORS["visit"],
                "fontWeight": "700",
            },
        ],
    )


def seccion_simulador():
    return html.Div(
        className="card",
        children=[
            html.H2("Simulador de partido"),
            html.P(
                "Comparativa de selecciones, marcador probable y mercados principales.",
                className="sub",
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col",
                        children=[
                            html.Label("Local"),
                            dcc.Dropdown(id="sel-local", persistence=True),
                        ],
                    ),
                    html.Div(
                        className="col",
                        children=[
                            html.Label("Visitante"),
                            dcc.Dropdown(id="sel-visit", persistence=True),
                        ],
                    ),
                ],
            ),
            dcc.Loading(
                type="dot",
                children=[
                    html.Div(id="metric-box"),
                    html.Div(
                        className="grid3",
                        children=[
                            html.Div(
                                className="analysis-panel",
                                children=[
                                    html.Div("Marcadores mas probables", className="panel-title"),
                                    html.Div(id="top5-box"),
                                ],
                            ),
                            html.Div(
                                className="analysis-panel",
                                children=[
                                    html.Div("Marcador exacto (%)", className="panel-title"),
                                    dcc.Graph(
                                        id="g-heat",
                                        config={"displayModeBar": False, "responsive": True},
                                    ),
                                ],
                            ),
                            html.Div(
                                className="analysis-panel",
                                children=[
                                    html.Div("Total de goles", className="panel-title"),
                                    dcc.Graph(
                                        id="g-total",
                                        config={"displayModeBar": False, "responsive": True},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
