import carga_csv
import carga_base_datos
import procesamiento_emocional
import generacion_evaluaciones
import  sanitacion
from pathlib import Path


def main():
    conexion = None

    try:
        conexion = carga_base_datos.conectar_base_datos()

        if conexion is None:
            print("No se pudo establecer conexión con la base de datos.")
            return

##        df_usuarios, usuarios = carga_base_datos.cargar_usuarios_a_dict(conexion)
##        df_contextos, contextos = carga_base_datos.cargar_contextos(conexion)
        df_etiquetas = carga_base_datos.cargar_etiquetas_emocionales(conexion)
        df_usuarios, usuarios = sanitacion.cargar_usuarios(conexion)
        df_contextos, contextos = sanitacion.cargar_contextos(conexion)
        ruta_carpeta = "dataset_salida"
        nombre_archivo = "registros_afectivos_validos.csv"

        df_registros_afectivos = carga_csv.leer_registros_afectivos(
            ruta_carpeta,
            nombre_archivo
        )

        if df_registros_afectivos.empty:
            print("No se pudo cargar el archivo de registros afectivos.")
            return
        #Verificar columnas obligatorias
        columnas_ok = carga_csv.verificar_columnas_csv(df_registros_afectivos)
        if not columnas_ok:
            print("El CSV no tiene las columnas necesarias.")
            return

        df_evaluaciones = procesamiento_emocional.procesar_emociones(
            df_registros_afectivos,
            df_etiquetas
        )

        df_evaluaciones_finales = generacion_evaluaciones.generar_evaluaciones(
            df_evaluaciones,
            df_usuarios,
            df_contextos
        )

        Path("dataset_salida").mkdir(exist_ok=True)

        df_evaluaciones_finales.to_csv(
            "dataset_salida/evaluaciones_emocionales_extendidas.csv",
            index=False,
            encoding="utf-8"
        )

        print("Evaluaciones emocionales generadas correctamente.")
        print("Cantidad de evaluaciones:", len(df_evaluaciones_finales))
        print(df_evaluaciones_finales.head())

    except Exception as error:
        print("Error general en el procesamiento emocional:", error)

    finally:
        if conexion is not None:
            carga_base_datos.cerrar_conexion(conexion)

main()
##if __name__ == "__main__":
##    main()
