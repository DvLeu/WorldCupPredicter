# WorldCupPredicter

Aplicacion web sencilla para consultar probabilidades de partidos de futbol internacional.  
El proyecto esta pensado para el Mundial 2026 y permite revisar partidos pendientes, probabilidades 1X2, marcadores probables y mercados de goles.

Este proyecto tambien fue hecho como parte de aprendizaje, para practicar Python, Dash, organizacion de codigo con MVC y uso de modelos estadisticos aplicados a datos reales.

## Que se uso

- Python
- Dash
- Plotly
- Pandas
- NumPy
- SciPy
- Requests

Los datos se descargan desde este repositorio publico:

```text
https://github.com/martj42/international_results
```

## Como funciona

La app descarga resultados historicos de selecciones nacionales y entrena un modelo estadistico.

## Modelos usados

Se usaron modelos estadisticos sencillos, pero utiles para este tipo de problema.

### Modelo Poisson

El modelo principal usa distribucion de Poisson.

Se uso porque en futbol los goles son eventos contables: 0, 1, 2, 3, etc. Poisson es una forma comun de estimar la probabilidad de que un equipo anote cierta cantidad de goles.

Con este modelo se calculan probabilidades como:

- Probabilidad de que el local meta 0 goles.
- Probabilidad de que el visitante meta 2 goles.
- Probabilidad de marcadores como 1-0, 1-1 o 2-1.

### Ajuste Dixon-Coles

Tambien se uso un ajuste Dixon-Coles.

Se uso porque el modelo Poisson simple puede fallar un poco en marcadores bajos, especialmente 0-0, 1-0, 0-1 y 1-1. Dixon-Coles ayuda a corregir esas probabilidades para que sean mas realistas.

### Ponderacion por tiempo y torneo

Ademas, se agrego peso a los partidos segun dos ideas:

- Los partidos recientes importan mas que partidos muy antiguos.
- Los partidos oficiales importan mas que los amistosos.

Esto se hizo porque el nivel de una seleccion cambia con el tiempo, y no todos los partidos tienen la misma importancia competitiva.

Con eso se calculan:

- Probabilidad de que gane el local.
- Probabilidad de empate.
- Probabilidad de que gane el visitante.
- Marcador mas probable.
- Goles esperados.
- Over 1.5, Over 2.5 y Over 3.5.
- Ambos equipos anotan.

## Estructura del proyecto

El proyecto esta separado usando una arquitectura MVC sencilla:

```text
src/
  app.py
  config.py
  controllers/
    callbacks.py
  models/
    predictor.py
  views/
    layout.py
    figures.py
    components.py
```

## Partes principales

`src/app.py`  
Es el archivo principal. Crea la aplicacion Dash, carga el layout y registra los callbacks.

`src/config.py`  
Tiene la configuracion general, como la URL de datos, constantes del modelo y colores.

`src/models/predictor.py`  
Contiene la parte estadistica del proyecto. Aqui se descargan los datos, se entrena el modelo y se calculan las probabilidades.

`src/views/layout.py`  
Define la estructura visual de la pagina.

`src/views/figures.py`  
Tiene las graficas hechas con Plotly.

`src/views/components.py`  
Tiene componentes visuales reutilizables, como tarjetas de metricas.

`src/controllers/callbacks.py`  
Conecta la interfaz con el modelo. Aqui estan los callbacks de Dash.

## Instalacion

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install dash plotly pandas numpy scipy requests
```

## Como ejecutar

Desde la raiz del proyecto:

```bash
python src/app.py
```

Despues abrir en el navegador:

```text
http://127.0.0.1:8050
```

## Despliegue en Vercel

El proyecto incluye estos archivos para poder desplegarlo en Vercel:

- `requirements.txt`: lista las librerias que Vercel debe instalar.
- `vercel.json`: indica que la app se ejecuta con Python.
- `api/index.py`: punto de entrada que conecta Vercel con la app Dash.

Pasos:

1. Subir el proyecto a GitHub.
2. En Vercel, elegir `New Project`.
3. Importar el repositorio.
4. En `Application Preset`, seleccionar `Other`.
5. Dejar `Root Directory` como `./`.
6. No es necesario agregar comandos de build.
7. Presionar `Deploy`.

Si Vercel pide configuracion manual:

```text
Framework Preset: Other
Root Directory: ./
Build Command: vacio
Output Directory: vacio
Install Command: pip install -r requirements.txt
```

Nota: Dash funciona mejor en servidores Python tradicionales como Render, Railway o PythonAnywhere. Vercel puede servir para una prueba sencilla, pero si la app crece o tarda mucho entrenando el modelo, conviene moverla a una plataforma pensada para apps Python persistentes.

## Uso

1. Abrir la aplicacion.
2. Esperar a que carguen los datos.
3. Revisar la seccion de partidos pendientes.
4. Usar el filtro por torneo si se quiere ver una competencia especifica.
5. En el simulador, seleccionar local y visitante.
6. La app muestra las probabilidades, marcadores y graficas.

## Nota

Las predicciones son solo orientativas.  
No son consejo financiero ni aseguran resultados reales.
