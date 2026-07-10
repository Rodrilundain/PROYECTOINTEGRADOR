from pathlib import Path
import pandas as pd




def leer_registros_afectivos(ruta_carpeta, nombre_archivo):
    """
    Lee el archivo CSV de registros afectivos.

    Recibe:
        ruta_carpeta: carpeta donde se encuentra el archivo.
        nombre_archivo: nombre del archivo CSV.

    Devuelve:
        DataFrame con los registros afectivos.
    """

    ruta_archivo = Path(ruta_carpeta) / nombre_archivo

    try:
        df_registros = pd.read_csv(
            ruta_archivo,
            encoding="utf-8"
        )

        return df_registros

    except UnicodeDecodeError:
        df_registros = pd.read_csv(
            ruta_archivo,
            encoding="latin1"
        )

        return df_registros

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_archivo}")
        return pd.DataFrame()

    except Exception as error:
        print("Error al leer el archivo CSV:", error)
        return pd.DataFrame()


##def leer_registros_afectivos():
##    df_registros_afectivos = pd.read_csv('dataset/registros_afectivos.csv', encoding='latin1')
##    return df_registros_afectivos

def verificar_columnas_csv(df):
  
    columnas_esperadas = [
        "id_registro",
        "id_usuario",
        "id_contexto",
        "fecha_hora",
        "valencia",
        "activacion",
        "comentario"
    ]
    columnas_csv = list(df.columns)
    faltantes = []
    for columna in columnas_esperadas:
        if columna not in columnas_csv:
            faltantes.append(columna)

    if len(faltantes) > 0:
        print("Error: faltan columnas obligatorias:")
        for columna in faltantes:
            print("-", columna)
        return False

    print("El CSV tiene todas las columnas necesarias.")
    return True
   
##df_registros = leer_registros_afectivos()
##
##print(df.head())
##
##if verificar_columnas_csv(df):
##    print("Se puede continuar con la limpieza.")
##else:
##    print("No se puede continuar.")




############



##mostrar_resumen_inicial(df)
