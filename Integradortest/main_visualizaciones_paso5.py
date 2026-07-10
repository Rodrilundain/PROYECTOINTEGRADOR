import carga_csv
import visualizaciones


def main():

    df_evaluaciones = carga_csv.leer_registros_afectivos(
        "dataset_salida",
        "evaluaciones_emocionales_extendidas.csv"
    )

    if df_evaluaciones.empty:
        print("No se pudo cargar el archivo de evaluaciones emocionales.")
        return

    rutas_graficos_basicos = visualizaciones.generar_todos_los_graficos(
    df_evaluaciones,
    carpeta_salida="graficos"
    )

    rutas_graficos_complementarios = visualizaciones.generar_graficos_complementarios(
    df_evaluaciones,
    carpeta_salida="graficos"
    )

    print("Gráficos básicos generados:")
    for ruta in rutas_graficos_basicos:
        print(ruta)

    print("\nGráficos complementarios generados:")
    for ruta in rutas_graficos_complementarios:
        print(ruta)
main()
##
##if __name__ == "__main__":
##    main()
