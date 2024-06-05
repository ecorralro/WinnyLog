import sqlite3

def conectar_bd():
    conn = sqlite3.connect('winny.db')
    return conn

def ejecutar_consulta(consulta, parametros=()):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(consulta, parametros)
    conn.commit()
    conn.close()

def obtener_resultados(consulta, parametros=()):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(consulta, parametros)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Crear la tabla de usuarios si no existe
def crear_tabla_usuarios():
    consulta = '''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT UNIQUE,
        contrasena TEXT
    );
    '''
    ejecutar_consulta(consulta)
# Crear el resto de tablas adicionales
def crear_tablas_adicionales():
    consulta_vinos = '''
    CREATE TABLE IF NOT EXISTS vinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        bodega TEXT,
        ano INTEGER,
        tipo_uva TEXT,
        denominacion_origen TEXT,
        precio REAL
    );
    '''
    ejecutar_consulta(consulta_vinos)

    consulta_opiniones = '''
    CREATE TABLE IF NOT EXISTS opiniones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        vino_id INTEGER,
        opinion TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(vino_id) REFERENCES vinos(id)
    );
    '''
    ejecutar_consulta(consulta_opiniones)

    consulta_experiencias = '''
    CREATE TABLE IF NOT EXISTS experiencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        vino_id INTEGER,
        fecha TEXT,
        contexto TEXT,
        maridaje TEXT,
        companeros TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(vino_id) REFERENCES vinos(id)
    );
    '''
    ejecutar_consulta(consulta_experiencias)