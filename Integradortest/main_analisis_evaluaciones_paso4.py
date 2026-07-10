import carga_csv
import analisis_evaluaciones


def main():

    df_evaluaciones = carga_csv.leer_registros_afectivos(
        "dataset_salida",
        "evaluaciones_emocionales_extendidas.csv"
    )

    print("\nEMOCIÓN PREDOMINANTE POR CONTEXTO")
    resultado_contexto = analisis_evaluaciones.emocion_predominante_por_contexto(
        df_evaluaciones
    )
    print(resultado_contexto.head())

    print("\nEMOCIÓN PREDOMINANTE POR USUARIO")
    resultado_usuario = analisis_evaluaciones.emocion_predominante_por_usuario(
        df_evaluaciones
    )
    print(resultado_usuario.head())

    print("\nUSUARIOS MÁS INESTABLES")
    resultado_inestables = analisis_evaluaciones.usuarios_mas_inestables(
        df_evaluaciones
    )
    print(resultado_inestables.head())

    print("\nPROMEDIO DE VALENCIA Y ACTIVACIÓN POR ETIQUETA")
    resultado_promedios = analisis_evaluaciones.promedio_valencia_activacion_por_etiqueta(
        df_evaluaciones
    )
    print(resultado_promedios)

    print("\nCONTEXTOS MÁS NEGATIVOS")
    resultado_negativos = analisis_evaluaciones.contextos_mas_negativos(
        df_evaluaciones
    )
    print(resultado_negativos.head())

    print("\nDISTRIBUCIÓN DE EMOCIONES")
    resultado_distribucion = analisis_evaluaciones.distribucion_emociones(
        df_evaluaciones
    )
    print(resultado_distribucion)

main()
##if __name__ == "__main__":
##    main()
