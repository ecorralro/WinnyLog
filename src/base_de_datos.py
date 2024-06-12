import sqlite3

def ejecutar_consulta(consulta, parametros=()):
    try:
        conexion = sqlite3.connect("winny.db")
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error en la ejecución de la consulta: {e}")
    finally:
        conexion.close()

def obtener_resultados(consulta, parametros=()):
    try:
        conexion = sqlite3.connect("winny.db")
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Error al obtener resultados: {e}")
        return []
    finally:
        conexion.close()

def crear_tabla_usuarios():
    consulta = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL,
        contrasena TEXT NOT NULL
    )
    """
    ejecutar_consulta(consulta)

def crear_tablas_adicionales():
    consultas = [
        """
        CREATE TABLE IF NOT EXISTS vinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            bodega TEXT,
            ano INTEGER,
            tipo_uva TEXT,
            denominacion_origen TEXT,
            precio REAL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS opiniones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vino INTEGER,
            opinion TEXT,
            FOREIGN KEY (id_vino) REFERENCES vinos(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS experiencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            contexto TEXT,
            maridaje TEXT,
            companeros TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """
    ]
    for consulta in consultas:
        ejecutar_consulta(consulta)

def agregar_vino(nombre, bodega, ano, tipo_uva, denominacion_origen, precio):
    consulta = """
    INSERT INTO vinos (nombre, bodega, ano, tipo_uva, denominacion_origen, precio)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    parametros = (nombre, bodega, ano, tipo_uva, denominacion_origen, precio)
    ejecutar_consulta(consulta, parametros)

def agregar_opinion(id_vino, opinion):
    consulta = """
    INSERT INTO opiniones (id_vino, opinion)
    VALUES (?, ?)
    """
    parametros = (id_vino, opinion)
    ejecutar_consulta(consulta, parametros)

def agregar_experiencia(usuario_id, contexto, maridaje, companeros):
    consulta = """
    INSERT INTO experiencias (usuario_id, contexto, maridaje, companeros)
    VALUES (?, ?, ?, ?)
    """
    parametros = (usuario_id, contexto, maridaje, companeros)
    ejecutar_consulta(consulta, parametros)

def obtener_vinos():
    consulta = "SELECT * FROM vinos"
    return obtener_resultados(consulta)

def obtener_opiniones():
    consulta = "SELECT * FROM opiniones"
    return obtener_resultados(consulta)

def obtener_experiencias(usuario_id):
    consulta = "SELECT * FROM experiencias WHERE usuario_id = ?"
    parametros = (usuario_id,)
    return obtener_resultados(consulta, parametros)
