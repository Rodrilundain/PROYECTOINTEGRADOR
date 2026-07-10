Sistema de análisis de evaluaciones emocionales a partir de registros afectivos
Documentación final del proyecto integrador
Integrantes: Rodrigo Ilundain, Franklin Barreto
Curso: Insight AI
Docente: Juan Francisco Rodríguez, Mario Ottati, Pablo Casanova, Claudia
Fecha: [Completar fecha de entrega]











2. Descripción general del problema
El objetivo de este proyecto es analizar el estado emocional de un grupo de estudiantes a partir de los registros afectivos que se fueron generando durante distintas actividades del curso, como prácticas, trabajos, evaluaciones, foros y otras instancias de participación.
Para poder hacer esto, el sistema trabaja con dos fuentes de información. Por un lado, una base de datos donde ya está almacenada la información de los usuarios, los contextos de cada actividad y las reglas que definen cada emoción. Por otro lado, recibe un archivo CSV con todos los registros afectivos.
Cada registro contiene el usuario que lo generó, el contexto donde ocurrió, la fecha y hora, dos valores numéricos llamados valencia y activación, y un comentario opcional.
Estos dos valores son simplemente números entre -1 y 1. Por sí solos no dicen si una persona estaba frustrada, tranquila o entusiasmada. Esa interpretación la hace el sistema durante el procesamiento.
Una vez que toda la información es validada y procesada, el programa genera un nuevo archivo donde cada registro queda mucho más completo. Además de conservar los datos originales, agrega información del usuario, del contexto y una interpretación emocional calculada automáticamente, indicando la intensidad de la emoción, el cuadrante emocional al que pertenece y una etiqueta como Entusiasta, Frustrado, Calmo o Neutro.
Con ese archivo final también se generan distintos análisis y gráficos que permiten obtener una visión general de cómo evolucionó el estado emocional de los estudiantes.
La idea principal del sistema no es reemplazar el criterio de un docente, sino facilitar el análisis cuando existe una gran cantidad de registros. En lugar de revisar miles de filas una por una, el sistema resume la información y ayuda a detectar tendencias, como qué actividades generan más frustración, cuáles producen mayor entusiasmo o qué estudiantes presentan una mayor variación emocional a lo largo del curso.

3. Descripción del dataset
3.1 Base de datos
Para este proyecto trabajamos con una base de datos MySQL que contiene toda la información necesaria para poder interpretar los registros afectivos.
La base está formada por cuatro tablas principales, aunque durante el procesamiento se utilizan especialmente tres de ellas como tablas de referencia.
Tabla usuarios
En esta tabla se almacena la información de cada estudiante.
Los datos principales son:
id_usuario
nombre
edad
género
Cada usuario tiene un identificador único que permite relacionarlo con los registros afectivos. Gracias a esta tabla después podemos saber quién generó cada registro y realizar análisis individuales, como descubrir cuál es la emoción predominante de cada estudiante o qué tan variable fue su comportamiento emocional durante el curso.
La tabla cuenta con 30 usuarios cargados.


Tabla contextos
Esta tabla describe el lugar o la actividad donde ocurrió cada registro afectivo.
Entre sus campos principales se encuentran:
id_contexto
origen
actividad
ubicación
descripción
Su función es agregar contexto a cada registro. No es lo mismo una emoción registrada durante un examen que durante un trabajo en equipo o una práctica de laboratorio.
Actualmente la base contiene 45 contextos diferentes, aunque para este proyecto solamente se utilizaron 12 de ellos.

Tabla etiquetas emocionales
Esta tabla es una de las más importantes del sistema porque define cómo interpretar las emociones.
Cada registro contiene:
id_etiqueta
nombre de la emoción
rango mínimo y máximo de valencia
rango mínimo y máximo de activación
cuadrante emocional
A partir de estos rangos el programa puede determinar automáticamente si un registro corresponde a emociones como Entusiasta, Calmo, Frustrado, Triste, Alerta, Neutro, Tenso o Cansado.
En total se utilizan 8 etiquetas emocionales.
Tabla registros afectivos
Esta tabla representa la estructura de los registros afectivos dentro de la base de datos.
Contiene información como:
id_registro
id_usuario
id_contexto
fecha y hora
valencia
activación
comentario
En este proyecto los registros no se leen directamente desde la base de datos, sino desde un archivo CSV. Sin embargo, esta tabla sirve como modelo para mantener la estructura de la información y validar que los datos respeten las relaciones entre usuarios y contextos.
Además, incluye restricciones para asegurar que los valores de valencia y activación siempre se encuentren dentro del rango permitido, que va desde -1 hasta 1.

3.2 Archivo CSV
El segundo origen de datos del proyecto es el archivo registros_afectivos.csv, que contiene 6.054 registros.
Cada fila representa un evento emocional y guarda la siguiente información:
id del registro
usuario que lo generó
contexto donde ocurrió
fecha y hora
valor de valencia
valor de activación
comentario opcional
Este archivo es el punto de partida del procesamiento.
Sin embargo, fue preparado con distintos errores de forma intencional para poner a prueba el sistema de validación.
Durante la carga pueden aparecer situaciones como:
valores escritos como texto donde debería haber números;
valores fuera del rango permitido;
fechas inválidas o vacías;
registros duplicados;
comentarios con problemas de codificación;
información incompleta.
Antes de comenzar cualquier análisis, el programa revisa todos esos datos, identifica los errores y separa los registros válidos de los inválidos para trabajar únicamente con información confiable.







4. Modelo de datos
Modelo Entidad-Relación (MER)
Antes de empezar a programar fue necesario definir cómo se iba a organizar toda la información. Para eso se diseñó un Modelo Entidad-Relación (MER), que muestra cómo se conectan los datos entre sí.
En este proyecto se trabajó con cuatro entidades principales:
Usuarios: almacena la información de cada estudiante.
Registros afectivos: guarda cada emoción registrada durante una actividad.
Contextos: describe en qué situación o actividad ocurrió cada registro.
Etiquetas emocionales: contiene las reglas que utiliza el sistema para interpretar cada emoción.
La relación principal del modelo es sencilla:
Un usuario puede generar muchos registros afectivos.
Cada registro afectivo pertenece únicamente a un usuario.
Un contexto puede aparecer en muchos registros.
Cada registro afectivo ocurre en un solo contexto.
Las etiquetas emocionales funcionan de una forma un poco diferente. No están relacionadas mediante una clave foránea, sino que el programa las utiliza durante el procesamiento para comparar los valores de valencia y activación de cada registro y determinar qué emoción le corresponde.

Pasaje del MER a las tablas
Una vez definido el modelo, cada entidad se convirtió en una tabla dentro de la base de datos.
Cada tabla tiene su propia clave primaria, que identifica de forma única cada registro.
Para relacionarlas entre sí se utilizaron claves foráneas. Por ejemplo, en la tabla registros_afectivos se almacenan los campos id_usuario e id_contexto, que permiten saber qué estudiante generó el registro y en qué actividad ocurrió.
De esta manera no es necesario repetir el nombre del usuario o la descripción del contexto en miles de filas diferentes. Si esa información cambia, solamente se actualiza una vez en su tabla correspondiente.
Normalización de la base de datos
La base fue diseñada siguiendo las primeras tres formas normales, con el objetivo de mantener la información organizada y evitar datos repetidos.
Primera Forma Normal (1FN)
Cada campo almacena un único dato. Es decir, no existen listas ni varios valores dentro de una misma celda.
Segunda Forma Normal (2FN)
Cada tabla tiene una única clave primaria y todos los datos dependen directamente de esa clave. Esto evita dependencias parciales y mantiene la información correctamente organizada.
Tercera Forma Normal (3FN)
La información se almacena únicamente donde corresponde.
Por ejemplo, el nombre, la edad y el género de un estudiante se guardan únicamente en la tabla usuarios y no se repiten en cada registro afectivo. Esto reduce la duplicación de datos y hace que la base sea mucho más fácil de mantener.

Relación entre las tablas
El vínculo entre las tablas permite que el sistema combine información de diferentes lugares durante el procesamiento.
Cuando el programa lee un registro afectivo, primero identifica qué usuario lo generó utilizando el id_usuario. Luego busca el id_contexto para obtener información sobre la actividad donde ocurrió.
Finalmente compara los valores de valencia y activación con los rangos definidos en la tabla etiquetas_emocionales para asignar automáticamente una emoción.
Gracias a esta estructura, el archivo CSV solamente necesita contener la información básica. Todo el resto de los datos se incorporan automáticamente durante el procesamiento.

¿Por qué la emoción no viene calculada en el CSV?
Se decidió que el archivo CSV guardara únicamente los datos originales y que la interpretación emocional se realizara dentro del programa.
Esto tiene una ventaja importante: si en el futuro se quiere modificar el criterio con el que se clasifican las emociones, alcanza con actualizar los rangos de la tabla etiquetas_emocionales.
De esta forma no es necesario modificar el archivo original ni volver a generarlo. Simplemente se vuelve a ejecutar el programa y todas las evaluaciones se recalculan utilizando las nuevas reglas.
Además, este enfoque mantiene separados los datos originales de la lógica del sistema, haciendo que el proyecto sea más flexible y mucho más fácil de mantener.
5. Organización modular del programa
Desde el principio se decidió dividir el proyecto en varios módulos, en lugar de escribir todo el código dentro de un único archivo.
La idea fue que cada módulo tuviera una responsabilidad específica. De esa manera el código queda más ordenado, es más fácil encontrar un problema cuando aparece un error y también resulta mucho más sencillo realizar cambios sin afectar el resto del sistema.
A continuación se explica qué hace cada módulo.

carga_base_datos.py
Este módulo se encarga de conectarse a la base de datos y cargar toda la información que el programa necesita para trabajar.
Desde aquí se obtienen los usuarios, los contextos y las etiquetas emocionales que después utilizarán los demás módulos durante el procesamiento.
También es el encargado de cerrar correctamente la conexión una vez que el programa termina de utilizar la base de datos.

carga_csv.py
Su función es leer el archivo registros_afectivos.csv.
Además de cargar la información, verifica que el archivo tenga todas las columnas obligatorias y contempla posibles problemas de codificación. Si el archivo no puede leerse con UTF-8, intenta nuevamente utilizando otra codificación para evitar errores durante la carga.

sanitacion.py
Este es uno de los módulos más importantes del proyecto.
Su trabajo consiste en revisar cada registro del archivo CSV para comprobar que la información sea válida.
Durante esta etapa se detectan registros duplicados, valores fuera de rango, fechas incorrectas, usuarios inexistentes, contextos inválidos y cualquier otro dato que pueda afectar los resultados.
Al finalizar la validación, el programa separa los registros válidos de los inválidos y genera un resumen con todos los errores encontrados.
Gracias a este proceso, el resto del sistema trabaja únicamente con datos confiables.

procesamiento_emocional.py
Una vez que los datos fueron validados, este módulo realiza la parte principal del proyecto.
Aquí se calcula la intensidad emocional de cada registro, se determina el cuadrante al que pertenece y finalmente se asigna una etiqueta emocional comparando los valores de valencia y activación con los rangos definidos en la base de datos.
En otras palabras, es el módulo que transforma dos números en una emoción que cualquier persona puede interpretar.

generacion_evaluaciones.py
Después de calcular las emociones, este módulo completa la información de cada registro.
Toma los resultados obtenidos en el procesamiento emocional y les agrega los datos del usuario y del contexto.
El resultado es el archivo final, donde cada registro ya contiene toda la información necesaria para realizar análisis o generar reportes.

analisis_evaluaciones.py
Con el archivo final ya generado, este módulo realiza los distintos análisis del proyecto.
Entre otras cosas permite identificar:
la emoción predominante de cada usuario;
la emoción predominante en cada contexto;
los usuarios con mayor variabilidad emocional;
los contextos con emociones más negativas;
los promedios por etiqueta emocional;
la distribución general de todas las emociones registradas.
Toda esta información sirve para entender mejor el comportamiento de los datos sin tener que revisar miles de registros manualmente.

visualizaciones.py
El último módulo se encarga de generar todos los gráficos utilizados en el proyecto.
A partir del archivo final crea gráficos de barras, dispersión, series temporales y rankings que permiten visualizar la información de una manera mucho más clara y facilitar su interpretación.


Organización de la ejecución
Además de separar la lógica en módulos, también se decidió dividir la ejecución del proyecto en diferentes scripts.
Cada uno ejecuta una etapa específica del proceso, lo que permite probar cada paso por separado sin tener que correr todo el programa nuevamente.
Los scripts principales son:
main_sanitacion.py: carga los datos, realiza la validación y genera los archivos con registros válidos e inválidos.
main_procesamiento_emocional.py: toma los registros válidos y calcula la evaluación emocional de cada uno.
main_gen_extension_evaluaciones_paso3.py: agrega la información de usuarios y contextos para generar el archivo final del proyecto.
main_analisis_evaluaciones_paso4.py: ejecuta todos los análisis estadísticos definidos para el proyecto.
main_visualizaciones_paso5.py: genera los gráficos finales a partir de la información procesada.

Flujo general del proyecto
En términos simples, el funcionamiento del sistema sigue siempre el mismo recorrido.
Primero se cargan los datos desde la base de datos y desde el archivo CSV.
Luego se validan todos los registros para detectar posibles errores.
Una vez que la información está limpia, el programa calcula la emoción correspondiente a cada registro.
Después incorpora los datos del usuario y del contexto para completar la información.
Finalmente, con todos los datos ya procesados, genera los análisis y las visualizaciones que permiten interpretar los resultados de forma sencilla.
Dividir el proyecto de esta manera hizo que cada parte tuviera una función bien definida, facilitando tanto el desarrollo como el mantenimiento del sistema.
6. Limpieza y validación de datos
Antes de empezar a realizar cualquier cálculo, el programa verifica que toda la información del archivo CSV sea correcta. Esta etapa es fundamental, porque si los datos de entrada tienen errores, los resultados finales también serán incorrectos.
Para realizar esta tarea se desarrolló el módulo sanitacion.py, cuya función es revisar cada registro y detectar cualquier problema que pueda afectar el procesamiento.
Durante esta validación se controlan distintos aspectos de la información.
Validaciones realizadas
El sistema verifica que:
Los campos de valencia, activación y fecha no estén vacíos.
Los valores de valencia y activación sean realmente números.
Esos valores se encuentren dentro del rango permitido, que va desde -1 hasta 1.
La fecha tenga un formato válido.
El usuario exista en la base de datos.
El contexto también exista en la base de datos.
No haya registros duplicados.
Los comentarios vacíos o con valores como "null", "none", "n/a" o "sin dato" se sustituyan automáticamente por "No informado", sin descartar el registro.
Cada una de estas verificaciones ayuda a garantizar que el sistema trabaje únicamente con información consistente.





Resultados obtenidos
Luego de ejecutar todas las validaciones sobre el archivo original, se obtuvieron los siguientes resultados:
Resultado
Cantidad
Registros procesados
6.054
Registros válidos
5.894
Registros inválidos
160
Total de errores detectados
240

Esto significa que aproximadamente el 97,4 % de los registros pudieron utilizarse para el análisis, mientras que solamente un 2,6 % fueron descartados por presentar algún tipo de inconveniente.

Tipos de errores encontrados
Los errores detectados durante la validación fueron los siguientes:
Tipo de error
Cantidad
Valencia no numérica
40
Valencia fuera de rango
60
Activación no numérica
40
Activación fuera de rango
60
Fecha inválida
20
Usuario inexistente
0
Contexto inexistente
0
Registros duplicados
20

Estos resultados muestran que la mayoría de los problemas estuvieron relacionados con valores incorrectos en los campos de valencia y activación.
Por otro lado, no se encontraron registros que hicieran referencia a usuarios o contextos inexistentes, lo que indica que esas relaciones estaban correctamente definidas.

¿Por qué aparecen más errores que registros inválidos?
A simple vista puede parecer raro que existan 240 errores, pero solamente 160 registros inválidos.
La explicación es sencilla: un mismo registro puede tener más de un problema al mismo tiempo.
Por ejemplo, si el valor de activación contiene el texto "sin_dato", primero falla la conversión a número y, además, tampoco es posible comprobar si ese valor está dentro del rango permitido.
En ese caso, el mismo registro acumula dos errores diferentes.
Por eso un registro puede aparecer una sola vez como inválido, pero tener más de un motivo por el cual fue descartado.

¿Por qué fue importante esta etapa?
La limpieza de datos fue una de las partes más importantes del proyecto.
Si el programa hubiera procesado directamente el archivo original sin realizar estas verificaciones, los análisis, los gráficos y las estadísticas podrían haber dado resultados incorrectos.
Gracias a esta etapa, solamente los registros confiables continuaron con el procesamiento emocional.
Además, el sistema no elimina la información con errores. Los registros inválidos se guardan en un archivo independiente para que puedan revisarse más adelante y entender qué ocurrió en cada caso.
Esto permite mantener la trazabilidad de los datos y facilita futuras correcciones sin modificar el archivo original.










7. Procesamiento emocional
Una vez que los registros fueron validados y se confirmó que los datos eran correctos, el programa comienza con el procesamiento emocional.
En esta etapa, los valores de valencia y activación dejan de ser simplemente números y pasan a convertirse en información que cualquier persona puede interpretar.
El objetivo es identificar qué emoción representa cada registro y medir qué tan intensa fue.

¿Qué es la valencia?
La valencia indica si una emoción es más positiva o más negativa.
Su valor puede ir desde -1 hasta 1.
Valores cercanos a -1 representan emociones negativas.
Valores cercanos a 1 representan emociones positivas.
Valores cercanos a 0 indican una emoción neutral.
La valencia permite saber cómo se siente una persona, pero por sí sola no alcanza para interpretar completamente una emoción.


¿Qué es la activación?
La activación representa el nivel de energía con el que se experimenta una emoción.
También toma valores entre -1 y 1.
Valores altos indican emociones con mayor energía o intensidad.
Valores bajos representan estados más tranquilos o relajados.
Valores cercanos a cero muestran un nivel intermedio de activación.
Al combinar la activación con la valencia es posible diferenciar emociones que pueden parecer similares, pero que en realidad tienen comportamientos distintos.

Cálculo de la intensidad emocional
Después de obtener ambos valores, el programa calcula la intensidad emocional de cada registro.
La intensidad permite medir qué tan fuerte fue la emoción registrada.
Por ejemplo, dos personas pueden clasificarse como Entusiastas, pero una puede haber sentido un entusiasmo moderado y la otra un entusiasmo muy intenso.
La etiqueta será la misma, pero la intensidad será diferente.
Por eso este cálculo agrega información que no se obtiene solamente mirando la categoría emocional.

Intensidad normalizada
Como la intensidad puede tomar valores superiores a 1, el sistema también calcula una versión normalizada.
Esto permite que todas las intensidades queden dentro de una misma escala y puedan compararse fácilmente entre distintos registros, usuarios o contextos.
Gracias a esta normalización, los análisis posteriores son mucho más consistentes.

Cuadrante emocional
Una vez calculada la intensidad, el sistema determina en qué cuadrante emocional se encuentra cada registro.
Para hacerlo combina los valores de valencia y activación.
Según esos valores, el registro puede clasificarse como:
Positiva - Alta
Positiva - Baja
Negativa - Alta
Negativa - Baja
Centro
El cuadrante Centro se utiliza para aquellos registros cuyos valores están muy cerca del punto neutro.
De esta forma se evita clasificar como positiva o negativa una emoción que, en realidad, prácticamente no presenta una tendencia clara.

Asignación de la etiqueta emocional
Con toda esa información disponible, el programa busca en la tabla etiquetas_emocionales cuál de los rangos coincide con los valores del registro.
Cuando encuentra una coincidencia, asigna automáticamente la emoción correspondiente.
Las etiquetas utilizadas en este proyecto son:
Entusiasta
Calmo
Frustrado
Triste
Tenso
Alerta
Neutro
Cansado
Gracias a este proceso, el sistema transforma datos numéricos en información mucho más fácil de interpretar.
En lugar de ver únicamente valores como 0,62 o -0,48, cualquier persona puede entender rápidamente si el registro representa una emoción positiva, negativa, intensa o neutral.

¿Por qué las etiquetas se obtienen desde la base de datos?
Las reglas que definen cada emoción no están escritas directamente dentro del código.
El programa las carga desde la base de datos cada vez que se ejecuta.
Esta decisión hace que el sistema sea mucho más flexible.
Si en algún momento se quiere modificar el rango de una emoción o agregar una nueva etiqueta, solamente es necesario actualizar la base de datos.
No hace falta modificar el código ni volver a desarrollar el programa.
Esto también facilita el mantenimiento del sistema y permite adaptar las reglas de clasificación sin afectar el resto del proyecto.

Resultado del procesamiento
Una vez finalizada esta etapa, cada registro ya cuenta con:
la intensidad emocional;
la intensidad normalizada;
el cuadrante emocional;
la etiqueta que mejor representa la emoción registrada.
Con esa información ya es posible continuar con la siguiente etapa del proyecto, donde se incorporan los datos del usuario y del contexto para generar el archivo final utilizado en los análisis y las visualizaciones.

8. Archivo final generado
Una vez que termina el procesamiento emocional, el programa genera el archivo final del proyecto llamado evaluaciones_emocionales_extendidas.csv.
Este archivo reúne toda la información procesada en un solo lugar y contiene 5.894 registros, uno por cada registro válido que pasó correctamente todas las validaciones.
Cada fila incluye tanto los datos originales del archivo CSV como toda la información que fue agregando el sistema durante las distintas etapas del procesamiento.

Entre los datos que contiene se encuentran:
Información del usuario (nombre, edad y género).
Información del contexto donde ocurrió el registro.
Fecha y hora del evento.
Valores de valencia y activación.
Comentario asociado.
Intensidad emocional.
Intensidad normalizada.
Cuadrante emocional.
Etiqueta emocional asignada.
Este archivo es el resultado principal del proyecto y sirve como base para generar todos los análisis y gráficos posteriores.
En lugar de tener la información distribuida entre varios archivos y tablas, todo queda integrado en un único archivo listo para ser analizado.
9. Análisis realizados
Con el archivo final ya generado, el sistema realiza distintos análisis para encontrar patrones y facilitar la interpretación de la información.
El objetivo no era solamente clasificar emociones, sino entender qué estaba ocurriendo a nivel general dentro del conjunto de datos.
Emoción predominante por contexto
En este análisis se buscó identificar cuál fue la emoción que apareció con mayor frecuencia en cada actividad o contexto.
Los resultados mostraron que la emoción Neutro fue la predominante en todos los contextos analizados.
Esto indica que, en términos generales, ninguna actividad generó una respuesta emocional extrema de forma sostenida.

Emoción predominante por usuario
También se analizó cuál fue la emoción más frecuente para cada estudiante.
En la mayoría de los casos volvió a aparecer la emoción Neutro como la predominante.
Sin embargo, se detectó un usuario cuya emoción principal fue Frustrado, lo que podría ser una señal para profundizar el análisis si se tratara de un caso real.
Usuarios con mayor variabilidad emocional
Otro análisis consistió en identificar qué estudiantes pasaron por una mayor cantidad de emociones diferentes.
Algunos usuarios registraron las ocho etiquetas emocionales disponibles durante el período analizado.
Esto demuestra que no mantuvieron siempre el mismo estado emocional, sino que fueron cambiando según la actividad realizada o el momento del curso.
Promedio por etiqueta emocional
También se calcularon los valores promedio de valencia, activación e intensidad para cada una de las etiquetas.
Los resultados mostraron que emociones como Frustrado y Entusiasta fueron las que presentaron mayor intensidad promedio.
En cambio, la emoción Neutro, aunque fue la más frecuente, resultó ser la menos intensa.
Esto confirma que una emoción puede aparecer muchas veces sin necesariamente representar una reacción emocional fuerte.
Contextos con menor valencia
El sistema también permitió identificar cuáles fueron las actividades con menor valencia promedio.
Aunque algunos contextos obtuvieron valores ligeramente inferiores al resto, ninguno presentó una tendencia claramente negativa.
Esto indica que el malestar observado en los datos no estuvo concentrado en una única actividad, sino que apareció de forma distribuida entre distintos contextos.
Distribución general de emociones
Por último, se analizó cómo se repartieron todas las emociones dentro del conjunto de datos.
La emoción Neutro fue la más frecuente, representando aproximadamente una cuarta parte de todos los registros.
Detrás aparecieron Frustrado, Alerta y Calmo, mientras que Cansado fue la emoción menos registrada.
Este análisis permitió obtener una visión general del comportamiento emocional de todo el grupo.

¿Qué nos permitieron descubrir estos análisis?
Más allá de los números, estos análisis ayudaron a responder preguntas concretas sobre los datos.
Por ejemplo:
cuáles fueron las emociones más frecuentes;
qué actividades generaron respuestas emocionales más intensas;
qué estudiantes mostraron mayor variabilidad emocional;
si existían contextos especialmente negativos;
cómo se distribuyeron las emociones a lo largo de todo el proyecto.
Gracias a esta información fue posible pasar de miles de registros individuales a una visión mucho más clara del comportamiento general de los estudiantes.




10. Visualizaciones y resultados obtenidos
Una vez finalizado el procesamiento y los análisis, el proyecto genera una serie de gráficos que ayudan a interpretar la información de una forma mucho más visual.
En lugar de revisar miles de registros o tablas con números, estos gráficos permiten identificar rápidamente tendencias, comparar resultados y detectar posibles situaciones que merezcan un análisis más profundo.
Entre las visualizaciones generadas se encuentran:
Gráfico de dispersión: muestra cómo se distribuyen los registros según los valores de valencia y activación, permitiendo observar cómo se agrupan las distintas emociones.
Distribución de emociones: presenta la cantidad de registros correspondientes a cada etiqueta emocional, facilitando una visión general del comportamiento del conjunto de datos.
Promedios por etiqueta: compara los valores promedio de valencia, activación e intensidad para cada emoción.
Serie temporal de intensidad: permite observar cómo fue cambiando la intensidad emocional a lo largo del tiempo.
Ranking de contextos: muestra qué actividades generaron emociones más intensas y cuáles presentaron una menor valencia promedio.
Ranking de usuarios: identifica qué estudiantes registraron una mayor variedad de emociones durante el período analizado.
Cada uno de estos gráficos complementa los análisis realizados anteriormente y facilita la interpretación de los resultados, especialmente para personas que no necesitan revisar el detalle técnico del procesamiento.




11. Resultados principales
Después de analizar toda la información procesada, se obtuvieron varias conclusiones importantes.
La emoción que apareció con mayor frecuencia fue Neutro, lo que indica que, en términos generales, los estudiantes mantuvieron un estado emocional estable durante gran parte de las actividades.
También se observó que emociones como Frustrado y Entusiasta fueron las que presentaron mayor intensidad. Esto significa que, aunque aparecieron menos veces que la emoción neutra, cuando estuvieron presentes lo hicieron con una carga emocional mucho más fuerte.
En cuanto a los contextos analizados, no se detectó ninguna actividad que concentrara de forma clara las emociones negativas. Si bien algunas mostraron valores de valencia algo menores que otras, las diferencias fueron pequeñas y no alcanzan para señalar un contexto como problemático.
Otro aspecto interesante fue la variabilidad emocional de algunos estudiantes. Varios de ellos registraron todas las etiquetas emocionales disponibles durante el período analizado, lo que demuestra que su estado emocional fue cambiando según las distintas actividades realizadas.
En conjunto, los resultados muestran que el sistema logró transformar miles de registros individuales en información útil para comprender el comportamiento general del grupo y detectar patrones que, de otra forma, serían muy difíciles de identificar.





12. Manejo de errores y decisiones de desarrollo
Durante el desarrollo del proyecto también fue necesario tomar varias decisiones técnicas para lograr que el sistema fuera más robusto y fácil de mantener.
Una de ellas fue utilizar bloques try-except-finally, que permiten controlar errores sin que el programa se detenga inesperadamente. De esta manera, si ocurre un problema durante la lectura de un archivo o la conexión con la base de datos, el sistema puede informar el error de forma clara y finalizar correctamente.
También se decidió cerrar siempre la conexión con la base de datos utilizando el bloque finally. Esto asegura que los recursos se liberen correctamente, incluso cuando ocurre algún error durante la ejecución.
Otra decisión importante fue separar los registros válidos de los inválidos. Gracias a esto, los errores encontrados en algunos registros no impiden continuar trabajando con el resto de la información. Además, los registros descartados quedan almacenados en un archivo independiente para poder revisarlos posteriormente.
El proyecto también fue organizado en módulos y funciones para evitar repetir código y facilitar su mantenimiento. Si en el futuro es necesario modificar una parte del sistema, el cambio puede realizarse sin afectar el resto del proyecto.
Por último, se eligió trabajar con la biblioteca pandas, ya que permite manipular grandes volúmenes de datos de forma mucho más sencilla y eficiente, especialmente cuando se trabaja con archivos CSV y consultas provenientes de una base de datos.
Todas estas decisiones ayudaron a desarrollar un proyecto más ordenado, reutilizable y preparado para futuras mejoras.



13. Limitaciones del sistema
Como cualquier desarrollo, este proyecto también tiene algunas limitaciones que es importante tener presentes.
La primera es que la clasificación de las emociones depende completamente de los rangos definidos en la base de datos. Si esos rangos no representan correctamente cada emoción, los resultados obtenidos también pueden verse afectados.
Otra limitación es que el sistema no interpreta el contenido de los comentarios escritos por los usuarios. Actualmente solamente utiliza los valores de valencia y activación para realizar la clasificación. Esto significa que dos comentarios completamente diferentes pueden recibir la misma etiqueta emocional si sus valores numéricos son iguales.
Además, el programa asume que los valores de valencia y activación ya fueron obtenidos correctamente. Es decir, no analiza cómo se generaron esos datos ni puede comprobar si representan realmente la emoción de la persona.
En cuanto a la validación de fechas, el sistema verifica que tengan un formato correcto, pero no determina si esa fecha tiene sentido dentro del contexto del proyecto. Por ejemplo, una fecha como 2099 tiene un formato válido y actualmente sería aceptada.
Por último, el análisis realizado sirve como una herramienta de apoyo para la toma de decisiones, pero no reemplaza el criterio de una persona. Los resultados muestran tendencias y patrones, aunque siempre deben interpretarse considerando el contexto en el que fueron generados.





14. Posibles mejoras
Durante el desarrollo surgieron varias ideas que podrían implementarse en futuras versiones para ampliar las funcionalidades del sistema.
Una de las mejoras más interesantes sería incorporar análisis del texto de los comentarios utilizando técnicas de procesamiento de lenguaje natural o inteligencia artificial. De esa forma no solo se analizarían los valores numéricos, sino también el contenido escrito por los usuarios.
También sería útil desarrollar una interfaz gráfica que permita ejecutar todo el proceso sin necesidad de utilizar la consola. Esto haría que cualquier usuario pudiera utilizar el sistema de una forma mucho más sencilla.
Otra mejora posible sería guardar automáticamente las evaluaciones emocionales nuevamente en la base de datos, evitando depender únicamente de archivos CSV para almacenar los resultados.
También sería interesante permitir que las etiquetas emocionales y sus rangos pudieran modificarse desde una interfaz de administración, sin necesidad de acceder directamente a la base de datos.
Por último, podrían incorporarse nuevos gráficos, filtros por fecha, usuario o contexto, e incluso generar reportes automáticos que faciliten todavía más el análisis de la información.
Todas estas mejoras permitirían que el sistema fuera más completo, más flexible y más fácil de utilizar.




15. Conclusión
Este proyecto nos permitió recorrer todas las etapas de un proceso de análisis de datos, desde la carga de la información hasta la generación de reportes y visualizaciones.
Durante el desarrollo trabajamos con datos provenientes de distintas fuentes, realizamos procesos de validación y limpieza, procesamos la información emocional y finalmente obtuvimos análisis que facilitaron la interpretación de los resultados.
Uno de los aprendizajes más importantes fue entender que un buen análisis no depende solamente del código. Antes de obtener cualquier resultado, fue necesario asegurarse de que los datos fueran confiables. Esa etapa de validación terminó siendo tan importante como el procesamiento posterior.
También quedó claro el valor de organizar el proyecto en módulos independientes. Esto hizo que el código fuera más ordenado, más fácil de mantener y mucho más simple de ampliar en el futuro.
Más allá de cumplir con los objetivos planteados para el proyecto, este trabajo nos permitió aplicar en un caso práctico muchos de los conceptos vistos durante el curso, como bases de datos relacionales, lectura de archivos CSV, validación de datos, programación modular, procesamiento de información y generación de reportes.
En lo personal, este proyecto también nos permitió entender que el verdadero valor de un sistema no está solamente en procesar datos, sino en transformarlos en información útil para que una persona pueda interpretarla y tomar mejores decisiones.
Creemos que el resultado obtenido cumple con los objetivos propuestos y deja una base sólida sobre la cual se pueden seguir incorporando nuevas funcionalidades y mejoras en futuras versiones.

