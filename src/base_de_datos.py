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

# CRUD momentos

def agregar_vino(nombre, bodega, ano, tipo_uva, denominacion_origen, precio):
    ejecutar_consulta("INSERT INTO vinos (nombre, bodega, ano, tipo_uva, denominacion_origen, precio) VALUES (?, ?, ?, ?, ?, ?)",
                      (nombre, bodega, ano, tipo_uva, denominacion_origen, precio))

def agregar_opinion(usuario_id, vino_id, opinion):
    ejecutar_consulta("INSERT INTO opiniones (usuario_id, vino_id, opinion) VALUES (?, ?, ?)", (usuario_id, vino_id, opinion))

def agregar_experiencia(usuario_id, vino_id, fecha, contexto, maridaje, companeros):
    ejecutar_consulta("INSERT INTO experiencias (usuario_id, vino_id, fecha, contexto, maridaje, companeros) VALUES (?, ?, ?, ?, ?, ?)",
                      (usuario_id, vino_id, fecha, contexto, maridaje, companeros))

def obtener_vinos():
    return obtener_resultados("SELECT * FROM vinos")

def obtener_opiniones(vino_id):
    return obtener_resultados("SELECT * FROM opiniones WHERE vino_id = ?", (vino_id,))

def obtener_experiencias(usuario_id):
    return obtener_resultados("SELECT * FROM experiencias WHERE usuario_id = ?", (usuario_id,))