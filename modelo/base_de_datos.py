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
