# Cuestionario de preparación para la defensa oral del proyecto integrador

---

## 1. Generalidades

**1. ¿Cuál es el objetivo general del proyecto?**
Desarrollar un sistema que combine datos de una base de datos relacional (usuarios, contextos, etiquetas emocionales) con un archivo CSV de registros afectivos, para limpiarlos, validarlos, calcular una interpretación emocional (intensidad, cuadrante y etiqueta emocional) sobre cada registro válido, y generar análisis y visualizaciones que permitan entender el estado emocional de un grupo de usuarios en distintos contextos.

**2. ¿Qué problema intenta resolver el sistema desarrollado?**
Interpretar de forma automática y sistemática miles de registros afectivos "crudos" (dos números: valencia y activación) que por sí solos no dicen nada sobre la emoción real, y que además pueden llegar con errores (datos faltantes, valores fuera de rango, texto donde debería haber números, fechas inválidas, referencias a usuarios o contextos que no existen, duplicados). El sistema limpia esos datos y los transforma en información interpretable.

**3. ¿Quiénes podrían usar los resultados generados por el sistema?**
Docentes, tutores o equipos de seguimiento académico, que podrían usar los análisis y gráficos para detectar en qué actividades los estudiantes se frustran o se entusiasman más, y qué estudiantes muestran mayor variabilidad emocional.

**4. ¿Qué parte del proyecto corresponde a carga de datos, cuál a limpieza, cuál a procesamiento y cuál a análisis?**
- Carga de datos: `carga_base_datos.py` (usuarios, contextos, etiquetas emocionales desde MySQL/MariaDB) y `carga_csv.py` (registros afectivos desde el archivo CSV).
- Limpieza: `sanitacion.py`.
- Procesamiento: `procesamiento_emocional.py` (cálculo de la evaluación emocional) y `generacion_evaluaciones.py` (enriquecimiento con usuarios y contextos).
- Análisis: `analisis_evaluaciones.py` (análisis numéricos) y `visualizaciones.py` (gráficos).

**5. ¿Cuál es el flujo general del programa desde que se cargan los datos hasta que se generan los resultados?**
Se cargan usuarios, contextos y etiquetas emocionales desde la base de datos, y los registros afectivos desde el CSV. Luego se sanitiza y valida cada registro, separando los válidos de los inválidos. Sobre los registros válidos se calcula la evaluación emocional (intensidad, cuadrante, etiqueta) y se incorporan los datos de usuario y contexto, generando el archivo final `evaluaciones_emocionales_extendidas.csv`. Por último, sobre ese archivo se ejecutan los análisis agregados y se generan los gráficos.

**6. ¿Qué archivos, tablas y/o módulos intervienen en el proyecto?**
- Tablas: `usuarios`, `contextos`, `etiquetas_emocionales`, `registros_afectivos`.
- Archivo: `registros_afectivos.csv`.
- Módulos: `carga_base_datos.py`, `carga_csv.py`, `sanitacion.py`, `procesamiento_emocional.py`, `generacion_evaluaciones.py`, `analisis_evaluaciones.py`, `visualizaciones.py`.
- Scripts de coordinación: `main_sanitacion.py`, `main_procesamiento_emocional.py`, `main_gen_extension_evaluaciones_paso3.py`, `main_analisis_evaluaciones_paso4.py`, `main_visualizaciones_paso5.py`.

---

## 2. Modelo de datos y base de datos

**1. ¿Qué tablas forman parte de la base de datos?**
`usuarios`, `contextos`, `etiquetas_emocionales` y `registros_afectivos`.

**2. ¿Qué información contiene la tabla `usuarios` (algunos campos)?**
`id_usuario` (clave primaria), `nombre`, `edad` y `genero`.

**3. ¿Qué información contiene la tabla `contextos` (algunos campos)?**
`id_contexto` (clave primaria), `origen`, `actividad`, `ubicacion` y `descripcion`.

**4. ¿Qué información contiene la tabla `etiquetas_emocionales` (algunos campos)?**
`id_etiqueta` (clave primaria), `nombre_etiqueta`, `valencia_min`, `valencia_max`, `activacion_min`, `activacion_max` y `cuadrante`.

**5. ¿Por qué los registros afectivos se leen desde un archivo CSV y no directamente desde la base de datos?**
Porque el proyecto simula un escenario real de integración de fuentes heterogéneas: los registros afectivos llegan como un archivo exportado desde otro sistema o proceso de captura, y no como datos ya cargados y validados en la base. Esto obliga a leer, limpiar y validar ese archivo externo antes de poder cruzarlo con la información confiable de usuarios y contextos que sí vive en la base de datos.

**6. Mencione algunos campos que contiene el archivo `registros_afectivos.csv`.**
`id_registro`, `id_usuario`, `id_contexto`, `fecha_hora`, `valencia`, `activacion` y `comentario`.

**7. ¿Por qué es importante validar que los usuarios del CSV existan en la base de datos?**
Porque si un registro afectivo referencia un `id_usuario` que no existe, no se lo podría asociar a una persona real (nombre, edad, género) al momento de enriquecer y analizar los datos; ese registro estaría "huérfano" y podría distorsionar cualquier análisis por usuario, además de indicar un posible error de carga.

**8. ¿Por qué es importante validar que los contextos del CSV existan en la base de datos?**
Por la misma razón, pero del lado del contexto: un `id_contexto` inexistente impediría enriquecer el registro con la actividad, el origen y la ubicación reales, y falsearía los análisis agrupados por contexto.

**9. ¿Qué representa una clave primaria?**
Es el campo (o conjunto de campos) que identifica de manera única a cada fila de una tabla; no puede repetirse ni ser nulo, y permite referenciar esa fila desde otras tablas.

**10. ¿Qué representa una clave foránea?**
Es un campo de una tabla que referencia la clave primaria de otra tabla, estableciendo una relación entre ambas (por ejemplo, `id_usuario` en `registros_afectivos` referencia a `usuarios`) y garantizando que ese valor exista realmente en la tabla referenciada.

---

## 3. Carga de datos

**1. ¿Qué hace el módulo `carga_base_datos.py`?**
Se encarga de abrir y cerrar la conexión a la base de datos MySQL/MariaDB, y de cargar como DataFrames de pandas las tablas `usuarios`, `contextos` y `etiquetas_emocionales`.

**2. ¿Qué hace la función `conectar_base_datos()`?**
Intenta abrir una conexión con `pymysql` a la base `proyectointegrador` en `localhost`; si la conexión se establece, la devuelve y muestra un mensaje de éxito; si falla, captura el error, lo informa por consola y devuelve `None`.

**3. ¿Por qué conviene separar la conexión a la base de datos en una función?**
Para no repetir el mismo código de conexión en cada script que necesita usar la base, poder reutilizarla desde todos los `main_*.py`, y centralizar en un único lugar el manejo del error de conexión.

**4. ¿Qué devuelve la función `cargar_usuarios(conexion)`?**
Un DataFrame con todos los registros de la tabla `usuarios` (`SELECT * FROM usuarios`). En `sanitacion.py` existe además una versión que adicionalmente devuelve un diccionario indexado por `id_usuario`, usado para validar rápidamente si un usuario existe.

**5. ¿Qué devuelve la función `cargar_contextos(conexion)`?**
Un DataFrame con todos los registros de la tabla `contextos`. Al igual que con usuarios, en `sanitacion.py` la función homónima también arma un diccionario indexado por `id_contexto` para las validaciones.

**6. ¿Qué devuelve la función `cargar_etiquetas_emocionales(conexion)`?**
Un DataFrame con todas las filas de la tabla `etiquetas_emocionales`, usado luego por `procesamiento_emocional.py` para clasificar cada registro.

**7. ¿Qué hace el módulo `carga_csv.py`?**
Lee el archivo CSV de registros afectivos y verifica que contenga todas las columnas obligatorias antes de continuar con el resto del procesamiento.

**8. ¿Qué hace la función `leer_registros_afectivos(ruta_carpeta, nombre_archivo)`?**
Arma la ruta completa del archivo con `pathlib`, intenta leerlo con `pandas.read_csv` usando codificación `utf-8`; si ocurre un error de decodificación, reintenta con `latin1`; si el archivo no existe o hay otro error, informa el problema por consola y devuelve un DataFrame vacío en lugar de interrumpir el programa.

**9. ¿Por qué conviene pasar la ruta y el nombre del archivo como parámetros?**
Para poder reutilizar la misma función con distintos archivos a lo largo del pipeline (`registros_afectivos.csv`, `registros_afectivos_validos.csv`, `evaluaciones_emocionales_extendidas.csv`) sin duplicar la lógica de lectura, solo cambiando los argumentos.

**10. ¿Por qué puede ser necesario usar `encoding="utf-8"` o `encoding="latin1"`?**
Porque el archivo puede haber sido generado o guardado por otro sistema o herramienta (por ejemplo, una planilla de Excel en Windows) con una codificación distinta a UTF-8. Si se lee con la codificación incorrecta, los caracteres especiales (tildes, eñes) aparecen corruptos o directamente se produce un error de decodificación; probar primero UTF-8 y luego Latin-1 permite leer el archivo igual sin que el programa se caiga.

**11. ¿Cómo se verifica que el CSV tenga las columnas obligatorias?**
La función `verificar_columnas_csv(df)` define la lista de columnas esperadas (`id_registro`, `id_usuario`, `id_contexto`, `fecha_hora`, `valencia`, `activacion`, `comentario`) y compara cuáles de ellas no están presentes en las columnas reales del DataFrame; si falta alguna, las informa por consola y devuelve `False` para que el programa no continúe con datos incompletos.

---

## 4. Sanitización y validación de datos

**1. ¿Qué significa sanitizar datos?**
Es el proceso de limpiar, convertir y validar los valores crudos de un conjunto de datos para que queden en un formato correcto y consistente, detectando y marcando lo que no cumple con las reglas esperadas antes de usarlos.

**2. ¿Por qué es necesaria la limpieza de datos antes del procesamiento emocional?**
Porque calcular intensidad, cuadrante o etiqueta emocional sobre un valor no numérico, vacío o fuera de rango produciría resultados incorrectos o directamente haría fallar el cálculo; primero hay que garantizar que solo se procesan datos numéricamente válidos.

**3. ¿Qué tipos de errores se pueden encontrar en el archivo CSV?**
Valores nulos o vacíos, texto vacío o escrito como "sin dato"/"null"/"na", valores no numéricos en valencia o activación, valores fuera del rango [-1, 1], fechas inválidas, usuarios inexistentes, contextos inexistentes y registros duplicados (mismo `id_registro`).

**4. ¿Qué hace la función `limpiar_texto()`?**
Recibe una celda de texto: si es nula, vacía, o una variante de "nulo escrito como texto" (`null`, `none`, `na`, `n/a`, `sin dato`), devuelve un valor por defecto (por ejemplo `"No informado"`); si el texto tiene espacios múltiples internos, los reemplaza por uno solo; en cualquier otro caso devuelve el texto ya limpio.

**5. ¿Qué valores de texto se consideran inválidos o incompletos?**
Valores nulos (`NaN`), cadenas vacías, y textos equivalentes a "sin dato" como `"null"`, `"none"`, `"na"`, `"n/a"` o `"sin dato"` (sin importar mayúsculas ni espacios extra).

**6. ¿Por qué es necesario convertir valencia y activación a números?**
Porque en el CSV llegan como texto (a veces con coma decimal, o directamente con valores como `"alto"`, `"bajo"` o `"sin_dato"`), y todas las fórmulas posteriores (intensidad, cuadrante, clasificación) necesitan operar con números reales, no con cadenas de texto.

**7. ¿Qué ocurre si un valor de valencia no se puede convertir a número?**
La función `convertir_a_float()` devuelve `None` junto con un mensaje de error (por ejemplo `"valencia no numérico: alto"`). Esa fila queda marcada con `error_conversion_valencia` y, al no tener un valor numérico disponible, la validación de rango también falla (`"valencia no disponible para validar"`), por lo que el registro termina siendo inválido.

**8. ¿Qué ocurre si un valor de activación está fuera del rango permitido?**
`validar_activacion()` devuelve `False` junto con un mensaje como `"activacion fuera de rango: 1.18"`, y ese registro se marca como inválido (columna `error_rango_activacion`), quedando excluido del conjunto de registros válidos.

**9. ¿Cuál es el rango válido para valencia y activación?**
De -1.00 a 1.00 para ambos campos (reforzado además por restricciones `CHECK` en la tabla `registros_afectivos` de la base de datos).

**10. ¿Qué hace la función `validar_fecha()`?**
Recibe un valor de fecha, controla que no esté vacío ni sea un "nulo escrito como texto", intenta convertirlo a un `datetime` real con `pandas.to_datetime`, y si no puede convertirse, devuelve `None` junto con un mensaje de error (`"fecha_hora inválida: valor"`).

**11. ¿Por qué se generan archivos separados para registros válidos e inválidos?**
Para poder seguir trabajando y analizando únicamente con los datos confiables, y al mismo tiempo conservar un registro auditable de qué filas fallaron y por qué motivo, sin mezclarlas con los datos limpios (`registros_afectivos_validos.csv` vs. `registros_afectivos_invalidos.csv`).

**12. ¿Qué archivo se usa luego para el procesamiento emocional?**
`dataset_salida/registros_afectivos_validos.csv`, que contiene únicamente los registros que pasaron todas las validaciones, con las columnas ya limpias y renombradas a sus nombres originales (`id_usuario`, `id_contexto`, `fecha_hora`, `valencia`, `activacion`, `comentario`).

---

## 5. Manejo de errores y estructura del programa

**1. ¿Para qué se usa `try`?**
Para delimitar un bloque de código que puede fallar (por ejemplo, conectarse a la base de datos o leer un archivo), de modo que si ocurre un error se pueda capturar en lugar de que el programa se detenga abruptamente.

**2. ¿Para qué se usa `except`?**
Para capturar y manejar el error que ocurrió dentro del `try`, por ejemplo mostrando un mensaje descriptivo o devolviendo un valor seguro (`None`, un DataFrame vacío) en lugar de dejar que la excepción interrumpa todo el programa.

**3. ¿Para qué se usa `finally`?**
Para ejecutar código que debe correr sí o sí, haya ocurrido un error o no, típicamente para liberar recursos como cerrar una conexión abierta.

**4. ¿Por qué la conexión a la base de datos se cierra en el bloque `finally`?**
Para garantizar que la conexión se cierre en cualquier escenario, tanto si el procesamiento terminó bien como si ocurrió un error en el medio, evitando dejar conexiones abiertas que consuman recursos del servidor.

**5. ¿El bloque `finally` se ejecuta si ocurre un error?**
Sí. Se ejecuta siempre: tanto si el bloque `try` terminó sin problemas, como si se lanzó una excepción (haya sido capturada por `except` o no).

**6. ¿Qué diferencia hay entre ejecutar un archivo directamente e importarlo como módulo?**
Al ejecutar un archivo directamente (`python archivo.py`) se corre todo su código de arriba a abajo, incluyendo cualquier llamado a `main()`. Al importarlo desde otro archivo (`import modulo`) Python también ejecuta el código de nivel superior del módulo, pero normalmente no se desea que eso dispare automáticamente su función principal.

**7. ¿Qué problema puede ocurrir si un módulo ejecuta código automáticamente al ser importado?**
Que cualquier otro script que solo necesite usar una función de ese módulo terminaría ejecutando efectos secundarios no deseados (por ejemplo, abrir una conexión a la base de datos, leer archivos o generar salidas) con el simple hecho de importarlo. La buena práctica es usar la guarda `if __name__ == "__main__":` antes de llamar a `main()`, para que solo se ejecute cuando el archivo se corre directamente. *(Nota: en los scripts `main_*.py` de este proyecto esa guarda aparece comentada y `main()` se llama de forma incondicional al final del archivo; funciona porque esos scripts se ejecutan siempre de forma directa, pero sería un punto de mejora aplicar esa buena práctica de forma consistente.)*

**8. ¿Cómo se puede cortar el flujo de un programa dentro de `main()`?**
Usando `return` dentro de la función `main()` cuando se detecta una condición de error (por ejemplo, si la conexión es `None` o el DataFrame quedó vacío), lo que termina la ejecución de `main()` sin continuar con los pasos siguientes. En este proyecto esto se combina con `try/except/finally` para que, aunque se corte el flujo, la conexión igual se cierre.

---

## 6. Procesamiento emocional

**1. ¿Qué hace el módulo `procesamiento_emocional.py` y qué datos recibe este módulo?**
Calcula los valores derivados de cada registro afectivo válido: intensidad, intensidad normalizada, cuadrante y etiqueta emocional. Recibe el DataFrame de registros válidos (con `valencia` y `activacion`) y el DataFrame de etiquetas emocionales cargado desde la base de datos.

**3. ¿Qué columnas nuevas agrega al DataFrame (mencione algunas)?**
`intensidad`, `intensidad_normalizada`, `cuadrante` y `etiqueta_emocional`.

**4. ¿Qué representa la valencia y activación?**
La valencia representa qué tan positiva o negativa es la emoción; la activación representa qué tan enérgica o activa es esa emoción. Juntas ubican cada registro en un plano bidimensional que permite describir la emoción.

**5. ¿Qué significa una valencia positiva o negativa?**
Positiva: emoción agradable (por ejemplo alegría, entusiasmo, calma). Negativa: emoción desagradable (por ejemplo tristeza, frustración).

**6. ¿Qué significa una activación alta o baja?**
Alta: mucha energía o alerta (por ejemplo enojo o entusiasmo). Baja: poca energía, calma o cansancio.

**7. ¿Qué es la intensidad emocional y por qué puede ser útil calcular la intensidad emocional?**
Es una medida de qué tan fuerte es la emoción, combinando valencia y activación en un solo número. Es útil porque dos registros pueden tener la misma etiqueta emocional (por ejemplo "Entusiasta") con magnitudes muy distintas: uno con valencia 0,40/activación 0,45 y otro con valencia 0,95/activación 0,90 son ambos "Entusiasta", pero el segundo es mucho más intenso. La intensidad permite capturar ese matiz.

**8. ¿Cómo se calcula la intensidad y por qué se normaliza?**
`intensidad = raíz_cuadrada(valencia² + activación²)`. Se normaliza porque ese valor puede superar 1 (hasta aproximadamente 1,41, que es `raíz_cuadrada(2)`), y dividirlo por `raíz_cuadrada(2)` lo lleva a un rango aproximado de 0 a 1, más fácil de interpretar y comparar entre registros.

**9. ¿Cuál es la diferencia entre intensidad e intensidad normalizada?**
La intensidad es el valor crudo (puede llegar hasta ~1,41); la intensidad normalizada es ese mismo valor dividido por `raíz_cuadrada(2)`, acotado a un rango aproximado de 0 a 1.

**10. ¿Qué significa el cuadrante emocional?**
Es la agrupación de un registro según el signo de su valencia y activación: `Positiva-Alta`, `Positiva-Baja`, `Negativa-Alta`, `Negativa-Baja`, o `Centro` si ambos valores están muy cerca de cero.

**11. ¿Qué es el umbral centro?**
Es el valor (0,30 en este proyecto) que define qué tan cerca de cero deben estar la valencia y la activación de un registro para considerarlo parte del cuadrante "Centro" en lugar de forzarlo a uno de los cuatro cuadrantes extremos.

**12. ¿Por qué no conviene clasificar valores muy cercanos a cero directamente en un cuadrante?**
Porque cerca de cero el signo puede deberse a ruido o a una emoción prácticamente neutra, no a una emoción realmente definida; forzar esos valores a "Positiva" o "Negativa" exageraría una diferencia que en la práctica es insignificante.

**13. ¿Por qué la clasificación emocional se hace usando la tabla `etiquetas_emocionales`?**
Porque esa tabla define de forma explícita los rangos de valencia y activación que corresponden a cada nombre de emoción, permitiendo que la función `clasificar_emocion()` compare cada registro contra esos rangos en lugar de tener las reglas de clasificación escritas de forma fija ("hardcodeadas") dentro del código Python.

**14. ¿Qué ventaja tiene guardar las etiquetas en la base de datos en lugar de escribirlas directamente en el código?**
Permite ajustar los límites de una emoción, o agregar/quitar etiquetas, modificando solo la tabla `etiquetas_emocionales`, sin tener que tocar ni volver a desplegar el código Python. Separa la configuración (los rangos) de la lógica de procesamiento.

**15. ¿Qué hace el módulo `generacion_evaluaciones.py`?**
Toma las evaluaciones emocionales ya calculadas y les incorpora los datos de usuarios (nombre, edad, género) y de contextos (origen, actividad, ubicación, descripción) mediante un `merge`, agrega un `id_evaluacion` correlativo y ordena las columnas del archivo final.

**16. ¿Por qué se incorpora información de usuarios a las evaluaciones emocionales?**
Para que el archivo final permita analizar y presentar resultados por persona (nombre, edad, género) sin tener que volver a cruzar manualmente con la tabla `usuarios` cada vez que se necesite esa información.

**17. ¿Por qué se incorpora información de contextos a las evaluaciones emocionales?**
Por la misma razón, pero del lado del contexto: permite analizar y presentar resultados por actividad, origen o ubicación directamente desde el archivo final, sin nuevas consultas a la base de datos.

---

## 7. Análisis de evaluaciones

**1. ¿Qué hace el módulo `analisis_evaluaciones.py`?**
Define las funciones que responden a las preguntas de análisis del proyecto (emoción predominante por contexto y por usuario, usuarios más inestables, promedios de valencia/activación por etiqueta, contextos más negativos y distribución general de emociones), todas operando sobre el archivo final `evaluaciones_emocionales_extendidas.csv`.

**2. ¿Qué pregunta responde la función `emocion_predominante_por_contexto()`?**
¿Cuál es la emoción más frecuente en cada contexto/actividad, y cuál es la intensidad emocional promedio de ese contexto?

**3. ¿Qué pregunta responde la función `emocion_predominante_por_usuario()`?**
¿Cuál es la emoción más frecuente en el historial de registros de cada usuario?

**4. ¿Cómo se puede calcular la emoción que más se repite?**
Agrupando los registros (por contexto o por usuario) y aplicando la moda estadística sobre la columna `etiqueta_emocional` (función `obtener_emocion_predominante()`, que usa `serie.mode()` y toma el primer valor de esa moda).

**5. ¿Qué significa que un usuario sea emocionalmente inestable en este proyecto?**
Que registra una mayor cantidad de etiquetas emocionales distintas (`cantidad_emociones_distintas`, calculado con `nunique()`) a lo largo de sus registros, es decir, que no permanece en un único estado emocional sino que atraviesa varios estados diferentes.

**6. ¿Qué hace la función `contextos_mas_negativos()`?**
Agrupa los registros por contexto, calcula el promedio de valencia de cada uno junto con su emoción predominante y la cantidad de registros, y ordena los contextos de menor a mayor valencia promedio, para identificar cuáles concentran las emociones más negativas.

---

## 8. Visualizaciones y presentación de resultados

**1. ¿Qué representa un gráfico de dispersión de valencia y activación?**
Cada punto es un registro afectivo ubicado según su valencia (eje X) y su activación (eje Y), coloreado según su etiqueta emocional; permite ver visualmente cómo se agrupan las distintas emociones en el plano y si los rangos definidos las separan razonablemente bien.

**2. ¿Qué representa una serie temporal emocional?**
Muestra la evolución de un valor emocional (por ejemplo, la intensidad normalizada promedio, o la valencia/activación promedio) día a día, permitiendo detectar tendencias, picos o caídas a lo largo del tiempo, incluso filtrando por un usuario o contexto puntual.

**3. ¿Por qué los gráficos ayudan a interpretar mejor los resultados?**
Porque permiten detectar patrones, tendencias y valores extremos de un vistazo, algo mucho más difícil de percibir leyendo tablas de miles de filas o incluso los resultados numéricos ya agregados.

**4. ¿Qué gráfico usarían para mostrar las emociones más frecuentes?**
Un gráfico de barras, como `distribucion_emociones.png`, que muestra la cantidad (y el porcentaje) de registros para cada etiqueta emocional.

---

## 9. Modularización y programación

**1. ¿Por qué el proyecto se dividió en módulos?**
Para separar responsabilidades claras (carga, limpieza, procesamiento, generación de evaluaciones, análisis, visualización) en archivos distintos, facilitando el mantenimiento, la prueba y la reutilización de cada parte por separado.

**2. ¿Qué ventajas tiene la programación modular?**
Código más organizado y legible, más fácil de probar y depurar por partes, reutilización de funciones entre distintos scripts, y menor riesgo de que un cambio en una parte rompa el resto del programa.

**3. ¿Qué módulo se encarga de cargar datos desde la base?**
`carga_base_datos.py`.

**4. ¿Qué módulo se encarga de leer archivos CSV?**
`carga_csv.py`.

**5. ¿Qué módulo se encarga de limpiar y validar datos?**
`sanitacion.py`.

**6. ¿Qué módulo se encarga del procesamiento emocional?**
`procesamiento_emocional.py`.

**7. ¿Qué módulo se encarga de enriquecer las evaluaciones con usuarios y contextos?**
`generacion_evaluaciones.py`.

**8. ¿Qué módulo se encarga de responder las preguntas de análisis?**
`analisis_evaluaciones.py`.

**9. ¿Qué ventajas tiene usar funciones?**
Evitan repetir código, permiten aislar y probar una lógica puntual, hacen el código más legible al darle un nombre a un bloque de lógica, y facilitan reutilizarla en distintos contextos (por ejemplo, `convertir_a_float()` se usa tanto para valencia como para activación).

**10. ¿Qué significa que una función tenga parámetros?**
Que recibe datos de entrada (argumentos) que puede usar dentro de su lógica en lugar de depender siempre de las mismas variables fijas; por ejemplo, `convertir_a_float(valor, nombre_campo)` recibe el valor a convertir y el nombre del campo, para poder armar un mensaje de error específico.

**11. ¿Qué significa que una función retorne valores?**
Que al finalizar su ejecución entrega un resultado (con `return`) que quien la llamó puede usar o guardar en una variable; por ejemplo, `validar_valencia()` retorna una tupla `(es_valida, error)`.

**12. ¿Por qué no conviene repetir código?**
Porque duplicar lógica aumenta el riesgo de errores (si hay que corregir algo, hay que recordar cambiarlo en todos los lugares donde se copió), dificulta el mantenimiento y hace el programa más largo e inconsistente.

**13. ¿Qué diferencia hay entre una variable local y una variable global?**
Una variable local se crea dentro de una función y solo existe y es accesible dentro de ella; una variable global se define fuera de las funciones, a nivel de módulo, y puede ser leída (y, con cuidado, modificada) desde distintas partes del código.

**13. ¿Por qué se usa pandas?**
Porque el proyecto trabaja con miles de registros tabulares (el CSV y los resultados de consultas SQL), y pandas permite leer, transformar, filtrar, agrupar y exportar esos datos de forma mucho más simple y eficiente que iterando manualmente fila por fila con estructuras nativas de Python.

**14. ¿Por qué una parte de los datos se carga desde CSV?**
Para reflejar un escenario real de integración: no todos los datos de un sistema viven en la misma fuente (los registros afectivos podrían provenir de una app externa que exporta un CSV), lo que obliga a integrar y validar información entre un archivo plano y una base de datos.

**15. ¿Por qué se validan los datos antes de analizarlos?**
Porque cualquier análisis o cálculo hecho sobre datos incorrectos (valores fuera de rango, no numéricos, referencias inexistentes) produciría resultados erróneos o haría fallar el programa, aunque la lógica de análisis en sí esté bien implementada.

**16. ¿Por qué se separan registros válidos e inválidos?**
Para poder seguir trabajando y analizando solo con los datos confiables, y a la vez conservar un registro auditable de las filas que fallaron y por qué motivo, sin mezclarlas con los datos limpios.

**17. ¿Por qué se incorporan datos de usuario y contexto en la evaluación final?**
Para que el archivo final sea autocontenido y permita hacer análisis y reportes (por nombre, edad, género, actividad, ubicación) sin tener que volver a consultar la base de datos cada vez que se necesite esa información.

**18. ¿Qué limitaciones tiene el sistema actual?**
Las etiquetas emocionales dependen de rangos predefinidos en la base de datos; el sistema no interpreta el contenido textual del comentario; no evalúa qué tan confiable es el origen de la valencia/activación; la validación de fecha solo controla que sea convertible a `datetime`, no que sea una fecha plausible (por ejemplo, una fecha `2099-01-01` pasaría la validación); la clasificación en 8 etiquetas y 5 cuadrantes es una simplificación del espectro emocional real; y el análisis no reemplaza la interpretación docente o humana.

**19. Si aparece una valencia igual a 1.5, ¿qué debería hacer el sistema?**
`validar_valencia()` detecta que 1,5 está fuera del rango permitido [-1, 1] y devuelve `False` con el mensaje `"valencia fuera de rango: 1.5"`. Ese registro queda marcado con `error_rango_valencia`, se considera inválido y se excluye del procesamiento emocional, quedando registrado en `registros_afectivos_invalidos.csv`.

**20. Si aparece una activación igual a -2, ¿qué debería hacer el sistema?**
De la misma forma, `validar_activacion()` detecta que -2 está fuera del rango [-1, 1] y devuelve `False` con el mensaje `"activacion fuera de rango: -2"`. El registro se marca como inválido y no se procesa emocionalmente.

**21. Si aparece un usuario que no existe en la base de datos, ¿qué debería hacer el sistema?**
`validar_usuarios_en_registros()` marca ese registro con `error_usuario = "id_usuario inexistente: N"` y `usuario_valido = False`. El registro se considera inválido y termina en `registros_afectivos_invalidos.csv`, sin participar del análisis.

**22. Si aparece un contexto inexistente, ¿qué debería hacer el sistema?**
Análogamente, `validar_contextos_en_registros()` marca el registro con `error_contexto = "id_contexto inexistente: N"` y `contexto_valido = False`, y el registro queda excluido del conjunto de registros válidos.
