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


def obtener_emocion_predominante(serie):
    """
    Devuelve la emoción que aparece con mayor frecuencia.
    """

    moda = serie.mode()

    if len(moda) == 0:
        return "Sin datos"

    return moda.iloc[0]


def emocion_predominante_por_contexto(df_evaluaciones):
    """
    Calcula la emoción predominante por contexto
    y el promedio de intensidad emocional.
    """

    verificar_columnas(
        df_evaluaciones,
        [
            "id_contexto",
            "origen",
            "actividad",
            "ubicacion",
            "etiqueta_emocional",
            "intensidad_normalizada"
        ],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones.groupby(
        ["id_contexto", "origen", "actividad", "ubicacion"]
    ).agg(
        emocion_predominante=("etiqueta_emocional", obtener_emocion_predominante),
        intensidad_promedio=("intensidad_normalizada", "mean"),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="intensidad_promedio",
        ascending=False
    )

    return resultado


def emocion_predominante_por_usuario(df_evaluaciones):
    """
    Calcula la emoción predominante por usuario.
    """

    verificar_columnas(
        df_evaluaciones,
        [
            "id_usuario",
            "nombre",
            "etiqueta_emocional",
            "intensidad_normalizada"
        ],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones.groupby(
        ["id_usuario", "nombre"]
    ).agg(
        emocion_predominante=("etiqueta_emocional", obtener_emocion_predominante),
        intensidad_promedio=("intensidad_normalizada", "mean"),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="cantidad_registros",
        ascending=False
    )

    return resultado


def usuarios_mas_inestables(df_evaluaciones):
    """
    Identifica usuarios con mayor variedad de etiquetas emocionales.
    """

    verificar_columnas(
        df_evaluaciones,
        [
            "id_usuario",
            "nombre",
            "etiqueta_emocional",
            "intensidad_normalizada"
        ],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones.groupby(
        ["id_usuario", "nombre"]
    ).agg(
        cantidad_emociones_distintas=("etiqueta_emocional", "nunique"),
        intensidad_promedio=("intensidad_normalizada", "mean"),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by=["cantidad_emociones_distintas", "intensidad_promedio"],
        ascending=False
    )

    return resultado


def promedio_valencia_activacion_por_etiqueta(df_evaluaciones):
    """
    Calcula el promedio de valencia y activación por etiqueta emocional.
    """

    verificar_columnas(
        df_evaluaciones,
        [
            "etiqueta_emocional",
            "valencia",
            "activacion",
            "intensidad_normalizada"
        ],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones.groupby(
        "etiqueta_emocional"
    ).agg(
        valencia_promedio=("valencia", "mean"),
        activacion_promedio=("activacion", "mean"),
        intensidad_promedio=("intensidad_normalizada", "mean"),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="cantidad_registros",
        ascending=False
    )

    return resultado


def contextos_mas_negativos(df_evaluaciones):
    """
    Identifica los contextos con menor valencia promedio.
    """

    verificar_columnas(
        df_evaluaciones,
        [
            "id_contexto",
            "origen",
            "actividad",
            "ubicacion",
            "valencia",
            "etiqueta_emocional"
        ],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones.groupby(
        ["id_contexto", "origen", "actividad", "ubicacion"]
    ).agg(
        valencia_promedio=("valencia", "mean"),
        emocion_predominante=("etiqueta_emocional", obtener_emocion_predominante),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="valencia_promedio",
        ascending=True
    )

    return resultado


def distribucion_emociones(df_evaluaciones):
    """
    Calcula la distribución general de emociones.
    """

    verificar_columnas(
        df_evaluaciones,
        ["etiqueta_emocional"],
        "df_evaluaciones"
    )

    resultado = df_evaluaciones["etiqueta_emocional"].value_counts().reset_index()

    resultado.columns = [
        "etiqueta_emocional",
        "cantidad_registros"
    ]

    total = resultado["cantidad_registros"].sum()

    resultado["porcentaje"] = (
        resultado["cantidad_registros"] / total * 100
    ).round(2)

    return resultado
