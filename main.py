import tkinter as tk
from tkinter import messagebox
from src.base_de_datos import (ejecutar_consulta, obtener_resultados, crear_tabla_usuarios, 
                           crear_tablas_adicionales, agregar_vino, agregar_opinion, 
                           agregar_experiencia, obtener_vinos, obtener_opiniones, obtener_experiencias)

class SesionUsuario:
    def __init__(self):
        self.id = None

    def iniciar_sesion(self, id):
        self.id = id

    def cerrar_sesion(self):
        self.id = None

    def es_activo(self):
        return self.id is not None
    
# Funciones de autenticación
def registrar_usuario(nombre_usuario, contrasena):
    try:
        ejecutar_consulta("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, contrasena))
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

def iniciar_sesion_usuario(nombre_usuario, contrasena):
    try:
        resultados = obtener_resultados("SELECT id FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (nombre_usuario, contrasena))
        if resultados:
            return resultados[0][0]
        return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None

# Interfaz gráfica
class VentanaInicioSesion(tk.Tk):
    def __init__(self, sesion_usuario):
        super().__init__()
        self.sesion_usuario = sesion_usuario
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
        usuario_id = iniciar_sesion_usuario(nombre_usuario, contrasena)
        if usuario_id:
            self.sesion_usuario.iniciar_sesion(usuario_id)
            messagebox.showinfo("Éxito", "Inicio de sesión correcto")
            self.destroy()
            VentanaPrincipal(self.sesion_usuario).mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar(self):
        self.toggle_window()
        ventana_registro = VentanaRegistro(self, self.sesion_usuario)
        ventana_registro.mainloop()
        self.toggle_window()

    def toggle_window(self):
        if self.state() == 'normal':
            self.withdraw()
        else:
            self.deiconify()

class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent, sesion_usuario):
        super().__init__(parent)
        self.sesion_usuario = sesion_usuario
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
    def __init__(self, sesion_usuario):
        super().__init__()
        self.sesion_usuario = sesion_usuario
        self.title("Winny - Principal")
        self.geometry("400x300")
        
        self.boton_mis_momentos = tk.Button(self, text="Mis Momentos", command=self.ver_mis_momentos)
        self.boton_mis_momentos.pack()

        self.boton_crear_momento = tk.Button(self, text="Crear Momento", command=self.crear_momento)
        self.boton_crear_momento.pack()

        self.boton_recordar_momento = tk.Button(self, text="Recordar Momento", command=self.recordar_momento)
        self.boton_recordar_momento.pack()

    def ver_mis_momentos(self):
        self.toggle_window()
        ventana_mis_momentos = VentanaMisMomentos(self, self.sesion_usuario)
        ventana_mis_momentos.mainloop()
        self.toggle_window()

    def crear_momento(self):
        self.toggle_window()
        ventana_crear_momento = VentanaCrearMomento(self, self.sesion_usuario)
        ventana_crear_momento.mainloop()
        self.toggle_window()

    def recordar_momento(self):
        self.toggle_window()
        ventana_recordar_momento = VentanaRecordarMomento(self, self.sesion_usuario)
        ventana_recordar_momento.mainloop()
        self.toggle_window()

    def toggle_window(self):
        if self.state() == 'normal':
            self.withdraw()
        else:
            self.deiconify()

class VentanaMisMomentos(tk.Toplevel):
    def __init__(self, parent, sesion_usuario):
        super().__init__(parent)
        self.sesion_usuario = sesion_usuario
        self.title("Mis Momentos")
        self.geometry("400x400")

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar)
        self.boton_regresar.pack()

        try:
            momentos = obtener_experiencias(self.sesion_usuario.id)  # Obtener los momentos del usuario actual
            for momento in momentos:
                momento_info = f"Vino: {momento[1]}, Contexto: {momento[2]}, Maridaje: {momento[3]}, Amigos: {momento[4]}"
                tk.Label(self, text=momento_info).pack()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener momentos: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaCrearMomento(tk.Toplevel):
    def __init__(self, parent, sesion_usuario):
        super().__init__(parent)
        self.sesion_usuario = sesion_usuario
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

        self.label_companeros = tk.Label(self, text="Compañeros")
        self.label_companeros.pack()
        self.entry_companeros = tk.Entry(self)
        self.entry_companeros.pack()

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
            companeros = self.entry_companeros.get()

            agregar_vino(nombre, bodega, ano, tipo_uva, denominacion_origen, precio)
            agregar_experiencia(self.sesion_usuario.id, contexto, maridaje, companeros)
            messagebox.showinfo("Éxito", "Momento agregado correctamente")
            self.destroy()
            self.master.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el momento: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaRecordarMomento(tk.Toplevel):
    def __init__(self, parent, sesion_usuario):
        super().__init__(parent)
        self.sesion_usuario = sesion_usuario
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

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar)
        self.boton_regresar.pack()

        self.resultados = tk.Text(self)
        self.resultados.pack()

    def buscar_momentos(self):
        try:
            contexto = self.entry_contexto.get()
            maridaje = self.entry_maridaje.get()
            amigos = self.entry_companeros.get()
            
            query = "SELECT * FROM experiencias WHERE id_usuario = ?"
            parametros = [self.sesion_usuario.id]

            if contexto:
                query += " AND contexto LIKE ?"
                parametros.append(f"%{contexto}%")
            if maridaje:
                query += " AND maridaje LIKE ?"
                parametros.append(f"%{maridaje}%")
            if amigos:
                query += " AND companeros LIKE ?"
                parametros.append(f"%{companeros}%")

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

    # Iniciar la sesión de usuario
    sesion_usuario = SesionUsuario()

    # Iniciar la aplicación
    app = VentanaInicioSesion(sesion_usuario)
    app.mainloop()
