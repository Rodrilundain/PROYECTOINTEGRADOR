import pymysql
import pandas as pd
import math
from pathlib import Path
import carga_base_datos
import carga_csv
import sanitacion

####Responsabilidad: calcular los valores derivados de cada registro afectivo.
####Funciones posibles:
####calcular_intensidad()
####calcular_intensidad_normalizada()
####determinar_cuadrante()
####clasificar_emocion()
####Ejemplo de datos calculados:
####intensidad
####cuadrante
####etiqueta_emocional
####La etiqueta emocional se genera en este módulo, no viene ya resuelta en el CSV.
##Seudocodigo
##
##FUNCIÓN calcular_intensidad(valencia, activacion)
##
####    Calcula la intensidad emocional a partir de valencia y activación.  Porque es interesante? Ejemplo:
####    Registro A
####    valencia = 0.40
####    activación = 0.45
####    etiqueta = Entusiasta
####
####    Registro B
####    valencia = 0.95
####    activación = 0.90
####    etiqueta = Entusiasta
####    Pero se observa que en registro B esta mucho mas intenso que el A
##
##
##
##    intensidad = RAÍZ_CUADRADA(valencia² + activacion²)
##
##    RETORNAR intensidad
##
##FIN FUNCIÓN
##
##
##
##FUNCIÓN calcular_intensidad_normalizada(intensidad)
######    porque la intensidad puede pasar el valor de 1
##    intensidad_normalizada = intensidad / RAÍZ_CUADRADA(2)
##
##    RETORNAR intensidad_normalizada
##
##FIN FUNCIÓN
####
####
####
##FUNCIÓN determinar_cuadrante(valencia, activacion, umbral_centro)
##
#### El umbral centro es un valor que usamos para decidir cuándo una emoción es tan cercana al punto
#### neutro que conviene clasificarla como “Centro” o “Neutra”, en lugar de forzarla a un cuadrante. Por ejemplo 0.3
##
##    SI valor_absoluto(valencia) < umbral_centro Y valor_absoluto(activacion) < umbral_centro ENTONCES
##        RETORNAR "Centro"
##    FIN SI
##
##    SI valencia >= 0 Y activacion >= 0 ENTONCES
##        RETORNAR "Positiva-Alta"
##
##    SINO SI valencia >= 0 Y activacion < 0 ENTONCES
##        RETORNAR "Positiva-Baja"
##
##    SINO SI valencia < 0 Y activacion >= 0 ENTONCES
##        RETORNAR "Negativa-Alta"
##
##    SINO
##        RETORNAR "Negativa-Baja"
##    FIN SI
##
##FIN FUNCIÓN
####
##
##
##FUNCIÓN clasificar_emocion(valencia, activacion, etiquetas)
##
##    PARA CADA etiqueta EN etiquetas HACER
##
##        cumple_valencia = valencia >= etiqueta.valencia_min Y valencia <= etiqueta.valencia_max
##
##        cumple_activacion = activacion >= etiqueta.activacion_min Y activacion <= etiqueta.activacion_max
##
##        SI cumple_valencia Y cumple_activacion ENTONCES
##            RETORNAR etiqueta.nombre_etiqueta
##        FIN SI
##
##    FIN PARA
##
##    RETORNAR "Sin clasificar"
##
##FIN FUNCIÓN
##
##
##
##FUNCIÓN procesar_emociones(registros_validos, etiquetas)
##
##    PARA CADA registro EN registros_validos HACER
##
##        valencia = registro.valencia
##        activacion = registro.activacion
##
##        intensidad = calcular_intensidad(valencia, activacion)
##
##        intensidad_normalizada = calcular_intensidad_normalizada(intensidad)
##
##        cuadrante = determinar_cuadrante(valencia, activacion, 0.30)
##
##        etiqueta_emocional = clasificar_emocion(valencia, activacion, etiquetas)
##
##        agregar intensidad al registro
##
##        agregar intensidad_normalizada al registro
##
##        agregar cuadrante al registro
##
##        agregar etiqueta_emocional al registro
##
##    FIN PARA
##
##    RETORNAR registros_validos procesados
##
##FIN FUNCIÓN
##
##
##Flujo general del módulo:
##
##INICIO
##
##    recibir registros_validos (de  csv)
##    recibir etiquetas_emocionales (de la BD)
##    evaluaciones_emocionales = procesar_emociones(registros_validos, etiquetas_emocionales)
##    mostrar primeras evaluaciones emocionales
##
##FIN
##
##

##FUNCIÓN calcular_intensidad(valencia, activacion)

##
##
##
##    intensidad = RAÍZ_CUADRADA(valencia² + activacion²)
##
##    RETORNAR intensidad
##
##FIN FUNCIÓN




import math

def calcular_intensidad(valencia, activacion):
    """
    Calcula la intensidad emocional a partir de valencia y activación.  Porque es interesante? Ejemplo:
    Registro A
    valencia = 0.40
    activación = 0.45
    etiqueta = Entusiasta

    Registro B
    valencia = 0.95
    activación = 0.90
    etiqueta = Entusiasta
    Pero se observa que en registro B esta mucho mas intenso que el A

    """

    intensidad = math.sqrt(valencia**2 + activacion**2)

    return intensidad







def calcular_intensidad_normalizada(intensidad):
    """
    Normaliza la intensidad emocional al rango aproximado 0 a 1. Esto se debe a que la intensidad puede pasar el valor de 1
    """

    intensidad_normalizada = intensidad / math.sqrt(2)

    return intensidad_normalizada

##FUNCIÓN determinar_cuadrante(valencia, activacion, umbral_centro)
##
#### El umbral centro es un valor que usamos para decidir cuándo una emoción es tan cercana al punto
#### neutro que conviene clasificarla como “Centro” o “Neutra”, en lugar de forzarla a un cuadrante. Por ejemplo 0.3
##
##    SI valor_absoluto(valencia) < umbral_centro Y valor_absoluto(activacion) < umbral_centro ENTONCES
##        RETORNAR "Centro"
##    FIN SI
##
##    SI valencia >= 0 Y activacion >= 0 ENTONCES
##        RETORNAR "Positiva-Alta"
##
##    SINO SI valencia >= 0 Y activacion < 0 ENTONCES
##        RETORNAR "Positiva-Baja"
##
##    SINO SI valencia < 0 Y activacion >= 0 ENTONCES
##        RETORNAR "Negativa-Alta"
##
##    SINO
##        RETORNAR "Negativa-Baja"
##    FIN SI
##
##FIN FUNCIÓN



def determinar_cuadrante(valencia, activacion, umbral_centro=0.30):
    """
    Determina el cuadrante emocional según valencia y activación. El umbral centro es un valor que usamos para decidir cuándo una emoción es tan cercana al punto neutro que conviene
    clasificarla como “Centro” o “Neutra”, en lugar de forzarla a un cuadrante. Por ejemplo 0.3
    """

    if abs(valencia) < umbral_centro and abs(activacion) < umbral_centro:
        return "Centro"

    if valencia >= 0 and activacion >= 0:
        return "Positiva-Alta"

    elif valencia >= 0 and activacion < 0:
        return "Positiva-Baja"

    elif valencia < 0 and activacion >= 0:
        return "Negativa-Alta"

    else:
        return "Negativa-Baja"


def clasificar_emocion(valencia, activacion, df_etiquetas):
    """
    Clasifica la emoción usando los rangos definidos en la tabla etiquetas_emocionales.
    """

    for _, etiqueta in df_etiquetas.iterrows():    ## el iterrow devuelve dos datos: el indice y la etiqueta en este caso, el _ indica que no lo voy a utilizar (al indice)

        cumple_valencia = (
            valencia >= etiqueta["valencia_min"]
            and valencia <= etiqueta["valencia_max"]
        )

        cumple_activacion = (
            activacion >= etiqueta["activacion_min"]
            and activacion <= etiqueta["activacion_max"]
        )

        if cumple_valencia and cumple_activacion:
            return etiqueta["nombre_etiqueta"]

    return "Sin clasificar"

def procesar_emociones(df_registros_validos, df_etiquetas):
    """
    Agrega intensidad, intensidad normalizada, cuadrante y etiqueta emocional.
    """

    df_registros_validos = df_registros_validos.copy()

    df_registros_validos["intensidad"] = df_registros_validos.apply(
        lambda fila: calcular_intensidad(
            fila["valencia"],
            fila["activacion"]
        ),
        axis=1
    )

    df_registros_validos["intensidad_normalizada"] = df_registros_validos["intensidad"].apply(
        calcular_intensidad_normalizada
    )

    df_registros_validos["cuadrante"] = df_registros_validos.apply(
        lambda fila: determinar_cuadrante(
            fila["valencia"],
            fila["activacion"]
        ),
        axis=1
    )

    df_registros_validos["etiqueta_emocional"] = df_registros_validos.apply(
        lambda fila: clasificar_emocion(
            fila["valencia"],
            fila["activacion"],
            df_etiquetas
        ),
        axis=1
    )

    return df_registros_validos



