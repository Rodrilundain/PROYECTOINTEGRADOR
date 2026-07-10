# Sistema de análisis de evaluaciones emocionales a partir de registros afectivos

**Documentación final del proyecto integrador**

- **Integrantes:** [Nombre del integrante 1], [Nombre del integrante 2], [Nombre del integrante 3]
- **Curso:** [Completar curso]
- **Docente:** [Completar docente]
- **Fecha:** [Completar fecha de entrega]

---

## 2. Descripción general del problema

El proyecto aborda el problema de interpretar el estado emocional de un grupo de estudiantes a partir de registros afectivos que ellos mismos (o el sistema que los captura) generan durante distintas actividades de un curso: prácticas de laboratorio, entregas virtuales, trabajos en equipo, evaluaciones, foros, consultas al docente, etc.

**Qué datos se reciben:** por un lado, información estructural que ya existe en una base de datos relacional (quiénes son los usuarios, en qué contextos/actividades participan y qué rangos definen cada emoción); por otro lado, un archivo CSV (`registros_afectivos.csv`) con los registros afectivos "crudos": para cada evento se recibe un identificador de usuario, un identificador de contexto, una fecha y hora, y dos valores numéricos —**valencia** y **activación**— además de un comentario libre opcional. Estos valores numéricos no traen ninguna interpretación: son solo números entre -1 y 1.

**Qué se espera obtener como resultado:** un archivo final (`evaluaciones_emocionales_extendidas.csv`) donde cada registro afectivo válido queda enriquecido con el nombre, la edad y el género del usuario, los datos del contexto (origen, actividad, ubicación, descripción) y, sobre todo, con la **interpretación emocional** calculada por el sistema: intensidad, intensidad normalizada, cuadrante emocional y una etiqueta con nombre (por ejemplo "Entusiasta", "Frustrado", "Neutro"). A partir de ese archivo se generan análisis agregados (por usuario, por contexto, por etiqueta) y gráficos.

**Para qué podría servir el sistema:** para que un docente o un equipo de seguimiento académico pueda detectar, sin leer registro por registro, en qué actividades los estudiantes tienden a sentirse más frustrados o más entusiasmados, qué estudiantes muestran mayor variabilidad emocional (posible señal de alerta) y cómo evoluciona el clima emocional del curso a lo largo del tiempo. No reemplaza el criterio docente, pero da una lectura cuantitativa que sería muy difícil de obtener a simple vista sobre miles de registros.

---

## 3. Descripción del dataset

### 3.1. Base de datos

La base de datos (`dataset/base de datos.sql`, cargada por el programa como `proyectointegrador`) contiene tres tablas que el programa utiliza como catálogos de referencia, más una cuarta tabla (`registros_afectivos`) que define la estructura de los registros afectivos a nivel de base de datos, aunque en la práctica el flujo del programa los recibe desde el CSV.

| Tabla | Campos principales | Clave primaria | Finalidad |
|---|---|---|---|
| `usuarios` | `id_usuario`, `nombre`, `edad` (12 a 100), `genero` | `id_usuario` | Identificar a la persona que generó cada registro afectivo y permitir análisis agrupados por usuario (emoción predominante, variabilidad emocional). Contiene 30 usuarios cargados. |
| `contextos` | `id_contexto`, `origen`, `actividad`, `ubicacion`, `descripcion` | `id_contexto` | Describir la situación académica en la que ocurrió el registro (por ejemplo "Aplicación educativa – Ejercicio de bucles – Laboratorio de informática"), para poder analizar qué contextos generan qué emociones. Contiene 45 contextos cargados (de los cuales el dataset de registros afectivos utiliza 12). |
| `etiquetas_emocionales` | `id_etiqueta`, `nombre_etiqueta`, `valencia_min`, `valencia_max`, `activacion_min`, `activacion_max`, `cuadrante` | `id_etiqueta` | Definir los rangos de valencia y activación que determinan a qué emoción corresponde un registro. Contiene 8 etiquetas: Entusiasta, Calmo, Frustrado, Triste, Tenso, Alerta, Neutro y Cansado. |
| `registros_afectivos` | `id_registro`, `id_usuario` (FK), `id_contexto` (FK), `fecha_hora`, `valencia`, `activacion`, `comentario` | `id_registro` | Modela en la base los registros afectivos individuales, con claves foráneas hacia `usuarios` y `contextos` y restricciones `CHECK` de rango (-1.00 a 1.00) sobre valencia y activación. |

### 3.2. Archivo CSV

El archivo `dataset/registros_afectivos.csv` contiene **6.054 registros** (sin contar el encabezado). Sus campos principales son:

| Campo | Descripción |
|---|---|
| `id_registro` | Identificador único del registro afectivo. |
| `id_usuario` | Referencia al usuario que generó el registro (debería existir en la tabla `usuarios`). |
| `id_contexto` | Referencia al contexto/actividad en la que ocurrió el registro (debería existir en la tabla `contextos`). |
| `fecha_hora` | Fecha y hora en que se generó el registro. |
| `valencia` | Valor numérico entre -1.00 y 1.00 que indica si la emoción es negativa o positiva. |
| `activacion` | Valor numérico entre -1.00 y 1.00 que indica el nivel de energía/activación de la emoción. |
| `comentario` | Texto libre opcional escrito por el usuario. |

Este archivo llega con datos "sucios" a propósito: valores no numéricos en `valencia`/`activacion` (por ejemplo `"sin_dato"`, `"alto"`, `"bajo"`), valores fuera de rango, fechas vacías, filas con `id_registro` repetido y comentarios con codificación irregular (se detectaron caracteres mal decodificados típicos de archivos guardados en `latin-1`).

---

## 4. Modelo de datos

### MER (resumen textual)

```
USUARIOS (id_usuario, nombre, edad, genero)
        1
        |
        | genera
        N
REGISTROS_AFECTIVOS (id_registro, id_usuario FK, id_contexto FK, fecha_hora, valencia, activacion, comentario)
        N
        |
        | ocurre_en
        1
CONTEXTOS (id_contexto, origen, actividad, ubicacion, descripcion)

ETIQUETAS_EMOCIONALES (id_etiqueta, nombre_etiqueta, valencia_min, valencia_max, activacion_min, activacion_max, cuadrante)
   -> no tiene una FK física en registros_afectivos; se relaciona en tiempo de procesamiento,
      comparando la valencia/activación de cada registro contra estos rangos.
```

### Pasaje a tablas

Cada entidad del MER se convirtió en una tabla independiente con su propia clave primaria. Las relaciones 1:N (`usuarios → registros_afectivos` y `contextos → registros_afectivos`) se implementaron como claves foráneas (`id_usuario`, `id_contexto`) dentro de `registros_afectivos`, en lugar de repetir el nombre del usuario o los datos del contexto en cada fila.

### Normalización

- **1FN:** todos los campos son atómicos (no hay listas ni valores compuestos en una misma celda).
- **2FN:** todas las tablas tienen clave primaria simple (un solo campo), por lo que no puede haber dependencias parciales.
- **3FN:** no existen dependencias transitivas; por ejemplo, el nombre y la edad de una persona dependen únicamente de `id_usuario`, no de `id_registro`, por lo que viven en `usuarios` y no se repiten en cada registro afectivo.

### Relaciones entre usuarios, contextos y registros afectivos

- **¿Cómo se relaciona un usuario con un registro afectivo?** A través de la clave foránea `id_usuario` presente en cada registro afectivo. Un usuario puede tener muchos registros afectivos a lo largo del tiempo (relación 1:N), pero cada registro pertenece a un único usuario.
- **¿Cómo se relaciona un contexto con un registro afectivo?** De la misma forma, a través de `id_contexto`. Un mismo contexto (por ejemplo "Ejercicio de bucles") puede repetirse en cientos de registros de distintos usuarios y momentos, pero cada registro ocurre en un único contexto.
- **¿Por qué la evaluación emocional se genera después y no viene directamente en el CSV?** Porque `valencia` y `activacion` son mediciones numéricas crudas; la interpretación de "a qué emoción corresponden" depende de una regla de negocio (los rangos definidos en `etiquetas_emocionales`) que puede cambiar con el tiempo o ajustarse por el equipo docente. Si la etiqueta viniera fija en el CSV, cualquier cambio en los rangos obligaría a regenerar el archivo de origen. Al calcularla en el programa (módulo `procesamiento_emocional.py`), la clasificación queda desacoplada de los datos crudos y puede recalcularse cuantas veces se necesite.

---

## 5. Organización modular del programa

| Módulo | Responsabilidad |
|---|---|
| `carga_base_datos.py` | Conectarse a la base de datos MySQL/MariaDB y cargar `usuarios`, `contextos` y `etiquetas_emocionales`. También cierra la conexión. |
| `carga_csv.py` | Leer `registros_afectivos.csv` (con reintento automático de codificación `utf-8` → `latin1`) y verificar que estén presentes todas las columnas obligatorias. |
| `sanitacion.py` | Limpiar texto, convertir y validar valencia/activación/fecha, validar existencia de usuario y contexto, detectar duplicados, separar registros válidos e inválidos y mostrar el resumen de errores. |
| `procesamiento_emocional.py` | Calcular intensidad, intensidad normalizada, cuadrante y etiqueta emocional de cada registro válido, usando los rangos de `etiquetas_emocionales`. |
| `generacion_evaluaciones.py` | Incorporar los datos de usuarios y contextos a las evaluaciones emocionales ya calculadas, y armar el archivo final ordenado. |
| `analisis_evaluaciones.py` | Responder las preguntas de análisis: emoción predominante por contexto/usuario, usuarios más inestables, promedios por etiqueta, contextos más negativos, distribución general de emociones. |
| `visualizaciones.py` | Generar los gráficos del proyecto (dispersión, distribución, promedios, series temporales, rankings por contexto/usuario). |

**Coordinación de la ejecución.** A diferencia de un único `main.py`, este proyecto separa la coordinación en cinco scripts, uno por etapa del pipeline, cada uno ejecutable de forma independiente:

| Script | Qué coordina |
|---|---|
| `main_sanitacion.py` | Conecta a la base, carga el CSV, ejecuta toda la sanitación y guarda `registros_afectivos_validados.csv`, `registros_afectivos_invalidos.csv` y `registros_afectivos_validos.csv`. |
| `main_procesamiento_emocional.py` | Carga los registros válidos y las etiquetas, calcula la evaluación emocional y guarda `evaluaciones_emocionales.csv` (paso intermedio, sin datos de usuario/contexto). |
| `main_gen_extension_evaluaciones_paso3.py` | Repite el cálculo emocional y además incorpora usuarios y contextos, generando el archivo final `evaluaciones_emocionales_extendidas.csv`. |
| `main_analisis_evaluaciones_paso4.py` | Ejecuta y muestra por consola los seis análisis definidos en `analisis_evaluaciones.py`. |
| `main_visualizaciones_paso5.py` | Genera todos los gráficos del proyecto a partir del archivo final. |

### Esquema del flujo

```
Base de datos (usuarios, contextos, etiquetas_emocionales) + CSV (registros_afectivos.csv)
 ↓
Carga de datos (carga_base_datos.py + carga_csv.py)
 ↓
Sanitización (sanitacion.py)
 ↓
Registros válidos / Registros inválidos
 ↓
Procesamiento emocional (procesamiento_emocional.py)
 ↓
Evaluaciones emocionales (intensidad, cuadrante, etiqueta)
 ↓
Enriquecimiento con usuarios y contextos (generacion_evaluaciones.py)
 ↓
Evaluaciones emocionales extendidas (evaluaciones_emocionales_extendidas.csv)
 ↓
Análisis (analisis_evaluaciones.py) y Visualizaciones (visualizaciones.py)
```

---

## 6. Limpieza y validación de datos

El módulo `sanitacion.py` controla, para cada registro del CSV:

- **Valores nulos o vacíos** en valencia, activación o fecha.
- **Textos vacíos o "nulos escritos como texto"** en el comentario (`"null"`, `"none"`, `"na"`, `"n/a"`, `"sin dato"`), que se reemplazan por `"No informado"` sin invalidar el registro.
- **Valores no numéricos** en valencia o activación (por ejemplo `"sin_dato"`, `"alto"`, `"bajo"`).
- **Valencia fuera de rango** (fuera de -1.00 a 1.00).
- **Activación fuera de rango** (fuera de -1.00 a 1.00).
- **Fechas inválidas** (que no pueden convertirse a un `datetime` real).
- **Usuarios inexistentes** (`id_usuario` que no está en la tabla `usuarios`).
- **Contextos inexistentes** (`id_contexto` que no está en la tabla `contextos`).
- **Duplicados** (mismo `id_registro` repetido más de una vez).

### Resultados obtenidos sobre este dataset

| Métrica | Valor |
|---|---|
| Total de registros en el CSV | 6.054 |
| Registros válidos | 5.894 (97,4 %) |
| Registros inválidos | 160 (2,6 %) |
| Total de errores detectados | 240 |

Errores por tipo:

| Tipo de error | Cantidad |
|---|---|
| Conversión de valencia (no numérica) | 40 |
| Valencia fuera de rango / no disponible | 60 |
| Conversión de activación (no numérica) | 40 |
| Activación fuera de rango / no disponible | 60 |
| Fecha inválida | 20 |
| Usuario inexistente | 0 |
| Contexto inexistente | 0 |
| Registro duplicado | 20 |

**¿Por qué puede haber más errores (240) que registros inválidos (160)?** Porque un mismo registro puede acumular más de un motivo de error a la vez. En este dataset, de los 160 registros inválidos, 80 tienen exactamente **un** error y 80 tienen exactamente **dos** errores simultáneos (80×1 + 80×2 = 240). Esto ocurre, por ejemplo, cuando la activación viene como texto no numérico (`"sin_dato"`, `"alto"`): al no poder convertirse a número, la función de validación de rango tampoco puede evaluarla y también la marca como inválida (`"activacion no disponible para validar"`). Así, una sola celda mal cargada dispara dos columnas de error distintas para el mismo registro.

---

## 7. Procesamiento emocional

- **Valencia:** qué tan positiva o negativa es la emoción registrada (-1 muy negativa, +1 muy positiva).
- **Activación:** qué tan enérgica o activa es la emoción (-1 muy baja energía/calma, +1 muy alta energía/alerta).
- **Intensidad:** `intensidad = raíz_cuadrada(valencia² + activación²)`. Puede superar el valor 1 (hasta aproximadamente 1,41, que es `raíz_cuadrada(2)`), porque combina dos ejes independientes.
- **Intensidad normalizada:** `intensidad_normalizada = intensidad / raíz_cuadrada(2)`, para llevar el valor a un rango aproximado de 0 a 1 y poder comparar intensidades entre registros de forma más intuitiva.
- **Cuadrante emocional:** ubicación de valencia/activación en uno de cinco grupos: `Centro`, `Positiva-Alta`, `Positiva-Baja`, `Negativa-Alta`, `Negativa-Baja`, usando un umbral de 0,30 para decidir cuándo un registro es tan cercano al punto neutro que se considera "Centro".
- **Etiqueta emocional:** nombre concreto asignado a partir de los rangos de la tabla `etiquetas_emocionales` (Entusiasta, Calmo, Frustrado, Triste, Tenso, Alerta, Neutro, Cansado).

**¿Por qué se calcula intensidad?** Porque dos registros pueden caer en la misma etiqueta emocional (por ejemplo "Entusiasta") con magnitudes muy distintas: un registro con valencia 0,40 y activación 0,45 y otro con valencia 0,95 y activación 0,90 son ambos "Entusiasta", pero el segundo representa una emoción mucho más fuerte. La intensidad permite capturar ese matiz de "cuánto", además de "qué" emoción es.

**¿Por qué se usa un umbral centro?** Porque valores muy cercanos a cero en valencia y activación representan ruido o indiferencia, no una emoción definida en un cuadrante extremo. El umbral (0,30) evita forzar a "Positiva" o "Negativa" un registro que en realidad está prácticamente en el punto neutro.

**¿Cómo se asigna una etiqueta emocional?** El programa recorre, en orden, las etiquetas cargadas desde la base de datos y devuelve el nombre de la primera cuyo rango de valencia y de activación contiene al registro (`clasificar_emocion()` en `procesamiento_emocional.py`). Si ningún rango coincide, el registro quedaría marcado como "Sin clasificar"; en este dataset no ocurrió ningún caso: los 5.894 registros válidos quedaron cubiertos exactamente por las 8 etiquetas existentes.

**¿Por qué las etiquetas se cargan desde la base de datos y no se escriben fijas en el código?** Para separar la configuración (los límites que definen cada emoción) de la lógica de procesamiento. Si el equipo docente decide ajustar el umbral de "Frustrado" o agregar una nueva etiqueta, alcanza con modificar la tabla `etiquetas_emocionales`, sin tocar ni volver a probar `procesamiento_emocional.py`.

---

## 8. Archivo final generado

El archivo final del pipeline es `dataset_salida/evaluaciones_emocionales_extendidas.csv` (5.894 filas, una por cada registro válido), generado por `main_gen_extension_evaluaciones_paso3.py`. Existe además un archivo intermedio, `evaluaciones_emocionales.csv`, que contiene el cálculo emocional pero todavía sin los datos de usuario y contexto (paso de `main_procesamiento_emocional.py`); el archivo extendido lo reemplaza como salida definitiva del proyecto.

Columnas del archivo final:

`id_evaluacion, id_registro, id_usuario, nombre, edad, genero, id_contexto, origen, actividad, ubicacion, descripcion, fecha_hora, valencia, activacion, comentario, intensidad, intensidad_normalizada, cuadrante, etiqueta_emocional`

Este archivo contiene los registros afectivos ya interpretados emocionalmente y enriquecidos con datos de usuario y contexto: cada fila permite saber, en un único lugar, quién generó el registro, en qué actividad, cuándo, con qué valencia/activación cruda y con qué interpretación emocional final.

---

## 9. Análisis realizados

Todos los análisis se calculan sobre `evaluaciones_emocionales_extendidas.csv` (25 usuarios distintos, 12 contextos distintos, 5.894 registros).

### Emoción predominante por contexto (`emocion_predominante_por_contexto`)
- **Pregunta que responde:** ¿qué emoción es la más frecuente en cada actividad/contexto, y cuál es su intensidad promedio?
- **Columnas usadas:** `id_contexto`, `origen`, `actividad`, `ubicacion`, `etiqueta_emocional`, `intensidad_normalizada`.
- **Resultado:** en todos los contextos analizados la emoción más frecuente es **"Neutro"**, con intensidades promedio relativamente parejas entre contextos (entre ~0,40 y ~0,41 en los de mayor intensidad, como "Ejercicio de bucles" o "Revisión cruzada entre pares").
- **Interpretación:** el clima emocional general del curso, contexto por contexto, tiende a ser neutro más que marcadamente positivo o negativo; no se observa un contexto que dispare una emoción extrema de forma dominante.

### Emoción predominante por usuario (`emocion_predominante_por_usuario`)
- **Pregunta que responde:** ¿cuál es la emoción más repetida en el historial de cada estudiante?
- **Columnas usadas:** `id_usuario`, `nombre`, `etiqueta_emocional`, `intensidad_normalizada`.
- **Resultado:** de los 25 usuarios, 24 tienen a "Neutro" como emoción predominante y 1 tiene a "Frustrado" como predominante.
- **Interpretación:** a nivel individual el patrón se repite: la mayoría de los estudiantes pasa la mayor parte del tiempo en un estado emocional neutro, con un caso puntual que merecería atención docente por predominancia de frustración.

### Usuarios más inestables (`usuarios_mas_inestables`)
- **Pregunta que responde:** ¿qué estudiantes muestran mayor variedad de emociones distintas (posible inestabilidad emocional)?
- **Columnas usadas:** `id_usuario`, `nombre`, `etiqueta_emocional`, `intensidad_normalizada`.
- **Resultado:** varios usuarios (por ejemplo Hernán Cardozo, Martín Castro, Diego Fernández, Gabriela López, Paula Costa) pasaron por las 8 etiquetas emocionales posibles, con intensidades promedio de entre 0,40 y 0,43.
- **Interpretación:** un número relevante de estudiantes no se mantiene en un único estado emocional, sino que atraviesa todo el espectro disponible; esto puede reflejar tanto variedad genuina de contextos como sensibilidad emocional a cambiar de actividad.

### Promedio de valencia y activación por etiqueta (`promedio_valencia_activacion_por_etiqueta`)
- **Pregunta que responde:** ¿qué valores típicos de valencia/activación caracterizan a cada etiqueta, y cuál es más intensa en promedio?
- **Columnas usadas:** `etiqueta_emocional`, `valencia`, `activacion`, `intensidad_normalizada`.
- **Resultado (extracto):** "Frustrado" combina valencia muy negativa (≈ -0,52) con activación alta (≈ 0,63) y es la etiqueta con mayor intensidad promedio (≈ 0,59) junto con "Entusiasta" (≈ 0,56); "Neutro" es la más frecuente (1.408 registros) pero la de menor intensidad (≈ 0,15).
- **Interpretación:** las emociones "extremas" (Frustrado, Entusiasta, Tenso) son, esperablemente, las más intensas; el estado más común del curso es también el más "plano" en términos de intensidad.

### Contextos más negativos (`contextos_mas_negativos`)
- **Pregunta que responde:** ¿qué contextos tienen, en promedio, la valencia más baja?
- **Columnas usadas:** `id_contexto`, `origen`, `actividad`, `ubicacion`, `valencia`, `etiqueta_emocional`.
- **Resultado:** el contexto con menor valencia promedio es "Trabajo en pares" (≈ 0,004), seguido de "Entrega de tarea individual" (≈ 0,02) y "Trabajo en equipo" (≈ 0,03).
- **Interpretación:** en este dataset ningún contexto muestra una valencia promedio claramente negativa; los "más negativos" son en realidad prácticamente neutros, lo que sugiere que el malestar (cuando aparece) no está concentrado en una actividad puntual sino distribuido de forma más pareja.

### Distribución general de emociones (`distribucion_emociones`)
- **Pregunta que responde:** ¿cómo se reparten, en cantidad y porcentaje, las 8 etiquetas emocionales sobre el total de registros?
- **Columnas usadas:** `etiqueta_emocional`.
- **Resultado:** Neutro 1.408 (23,9 %), Frustrado 1.039 (17,6 %), Alerta 949 (16,1 %), Calmo 913 (15,5 %), Entusiasta 786 (13,3 %), Tenso 390 (6,6 %), Triste 239 (4,1 %), Cansado 170 (2,9 %).
- **Interpretación:** casi un cuarto de los registros son neutros, pero sumando "Frustrado" y "Tenso" (24,3 %) el volumen de emociones negativas/de tensión es comparable al de neutralidad, y algo mayor que el de emociones positivas de baja energía ("Calmo", 15,5 %).

---

## 10. Visualizaciones

Todos los gráficos se generan con `visualizaciones.py` y se guardan en la carpeta `graficos/`.

| Gráfico (archivo) | Qué representa | Qué conclusión permite observar |
|---|---|---|
| `dispersion_valencia_activacion.png` | Dispersión de todos los registros según valencia (eje X) y activación (eje Y), coloreados por etiqueta emocional. | Permite ver visualmente los "clusters" de cada emoción y confirmar que los límites definidos en `etiquetas_emocionales` separan razonablemente bien las nubes de puntos. |
| `distribucion_emociones.png` | Cantidad de registros por etiqueta emocional (gráfico de barras). | Confirma visualmente el predominio de "Neutro" y "Frustrado" sobre el resto de las etiquetas. |
| `promedios_por_etiqueta.png` | Promedio de valencia y de activación para cada etiqueta emocional. | Muestra qué tan "puras" o consistentes son las etiquetas: por ejemplo, "Frustrado" concentra valencia negativa y activación alta de forma consistente. |
| `serie_temporal_intensidad.png` | Evolución de la intensidad emocional normalizada promedio por día. | Permite ver si hay picos o caídas de intensidad emocional en fechas puntuales (por ejemplo, cerca de entregas o evaluaciones). |
| `intensidad_promedio_por_contexto.png` | Ranking (top 10) de contextos según intensidad emocional promedio. | Identifica qué actividades generan reacciones emocionales más intensas, más allá de si son positivas o negativas. |
| `contextos_mas_negativos.png` | Ranking (top 10) de contextos según menor valencia promedio. | Ayuda a priorizar qué actividades revisar primero si se buscara reducir malestar, aunque en este dataset las diferencias entre contextos son pequeñas. |
| `usuarios_mas_inestables.png` | Ranking (top 10) de usuarios según cantidad de etiquetas emocionales distintas registradas. | Señala qué estudiantes atraviesan mayor variedad emocional y podrían ser objeto de seguimiento. |
| `emocion_predominante_por_contexto.png` | Emoción más frecuente en cada uno de los contextos principales, con la cantidad de registros asociada. | Complementa el análisis tabular mostrando de un vistazo qué emoción "domina" cada actividad. |
| `serie_temporal_valencia_activacion.png` | Evolución diaria del promedio de valencia y de activación por separado. | Permite distinguir si un cambio en el clima emocional se debe a que las emociones se volvieron más negativas (valencia) o más intensas/activas (activación), o ambas cosas. |

---

## 11. Resultados principales

- **¿Cuáles fueron las emociones más frecuentes?** Neutro (23,9 %) y Frustrado (17,6 %), seguidas de Alerta (16,1 %) y Calmo (15,5 %).
- **¿Qué contextos tuvieron emociones más negativas?** Ninguno de forma marcada; el más cercano a valencia negativa promedio fue "Trabajo en pares", aunque su valor (≈0,004) es prácticamente neutro. No se detectó un contexto "problemático" claro en este dataset.
- **¿Qué usuarios mostraron mayor variabilidad emocional?** Un grupo de estudiantes (entre ellos Hernán Cardozo, Martín Castro, Diego Fernández, Gabriela López y Paula Costa) registró las 8 etiquetas emocionales posibles a lo largo de sus distintos eventos.
- **¿Qué etiquetas tuvieron mayor intensidad promedio?** "Frustrado" (≈0,59) y "Entusiasta" (≈0,56), es decir, las emociones con carga afectiva más marcada (positiva o negativa), muy por encima de "Neutro" (≈0,15).
- **¿Qué conclusiones generales se pueden obtener?** El curso, en conjunto, presenta un clima emocional mayormente neutro pero con una proporción no menor de frustración/tensión (24,3 % combinado) que amerita atención; la variabilidad emocional no está concentrada en pocos estudiantes, sino que es un fenómeno relativamente extendido; y las diferencias entre contextos son sutiles, por lo que el malestar detectado no puede atribuirse a una sola actividad puntual del curso.

---

## 12. Manejo de errores y decisiones técnicas

- **¿Por qué se usó `try-except-finally`?** Porque el programa depende de recursos externos que pueden fallar (conexión a la base de datos, lectura de un archivo que podría no existir o tener una codificación distinta). El `try-except` evita que el programa se corte abruptamente ante un error esperable, y permite informar el problema de forma clara en lugar de mostrar una traza técnica al usuario.
- **¿Por qué se cerró la conexión en `finally`?** Porque el bloque `finally` se ejecuta siempre, haya habido error o no. Esto garantiza que la conexión a la base de datos se cierre correctamente en todos los casos, evitando dejar conexiones abiertas que consuman recursos del servidor.
- **¿Por qué se separaron registros válidos e inválidos?** Para que los errores de un subconjunto de datos no impidan avanzar con el análisis del resto, y para poder auditar después específicamente qué registros fallaron y por qué (archivo `registros_afectivos_invalidos.csv`), sin mezclarlos con los datos limpios que sí se usan en el procesamiento emocional.
- **¿Por qué se usaron módulos?** Para dividir el programa según responsabilidades claras (carga, sanitación, procesamiento, generación, análisis, visualización), lo que facilita probar y modificar una parte sin afectar a las demás, y hace que cada archivo sea más corto y entendible.
- **¿Por qué se usaron funciones?** Para evitar repetir código (por ejemplo, la validación de rango se escribe una sola vez y se aplica a cada valor de valencia/activación) y para poder probar cada paso de forma aislada con casos concretos.
- **¿Por qué se usó pandas?** Porque el proyecto trabaja con miles de registros tabulares (CSV y resultados de consultas SQL) y pandas permite leer, transformar, filtrar, agrupar y exportar esos datos de forma mucho más simple y eficiente que iterando manualmente fila por fila con estructuras nativas de Python.
- **¿Por qué no se modificó el CSV original?** Para preservar la trazabilidad de los datos de origen: si se detecta un problema en el análisis, siempre se puede volver a `registros_afectivos.csv` tal como llegó y verificar si el error viene de los datos originales o de algún paso del procesamiento. Todo el trabajo de limpieza se guarda en archivos nuevos dentro de `dataset_salida/`.

---

## 13. Limitaciones del sistema

- Las etiquetas emocionales dependen de rangos numéricos definidos previamente en la base de datos; si esos rangos están mal calibrados, la clasificación hereda ese error.
- El sistema no interpreta el contenido textual del comentario: dos comentarios con significados emocionales opuestos pero con la misma valencia/activación numérica reciben la misma etiqueta.
- Los valores de valencia y activación ya vienen dados en el CSV; el sistema no evalúa qué tan confiable es la fuente que los generó.
- La validación de fecha solo controla que el valor sea convertible a un `datetime` válido, no que sea una fecha razonable: en este dataset se detectó al menos un registro con fecha `2099-01-01`, técnicamente válida pero claramente incorrecta, que pasa la validación sin marcarse como error.
- La clasificación en 8 etiquetas y 5 cuadrantes es una simplificación del espectro emocional real; estados intermedios o mixtos quedan forzados a la etiqueta más cercana.
- El análisis no reemplaza la interpretación docente o humana: señala patrones y tendencias, pero no explica sus causas.

---

## 14. Mejoras futuras

- Agregar análisis del texto del comentario (por ejemplo, detección de palabras clave o análisis de sentimiento) para complementar los valores numéricos.
- Agregar más gráficos, por ejemplo comparaciones entre usuarios o entre grupos de contextos.
- Crear una interfaz (web o de escritorio) que permita ejecutar el pipeline y explorar los resultados sin usar la consola.
- Guardar las evaluaciones emocionales generadas nuevamente en la base de datos, en lugar de (o además de) un CSV.
- Permitir configurar o editar las etiquetas emocionales desde un formulario, en lugar de modificar la tabla directamente.
- Detectar y advertir sobre superposición de rangos entre etiquetas emocionales al momento de cargarlas.
- Agregar filtros interactivos por usuario, contexto o rango de fechas antes de generar los análisis y gráficos.

---

## 15. Conclusión

El desarrollo de este proyecto permitió aprender a construir un pipeline completo de datos que combina dos fuentes heterogéneas (una base de datos relacional y un archivo CSV), y a organizarlo en módulos con responsabilidades bien definidas en lugar de un único script monolítico. El sistema logró tomar 6.054 registros afectivos "crudos", detectar y aislar 160 registros inválidos por 8 tipos de error distintos, calcular sobre los 5.894 registros restantes una interpretación emocional completa (intensidad, cuadrante y etiqueta) y producir tanto un archivo final enriquecido como seis análisis agregados y nueve visualizaciones.

La principal dificultad estuvo en anticipar todas las formas en que un dato puede llegar "mal" (textos en lugar de números, valores fuera de rango, referencias a usuarios o contextos inexistentes, duplicados, fechas imposibles) y decidir, para cada caso, si correspondía limpiar el valor, marcarlo como error o descartar el registro completo. Este proceso dejó en claro que **limpiar y validar los datos antes de analizarlos no es un paso secundario**: sin él, cualquier promedio o clasificación calculada sobre datos sucios sería directamente incorrecta, aunque el código que la calcula esté bien escrito.

Finalmente, el proyecto muestra el valor de transformar datos numéricos aparentemente abstractos (dos números entre -1 y 1) en información interpretable y accionable: pasar de "valencia = -0.52, activación = 0.63" a "Frustrado, con intensidad alta" es lo que permite que una persona sin formación técnica —como un docente— pueda usar estos resultados para tomar decisiones sobre su curso.

---

## Entregables sugeridos

1. **Objetivo del proyecto:** ver Sección 2.
2. **Descripción de datos:** ver Secciones 3 y 4.
3. **Módulos implementados:** ver Sección 5.
4. **Limpieza y validación:** ver Sección 6.
5. **Procesamiento emocional:** ver Sección 7.
6. **Evaluaciones generadas:** ver Sección 8.
7. **Análisis y resultados:** ver Secciones 9, 10 y 11.
8. **Conclusiones y mejoras:** ver Secciones 13, 14 y 15.

> **Importante:** la documentación, el código fuente y las fuentes de datos utilizadas deben compartirse con el docente a través de GitHub, en un archivo comprimido, según lo solicitado en la consigna.
