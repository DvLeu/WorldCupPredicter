# WorldCupPredicter

WorldCupPredicter es una herramienta visual para explorar probabilidades de partidos internacionales de fútbol, con enfoque en el camino hacia el Mundial 2026.

Este proyecto fue creado con fines de aprendizaje. Su objetivo principal es practicar desarrollo web con Python, visualización de datos y modelos estadísticos aplicados a información real de fútbol.

La aplicación ayuda a responder preguntas simples:

- ¿Qué selección tiene más probabilidad de ganar?
- ¿Qué tan probable es un empate?
- ¿Cuáles son los marcadores más probables?
- ¿Cuántos goles se esperan en el partido?
- ¿Qué partidos pendientes hay por torneo?

No busca adivinar el futuro ni prometer resultados. Su objetivo es mostrar una lectura estadística clara, fácil de revisar y basada en datos históricos.

## Qué puedes ver

### Partidos pendientes

La app muestra una lista de partidos internacionales que aún no se han jugado. Desde ahí puedes filtrar por torneo y revisar:

- Probabilidad de victoria del local.
- Probabilidad de empate.
- Probabilidad de victoria del visitante.
- Marcador más probable.
- Goles esperados.
- Probabilidades de mercados como Over 1.5, Over 2.5 y ambos equipos anotan.

### Simulador de partido

También puedes elegir dos selecciones y comparar sus probabilidades. El simulador muestra:

- Probabilidades 1X2.
- Goles esperados para cada equipo.
- Top 5 de marcadores exactos más probables.
- Mapa de probabilidad por marcador.
- Distribución de goles totales.

## Cómo interpretar las probabilidades

Una probabilidad alta no significa que un resultado sea seguro. En fútbol, incluso un equipo favorito puede perder o empatar.

Por ejemplo, si una selección aparece con 55% de probabilidad de ganar, significa que el modelo la ve como favorita, pero también reconoce un 45% combinado para otros resultados.

Las predicciones deben leerse como una guía comparativa, no como una certeza.

## De dónde salen los datos

WorldCupPredicter usa resultados históricos de selecciones nacionales disponibles públicamente en el proyecto `international_results`.

Con esos datos se estiman tendencias como rendimiento ofensivo, rendimiento defensivo, importancia del torneo, forma histórica y fuerza relativa de cada selección.

## Qué toma en cuenta el modelo

El proyecto usa una combinación de modelos estadísticos sencillos e interpretables. Se eligieron porque permiten explicar de forma clara por qué una predicción cambia entre un partido y otro.

### Modelos usados

- **Poisson:** se usa para estimar cuántos goles puede anotar cada selección. Es útil porque los goles son eventos contables: 0, 1, 2, 3, etc.
- **Ajuste Dixon-Coles:** se usa para corregir marcadores bajos, como 0-0, 1-0, 0-1 y 1-1, que son muy comunes en fútbol.
- **Ponderación por tiempo:** da más importancia a partidos recientes, porque el nivel de una selección cambia con los años.
- **Ponderación por torneo:** diferencia partidos amistosos, eliminatorias y torneos oficiales, ya que no todos tienen el mismo peso competitivo.
- **Rating ELO:** ayuda a representar la fuerza histórica relativa de cada selección y complementa las probabilidades de victoria, empate y derrota.

### Variables consideradas

El modelo toma en cuenta variables como:

- Resultados históricos recientes.
- Goles anotados y recibidos por cada selección.
- Rendimiento ofensivo y defensivo.
- Tipo de torneo.
- Fecha del partido.
- Condición de local, visitante o sede neutral.
- Fuerza ofensiva y defensiva de cada selección.
- Frecuencia histórica de marcadores.
- Ajustes para marcadores bajos, comunes en fútbol.
- Rating histórico tipo ELO para complementar la fuerza de los equipos.

El resultado final es una estimación estadística presentada de forma visual.

## Uso de inteligencia artificial

Durante el desarrollo se utilizó IA, específicamente Codex, como apoyo para generar archivos repetitivos, organizar partes del proyecto y acelerar tareas mecánicas de implementación.

El objetivo fue usarla como herramienta de aprendizaje y productividad, no como reemplazo del análisis del proyecto. Las decisiones principales sobre el enfoque, los datos, la interfaz y el propósito educativo del proyecto fueron guiadas por el autor.

## Para qué sirve

WorldCupPredicter puede servir para:

- Analizar partidos antes de que se jueguen.
- Comparar selecciones de forma rápida.
- Explorar posibles marcadores.
- Entender mejor cómo cambian las probabilidades entre equipos.
- Revisar tendencias de goles en partidos internacionales.

## Limitaciones

El fútbol depende de muchos factores que un modelo simple no siempre puede capturar, como lesiones, convocatorias, rotaciones, clima, contexto emocional, táctica del entrenador o cambios de último momento.

Por eso, las predicciones son solo orientativas. No garantizan resultados reales y no deben tomarse como consejo financiero ni como recomendación de apuesta.
