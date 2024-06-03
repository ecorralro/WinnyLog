from .base_de_datos import ejecutar_consulta, obtener_resultados

def registrar_usuario(nombre_usuario, contrasena):
    try:
        ejecutar_consulta("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, contrasena))
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

def iniciar_sesion_usuario(nombre_usuario, contrasena):
    resultados = obtener_resultados("SELECT * FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (nombre_usuario, contrasena))
    return len(resultados) > 0