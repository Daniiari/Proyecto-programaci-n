import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sqlite3
import database  # Asegúrate de que este módulo esté correctamente implementado

# Clase para representar un personaje
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

# Lista para almacenar personajes creados
personajes_creados = []

# Datos de vida base y atributos por raza
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

# Función para cargar personajes de la base de datos
def cargar_personajes_de_db(usuario):
    personajes = []
    conn = sqlite3.connect('rpg_personajes.db')  # Cambia esto al nombre de tu base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, raza, genero, vida, atributos, habilidades, gif_path FROM personajes WHERE usuario=?", (usuario,))
    filas = cursor.fetchall()
    for fila in filas:
        nombre, raza, genero, vida, atributos_str, habilidades_str, gif_path = fila
        atributos = eval(atributos_str)  # Convierte la cadena de atributos de vuelta a un diccionario
        habilidades = habilidades_str.split(', ')  # Convierte la cadena de habilidades a una lista
        personaje = Personaje(nombre, raza, genero, atributos, habilidades, vida, gif_path)
        personajes.append(personaje)
    conn.close()
    return personajes

# Función para crear la ventana de creación de personajes
def crear_personaje():
    ventana = tk.Toplevel()
    ventana.title("Crear Personaje")
    ventana.geometry("425x650")
    ventana.configure(bg="#f0f0f0")

    # Frame para el nombre
    frame_nombre = ttk.Frame(ventana, padding=5)
    frame_nombre.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_nombre, text="Nombre del Personaje:", font=("Arial", 10)).pack(anchor="w")
    entrada_nombre = ttk.Entry(frame_nombre)
    entrada_nombre.pack(fill="x")

    # Frame para la raza
    frame_raza = ttk.Frame(ventana, padding=5)
    frame_raza.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_raza, text="Raza:", font=("Arial", 10)).pack(anchor="w")
    raza_var = tk.StringVar()
    raza_var.set("Humano")
    razas = ["Humano", "Elfo", "Enano", "Orco", "Hombre Lobo", "Duende", "Demonio"]
    menu_raza = ttk.OptionMenu(frame_raza, raza_var, raza_var.get(), *razas)
    menu_raza.pack(fill="x")

    # Frame para el género
    frame_genero = ttk.Frame(ventana, padding=5)
    frame_genero.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_genero, text="Género:", font=("Arial",  10)).pack(anchor="w")
    genero_var = tk.StringVar()
    genero_var.set("Masculino")
    ttk.OptionMenu(frame_genero, genero_var, "Masculino", "Masculino", "Femenino").pack(fill="x")

    # Frame para el color de piel
    frame_piel = ttk.Frame(ventana, padding=5)
    frame_piel.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_piel, text="Color de Piel:", font=("Arial", 10)).pack(anchor="w")
    color_piel_var = tk.StringVar()
    color_piel_var.set("Blanco")
    opcion_piel_menu = ttk.OptionMenu(frame_piel, color_piel_var, "Blanco", "Blanco", "Moreno")
    opcion_piel_menu.pack(fill="x")

    # Frame para la versión del aspecto
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
        color_piel = color_piel_var.get()
        version = version_var.get()
        try:
            # verifica si la raza tiene subdivicion por color de piel
            if  raza in ['Humano', 'Elfo', 'Enano']:
                gif_path = pixelart_gifs[raza][genero][color_piel][int(version[-1]) - 1]
            else:
                gif_path = pixelart_gifs[raza][genero][int(version[-1]) - 1]
            # Cargar y mostrar la imagen
            imagen = Image.open(gif_path)
            imagen = imagen.resize((120, 120))
            gif = ImageTk.PhotoImage(imagen)
            gif_label.config(image=gif)
            gif_label.image = gif
        except (KeyError, IndexError, tk.TclError, TypeError):
            gif_label.config(text="Imagen no disponible", image="")
            gif_label.image = None

    def actualizar_opcion_piel(*args):
        raza_actual = raza_var.get()
        razas_con_color_piel = ["Humano", "Elfo", "Enano"]
        if raza_actual in razas_con_color_piel:
            opcion_piel_menu.config(state="normal")
        else:
            opcion_piel_menu.config(state="disabled")

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

    def actualizar_labels():
        label_fuerza.config(text=f"Fuerza: {atributos['Fuerza']}")
        label_agilidad.config(text=f"Agilidad: {atributos['Agilidad']}")
        label_inteligencia.config(text=f"Inteligencia: {atributos['Inteligencia']}")
        label_puntos.config(text=f"Puntos disponibles: {puntos_disponibles}")

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
        if cambio > 0 and puntos_disponibles > 0:
            atributos[atributo] += cambio 
            puntos_disponibles -= cambio
        elif cambio < 0 and atributos[atributo] > 0:
            atributos[atributo] += cambio
            puntos_disponibles -= cambio
        actualizar_labels()

    frame_puntos = ttk.Frame(ventana, padding=5)
    frame_puntos.pack(fill="x", padx=10, pady=5)
    label_puntos = tk.Label(frame_puntos, text=f"Puntos disponibles: {puntos_disponibles}", font=("Arial", 10, "bold"))
    label_puntos.pack()

    def guardar_personaje():
        nombre = entrada_nombre.get().strip()
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
        nuevo_personaje = Personaje(nombre, raza, genero, nuevos_atributos, habilidades, vida, gif_path)
        personajes_creados.append(nuevo_personaje)
        # Registrar el personaje en la base de datos
        database.registrar_personaje(usuario, nombre, raza, genero, vida, str(nuevos_atributos), ', '.join(habilidades), gif_path)
        messagebox.showinfo("Éxito", f"Personaje {nombre} creado con éxito.")
        ventana.destroy()

    guardar_boton = ttk.Button(ventana, text="Guardar Personaje", command=guardar_personaje)
    guardar_boton.pack(pady=10)
    
def ver_personajes():
    ventana = tk.Toplevel()
    ventana.title("Personajes Creados")
    ventana.geometry("500x400")

    # Crear canvas y scrollbar
    contenedor_canvas = tk.Frame(ventana)
    contenedor_canvas.pack(fill="both", expand=True)

    canvas = tk.Canvas(contenedor_canvas)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(contenedor_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno dentro del canvas
    frame_contenido = ttk.Frame(canvas)
    frame_contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Añadir frame_contenido al canvas
    canvas.create_window((0, 0), window=frame_contenido, anchor="nw")

    # Cargar personajes del usuario desde la base de datos
    personajes_cargados = cargar_personajes_de_db(usuario)

    # Combinar personajes creados en la sesión actual y los cargados de la base de datos
    todos_los_personajes = personajes_cargados.copy()  # Inicia con personajes de la base de datos
    nombres_existentes = {p.nombre for p in personajes_cargados}  # Nombres ya cargados

    # Añadir personajes creados en la sesión si no están duplicados
    for personaje in personajes_creados:
        if personaje.nombre not in nombres_existentes:
            todos_los_personajes.append(personaje)
            nombres_existentes.add(personaje.nombre)

    # Añadir información de los personajes al frame_contenido
    for personaje in todos_los_personajes:
        frame = ttk.Frame(frame_contenido, padding=5)
        frame.pack(fill="x", padx=5, pady=5)

        try:
            imagen = Image.open(personaje.gif_path)
            imagen = imagen.resize((80, 80))
            gif = ImageTk.PhotoImage(imagen)
            gif_label = tk.Label(frame, image=gif)
            gif_label.image = gif
            gif_label.pack(side="left", padx=5)
        except:
            tk.Label(frame, text="Imagen no disponible").pack(side="left", padx=5)

        info = (f"Nombre: {personaje.nombre}\n"
                f"Raza: {personaje.raza}\n"
                f"Género: {personaje.genero}\n"
                f"Vida: {personaje.vida}\n"
                f"Atributos: {personaje.atributos}\n")

        tk.Label(frame, text=info, wraplength=400, justify="left").pack(side="left", padx=10)

    # Activar scroll con el mouse
    def scroll(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", scroll)


def eliminar_personaje():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Personaje")
    ventana.geometry("500x400")
    
    tk.Label(ventana, text="Selecciona un personaje para eliminar:", font=("Arial", 12)).pack(pady=10)
    
    lista_personajes = tk.Listbox(ventana, width=60, height=15)
    lista_personajes.pack(pady=10)
    
    # Cargar personajes desde base de datos y memoria
    personajes_cargados = cargar_personajes_de_db(usuario)
    todos_los_personajes = list({p.nombre: p for p in personajes_creados + personajes_cargados}.values())
    
    # Relación de nombres a objetos de personajes
    nombres_a_personajes = {p.nombre: p for p in todos_los_personajes}
    
    # Insertar nombres en la lista
    for personaje in nombres_a_personajes.keys():
        lista_personajes.insert(tk.END, personaje)
    
    def confirmar_eliminacion():
        seleccionado = lista_personajes.curselection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un personaje para eliminar.")
            return
        
        nombre_seleccionado = lista_personajes.get(seleccionado[0])
        personaje_a_eliminar = nombres_a_personajes.get(nombre_seleccionado)
        
        if not personaje_a_eliminar:
            messagebox.showerror("Error", "No se pudo encontrar el personaje.")
            return
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar a {nombre_seleccionado}?")
        if not confirmacion:
            return
        
        # Eliminar de la base de datos
        conn = sqlite3.connect('rpg_personajes.db')  # Cambia esto al nombre de tu base de datos
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personajes WHERE nombre=? AND usuario=?", (nombre_seleccionado, usuario))
        conn.commit()
        conn.close()
        
        # Eliminar de la lista de personajes en memoria
        if personaje_a_eliminar in personajes_creados:
            personajes_creados.remove(personaje_a_eliminar)
        
        # Actualizar la lista visual en la interfaz
        lista_personajes.delete(seleccionado[0])
        messagebox.showinfo("Éxito", f"El personaje {nombre_seleccionado} ha sido eliminado.")
    
    tk.Button(ventana, text="Eliminar", command=confirmar_eliminacion, bg="red", fg="white").pack(pady=10)
    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=5)


def cambiar_usuario():
    nuevo_usuario = simpledialog.askstring("Cambio de Usuario", "Por favor, ingresa un nuevo nombre de usuario:")
    if nuevo_usuario:
        global usuario  # Actualizar la variable global del usuario
        usuario = nuevo_usuario.lower()
        messagebox.showinfo("Usuario cambiado", f"El nombre de usuario ha sido cambiado a: {usuario}")
        ventana_principal.title(f"Creador de Personajes RPG - {usuario}")  # Actualizar el título de la ventana



ventana_principal = tk.Tk()
ventana_principal.title("Creador de Personajes RPG")
ventana_principal.geometry("300x200")
# Dentro de la ventana_principal:
ttk.Button(ventana_principal, text="Cambiar Usuario", command=cambiar_usuario).pack(pady=10)


# Solicitar nombre del usuario
usuario = simpledialog.askstring("Inicio de sesión", "Por favor, ingresa tu nombre de usuario:").lower()
if not usuario:
    messagebox.showerror("Error", "Debes ingresar un nombre de usuario para continuar.")
    ventana_principal.destroy()
else:
    messagebox.showinfo("Bienvenido", f"Hola, {usuario}! Bienvenido al creador de personajes.")
    ttk.Button(ventana_principal, text="Crear Personaje", command=crear_personaje).pack(pady=10)
    ttk.Button(ventana_principal, text="Ver Personajes", command=ver_personajes).pack(pady=10)
    ttk.Button(ventana_principal, text="Eliminar Personaje", command=eliminar_personaje).pack(pady=10)


ventana_principal.mainloop()
