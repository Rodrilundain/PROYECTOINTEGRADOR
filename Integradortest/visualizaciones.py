from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def crear_carpeta_salida(carpeta_salida):
    """
    Crea la carpeta donde se guardarán los gráficos.
    """

    Path(carpeta_salida).mkdir(exist_ok=True)


def verificar_columnas(df, columnas_obligatorias, nombre_dataframe):
    """
    Verifica que el DataFrame tenga las columnas necesarias.
    """

    columnas_faltantes = []

    for columna in columnas_obligatorias:
        if columna not in df.columns:
            columnas_faltantes.append(columna)

    if len(columnas_faltantes) > 0:
        raise ValueError(
            f"Faltan columnas en {nombre_dataframe}: {columnas_faltantes}"
        )


def graficar_dispersion(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="dispersion_valencia_activacion.png",
    mostrar=False
):
    """
    Genera un gráfico de dispersión valencia-activación.
    """

    verificar_columnas(
        df_evaluaciones,
        ["valencia", "activacion", "etiqueta_emocional"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    plt.figure(figsize=(8, 6))

    etiquetas = df_evaluaciones["etiqueta_emocional"].dropna().unique()

    for etiqueta in etiquetas:
        datos_etiqueta = df_evaluaciones[
            df_evaluaciones["etiqueta_emocional"] == etiqueta
        ]

        plt.scatter(
            datos_etiqueta["valencia"],
            datos_etiqueta["activacion"],
            label=etiqueta,
            alpha=0.6
        )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.axvline(0, linestyle="--", linewidth=1)

    plt.title("Dispersión valencia-activación")
    plt.xlabel("Valencia")
    plt.ylabel("Activación")
    plt.legend()
    plt.grid(True)

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida



def graficar_distribucion_emociones(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="distribucion_emociones.png",
    mostrar=False
):
    """
    Genera un gráfico de barras con la cantidad de registros por emoción.
    """

    verificar_columnas(
        df_evaluaciones,
        ["etiqueta_emocional"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    distribucion = df_evaluaciones["etiqueta_emocional"].value_counts()

    plt.figure(figsize=(9, 6))

    distribucion.plot(kind="bar")

    plt.title("Distribución de emociones")
    plt.xlabel("Etiqueta emocional")
    plt.ylabel("Cantidad de registros")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida



def graficar_promedios_por_etiqueta(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="promedios_por_etiqueta.png",
    mostrar=False
):
    """
    Genera un gráfico de barras con los promedios de valencia y activación
    por etiqueta emocional.
    """

    verificar_columnas(
        df_evaluaciones,
        ["etiqueta_emocional", "valencia", "activacion"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    promedios = df_evaluaciones.groupby(
        "etiqueta_emocional"
    )[["valencia", "activacion"]].mean()

    plt.figure(figsize=(10, 6))

    promedios.plot(kind="bar", figsize=(10, 6))

    plt.title("Promedio de valencia y activación por etiqueta emocional")
    plt.xlabel("Etiqueta emocional")
    plt.ylabel("Promedio")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")
    plt.legend(["Valencia promedio", "Activación promedio"])

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida



def graficar_serie_temporal(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="serie_temporal_intensidad.png",
    id_usuario=None,
    id_contexto=None,
    mostrar=False
):
    """
    Genera una serie temporal de intensidad emocional normalizada.

    Puede filtrarse por usuario o por contexto.
    """

    verificar_columnas(
        df_evaluaciones,
        ["fecha_hora", "intensidad_normalizada"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    df = df_evaluaciones.copy()

    df["fecha_hora"] = pd.to_datetime(
        df["fecha_hora"],
        errors="coerce"
    )

    df = df.dropna(subset=["fecha_hora"])

    if id_usuario is not None:
        verificar_columnas(df, ["id_usuario"], "df_evaluaciones")
        df = df[df["id_usuario"] == id_usuario]

    if id_contexto is not None:
        verificar_columnas(df, ["id_contexto"], "df_evaluaciones")
        df = df[df["id_contexto"] == id_contexto]

    if df.empty:
        print("No hay datos para generar la serie temporal.")
        return None

    df = df.sort_values("fecha_hora")

    serie = df.groupby(
        df["fecha_hora"].dt.date
    )["intensidad_normalizada"].mean()

    plt.figure(figsize=(10, 6))

    plt.plot(
        serie.index,
        serie.values,
        marker="o"
    )

    plt.title("Serie temporal de intensidad emocional")
    plt.xlabel("Fecha")
    plt.ylabel("Intensidad emocional normalizada")
    plt.xticks(rotation=45)
    plt.grid(True)

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida

def graficar_intensidad_promedio_por_contexto(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="intensidad_promedio_por_contexto.png",
    top_n=10,
    mostrar=False
):
    """
    Genera un gráfico de barras con los contextos de mayor intensidad emocional promedio.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_contexto", "actividad", "intensidad_normalizada"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    resultado = df_evaluaciones.groupby(
        ["id_contexto", "actividad"]
    ).agg(
        intensidad_promedio=("intensidad_normalizada", "mean"),
        cantidad_registros=("intensidad_normalizada", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="intensidad_promedio",
        ascending=False
    ).head(top_n)

    resultado["contexto"] = resultado["id_contexto"].astype(str) + " - " + resultado["actividad"]

    plt.figure(figsize=(10, 6))

    plt.barh(
        resultado["contexto"],
        resultado["intensidad_promedio"]
    )

    plt.title("Contextos con mayor intensidad emocional promedio")
    plt.xlabel("Intensidad promedio normalizada")
    plt.ylabel("Contexto")
    plt.gca().invert_yaxis()
    plt.grid(axis="x")

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida



def graficar_contextos_mas_negativos(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="contextos_mas_negativos.png",
    top_n=10,
    mostrar=False
):
    """
    Genera un gráfico con los contextos de menor valencia promedio.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_contexto", "actividad", "valencia"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    resultado = df_evaluaciones.groupby(
        ["id_contexto", "actividad"]
    ).agg(
        valencia_promedio=("valencia", "mean"),
        cantidad_registros=("valencia", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="valencia_promedio",
        ascending=True
    ).head(top_n)

    resultado["contexto"] = resultado["id_contexto"].astype(str) + " - " + resultado["actividad"]

    plt.figure(figsize=(10, 6))

    plt.barh(
        resultado["contexto"],
        resultado["valencia_promedio"]
    )

    plt.title("Contextos con menor valencia promedio")
    plt.xlabel("Valencia promedio")
    plt.ylabel("Contexto")
    plt.gca().invert_yaxis()
    plt.grid(axis="x")

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida

def graficar_usuarios_mas_inestables(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="usuarios_mas_inestables.png",
    top_n=10,
    mostrar=False
):
    """
    Genera un gráfico con los usuarios que presentan mayor variedad de emociones.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_usuario", "nombre", "etiqueta_emocional"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    resultado = df_evaluaciones.groupby(
        ["id_usuario", "nombre"]
    ).agg(
        cantidad_emociones_distintas=("etiqueta_emocional", "nunique"),
        cantidad_registros=("etiqueta_emocional", "count")
    ).reset_index()

    resultado = resultado.sort_values(
        by="cantidad_emociones_distintas",
        ascending=False
    ).head(top_n)

    resultado["usuario"] = resultado["id_usuario"].astype(str) + " - " + resultado["nombre"]

    plt.figure(figsize=(10, 6))

    plt.barh(
        resultado["usuario"],
        resultado["cantidad_emociones_distintas"]
    )

    plt.title("Usuarios con mayor variedad de emociones")
    plt.xlabel("Cantidad de emociones distintas")
    plt.ylabel("Usuario")
    plt.gca().invert_yaxis()
    plt.grid(axis="x")

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida


def graficar_emocion_predominante_por_contexto(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="emocion_predominante_por_contexto.png",
    top_n=15,
    mostrar=False
):
    """
    Genera un gráfico con la emoción predominante de cada contexto.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_contexto", "actividad", "etiqueta_emocional"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    conteo = df_evaluaciones.groupby(
        ["id_contexto", "actividad", "etiqueta_emocional"]
    ).size().reset_index(name="cantidad")

    indices_maximos = conteo.groupby(
        ["id_contexto", "actividad"]
    )["cantidad"].idxmax()

    resultado = conteo.loc[indices_maximos]

    resultado = resultado.sort_values(
        by="cantidad",
        ascending=False
    ).head(top_n)

    resultado["contexto"] = resultado["id_contexto"].astype(str) + " - " + resultado["actividad"]

    plt.figure(figsize=(10, 7))

    plt.barh(
        resultado["contexto"],
        resultado["cantidad"]
    )

    for indice, fila in resultado.iterrows():
        plt.text(
            fila["cantidad"],
            list(resultado["contexto"]).index(fila["contexto"]),
            " " + fila["etiqueta_emocional"],
            va="center"
        )

    plt.title("Emoción predominante por contexto")
    plt.xlabel("Cantidad de registros")
    plt.ylabel("Contexto")
    plt.gca().invert_yaxis()
    plt.grid(axis="x")

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida



def graficar_serie_temporal_valencia_activacion(
    df_evaluaciones,
    carpeta_salida="graficos",
    nombre_archivo="serie_temporal_valencia_activacion.png",
    id_usuario=None,
    id_contexto=None,
    mostrar=False
):
    """
    Genera una serie temporal con los promedios diarios de valencia y activación.
    Puede filtrarse por usuario o contexto.
    """

    verificar_columnas(
        df_evaluaciones,
        ["fecha_hora", "valencia", "activacion"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    df = df_evaluaciones.copy()

    df["fecha_hora"] = pd.to_datetime(
        df["fecha_hora"],
        errors="coerce"
    )

    df = df.dropna(subset=["fecha_hora"])

    if id_usuario is not None:
        verificar_columnas(df, ["id_usuario"], "df_evaluaciones")
        df = df[df["id_usuario"] == id_usuario]

    if id_contexto is not None:
        verificar_columnas(df, ["id_contexto"], "df_evaluaciones")
        df = df[df["id_contexto"] == id_contexto]

    if df.empty:
        print("No hay datos para generar la serie temporal.")
        return None

    df["fecha"] = df["fecha_hora"].dt.date

    serie = df.groupby("fecha").agg(
        valencia_promedio=("valencia", "mean"),
        activacion_promedio=("activacion", "mean")
    ).reset_index()

    plt.figure(figsize=(10, 6))

    plt.plot(
        serie["fecha"],
        serie["valencia_promedio"],
        marker="o",
        label="Valencia promedio"
    )

    plt.plot(
        serie["fecha"],
        serie["activacion_promedio"],
        marker="o",
        label="Activación promedio"
    )

    plt.axhline(0, linestyle="--", linewidth=1)

    plt.title("Serie temporal de valencia y activación")
    plt.xlabel("Fecha")
    plt.ylabel("Promedio")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    ruta_salida = Path(carpeta_salida) / nombre_archivo
    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida


def graficar_evolucion_usuario(
    df_evaluaciones,
    id_usuario,
    carpeta_salida="graficos",
    mostrar=False
):
    """
    Genera la evolución temporal de intensidad emocional para un usuario específico.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_usuario", "fecha_hora", "intensidad_normalizada"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    df = df_evaluaciones.copy()

    df["fecha_hora"] = pd.to_datetime(
        df["fecha_hora"],
        errors="coerce"
    )

    df = df.dropna(subset=["fecha_hora"])

    df_usuario = df[df["id_usuario"] == id_usuario]

    if df_usuario.empty:
        print(f"No hay datos para el usuario {id_usuario}.")
        return None

    df_usuario = df_usuario.sort_values("fecha_hora")

    serie = df_usuario.groupby(
        df_usuario["fecha_hora"].dt.date
    )["intensidad_normalizada"].mean()

    plt.figure(figsize=(10, 6))

    plt.plot(
        serie.index,
        serie.values,
        marker="o"
    )

    plt.title(f"Evolución emocional del usuario {id_usuario}")
    plt.xlabel("Fecha")
    plt.ylabel("Intensidad emocional normalizada")
    plt.xticks(rotation=45)
    plt.grid(True)

    nombre_archivo = f"evolucion_usuario_{id_usuario}.png"
    ruta_salida = Path(carpeta_salida) / nombre_archivo

    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida


def graficar_distribucion_emociones_usuario(
    df_evaluaciones,
    id_usuario,
    carpeta_salida="graficos",
    mostrar=False
):
    """
    Genera un gráfico de barras con la distribución de emociones de un usuario.
    """

    verificar_columnas(
        df_evaluaciones,
        ["id_usuario", "etiqueta_emocional"],
        "df_evaluaciones"
    )

    crear_carpeta_salida(carpeta_salida)

    df_usuario = df_evaluaciones[
        df_evaluaciones["id_usuario"] == id_usuario
    ]

    if df_usuario.empty:
        print(f"No hay datos para el usuario {id_usuario}.")
        return None

    distribucion = df_usuario["etiqueta_emocional"].value_counts()

    plt.figure(figsize=(9, 6))

    distribucion.plot(kind="bar")

    plt.title(f"Distribución de emociones del usuario {id_usuario}")
    plt.xlabel("Etiqueta emocional")
    plt.ylabel("Cantidad de registros")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")

    nombre_archivo = f"distribucion_emociones_usuario_{id_usuario}.png"
    ruta_salida = Path(carpeta_salida) / nombre_archivo

    plt.savefig(ruta_salida, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    return ruta_salida





def generar_todos_los_graficos(df_evaluaciones, carpeta_salida="graficos"):
    """
    Genera todos los gráficos esperados del proyecto.
    """

    rutas = []

    ruta_dispersion = graficar_dispersion(
        df_evaluaciones,
        carpeta_salida=carpeta_salida
    )
    rutas.append(ruta_dispersion)

    ruta_distribucion = graficar_distribucion_emociones(
        df_evaluaciones,
        carpeta_salida=carpeta_salida
    )
    rutas.append(ruta_distribucion)

    ruta_promedios = graficar_promedios_por_etiqueta(
        df_evaluaciones,
        carpeta_salida=carpeta_salida
    )
    rutas.append(ruta_promedios)

    ruta_serie_temporal = graficar_serie_temporal(
        df_evaluaciones,
        carpeta_salida=carpeta_salida
    )
    rutas.append(ruta_serie_temporal)

    return rutas


def generar_graficos_complementarios(df_evaluaciones, carpeta_salida="graficos"):
    """
    Genera gráficos complementarios para el análisis emocional.
    """

    rutas = []

    rutas.append(
        graficar_intensidad_promedio_por_contexto(
            df_evaluaciones,
            carpeta_salida=carpeta_salida
        )
    )

    rutas.append(
        graficar_contextos_mas_negativos(
            df_evaluaciones,
            carpeta_salida=carpeta_salida
        )
    )

    rutas.append(
        graficar_usuarios_mas_inestables(
            df_evaluaciones,
            carpeta_salida=carpeta_salida
        )
    )

    rutas.append(
        graficar_emocion_predominante_por_contexto(
            df_evaluaciones,
            carpeta_salida=carpeta_salida
        )
    )

    rutas.append(
        graficar_serie_temporal_valencia_activacion(
            df_evaluaciones,
            carpeta_salida=carpeta_salida
        )
    )

    return rutas

