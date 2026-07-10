import pymysql
from pymysql import Error
import pandas as pd

def conectar_base_datos():
    
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="proyectointegrador"
        )

        print("Conexión exitosa a la base de datos.")
        return conexion

    except Error as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None


def cerrar_conexion(conexion):
    
    try:
        if conexion is not None:
            conexion.close()
            print("Conexión cerrada correctamente.")

    except Error as error:
        print(f"Error al cerrar la conexión: {error}")

def cargar_usuarios(conexion):
     try:
        df_usuarios = pd.read_sql("SELECT * FROM usuarios", conexion)
        return df_usuarios
     except Error as error:
        print(f"Error al cerrar la conexión: {error}")
        return None


def cargar_contextos(conexion):
     try:
        df_contextos = pd.read_sql("SELECT * FROM contextos", conexion)
        return df_contextos
     except Error as error:
        print(f"Error al cerrar la conexión: {error}")
        return None



##cargar_etiquetas_emocionales()

def cargar_etiquetas_emocionales(conexion):
     try:
        df_etiquetas_emocionales = pd.read_sql("SELECT * FROM etiquetas_emocionales", conexion)
        return df_etiquetas_emocionales
     except Error as error:
        print(f"Error al cerrar la conexión: {error}")
        return None

