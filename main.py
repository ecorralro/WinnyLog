import tkinter as tk
from tkinter import messagebox
from src.base_de_datos import ejecutar_consulta, obtener_resultados, crear_tabla_usuarios

# Funciones de autenticación
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

# Interfaz gráfica
class VentanaInicioSesion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Winny - Iniciar Sesión")
        self.geometry("300x200")
        
        self.label_usuario = tk.Label(self, text="Usuario")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack()

        self.label_contrasena = tk.Label(self, text="Contraseña")
        self.label_contrasena.pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        self.boton_iniciar_sesion = tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.boton_iniciar_sesion.pack()

        self.boton_registrar = tk.Button(self, text="Registrar", command=self.registrar)
        self.boton_registrar.pack()

    def iniciar_sesion(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        if iniciar_sesion_usuario(nombre_usuario, contrasena):
            messagebox.showinfo("Éxito", "Inicio de sesión correcto")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar(self):
        ventana_registro = VentanaRegistro()
        ventana_registro.mainloop()

class VentanaRegistro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Winny - Registrar")
        self.geometry("300x200")
        
        self.label_usuario = tk.Label(self, text="Usuario")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack()

        self.label_contrasena = tk.Label(self, text="Contraseña")
        self.label_contrasena.pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        self.boton_registrar = tk.Button(self, text="Registrar", command=self.registrar)
        self.boton_registrar.pack()

    def registrar(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        if registrar_usuario(nombre_usuario, contrasena):
            messagebox.showinfo("Éxito", "Registro correcto")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario")

if __name__ == "__main__":
    # Crear la tabla de usuarios
    crear_tabla_usuarios()

    # Iniciar la aplicación
    app = VentanaInicioSesion()
    app.mainloop()
