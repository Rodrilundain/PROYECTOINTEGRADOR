import pandas as pd


def verificar_columnas(df, columnas_obligatorias, nombre_dataframe):
    """
    Verifica que un DataFrame tenga las columnas necesarias.
    """

    columnas_faltantes = []

    for columna in columnas_obligatorias:
        if columna not in df.columns:
            columnas_faltantes.append(columna)

    if len(columnas_faltantes) > 0:
        raise ValueError(
            f"Faltan columnas en {nombre_dataframe}: {columnas_faltantes}"
        )


def incorporar_datos_usuario(df_evaluaciones, df_usuarios):
    """
    Incorpora los datos del usuario a las evaluaciones emocionales.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_usuario"],
        "df_evaluaciones"
    )

    verificar_columnas(
        df_usuarios,
        ["id_usuario", "nombre", "edad", "genero"],
        "df_usuarios"
    )

    df_resultado = df_evaluaciones.merge(
        df_usuarios[["id_usuario", "nombre", "edad", "genero"]],
        on="id_usuario",
        how="left"
    )

    return df_resultado


def incorporar_datos_contexto(df_evaluaciones, df_contextos):
    """
    Incorpora los datos del contexto a las evaluaciones emocionales.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_contexto"],
        "df_evaluaciones"
    )

    verificar_columnas(
        df_contextos,
        ["id_contexto", "origen", "actividad", "ubicacion", "descripcion"],
        "df_contextos"
    )

    df_resultado = df_evaluaciones.merge(
        df_contextos[
            [
                "id_contexto",
                "origen",
                "actividad",
                "ubicacion",
                "descripcion"
            ]
        ],
        on="id_contexto",
        how="left"
    )

    return df_resultado


def generar_evaluaciones(df_evaluaciones, df_usuarios, df_contextos):
    """
    Genera el DataFrame final de evaluaciones emocionales enriquecidas.

    Combina:
        - evaluaciones emocionales
        - datos de usuarios
        - datos de contextos
    """

    df_resultado = df_evaluaciones.copy()

    df_resultado = incorporar_datos_usuario(
        df_resultado,
        df_usuarios
    )

    df_resultado = incorporar_datos_contexto(
        df_resultado,
        df_contextos
    )

    df_resultado.insert(
        0,
        "id_evaluacion",
        range(1, len(df_resultado) + 1)
    )

    columnas_ordenadas = [
        "id_evaluacion",
        "id_registro",
        "id_usuario",
        "nombre",
        "edad",
        "genero",
        "id_contexto",
        "origen",
        "actividad",
        "ubicacion",
        "descripcion",
        "fecha_hora",
        "valencia",
        "activacion",
        "comentario",
        "intensidad",
        "intensidad_normalizada",
        "cuadrante",
        "etiqueta_emocional"
    ]

    columnas_existentes = []

    for columna in columnas_ordenadas:
        if columna in df_resultado.columns:
            columnas_existentes.append(columna)

    df_resultado = df_resultado[columnas_existentes]

    return df_resultado
