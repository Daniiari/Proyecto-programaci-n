import sqlite3

# Crear conexión a la base de datos
def crear_conexion():
    """Crea una conexión a la base de datos SQLite."""
    conn = sqlite3.connect('rpg_personajes.db')
    return conn

# Crear las tablas en la base de datos si no existen
def crear_tablas():
    """Crea las tablas necesarias en la base de datos."""
    conn = crear_conexion()
    cursor = conn.cursor()
    # Crear tabla de personajes
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS personajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            nombre TEXT NOT NULL,
            raza TEXT NOT NULL,
            genero TEXT NOT NULL,
            vida INTEGER NOT NULL,
            atributos TEXT NOT NULL,
            habilidades TEXT NOT NULL,
            gif_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Registrar un nuevo personaje en la base de datos
def registrar_personaje(usuario, nombre, raza, genero, vida, atributos, habilidades, gif_path):
    """Registra un nuevo personaje en la base de datos."""
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO personajes (usuario, nombre, raza, genero, vida, atributos, habilidades, gif_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (usuario, nombre, raza, genero, vida, atributos, habilidades, gif_path))
    conn.commit()
    conn.close()

# Cargar los personajes de la base de datos
def cargar_personajes_de_db(usuario):
    """Carga los personajes creados por un usuario desde la base de datos."""
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, raza, genero, vida, atributos, habilidades, gif_path FROM personajes WHERE usuario=?", (usuario,))
    personajes = cursor.fetchall()
    conn.close()
    
    return personajes

# Eliminar un personaje de la base de datos
def eliminar_personaje_de_db(id_personaje):
    """Elimina un personaje de la base de datos por su ID."""
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personajes WHERE id=?", (id_personaje,))
    conn.commit()
    conn.close()

# Mostrar personajes cargados de la base de datos
def mostrar_personajes(usuario):
    """Muestra los personajes del usuario."""
    personajes = cargar_personajes_de_db(usuario)
    
    if personajes:
        print(f"Personajes de {usuario}:")
        for personaje in personajes:
            print(f"ID: {personaje[0]}, Nombre: {personaje[1]}, Raza: {personaje[2]}, Género: {personaje[3]}, Vida: {personaje[4]}")
            print(f"Atributos: {personaje[5]}")
            print(f"Habilidades: {personaje[6]}")
            print(f"GIF: {personaje[7]}")
            print("-" * 40)
    else:
        print(f"No hay personajes registrados para el usuario {usuario}.")

# Función principal para eliminar un personaje por ID
def eliminar_personaje(usuario, id_personaje):
    """Elimina un personaje del usuario y muestra la lista actualizada."""
    print(f"Eliminando personaje con ID {id_personaje}...")
    eliminar_personaje_de_db(id_personaje)
    mostrar_personajes(usuario)

