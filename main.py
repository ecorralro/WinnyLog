import tkinter as tk
from tkinter import messagebox
from src.base_de_datos import *

# Variable global para almacenar el ID del usuario actual
usuario_actual_id = None

# Funciones de autenticación
def registrar_usuario(nombre_usuario, contrasena):
    try:
        ejecutar_consulta("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, contrasena))
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

def iniciar_sesion_usuario(nombre_usuario, contrasena):
    global usuario_actual_id
    try:
        resultados = obtener_resultados("SELECT id FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (nombre_usuario, contrasena))
        if len(resultados) > 0:
            usuario_actual_id = resultados[0][0]
            return True
        return False
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return False

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
            self.destroy()
            VentanaPrincipal().mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar(self):
        self.withdraw()
        ventana_registro = VentanaRegistro(self)
        ventana_registro.mainloop()
        self.deiconify()

class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
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
        
        self.boton_mis_momentos = tk.Button(self, text="Mis Momentos", command=self.ver_mis_momentos)
        self.boton_mis_momentos.pack()

        self.boton_crear_momento = tk.Button(self, text="Crear Momento", command=self.crear_momento)
        self.boton_crear_momento.pack()

        self.boton_recordar_momento = tk.Button(self, text="Recordar Momento", command=self.recordar_momento)
        self.boton_recordar_momento.pack()

    def ver_mis_momentos(self):
        self.withdraw()
        ventana_mis_momentos = VentanaMisMomentos(self)
        ventana_mis_momentos.mainloop()
        self.deiconify()

    def crear_momento(self):
        self.withdraw()
        ventana_crear_momento = VentanaCrearMomento(self)
        ventana_crear_momento.mainloop()
        self.deiconify()

    def recordar_momento(self):
        self.withdraw()
        ventana_recordar_momento = VentanaRecordarMomento(self)
        ventana_recordar_momento.mainloop()
        self.deiconify()

class VentanaMisMomentos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Mis Momentos")
        self.geometry("400x400")

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar)
        self.boton_regresar.pack()

        try:
            momentos = obtener_experiencias()  # Obtener los momentos del usuario actual
            for momento in momentos:
                momento_info = f"Vino: {momento[1]}, Contexto: {momento[2]}, Maridaje: {momento[3]}, Amigos: {momento[4]}"
                tk.Label(self, text=momento_info).pack()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener momentos: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaCrearMomento(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Momento")
        self.geometry("300x500")

        self.label_nombre = tk.Label(self, text="Nombre del Vino")
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

        self.label_contexto = tk.Label(self, text="Contexto")
        self.label_contexto.pack()
        self.entry_contexto = tk.Entry(self)
        self.entry_contexto.pack()

        self.label_maridaje = tk.Label(self, text="Maridaje")
        self.label_maridaje.pack()
        self.entry_maridaje = tk.Entry(self)
        self.entry_maridaje.pack()

        self.label_amigos = tk.Label(self, text="Amigos")
        self.label_amigos.pack()
        self.entry_amigos = tk.Entry(self)
        self.entry_amigos.pack()

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_momento)
        self.boton_guardar.pack()

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar)
        self.boton_regresar.pack()

    def guardar_momento(self):
        try:
            nombre = self.entry_nombre.get()
            bodega = self.entry_bodega.get()
            ano = self.entry_ano.get()
            tipo_uva = self.entry_tipo_uva.get()
            denominacion_origen = self.entry_denominacion_origen.get()
            precio = self.entry_precio.get()
            contexto = self.entry_contexto.get()
            maridaje = self.entry_maridaje.get()
            amigos = self.entry_amigos.get()

            agregar_vino(nombre, bodega, ano, tipo_uva, denominacion_origen, precio)
            agregar_experiencia(usuario_actual_id, contexto, maridaje, amigos)
            messagebox.showinfo("Éxito", "Momento agregado correctamente")
            self.destroy()
            self.master.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el momento: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaRecordarMomento(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Recordar Momento")
        self.geometry("400x500")

        self.label_contexto = tk.Label(self, text="Contexto")
        self.label_contexto.pack()
        self.entry_contexto = tk.Entry(self)
        self.entry_contexto.pack()

        self.label_maridaje = tk.Label(self, text="Maridaje")
        self.label_maridaje.pack()
        self.entry_maridaje = tk.Entry(self)
        self.entry_maridaje.pack()

        self.label_amigos = tk.Label(self, text="Amigos")
        self.label_amigos.pack()
        self.entry_amigos = tk.Entry(self)
        self.entry_amigos.pack()

        self.boton_buscar = tk.Button(self, text="Buscar", command=self.buscar_momentos)
        self.boton_buscar.pack()

        self.resultados = tk.Text(self)
        self.resultados.pack()

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar)
        self.boton_regresar.pack()

    def buscar_momentos(self):
        try:
            contexto = self.entry_contexto.get()
            maridaje = self.entry_maridaje.get()
            amigos = self.entry_amigos.get()
            
            query = "SELECT * FROM experiencias WHERE 1=1"
            parametros = []

            if contexto:
                query += " AND contexto LIKE ?"
                parametros.append(f"%{contexto}%")
            if maridaje:
                query += " AND maridaje LIKE ?"
                parametros.append(f"%{maridaje}%")
            if amigos:
                query += " AND amigos LIKE ?"
                parametros.append(f"%{amigos}%")

            momentos = obtener_resultados(query, parametros)
            self.resultados.delete(1.0, tk.END)
            for momento in momentos:
                momento_info = f"Vino: {momento[1]}, Contexto: {momento[2]}, Maridaje: {momento[3]}, Amigos: {momento[4]}"
                self.resultados.insert(tk.END, momento_info + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar momentos: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

if __name__ == "__main__":
    # Crear las tablas de la base de datos
    crear_tabla_usuarios()
    crear_tablas_adicionales()

    # Iniciar la aplicación
    app = VentanaInicioSesion()
    app.mainloop()
