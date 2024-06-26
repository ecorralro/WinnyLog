import tkinter as tk
from tkinter import messagebox
from src.base_de_datos import ejecutar_consulta, obtener_resultados, crear_tabla_usuarios, crear_tablas_adicionales
from src.base_de_datos import agregar_vino, agregar_experiencia, agregar_puntuacion, obtener_experiencias, obtener_vinos, obtener_puntuaciones, obtener_vino_mejor_rcp, obtener_vino_mejor_puntuacion

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
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.label_usuario = tk.Label(self, text="Usuario", bg="#4B0E0E", fg="white")
        self.label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.label_contrasena = tk.Label(self, text="Contraseña", bg="#4B0E0E", fg="white")
        self.label_contrasena.pack(pady=5)
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack(pady=5)

        self.boton_iniciar_sesion = tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#8B0000", fg="white")
        self.boton_iniciar_sesion.pack(pady=10)

        self.boton_registrar = tk.Button(self, text="Registrar", command=self.registrar, bg="#A52A2A", fg="white")
        self.boton_registrar.pack(pady=5)

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
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.label_usuario = tk.Label(self, text="Usuario", bg="#4B0E0E", fg="white")
        self.label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.label_contrasena = tk.Label(self, text="Contraseña", bg="#4B0E0E", fg="white")
        self.label_contrasena.pack(pady=5)
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack(pady=5)

        self.boton_registrar = tk.Button(self, text="Registrar", command=self.registrar, bg="#8B0000", fg="white")
        self.boton_registrar.pack(pady=10)

    def registrar(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        if registrar_usuario(nombre_usuario, contrasena):
            messagebox.showinfo("Éxito", "Registro correcto")
            self.destroy()
            VentanaInicioSesion().mainloop()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario")

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Winny - Principal")
        self.geometry("400x300")
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.boton_mis_momentos = tk.Button(self, text="Mis Momentos", command=self.ver_mis_momentos, bg="#8B0000", fg="white")
        self.boton_mis_momentos.pack(pady=10)

        self.boton_crear_momento = tk.Button(self, text="Crear Momento", command=self.crear_momento, bg="#A52A2A", fg="white")
        self.boton_crear_momento.pack(pady=10)

        self.boton_top = tk.Button(self, text="Top Vinos", command=self.top_vinos, bg="#B22222", fg="white")
        self.boton_top.pack(pady=10)

        self.boton_cerrar_sesion = tk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion, bg="#800000", fg="white")
        self.boton_cerrar_sesion.pack(pady=10)

    def ver_mis_momentos(self):
        self.withdraw()
        ventana_mis_momentos = VentanaMisMomentos(self, usuario_actual_id)
        ventana_mis_momentos.mainloop()
        self.deiconify()

    def crear_momento(self):
        self.withdraw()
        ventana_crear_momento = VentanaCrearMomento(self, usuario_actual_id)
        ventana_crear_momento.mainloop()
        self.deiconify()

    def top_vinos(self):
        self.withdraw()
        ventana_top_vinos = VentanaTopVinos(self, usuario_actual_id)
        ventana_top_vinos.mainloop()
        self.deiconify()

    def cerrar_sesion(self):
        self.withdraw()
        ventana_inicio = VentanaInicioSesion()
        ventana_inicio.mainloop()
        self.deiconify()

class VentanaMisMomentos(tk.Toplevel):
    def __init__(self, parent, usuario_actual_id):
        super().__init__(parent)
        self.usuario_actual_id = usuario_actual_id
        self.title("Mis Momentos")
        self.geometry("400x400")
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar, bg="#800000", fg="white")
        self.boton_regresar.pack(pady=10)

        try:
            momentos = obtener_experiencias(self.usuario_actual_id)  # Obtener los momentos del usuario actual
            for momento in momentos:
                vino_info = obtener_vinos(momento[2])  # Obtener información del vino por vino_id
                momento_info = f"Vino: {vino_info}, Contexto: {momento[3]}, Maridaje: {momento[4]}, Compañeros: {momento[5]}"
                tk.Label(self, text=momento_info, bg="#4B0E0E", fg="white").pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener momentos: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaCrearMomento(tk.Toplevel):
    def __init__(self, parent, usuario_actual_id):
        super().__init__(parent)
        self.usuario_actual_id = usuario_actual_id
        self.title("Crear Momento - Paso 1")
        self.geometry("400x400")
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.label_vino = tk.Label(self, text="Vino", bg="#4B0E0E", fg="white")
        self.label_vino.pack(pady=5)
        self.entry_vino = tk.Entry(self)
        self.entry_vino.pack(pady=5)

        self.label_bodega = tk.Label(self, text="Bodega", bg="#4B0E0E", fg="white")
        self.label_bodega.pack(pady=5)
        self.entry_bodega = tk.Entry(self)
        self.entry_bodega.pack(pady=5)

        self.label_ano = tk.Label(self, text="Año", bg="#4B0E0E", fg="white")
        self.label_ano.pack(pady=5)
        self.entry_ano = tk.Entry(self)
        self.entry_ano.pack(pady=5)

        self.label_tipo_uva = tk.Label(self, text="Tipo de Uva", bg="#4B0E0E", fg="white")
        self.label_tipo_uva.pack(pady=5)
        self.entry_tipo_uva = tk.Entry(self)
        self.entry_tipo_uva.pack(pady=5)

        self.label_denominacion_origen = tk.Label(self, text="Denominación de Origen", bg="#4B0E0E", fg="white")
        self.label_denominacion_origen.pack(pady=5)
        self.entry_denominacion_origen = tk.Entry(self)
        self.entry_denominacion_origen.pack(pady=5)

        self.label_precio = tk.Label(self, text="Precio", bg="#4B0E0E", fg="white")
        self.label_precio.pack(pady=5)
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack(pady=5)

        self.boton_siguiente = tk.Button(self, text="Siguiente", command=self.guardar_vino, bg="#8B0000", fg="white")
        self.boton_siguiente.pack(pady=10)

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar, bg="#800000", fg="white")
        self.boton_regresar.pack(pady=10)

    def guardar_vino(self):
        try:
            # Obtener datos de vino
            nombre_vino = self.entry_vino.get()
            bodega = self.entry_bodega.get()
            ano = int(self.entry_ano.get()) if self.entry_ano.get() else 0
            tipo_uva = self.entry_tipo_uva.get()
            denominacion_origen = self.entry_denominacion_origen.get()
            precio = float(self.entry_precio.get()) if self.entry_precio.get() else 0.0

            # Agregar vino y obtener su ID
            self.vino_id = agregar_vino(nombre_vino, bodega, ano, tipo_uva, denominacion_origen, precio)

            # Pasar a la siguiente ventana
            self.withdraw()
            ventana_crear_momento2 = VentanaCrearMomento2(self, self.usuario_actual_id,self.vino_id)
            ventana_crear_momento2.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar vino: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaCrearMomento2(tk.Toplevel):
    def __init__(self, parent, usuario_actual_id, vino_id):
        super().__init__(parent)
        self.title("Crear Momento - Paso 2")
        self.geometry("400x400")
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro
        self.usuario_actual_id = usuario_actual_id
        self.vino_id = vino_id

        self.label_contexto = tk.Label(self, text="Contexto", bg="#4B0E0E", fg="white")
        self.label_contexto.pack(pady=5)
        self.entry_contexto = tk.Entry(self)
        self.entry_contexto.pack(pady=5)

        self.label_maridaje = tk.Label(self, text="Maridaje", bg="#4B0E0E", fg="white")
        self.label_maridaje.pack(pady=5)
        self.entry_maridaje = tk.Entry(self)
        self.entry_maridaje.pack(pady=5)

        self.label_companeros = tk.Label(self, text="Compañeros", bg="#4B0E0E", fg="white")
        self.label_companeros.pack(pady=5)
        self.entry_companeros = tk.Entry(self)
        self.entry_companeros.pack(pady=5)

        self.label_puntuacion = tk.Label(self, text="Puntuación", bg="#4B0E0E", fg="white")
        self.label_puntuacion.pack(pady=5)
        self.entry_puntuacion = tk.Entry(self)
        self.entry_puntuacion.pack(pady=5)

        self.boton_guardar = tk.Button(self, text="Guardar Momento", command=self.guardar_momento, bg="#8B0000", fg="white")
        self.boton_guardar.pack(pady=10)

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar, bg="#800000", fg="white")
        self.boton_regresar.pack(pady=10)

    def guardar_momento(self):
        try:
            # Obtener datos de la experiencia
            contexto = self.entry_contexto.get()
            maridaje = self.entry_maridaje.get()
            companeros = self.entry_companeros.get()

            # Agregar experiencia
            agregar_experiencia(self.usuario_actual_id, self.vino_id, contexto, maridaje, companeros)   

            # Obtener puntuación
            puntuacion = int(self.entry_puntuacion.get()) if self.entry_puntuacion.get() else 0

            # Agregar puntuación
            agregar_puntuacion(self.usuario_actual_id,self.vino_id,  puntuacion)

            messagebox.showinfo("Éxito", "Momento guardado correctamente")
            self.destroy()
            self.master.master.deiconify()  # Regresar a la ventana principal
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el momento: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

class VentanaTopVinos(tk.Toplevel):
    def __init__(self, parent, usuario_actual_id):
        super().__init__(parent)
        self.usuario_actual_id = usuario_actual_id
        self.title("Top vinos")
        self.geometry("400x400")
        self.configure(bg="#4B0E0E")  # Fondo color burdeos oscuro

        self.boton_rcp = tk.Button(self, text="Mejor RCP", command=self.rcp, bg="#8B0000", fg="white")
        self.boton_rcp.pack(pady=10)

        self.boton_mejor = tk.Button(self, text="Mejor Vino", command=self.mejor, bg="#A52A2A", fg="white")
        self.boton_mejor.pack(pady=10)

        self.boton_regresar = tk.Button(self, text="Regresar", command=self.regresar, bg="#800000", fg="white")
        self.boton_regresar.pack(pady=10)

    def rcp(self):
        try:
            vinos_rcp = obtener_vino_mejor_rcp(self.usuario_actual_id)
            if vinos_rcp:
                for vino in vinos_rcp:
                    info_vino = f"Nombre: {vino[0]}, Precio: {vino[1]}, Puntuación: {vino[2]}"
                    tk.Label(self, text=info_vino, bg="#4B0E0E", fg="white").pack(pady=5)
            else:
                messagebox.showinfo("Info", "No se encontraron vinos con RCP")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener el vino con mejor RCP: {e}")

    def mejor(self):
        try:
            mejor_vino = obtener_vino_mejor_puntuacion(self.usuario_actual_id)
            if mejor_vino:
                info_vino = f"Nombre: {mejor_vino[0]}, Puntuación: {mejor_vino[1]}"
                tk.Label(self, text=info_vino, bg="#4B0E0E", fg="white").pack(pady=5)
            else:
                messagebox.showinfo("Info", "No se encontraron vinos con mejor puntuación")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener el vino con mejor puntuación: {e}")

    def regresar(self):
        self.destroy()
        self.master.deiconify()

if __name__ == "__main__": # en Python se utiliza para asegurar que cierto bloque de código solo se ejecute cuando el archivo es ejecutado directamente, y no cuando es importado como módulo en otro archivo.
    # Crear las tablas de la base de datos
    crear_tabla_usuarios()
    crear_tablas_adicionales()

    # Iniciar la aplicación
    app = VentanaInicioSesion()
    app.mainloop()
