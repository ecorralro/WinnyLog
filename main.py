import tkinter as tk
from tkinter import messagebox
from src.base_de_datos import ejecutar_consulta, obtener_resultados, crear_tabla_usuarios
from src.base_de_datos import agregar_vino, agregar_opinion, agregar_experiencia, obtener_vinos, obtener_opiniones, obtener_experiencias

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

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Winny - Principal")
        self.geometry("400x300")
        
        self.boton_agregar_vino = tk.Button(self, text="Agregar Vino", command=self.agregar_vino)
        self.boton_agregar_vino.pack()

        self.boton_ver_vinos = tk.Button(self, text="Ver Vinos", command=self.ver_vinos)
        self.boton_ver_vinos.pack()

    def agregar_vino(self):
        ventana_agregar_vino = VentanaAgregarVino()
        ventana_agregar_vino.mainloop()

    def ver_vinos(self):
        ventana_ver_vinos = VentanaVerVinos()
        ventana_ver_vinos.mainloop()

class VentanaAgregarVino(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agregar Vino")
        self.geometry("300x400")

        self.label_nombre = tk.Label(self, text="Nombre")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        self.label_bodega = tk.Label(self, text="Bodega")
        self.label_bodega.pack()
        self.entry_bodega = tk.Entry(self)
        self.entry_bodega.pack()

        self.label_ano = tk.Label(self, text="Año")
        self.label_ano.pack()
        self.entry_ano = tk.Entry(self)
        self.entry_ano.pack()

        self.label_tipo_uva = tk.Label(self, text="Tipo de Uva")
        self.label_tipo_uva.pack()
        self.entry_tipo_uva = tk.Entry(self)
        self.entry_tipo_uva.pack()

        self.label_denominacion_origen = tk.Label(self, text="Denominación de Origen")
        self.label_denominacion_origen.pack()
        self.entry_denominacion_origen = tk.Entry(self)
        self.entry_denominacion_origen.pack()

        self.label_precio = tk.Label(self, text="Precio")
        self.label_precio.pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_vino)
        self.boton_guardar.pack()

    def guardar_vino(self):
        nombre = self.entry_nombre.get()
        bodega = self.entry_bodega.get()
        ano = self.entry_ano.get()
        tipo_uva = self.entry_tipo_uva.get()
        denominacion_origen = self.entry_denominacion_origen.get()
        precio = self.entry_precio.get()

        agregar_vino(nombre, bodega, ano, tipo_uva, denominacion_origen, precio)
        messagebox.showinfo("Éxito", "Vino agregado correctamente")
        self.destroy()

class VentanaVerVinos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ver Vinos")
        self.geometry("400x400")

        vinos = obtener_vinos()

        for vino in vinos:
            vino_info = f"Nombre: {vino[1]}, Bodega: {vino[2]}, Año: {vino[3]}, Tipo de Uva: {vino[4]}, Denominación de Origen: {vino[5]}, Precio: {vino[6]}"
            tk.Label(self, text=vino_info).pack()

if __name__ == "__main__":
    # Crear la tabla de usuarios
    crear_tabla_usuarios()

    # Iniciar la aplicación
    app = VentanaInicioSesion()
    app.mainloop()
