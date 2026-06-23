"""
Mundial 2026 - probabilidades y parlays.
"""

from dash import Dash

from controllers.callbacks import registrar_callbacks
from views.layout import INDEX_STRING, crear_layout


def crear_app():
    app = Dash(__name__)
    app.title = "Mundial 2026 - Predictor"
    app.index_string = INDEX_STRING
    app.layout = crear_layout()

    registrar_callbacks(app)
    return app


app = crear_app()


if __name__ == "__main__":
    app.run(debug=True)
