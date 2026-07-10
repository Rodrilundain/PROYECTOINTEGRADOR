
##import sanitacion
##import procesamiento_emocional
##import evaluacion_emocional
##import analisis_estadistico
##import analisis_estadistico
##conn= carga_base_datos.conectar_base_datos()
##df_usuarios=carga_base_datos.cargar_usuarios(conn)
##print(df_usuarios.head())
##Esto es un comentario
##carga_base_datos.cerrar_conexion(conn)




from pathlib import Path
import carga_base_datos
import carga_csv
import sanitacion

def main():
    conexion = None

    try:
        #Conectamos a la base de datos
        conexion = carga_base_datos.conectar_base_datos()

        if conexion is None:
            print("No se pudo establecer conexión con la base de datos.")
            return

        #Cargar datos desde la base
        df_usuarios, usuarios = sanitacion.cargar_usuarios(conexion)
        df_contextos, contextos = sanitacion.cargar_contextos(conexion)
        #Cargar el módulo de etiquetas emocionales (para usar mas adelante)
        df_etiquetas = carga_base_datos.cargar_etiquetas_emocionales(conexion)
        print("Usuarios cargados:", len(df_usuarios))
        print("Contextos cargados:", len(df_contextos))
        print("Etiquetas cargadas:", len(df_etiquetas))

        #Leer CSV de registros afectivos
        ruta_carpeta="dataset"
        nombre_archivo="registros_afectivos.csv"
        
        df_registros = carga_csv.leer_registros_afectivos(ruta_carpeta, nombre_archivo)

        if df_registros.empty:
            print("No se pudo cargar el archivo de registros afectivos.")
            return

        #Verificar columnas obligatorias
        columnas_ok = carga_csv.verificar_columnas_csv(df_registros)

        if not columnas_ok:
            print("El CSV no tiene las columnas necesarias.")
            return

        #Ejecutar sanitación completa
        df_registros = sanitacion.limpiar_registros(
            df_registros,
            usuarios,
            contextos
        )

        #Separar registros válidos e inválidos
        registros_validos, registros_invalidos = sanitacion.separar_registros_validos_invalidos(
            df_registros
        )

        #Mostrar resumen de errores
        sanitacion.mostrar_resumen_errores(df_registros)

        #Crear carpeta de salida
        Path("dataset_salida").mkdir(exist_ok=True)

        #Guardar dataset completo validado
        df_registros.to_csv(
            "dataset_salida/registros_afectivos_validados.csv",
            index=False,
            encoding="utf-8"
        )

        #Guardar registros inválidos
        registros_invalidos.to_csv(
            "dataset_salida/registros_afectivos_invalidos.csv",
            index=False,
            encoding="utf-8"
        )

        #Crear dataset limpio para el próximo módulo
        columnas_validas = [
            "id_registro",
            "id_usuario_limpio",
            "id_contexto_limpio",
            "fecha_hora_limpia",
            "valencia_limpia",
            "activacion_limpia",
            "comentario_limpio"
        ]

        registros_validos_limpios = registros_validos[columnas_validas].copy()

        registros_validos_limpios = registros_validos_limpios.rename(columns={
            "id_usuario_limpio": "id_usuario",
            "id_contexto_limpio": "id_contexto",
            "fecha_hora_limpia": "fecha_hora",
            "valencia_limpia": "valencia",
            "activacion_limpia": "activacion",
            "comentario_limpio": "comentario"
        })

        registros_validos_limpios.to_csv(
            "dataset_salida/registros_afectivos_validos.csv",
            index=False,
            encoding="utf-8"
        )

        print("\nProceso de sanitación finalizado correctamente.")
        print("Registros válidos:", len(registros_validos_limpios))
        print("Registros inválidos:", len(registros_invalidos))

    except Exception as error:
        print("Error general en el programa:", error)



    finally:
        if conexion is not None:
            carga_base_datos.cerrar_conexion(conexion)
main()

###### Lo siguiente es una buena practica de programacion: Ejecutar main() solamente si este archivo se está ejecutando directamente (no si se esta importando de otro archivo).
##
##if __name__ == "__main__":
##    main()
