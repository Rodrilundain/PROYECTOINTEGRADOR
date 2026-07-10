##Funciones posibles:
##limpiar_texto()
"""
Los datos que son texto pueden necesitar ciertas transformaciones, por ejemplo si hay espacios en blancos al final del string, etc. Esta parte se divide en dos funciones:
requiere_limpieza_texto:  devuelve la lista de motivos detectada que requieren transformacion; luego se pasan a la funcion limpiar_texto
que hace las transformaciones indicadas
"""
import carga_csv
import pandas as pd

def requiere_limpieza_texto(valor):
    """Detecta si una celda de texto necesita limpieza y devuelve True/False más los motivos"""

    motivos = []

    if pd.isna(valor):
        motivos.append("valor nulo")
        return True, motivos

    texto = str(valor)

    if texto != texto.strip():
        motivos.append("espacios al inicio o al final")

    if texto.strip() == "":
        motivos.append("texto vacío")

    if texto.strip().lower() in ["null", "none", "na", "n/a", "sin dato"]:
        motivos.append("valor nulo escrito como texto")

    if "  " in texto:
        motivos.append("espacios múltiples")

    return len(motivos) > 0, motivos


def diagnosticar_columna_texto(df, columna):
    """Recorre una columna de texto y muestra o resume cuántos valores necesitan limpieza. """
    total = len(df)
    cantidad_con_problemas = 0
    resumen_motivos = {}

    for valor in df[columna]:
        necesita, motivos = requiere_limpieza_texto(valor)

        if necesita:
            cantidad_con_problemas += 1

            for motivo in motivos:
                if motivo not in resumen_motivos:
                    resumen_motivos[motivo] = 0
                resumen_motivos[motivo] += 1

    print(f"Columna analizada: {columna}")
    print(f"Total de registros: {total}")
    print(f"Registros que necesitan limpieza: {cantidad_con_problemas}")

    print("\nMotivos detectados:")
    for motivo, cantidad in resumen_motivos.items():
        print(f"- {motivo}: {cantidad}")

    return cantidad_con_problemas, resumen_motivos

##df=carga_csv.leer_registros_afectivos()
##
##diagnosticar_columna_texto(df, "comentario")


def limpiar_texto(valor, valor_defecto="No informado"):
    """
    Limpia o modifica un valor de texto.

    Recibe:
        valor: una celda del DataFrame.
        valor_defecto: texto que se usará si el valor está vacío o es nulo.

    Devuelve:
        texto_limpio
    """

    # Valor nulo real: NaN, None, etc.
    if pd.isna(valor):
        return valor_defecto

    texto = str(valor).strip()

    # Texto vacío
    if texto == "":
        return valor_defecto

    # Valores nulos escritos como texto
    if texto.lower() in ["null", "none", "na", "n/a", "sin dato"]:
        return valor_defecto

    # Reemplazar espacios múltiples internos por un solo espacio
    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto

##df["comentario"] = df["comentario"].apply(
##    lambda valor: limpiar_texto(valor, "Sin comentario")
##)

##diagnosticar_columna_texto(df, "comentario")

##convertir_a_float()

def convertir_a_float(valor, nombre_campo="valor"):
    """
    convierte un valor a float y devuelve también un posible error

    Recibe:
        valor: una celda del DataFrame.
        nombre_campo: nombre del campo que se está convirtiendo,
                      por ejemplo 'valencia' o 'activacion'.

    Devuelve:
        numero: valor convertido a float, o None si no se puede convertir.
        error: mensaje de error, o None si la conversión fue correcta.
    """

    # Caso 1: valor nulo real de pandas, por ejemplo NaN
    if pd.isna(valor):
        return None, f"{nombre_campo} vacío"

    # Convertir a texto y limpiar espacios
    texto = str(valor).strip()

    # Caso 2: texto vacío
    if texto == "":
        return None, f"{nombre_campo} vacío"

    # Caso 3: valores nulos escritos como texto
    if texto.lower() in ["null", "none", "na", "n/a", "sin dato"]:
        return None, f"{nombre_campo} sin dato"

    # Caso 4: decimal con coma
    texto = texto.replace(",", ".")

    # Caso 5: intentar convertir a float
    try:
        numero = float(texto)
        return numero, None

    except ValueError:
        return None, f"{nombre_campo} no numérico: {valor}"

##df[["valencia_limpia", "error_valencia"]] = df["valencia"].apply(
##    lambda valor: pd.Series(convertir_a_float(valor, "valencia"))
##)
##
##df[["activacion_limpia", "error_activacion"]] = df["activacion"].apply(
##    lambda valor: pd.Series(convertir_a_float(valor, "activacion"))
##)
##
##errores_valencia = df[df["error_valencia"].notna()]
##errores_activacion = df[df["error_activacion"].notna()]

##print(errores_valencia[["id_registro", "valencia", "error_valencia"]])
##print(errores_activacion[["id_registro", "activacion", "error_activacion"]])
##el mensaje eerror valencia o error activacion se agregan como nuevas columnas en el df


def validar_valencia(valor):
    """
    Valida que la valencia sea un número dentro del rango permitido, de [-1.0, 1.0]

    Recibe:
        valor: una celda ya convertida a float.

    Devuelve:
        es_valida: True o False
        error: None si es válida, o mensaje de error si no lo es
    """

    if pd.isna(valor):
        return False, "valencia no disponible para validar"

    if valor < -1.0 or valor > 1.0:
        return False, f"valencia fuera de rango: {valor}"

    return True, None


##df[["valencia_valida", "error_rango_valencia"]] = df["valencia_limpia"].apply(
##    lambda valor: pd.Series(validar_valencia(valor))
##)



##validar_activacion()
def validar_activacion(valor):
    """
    Valida que la activación sea un número dentro del rango permitido, de [-1.0, 1.0]
    """

    if pd.isna(valor):
        return False, "activacion no disponible para validar"

    if valor < -1.0 or valor > 1.0:
        return False, f"activacion fuera de rango: {valor}"

    return True, None


##df[["activacion_valida", "error_rango_activacion"]] = df["activacion_limpia"].apply(
##    lambda valor: pd.Series(validar_activacion(valor))
##)

##print(df.head())
##


##validar_fecha()

#### para ver las fechas que pueden tener error:
def mostrar_fechas_con_error(df):
    #### para ver las fechas que pueden tener error: muestra registros con fechas que no pueden convertirse correctamente
    fechas_prueba = pd.to_datetime(df["fecha_hora"], errors="coerce")

    fechas_con_error = df[fechas_prueba.isna()]

    print("Cantidad de fechas con error:", len(fechas_con_error))

    if len(fechas_con_error) > 0:
        print(fechas_con_error[["id_registro", "fecha_hora"]])

    return fechas_con_error
## para ejecutarlo
##fechas_con_error = mostrar_fechas_con_error(df)



def validar_fecha(valor, nombre_campo="fecha_hora"):
    """
    Valida y convierte una fecha/hora.

    Recibe:
        valor: una celda del DataFrame.

    Devuelve:
        fecha_convertida: valor convertido a datetime, o None si es inválido.
        error: None si es válido, o mensaje de error si no lo es.
    """

    if pd.isna(valor):
        return None, f"{nombre_campo} vacío"

    texto = str(valor).strip()

    if texto == "":
        return None, f"{nombre_campo} vacío"

    if texto.lower() in ["null", "none", "na", "n/a", "sin dato"]:
        return None, f"{nombre_campo} sin dato"

    try:
        fecha_convertida = pd.to_datetime(texto, errors="raise")
        return fecha_convertida, None

    except Exception:
        return None, f"{nombre_campo} inválida: {valor}"




##df[["fecha_hora_limpia", "error_fecha"]] = df["fecha_hora"].apply(
##    lambda valor: pd.Series(validar_fecha(valor))
##)
##
### para ver los registros con errores de fecha:
##errores_fecha = df[df["error_fecha"].notna()]
##print(errores_fecha[["id_registro", "fecha_hora", "error_fecha"]])




##validar_usuario()

"""Los errores en el usuario pueden ser:
1. Que el id_usuario no esté vacío.
2. Que pueda convertirse a número entero. 
3. Que el id_usuario exista en la tabla usuarios.
4. Si no existe el usuario hay que marcarlo al registro como inválido.

Se hace en tres pasos:
1) Cargar desde la base de datos a los usuarios en un diccionarlo
2) funcion para verificar las que tienen errores
3) funcion para limpiar registros de usuarios
"""
import carga_base_datos
##conexion=carga_base_datos.conectar_base_datos()




def cargar_usuarios(conexion):
    """
    Carga los usuarios desde MySQL usando pandas.

    Devuelve:
        df_usuarios: DataFrame con los usuarios.
        usuarios: diccionario indexado por id_usuario.
        porque validar_usuario() necesita saber si el id_usuario del CSV de registros afectivos existe en la base.
    """

    consulta = """
        SELECT id_usuario, nombre, edad, genero
        FROM usuarios;
    """

    try:
        df_usuarios = pd.read_sql(consulta, conexion)

        usuarios = df_usuarios.set_index(
            "id_usuario", 
            drop=False
        ).to_dict("index")

        return df_usuarios, usuarios

    except Exception as error:
        print("Error al cargar usuarios:", error)
        return pd.DataFrame(), {}


##Para probarlo:
##df_usuarios, usuarios = cargar_usuarios(conexion)
##
##print(df_usuarios.head())
##para ver el diccionario con los usuarios
##print(usuarios)



def mostrar_errores_usuario(df, usuarios):
    """
    Revisa los registros afectivos y muestra cuáles tienen errores en id_usuario.

    Controla:
    1. id_usuario vacío.
    2. id_usuario no convertible a entero.
    3. id_usuario inexistente en la base de datos.

    Recibe:
        df: DataFrame de registros_afectivos.csv.
        usuarios: diccionario de usuarios válidos cargados desde la base.

    Devuelve:
        df_errores: DataFrame con los registros que tienen error de usuario.
    """

    errores = []

    for indice, fila in df.iterrows():
        valor = fila["id_usuario"]

        # Caso 1: id_usuario vacío o nulo
        if pd.isna(valor):
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_usuario": valor,
                "error_usuario": "id_usuario vacío"
            })
            continue

        texto = str(valor).strip()

        if texto == "":
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_usuario": valor,
                "error_usuario": "id_usuario vacío"
            })
            continue

        # Caso 2: id_usuario no numérico
        try:
            id_usuario = int(texto)

        except ValueError:
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_usuario": valor,
                "error_usuario": f"id_usuario no numérico: {valor}"
            })
            continue

        # Caso 3: id_usuario inexistente
        if id_usuario not in usuarios:
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_usuario": valor,
                "error_usuario": f"id_usuario inexistente: {id_usuario}"
            })

    df_errores = pd.DataFrame(errores)

    print("Cantidad de registros con error de usuario:", len(df_errores))

    if len(df_errores) > 0:
        print(df_errores)

    return df_errores


##Primero tener cargados los usuarios desde la base:

##df_usuarios, usuarios = cargar_usuarios(conexion)
##df_registros = pd.read_csv(
##    "dataset/registros_afectivos.csv",
##    encoding="latin1"
##)

## probamos la funcion mostrar_errores_usuario
##errores_usuario = mostrar_errores_usuario(df_registros, usuarios)


##Luego
##errores_usuario = mostrar_errores_usuario(df, usuarios)
##





def validar_usuarios_en_registros(df, usuarios):
    """
    Valida el campo id_usuario de cada registro afectivo.

    Controla:
    1. Que id_usuario no esté vacío.
    2. Que pueda convertirse a número entero.
    3. Que exista en el diccionario de usuarios.
    4. Si no existe o tiene error, marca el registro como inválido.

    Recibe:
        df: DataFrame de registros afectivos.
        usuarios: diccionario de usuarios cargado desde la base de datos.

    Devuelve:
        df: DataFrame con columnas nuevas de validación.
    """

    id_usuarios_limpios = []
    errores_usuario = []
    usuarios_validos = []

    for valor in df["id_usuario"]:

        # Caso 1: id_usuario vacío o nulo
        if pd.isna(valor):
            id_usuarios_limpios.append(None)
            errores_usuario.append("id_usuario vacío")
            usuarios_validos.append(False)
            continue

        texto = str(valor).strip()

        if texto == "":
            id_usuarios_limpios.append(None)
            errores_usuario.append("id_usuario vacío")
            usuarios_validos.append(False)
            continue

        # Caso 2: intentar convertir a entero
        try:
            id_usuario = int(texto)

        except ValueError:
            id_usuarios_limpios.append(None)
            errores_usuario.append(f"id_usuario no numérico: {valor}")
            usuarios_validos.append(False)
            continue

        # Caso 3: verificar si existe en la base de datos
        if id_usuario not in usuarios:
            id_usuarios_limpios.append(None)
            errores_usuario.append(f"id_usuario inexistente: {id_usuario}")
            usuarios_validos.append(False)
            continue

        # Caso 4: usuario válido
        id_usuarios_limpios.append(id_usuario)
        errores_usuario.append(None)
        usuarios_validos.append(True)

    # Agregar columnas nuevas al DataFrame
    df["id_usuario_limpio"] = id_usuarios_limpios
    df["error_usuario"] = errores_usuario
    df["usuario_valido"] = usuarios_validos

    return df


##df_registros = validar_usuarios_en_registros(df_registros, usuarios)
##luego de corer estas lineas, se agregan en el dataset nuevos campos: id_usuario_limpio, error_usuario, usuario_valido. La función no elimina filas.
##Solo marca cuáles registros tienen usuario válido y cuáles no.
## para ver los invalidos:
##print(df_registros[df_registros["usuario_valido"] == False])

## para ver algunos campos:
##print(
##    df_registros[df_registros["usuario_valido"] == False]
##    [["id_registro", "id_usuario", "error_usuario"]]
##)


## para gusardar el nuevo dataframe en un nuevo csv:
##df_registros.to_csv(
##    "dataset/registros_afectivos_con_validacion_usuario.csv",
##    index=False,
##    encoding="utf-8"
##)

##
##validar_contexto()



def cargar_contextos(conexion):
    # Carga contextos desde la base y genera el diccionario necesario para validar
    consulta = """
        SELECT id_contexto, origen, actividad, ubicacion, descripcion
        FROM contextos;
    """

    df_contextos = pd.read_sql(consulta, conexion)

    contextos = df_contextos.set_index(
        "id_contexto",
        drop=False
    ).to_dict("index")

    return df_contextos, contextos


# Convierte un id a entero si es posible
def convertir_id_entero(valor, nombre_campo):
    # Convierte un id a entero si es posible
    if pd.isna(valor):
        return None, f"{nombre_campo} vacío"

    texto = str(valor).strip()

    if texto == "":
        return None, f"{nombre_campo} vacío"

    try:
        numero = float(texto)

        if not numero.is_integer():
            return None, f"{nombre_campo} no entero: {valor}"

        return int(numero), None

    except ValueError:
        return None, f"{nombre_campo} no numérico: {valor}"


# Muestra registros del CSV cuyo id_contexto no existe o es inválido
def mostrar_errores_contexto(df_registros, contextos):
    # Muestra registros del CSV cuyo id_contexto no existe o es inválido
    errores = []

    for indice, fila in df_registros.iterrows():
        id_contexto, error = convertir_id_entero(
            fila["id_contexto"],
            "id_contexto"
        )

        if error is not None:
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_contexto": fila["id_contexto"],
                "error_contexto": error
            })
            continue

        if id_contexto not in contextos:
            errores.append({
                "indice": indice,
                "id_registro": fila["id_registro"],
                "id_contexto": fila["id_contexto"],
                "error_contexto": f"id_contexto inexistente: {id_contexto}"
            })

    columnas = ["indice", "id_registro", "id_contexto", "error_contexto"]
    df_errores = pd.DataFrame(errores, columns=columnas)

    if df_errores.empty:
        print("No se detectaron errores de contexto.")
    else:
        print(df_errores)

    return df_errores









# Valida el campo id_contexto y agrega columnas nuevas al DataFrame
def validar_contextos_en_registros(df_registros, contextos):
    # Valida el campo id_contexto y agrega columnas nuevas al DataFrame
    id_contextos_limpios = []
    errores_contexto = []
    contextos_validos = []

    for valor in df_registros["id_contexto"]:

        id_contexto, error = convertir_id_entero(valor, "id_contexto")

        if error is not None:
            id_contextos_limpios.append(None)
            errores_contexto.append(error)
            contextos_validos.append(False)
            continue

        if id_contexto not in contextos:
            id_contextos_limpios.append(None)
            errores_contexto.append(f"id_contexto inexistente: {id_contexto}")
            contextos_validos.append(False)
            continue

        id_contextos_limpios.append(id_contexto)
        errores_contexto.append(None)
        contextos_validos.append(True)

    df_registros["id_contexto_limpio"] = id_contextos_limpios
    df_registros["error_contexto"] = errores_contexto
    df_registros["contexto_valido"] = contextos_validos

    return df_registros


# Ejecución
##df_contextos, contextos = cargar_contextos(conexion)
##
##df_registros = pd.read_csv(
##    "dataset/registros_afectivos.csv",
##    encoding="latin1"
##)
##
##errores_contexto = mostrar_errores_contexto(df_registros, contextos)
##
##print(errores_contexto)
##
##df_registros = validar_contextos_en_registros(df_registros, contextos)
##
##print(
##    df_registros[
##        df_registros["contexto_valido"] == False
##    ][
##        ["id_registro", "id_contexto", "error_contexto"]
##    ]
##)
##
##
##

##detectar_duplicados()


def detectar_duplicados(df):
    """
    Detecta registros duplicados en el DataFrame.
    Agrega columnas para marcar duplicados.
    """

    df = df.copy()

    if "id_registro" in df.columns:
        df["duplicado_id_registro"] = df.duplicated(
            subset=["id_registro"],
            keep=False
        )

        df["error_duplicado"] = df["duplicado_id_registro"].apply(
            lambda x: "id_registro duplicado" if x else None
        )
    else:
        df["duplicado_id_registro"] = False
        df["error_duplicado"] = "no existe columna id_registro"

    df["duplicado_fila_completa"] = df.duplicated(keep=False)

    return df

##df_registros = pd.read_csv(
##    "dataset/registros_afectivos.csv",
##    encoding="latin1"
##)
##
##df_registros = detectar_duplicados(df_registros)
##duplicados = df_registros[df_registros["duplicado_id_registro"] == True]

##print(
##    duplicados[
##        ["id_registro", "id_usuario", "id_contexto", "fecha_hora", "error_duplicado"]
##    ]
##)

##limpiar_registros()


def limpiar_registros(df_registros, usuarios, contextos):
    """
    Ejecuta el proceso completo de limpieza y validación de registros afectivos.
    Agrega columnas limpias y columnas de error al DataFrame.
    """

    df_registros = df_registros.copy()

    # Limpiar comentario
    if "comentario" in df_registros.columns:
        df_registros["comentario_limpio"] = df_registros["comentario"].apply(
            lambda valor: limpiar_texto(valor, "Sin comentario")
        )

    # Convertir y validar valencia
    df_registros[["valencia_limpia", "error_conversion_valencia"]] = df_registros["valencia"].apply(
        lambda valor: pd.Series(convertir_a_float(valor, "valencia"))
    )

    df_registros[["valencia_valida", "error_rango_valencia"]] = df_registros["valencia_limpia"].apply(
        lambda valor: pd.Series(validar_valencia(valor))
    )

    # Convertir y validar activación
    df_registros[["activacion_limpia", "error_conversion_activacion"]] = df_registros["activacion"].apply(
        lambda valor: pd.Series(convertir_a_float(valor, "activacion"))
    )

    df_registros[["activacion_valida", "error_rango_activacion"]] = df_registros["activacion_limpia"].apply(
        lambda valor: pd.Series(validar_activacion(valor))
    )

    # Validar fecha
    df_registros[["fecha_hora_limpia", "error_fecha"]] = df_registros["fecha_hora"].apply(
        lambda valor: pd.Series(validar_fecha(valor))
    )

    # Validar usuarios
    df_registros = validar_usuarios_en_registros(df_registros, usuarios)

    # Validar contextos
    df_registros = validar_contextos_en_registros(df_registros, contextos)

    # Detectar duplicados
    df_registros = detectar_duplicados(df_registros)

    return df_registros

##df_registros = limpiar_registros(
##    df_registros,
##    usuarios,
##    contextos
##)
##print(df_registros.head())

#### Para ver solo las columnas mas importantes:
##columnas_revision = [
##    "id_registro",
##    "id_usuario",
##    "id_usuario_limpio",
##    "error_usuario",
##    "id_contexto",
##    "id_contexto_limpio",
##    "error_contexto",
##    "valencia",
##    "valencia_limpia",
##    "error_conversion_valencia",
##    "error_rango_valencia",
##    "activacion",
##    "activacion_limpia",
##    "error_conversion_activacion",
##    "error_rango_activacion",
##    "fecha_hora",
##    "fecha_hora_limpia",
##    "error_fecha",
##    "error_duplicado"
##]
##
##print(df_registros[columnas_revision].head(20))


def separar_registros_validos_invalidos(df_registros):
    """
    Separa los registros válidos e inválidos según las columnas de error.
    """

    columnas_error = [
        "error_conversion_valencia",
        "error_rango_valencia",
        "error_conversion_activacion",
        "error_rango_activacion",
        "error_fecha",
        "error_usuario",
        "error_contexto",
        "error_duplicado"
    ]

    columnas_existentes = []

    for columna in columnas_error:
        if columna in df_registros.columns:
            columnas_existentes.append(columna)

    condicion_invalida = df_registros[columnas_existentes].notna().any(axis=1)

    registros_invalidos = df_registros[condicion_invalida]
    registros_validos = df_registros[~condicion_invalida]

    return registros_validos, registros_invalidos

##df_registros = limpiar_registros(
##    df_registros,
##    usuarios,
##    contextos
##)
##
##registros_validos, registros_invalidos = separar_registros_validos_invalidos(
##    df_registros
##)
##print("Registros válidos:", len(registros_validos))
##print("Registros inválidos:", len(registros_invalidos))
##
##print(registros_invalidos.head())
##

#### Puewde ocurrir que haya 391 filas inválidas pero 483 errores totales (porque algunas filas tienen dos o más errores.)

##Salidas esperadas:

##registros_validos, registros_invalidos = separar_registros_validos_invalidos(df_registros)
##mostrar_resumen_errores(df_registros)

def mostrar_resumen_errores(df_registros):
    columnas_error = [
        "error_conversion_valencia",
        "error_rango_valencia",
        "error_conversion_activacion",
        "error_rango_activacion",
        "error_fecha",
        "error_usuario",
        "error_contexto",
        "error_duplicado"
    ]

    columnas_existentes = [
        columna for columna in columnas_error
        if columna in df_registros.columns
    ]

    df_registros["cantidad_errores"] = df_registros[columnas_existentes].notna().sum(axis=1)
    df_registros["registro_valido"] = df_registros["cantidad_errores"] == 0

    registros_validos = df_registros[df_registros["registro_valido"] == True]
    registros_invalidos = df_registros[df_registros["registro_valido"] == False]

    print("\nRESUMEN DE ERRORES")
    print("-" * 50)

    print("Total de registros:", len(df_registros))
    print("Registros válidos:", len(registros_validos))
    print("Registros inválidos:", len(registros_invalidos))

    print("\nErrores por tipo:")
    total_errores = 0

    for columna in columnas_existentes:
        cantidad = df_registros[columna].notna().sum()
        total_errores += cantidad
        print(f"{columna}: {cantidad}")

    print("\nCantidad de errores por registro:")
    print(df_registros["cantidad_errores"].value_counts().sort_index())

    print("-" * 50)
    print("Total de errores detectados:", total_errores)
    print("-" * 50)

    return registros_validos, registros_invalidos

##mostrar_resumen_errores(df_registros)


##registros_validos
##registros_invalidos
##resumen_errores
