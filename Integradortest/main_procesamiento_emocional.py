####recibir registros_validos (de  csv)
##    recibir etiquetas_emocionales (de la BD)



import procesamiento_emocional
import carga_base_datos
import carga_csv
from pathlib import Path

##import inspect
##print("Archivo importado:", carga_csv.__file__)
##print("Firma de la función:", inspect.signature(carga_csv.leer_registros_afectivos))

def main():
    conexion = None

    try:
        conexion = carga_base_datos.conectar_base_datos()

        if conexion is None:
            print("No se pudo establecer conexión con la base de datos.")
            return

        df_etiquetas = carga_base_datos.cargar_etiquetas_emocionales(conexion)
        print("Etiquetas cargadas:", len(df_etiquetas))
        ##ruta_carpeta = "."
        ruta_carpeta = "dataset_salida"
        nombre_archivo = "registros_afectivos_validos.csv"
        #Leer CSV de registros afectivos
        df_registros_afectivos = carga_csv.leer_registros_afectivos(ruta_carpeta,nombre_archivo)

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

        Path("dataset_salida").mkdir(exist_ok=True)

        df_evaluaciones.to_csv(
            "dataset_salida/evaluaciones_emocionales.csv",
            index=False,
            encoding="utf-8"
        )

        print("Procesamiento emocional finalizado correctamente.")
        print("Evaluaciones generadas:", len(df_evaluaciones))

    except Exception as error:
        print("Error general en el procesamiento emocional:", error)

    finally:
        if conexion is not None:
            carga_base_datos.cerrar_conexion(conexion)
main()

###### Lo siguiente es una buena practica de programacion: Ejecutar main() solamente si este archivo se está ejecutando directamente (no si se esta importando de otro archivo).
##
##if __name__ == "__main__":
##    main()
