# WorldCupPredicter

**Languages:** English | [Español](#español)

WorldCupPredicter is a visual tool for exploring probabilities in international football matches, with a focus on the road to the 2026 FIFA World Cup.

You can view the live application here: https://world-cup-predicter.vercel.app/

This project was created for learning purposes. Its main goal is to practice web development with Python, data visualization, and statistical modeling using real football data.

The application helps answer simple questions:

- Which national team is more likely to win?
- How likely is a draw?
- What are the most likely scorelines?
- How many goals are expected in a match?
- Which upcoming matches are listed by tournament?

It does not try to predict the future or guarantee results. Its purpose is to present a clear, easy-to-read statistical view based on historical data.

## What You Can See

### Upcoming Matches

The app shows a list of international matches that have not been played yet. You can filter by tournament and review:

- Home win probability.
- Draw probability.
- Away win probability.
- Most likely scoreline.
- Expected goals.
- Markets such as Over 1.5, Over 2.5, and both teams to score.

### Match Simulator

You can also select two national teams and compare their probabilities. The simulator shows:

- 1X2 probabilities.
- Expected goals for each team.
- Top 5 most likely exact scores.
- Exact score probability map.
- Total goals distribution.

## How To Read The Probabilities

A high probability does not mean a result is guaranteed. In football, even a favorite can lose or draw.

For example, if a team has a 55% chance of winning, the model sees it as the favorite, but it still leaves a combined 45% chance for other outcomes.

The predictions should be read as a comparative guide, not as certainty.

## Data Source

WorldCupPredicter uses publicly available historical results from the `international_results` project.

Those results are used to estimate trends such as attacking performance, defensive performance, tournament importance, historical form, and relative team strength.

## Model Approach

The project uses a combination of simple and interpretable statistical models. They were chosen because they make it easier to understand why predictions change from one match to another.

### Models Used

- **Poisson:** estimates how many goals each team may score. This is useful because goals are countable events: 0, 1, 2, 3, and so on.
- **Dixon-Coles adjustment:** improves low-score estimates such as 0-0, 1-0, 0-1, and 1-1, which are common in football.
- **Time weighting:** gives more importance to recent matches because national teams change over time.
- **Tournament weighting:** separates friendlies, qualifiers, and official tournaments because not every match has the same competitive value.
- **ELO rating:** represents historical relative team strength and complements win, draw, and loss probabilities.

### Variables Considered

The model considers variables such as:

- Recent historical results.
- Goals scored and conceded by each team.
- Attacking and defensive performance.
- Tournament type.
- Match date.
- Home, away, or neutral venue condition.
- Historical scoreline frequency.
- Low-score adjustments.
- Historical ELO-style team strength.

The final result is a statistical estimate presented visually.

## Use Of AI

During development, AI was used, specifically Codex, to help generate repetitive files, organize parts of the project, and speed up mechanical implementation tasks.

The goal was to use it as a learning and productivity tool, not as a replacement for project analysis. The main decisions about the approach, data, interface, and educational purpose were guided by the author.

## What It Is Useful For

WorldCupPredicter can be useful for:

- Analyzing matches before they are played.
- Comparing national teams quickly.
- Exploring possible scorelines.
- Understanding how probabilities change between teams.
- Reviewing goal trends in international football.

## Limitations

Football depends on many factors that a simple model cannot always capture, such as injuries, squad selection, rotations, weather, emotional context, coaching tactics, or last-minute changes.

For that reason, the predictions are only informative. They do not guarantee real results and should not be taken as financial advice or betting recommendations.

---

# Español

WorldCupPredicter es una herramienta visual para explorar probabilidades de partidos internacionales de fútbol, con enfoque en el camino hacia el Mundial 2026.

Puedes ver la aplicación en vivo aquí: https://world-cup-predicter.vercel.app/

Este proyecto fue creado con fines de aprendizaje. Su objetivo principal es practicar desarrollo web con Python, visualización de datos y modelos estadísticos aplicados a información real de fútbol.

La aplicación ayuda a responder preguntas simples:

- ¿Qué selección tiene más probabilidad de ganar?
- ¿Qué tan probable es un empate?
- ¿Cuáles son los marcadores más probables?
- ¿Cuántos goles se esperan en el partido?
- ¿Qué partidos pendientes hay por torneo?

No busca adivinar el futuro ni prometer resultados. Su objetivo es mostrar una lectura estadística clara, fácil de revisar y basada en datos históricos.

## Qué Puedes Ver

### Partidos Pendientes

La app muestra una lista de partidos internacionales que aún no se han jugado. Desde ahí puedes filtrar por torneo y revisar:

- Probabilidad de victoria del local.
- Probabilidad de empate.
- Probabilidad de victoria del visitante.
- Marcador más probable.
- Goles esperados.
- Probabilidades de mercados como Over 1.5, Over 2.5 y ambos equipos anotan.

### Simulador De Partido

También puedes elegir dos selecciones y comparar sus probabilidades. El simulador muestra:

- Probabilidades 1X2.
- Goles esperados para cada equipo.
- Top 5 de marcadores exactos más probables.
- Mapa de probabilidad por marcador.
- Distribución de goles totales.

## Cómo Interpretar Las Probabilidades

Una probabilidad alta no significa que un resultado sea seguro. En fútbol, incluso un equipo favorito puede perder o empatar.

Por ejemplo, si una selección aparece con 55% de probabilidad de ganar, significa que el modelo la ve como favorita, pero también reconoce un 45% combinado para otros resultados.

Las predicciones deben leerse como una guía comparativa, no como una certeza.

## Fuente De Datos

WorldCupPredicter usa resultados históricos de selecciones nacionales disponibles públicamente en el proyecto `international_results`.

Con esos datos se estiman tendencias como rendimiento ofensivo, rendimiento defensivo, importancia del torneo, forma histórica y fuerza relativa de cada selección.

## Enfoque Del Modelo

El proyecto usa una combinación de modelos estadísticos sencillos e interpretables. Se eligieron porque permiten explicar de forma clara por qué una predicción cambia entre un partido y otro.

### Modelos Usados

- **Poisson:** se usa para estimar cuántos goles puede anotar cada selección. Es útil porque los goles son eventos contables: 0, 1, 2, 3, etc.
- **Ajuste Dixon-Coles:** se usa para corregir marcadores bajos, como 0-0, 1-0, 0-1 y 1-1, que son muy comunes en fútbol.
- **Ponderación por tiempo:** da más importancia a partidos recientes, porque el nivel de una selección cambia con los años.
- **Ponderación por torneo:** diferencia partidos amistosos, eliminatorias y torneos oficiales, ya que no todos tienen el mismo peso competitivo.
- **Rating ELO:** ayuda a representar la fuerza histórica relativa de cada selección y complementa las probabilidades de victoria, empate y derrota.

### Variables Consideradas

El modelo toma en cuenta variables como:

- Resultados históricos recientes.
- Goles anotados y recibidos por cada selección.
- Rendimiento ofensivo y defensivo.
- Tipo de torneo.
- Fecha del partido.
- Condición de local, visitante o sede neutral.
- Frecuencia histórica de marcadores.
- Ajustes para marcadores bajos.
- Fuerza histórica tipo ELO.

El resultado final es una estimación estadística presentada de forma visual.

## Uso De Inteligencia Artificial

Durante el desarrollo se utilizó IA, específicamente Codex, como apoyo para generar archivos repetitivos, organizar partes del proyecto y acelerar tareas mecánicas de implementación.

El objetivo fue usarla como herramienta de aprendizaje y productividad, no como reemplazo del análisis del proyecto. Las decisiones principales sobre el enfoque, los datos, la interfaz y el propósito educativo del proyecto fueron guiadas por el autor.

## Para Qué Sirve

WorldCupPredicter puede servir para:

- Analizar partidos antes de que se jueguen.
- Comparar selecciones de forma rápida.
- Explorar posibles marcadores.
- Entender mejor cómo cambian las probabilidades entre equipos.
- Revisar tendencias de goles en partidos internacionales.

## Limitaciones

El fútbol depende de muchos factores que un modelo simple no siempre puede capturar, como lesiones, convocatorias, rotaciones, clima, contexto emocional, táctica del entrenador o cambios de último momento.

Por eso, las predicciones son solo orientativas. No garantizan resultados reales y no deben tomarse como consejo financiero ni como recomendación de apuesta.
