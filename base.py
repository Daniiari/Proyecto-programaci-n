import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

# Conectar a la base de datos
conn = sqlite3.connect("personajes_rpg.db")
cursor = conn.cursor()

# Variable global para el usuario actual
usuario_actual_id = None

# Conexión a la base de datos
conn = sqlite3.connect('personajes_rpg.db')
cursor = conn.cursor()

def inicio_sesion():
    def autenticar():
        global usuario_actual_id
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        cursor.execute("SELECT id FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            usuario_actual_id = resultado[0]
            messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
            ventana.destroy()  # Cierra la ventana de inicio de sesión
            # Aquí puedes añadir tu lógica para continuar con el juego
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    ventana = Toplevel()
    ventana.title("Iniciar Sesión")
    ventana.geometry("300x200")

    Label(ventana, text="Usuario:").pack(pady=5)
    entry_usuario = Entry(ventana)
    entry_usuario.pack(pady=5)

    Label(ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = Entry(ventana, show="*")
    entry_contrasena.pack(pady=5)

    Button(ventana, text="Iniciar Sesión", command=autenticar).pack(pady=10)

def registro_usuario():
    def registrar():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
            conn.commit()
            messagebox.showinfo("Registro", "¡Usuario registrado con éxito!")
            ventana.destroy()  # Cierra la ventana de registro
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")

    ventana = Toplevel()
    ventana.title("Registrar Usuario")
    ventana.geometry("300x200")

    Label(ventana, text="Usuario:").pack(pady=5)
    entry_usuario = Entry(ventana)
    entry_usuario.pack(pady=5)

    Label(ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = Entry(ventana, show="*")
    entry_contrasena.pack(pady=5)

    Button(ventana, text="Registrar", command=registrar).pack(pady=10)


class Personaje:
    def __init__(self, nombre, raza, genero, atributos, habilidades, vida, gif_path):
        self.nombre = nombre
        self.raza = raza
        self.genero = genero
        self.atributos = atributos
        self.habilidades = habilidades
        self.vida = vida
        self.gif_path = gif_path
        self.inventario = []

personajes_creados = []

vida_base_por_raza = {
    "Humano": 100,
    "Elfo": 80,
    "Enano": 120,
    "Orco": 150,
    "Hombre Lobo": 140,
    "Duende": 90,
    "Demonio": 130
}

atributos_por_raza = {
    "Humano": {"Fuerza": 5, "Agilidad": 5, "Inteligencia": 5},
    "Elfo": {"Fuerza": 3, "Agilidad": 7, "Inteligencia": 6},
    "Enano": {"Fuerza": 7, "Agilidad": 4, "Inteligencia": 5},
    "Orco": {"Fuerza": 8, "Agilidad": 3, "Inteligencia": 4},
    "Hombre Lobo": {"Fuerza": 8, "Agilidad": 7, "Inteligencia": 3},
    "Duende": {"Fuerza": 3, "Agilidad": 8, "Inteligencia": 7},
    "Demonio": {"Fuerza": 8, "Agilidad": 3, "Inteligencia": 8}
}

# Función para verificar inicio de sesión
def inicio_sesion():
    ventana_principal.withdraw()  # Ocultar la ventana principal temporalmente
    login_ventana = tk.Toplevel()
    login_ventana.title("Iniciar Sesión")
    login_ventana.geometry("300x250")

    tk.Label(login_ventana, text="Usuario:").pack(pady=5)
    entry_usuario = ttk.Entry(login_ventana)
    entry_usuario.pack()

    tk.Label(login_ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = ttk.Entry(login_ventana, show="*")
    entry_contrasena.pack()

    def autenticar():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Debe ingresar un usuario y contraseña.")
            return

        cursor.execute("SELECT id FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            global usuario_actual_id
            usuario_actual_id = resultado[0]
            login_ventana.destroy()
            ventana_principal.deiconify()  # Mostrar la ventana principal nuevamente
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Debe ingresar un usuario y contraseña.")
            return

        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")

    ttk.Button(login_ventana, text="Iniciar Sesión", command=autenticar).pack(pady=10)
    ttk.Button(login_ventana, text="Registrar", command=registrar).pack(pady=10)

def crear_personaje():
    ventana = tk.Toplevel()
    ventana.title("Crear Personaje")
    ventana.geometry("425x650")
    ventana.configure(bg="#f0f0f0")

    frame_nombre = ttk.Frame(ventana, padding=5)
    frame_nombre.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_nombre, text="Nombre del Personaje:", font=("Arial", 10)).pack(anchor="w")
    entry_nombre = ttk.Entry(frame_nombre)
    entry_nombre.pack(fill="x")

    frame_raza = ttk.Frame(ventana, padding=5)
    frame_raza.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_raza, text="Raza:", font=("Arial", 10)).pack(anchor="w")
    raza_var = tk.StringVar()
    raza_var.set("Humano")
    razas = ["Humano", "Humano", "Elfo", "Enano", "Orco", "Hombre Lobo", "Duende", "Demonio"]
    ttk.OptionMenu(frame_raza, raza_var, *razas).pack(fill="x")

    frame_genero = ttk.Frame(ventana, padding=5)
    frame_genero.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_genero, text="Género:", font=("Arial", 10)).pack(anchor="w")
    genero_var = tk.StringVar()
    genero_var.set("Masculino")
    ttk.OptionMenu(frame_genero, genero_var, "Masculino", "Masculino", "Femenino").pack(fill="x")

    frame_piel = ttk.Frame(ventana, padding=5)
    frame_piel.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_piel, text="Color de Piel:", font=("Arial", 10)).pack(anchor="w")
    color_piel_var = tk.StringVar()
    color_piel_var.set("Blanco")
    opcion_piel_menu = ttk.OptionMenu(frame_piel, color_piel_var, "Blanco", "Blanco", "Moreno")
    opcion_piel_menu.pack(fill="x")

    frame_version = ttk.Frame(ventana, padding=5)
    frame_version.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_version, text="Versión del Aspecto:", font=("Arial", 10)).pack(anchor="w")
    version_var = tk.StringVar()
    version_var.set("v1")
    ttk.OptionMenu(frame_version, version_var, "v1", "v1", "v2", "v3").pack(fill="x")

    gif_label = tk.Label(ventana)
    gif_label.pack(pady=10)

    pixelart_gifs = {
        "Humano": {"Masculino": {"Blanco": ["imagenes/humano_m_b.v1.gif", "imagenes/humano_m_b.v2.gif", "imagenes/humano_m_b.v3.gif"],
                                 "Moreno": ["imagenes/humano_m_n.v1.gif", "imagenes/humano_m_n.v2.gif", "imagenes/humano_m_n.v3.gif"]},
                   "Femenino": {"Blanco": ["imagenes/humano_f_b.v1.gif", "imagenes/humano_f_b.v2.gif", "imagenes/humano_f_b.v3.gif"],
                                "Moreno": ["imagenes/humano_f_n.v1.gif", "imagenes/humano_f_n.v2.gif", "imagenes/humano_f_n.v3.gif"]}},
        "Elfo": {"Masculino": {"Blanco": ["imagenes/elfo_m_b.v1.gif", "imagenes/elfo_m_b.v2.gif", "imagenes/elfo_m_b.v3.gif"],
                               "Moreno": ["imagenes/elfo_m_n.v1.gif", "imagenes/elfo_m_n.v2.gif", "imagenes/elfo_m_n.v3.gif"]},
                 "Femenino": {"Blanco": ["imagenes/elfo_f_b.v1.gif", "imagenes/elfo_f_b.v2.gif", "imagenes/elfo_f_b.v3.gif"],
                              "Moreno": ["imagenes/elfo_f_n.v1.gif", "imagenes/elfo_f_n.v2.gif", "imagenes/elfo_f_n.v3.gif"]}},
        "Enano": {"Masculino": {"Blanco": ["imagenes/enano_m_b.v1.gif", "imagenes/enano_m_b.v2.gif", "imagenes/enano_m_b.v3.gif"],
                                "Moreno": ["imagenes/enano_m_n.v1.gif", "imagenes/enano_m_n.v2.gif", "imagenes/enano_m_n.v3.gif"]},
                  "Femenino": {"Blanco": ["imagenes/enano_f_b.v1.gif", "imagenes/enano_f_b.v2.gif", "imagenes/enano_f_b.v3.gif"],
                               "Moreno": ["imagenes/enano_f_n.v1.gif", "imagenes/enano_f_n.v2.gif", "imagenes/enano_f_n.v3.gif"]}},
        "Orco": {"Masculino": ["imagenes/orco_m.v1.gif", "imagenes/orco_m.v2.gif", "imagenes/orco_m.v3.gif"],
                "Femenino": ["imagenes/orco_f.v1.gif", "imagenes/orco_f.v2.gif", "imagenes/orco_f.v3.gif"]},
        "Hombre Lobo": {"Masculino": ["imagenes/Lobo_m.v1.gif", "imagenes/Lobo_m.v2.gif", "imagenes/Lobo_m.v3.gif"],
                 "Femenino": ["imagenes/Lobo_f.v1.gif", "imagenes/Lobo_f.v2.gif", "imagenes/Lobo_f.v3.gif"]},
        "Duende": {"Masculino": ["imagenes/Duende_m.v1.gif", "imagenes/Duende_m.v2.gif", "imagenes/Duende_m.v3.gif"],
                 "Femenino": ["imagenes/Duende_f.v1.gif", "imagenes/Duende_f.v2.gif", "imagenes/Duende_f.v3.gif"]},
        "Demonio": {"Masculino": ["imagenes/Demonio_m.v1.gif", "imagenes/Demonio_m.v2.gif", "imagenes/Demonio_m.v3.gif"],
                 "Femenino": ["imagenes/Demonio_f.v1.gif", "imagenes/Demonio_f.v2.gif", "imagenes/Demonio_f.v3.gif"]}
    }

    def actualizar_pixelart(*args):
        raza = raza_var.get()
        genero = genero_var.get()
        color_piel = color_piel_var.get() if raza in ["Humano", "Elfo", "Enano"] else None
        version = version_var.get()
        try:
            if color_piel: 
                gif_path = pixelart_gifs[raza][genero][color_piel][int(version[-1]) - 1]
            else:  
                gif_path = pixelart_gifs[raza][genero][int(version[-1]) - 1]

            imagen = Image.open(gif_path)
            imagen = imagen.resize((120, 120))
            gif = ImageTk.PhotoImage(imagen)
            gif_label.config(image=gif)
            gif_label.image = gif
        except (KeyError, IndexError, tk.TclError):
            gif_label.config(text="Imagen no disponible", image="")
            gif_label.image = None

    def actualizar_opcion_piel(*args):
        raza_actual = raza_var.get()
        razas_con_color_piel = ["Humano", "Elfo", "Enano"]

        if raza_actual in razas_con_color_piel:
            opcion_piel_menu.config(state="normal")
        else:
            opcion_piel_menu.config(state="disabled")

    actualizar_pixelart()

    raza_var.trace("w", lambda *args: (actualizar_pixelart(), actualizar_opcion_piel()))
    genero_var.trace("w", actualizar_pixelart)
    color_piel_var.trace("w", actualizar_pixelart)
    version_var.trace("w", actualizar_pixelart)
    actualizar_pixelart()

    frame_atributos = ttk.Frame(ventana, padding=5)
    frame_atributos.pack(fill="x", padx=10, pady=10)
    tk.Label(frame_atributos, text="Atributos:", font=("Arial", 10, "bold")).pack(anchor="w")
    puntos_disponibles = 10
    atributos = atributos_por_raza[raza_var.get()].copy()

    def actualizar_atributos_por_raza(*args):
        nonlocal atributos
        atributos = atributos_por_raza[raza_var.get()].copy()
        actualizar_labels()

    raza_var.trace("w", actualizar_atributos_por_raza)

    label_fuerza = ttk.Label(frame_atributos, text=f"Fuerza: {atributos['Fuerza']}")
    label_fuerza.pack(side="left", padx=5)
    ttk.Button(frame_atributos, text="-", width=3, command=lambda a="Fuerza": actualizar_atributos(a, -1)).pack(side="left")
    ttk.Button(frame_atributos, text="+", width=3, command=lambda a="Fuerza": actualizar_atributos(a, 1)).pack(side="left")

    label_agilidad = ttk.Label(frame_atributos, text=f"Agilidad: {atributos['Agilidad']}")
    label_agilidad.pack(side="left", padx=5)
    ttk.Button(frame_atributos, text="-", width=3, command=lambda a="Agilidad": actualizar_atributos(a, -1)).pack(side="left")
    ttk.Button(frame_atributos, text="+", width=3, command=lambda a="Agilidad": actualizar_atributos(a, 1)).pack(side="left")

    label_inteligencia = ttk.Label(frame_atributos, text=f"Inteligencia: {atributos['Inteligencia']}")
    label_inteligencia.pack(side="left", padx=5)
    ttk.Button(frame_atributos, text="-", width=3, command=lambda a="Inteligencia": actualizar_atributos(a, -1)).pack(side="left")
    ttk.Button(frame_atributos, text="+", width=3, command=lambda a="Inteligencia": actualizar_atributos(a, 1)).pack(side="left")

    def actualizar_atributos(atributo, cambio):
        nonlocal puntos_disponibles
        if (cambio > 0 and puntos_disponibles > 0) or (cambio < 0 and atributos[atributo] > 0):
            atributos[atributo] += cambio
            puntos_disponibles -= cambio
            actualizar_labels()

    frame_puntos = ttk.Frame(ventana, padding=5)
    frame_puntos.pack(fill="x", padx=10, pady=5)
    label_puntos = tk.Label(frame_puntos, text=f"Puntos disponibles: {puntos_disponibles}", font=("Arial", 10, "bold"))
    label_puntos.pack()

    def actualizar_labels():
        label_fuerza.config(text=f"Fuerza: {atributos['Fuerza']}")
        label_agilidad.config(text=f"Agilidad: {atributos['Agilidad']}")
        label_inteligencia.config(text=f"Inteligencia: {atributos['Inteligencia']}")
        label_puntos.config(text=f"Puntos disponibles: {puntos_disponibles}")

    
    def guardar_personaje():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El personaje debe tener un nombre.")
            return
        raza = raza_var.get()
        genero = genero_var.get()
        color_piel = color_piel_var.get()
        version = version_var.get()

        if raza in ["Humano", "Elfo", "Enano"]:
            gif_path = pixelart_gifs[raza][genero][color_piel][int(version[-1]) - 1]
        else:
            gif_path = pixelart_gifs[raza][genero][int(version[-1]) - 1]

        vida = vida_base_por_raza[raza]
        habilidades = ["Espadas"]

        nuevos_atributos = atributos.copy()

        cursor.execute('''
            INSERT INTO personajes (usuario_id, nombre, raza, genero, atributos, habilidades, vida, gif_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_actual_id, nombre, raza, genero, str(nuevos_atributos), str(habilidades), vida, gif_path))
        conn.commit()

        messagebox.showinfo("Éxito", f"Personaje {nombre} creado con éxito.")
        ventana.destroy()

    guardar_button = ttk.Button(ventana, text="Guardar Personaje", command=guardar_personaje)
    guardar_button.pack(pady=10)


def ver_personajes():
    # Crear ventana para ver personajes
    ventana_ver = tk.Toplevel()
    ventana_ver.title("Tus personajes")
    ventana_ver.geometry("500x500")

    # Título
    tk.Label(ventana_ver, text="Tus Personajes", font=("Arial", 16)).pack(pady=10)

    # Obtener personajes del usuario actual
    cursor.execute("SELECT nombre, raza, genero, vida, atributos, habilidades, gif_path FROM personajes WHERE usuario_id = ?", (usuario_actual_id,))
    personajes = cursor.fetchall()

    if not personajes:
        tk.Label(ventana_ver, text="No tienes personajes creados.").pack(pady=20)
    else:
        for personaje in personajes:
            # Desempaquetar los datos
            nombre, raza, genero, vida, atributos, habilidades, gif_path = personaje

            # Crear un marco para cada personaje
            marco = tk.Frame(ventana_ver, bd=2, relief="groove", padx=10, pady=10)
            marco.pack(fill="x", padx=10, pady=5)

            # Mostrar detalles del personaje
            tk.Label(marco, text=f"Nombre: {nombre}", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(marco, text=f"Raza: {raza}").pack(anchor="w")
            tk.Label(marco, text=f"Género: {genero}").pack(anchor="w")
            tk.Label(marco, text=f"Vida: {vida}").pack(anchor="w")
            tk.Label(marco, text=f"Atributos: {atributos}").pack(anchor="w")
            tk.Label(marco, text=f"Habilidades: {habilidades}").pack(anchor="w")

            # Mostrar GIF (si existe)
            if gif_path and os.path.exists(gif_path):
                img = tk.PhotoImage(file=gif_path)
                tk.Label(marco, image=img).pack(anchor="center")
                # Importante: mantener una referencia para evitar que la imagen se elimine
                marco.image = img

ventana = Tk()
ventana.title("Juego RPG")
ventana.geometry("400x300")

ttk.Button(ventana, text="Iniciar Sesión", command=inicio_sesion).pack(pady=10)
ttk.Button(ventana, text="Registrar Usuario", command=registro_usuario).pack(pady=10)

ventana_principal = tk.Tk()
ventana_principal.title("Creador de Personajes RPG")
ventana_principal.geometry("300x200")

ttk.Button(ventana_principal, text="Crear Personaje", command=crear_personaje).pack(pady=10)
ttk.Button(ventana_principal, text="Ver Personajes", command=ver_personajes).pack(pady=10)

ventana_principal.mainloop()