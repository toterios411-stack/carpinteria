import sqlite3  # Importa la librería para manejar la base de datos SQLite

DB_NAME = "carpinteria.db"  # Nombre del archivo de la base de datos local

def obtener_conexion():
    conn = sqlite3.connect(DB_NAME)  # Abre o crea la conexión con la base de datos
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn  # Devuelve la conexión activa

def inicializar_bd():
    conn = obtener_conexion()  # Abre conexión con la BD
    cursor = conn.cursor()  # Crea el cursor para ejecutar sentencias SQL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
    """)  # Crea la tabla de usuarios si no existe
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))  # Busca si existe el usuario 'admin'
    if not cursor.fetchone():  # Si no existe 'admin'...
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", "1234"))  # Inserta usuario por defecto
        
    conn.commit()  # Guarda los cambios en el archivo .db
    conn.close()  # Cierra la conexión para liberar memoria

def validar_login(usuario, clave):
    conn = obtener_conexion()  # Abre la conexión
    cursor = conn.cursor()  # Crea el cursor
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))  # Verifica credenciales
    resultado = cursor.fetchone()  # Obtiene el registro encontrado
    conn.close()  # Cierra conexión
    return resultado is not None  # Retorna True si coincide, False si no

def registrar_usuario(usuario, clave):
    try:
        conn = obtener_conexion()  # Abre conexión
        cursor = conn.cursor()  # Crea el cursor
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario, clave))  # Agrega nuevo usuario
        conn.commit()  # Guarda los cambios
        conn.close()  # Cierra conexión
        return True, "Usuario registrado con éxito."  # Retorna tupla de éxito
    except sqlite3.IntegrityError:  # Captura error si el usuario ya existe (UNIQUE)
        return False, "El nombre de usuario ya existe."  # Retorna mensaje de error

def cambiar_clave(usuario, nueva_clave):
    conn = obtener_conexion()  # Abre la conexión
    cursor = conn.cursor()  # Crea el cursor
    cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (nueva_clave, usuario))  # Modifica la contraseña
    conn.commit()  # Guarda los cambios
    conn.close()  # Cierra la conexión
    return True, "Contraseña actualizada con éxito."  # Retorna mensaje de éxito

def cambiar_usuario(usuario_actual, nuevo_usuario):
    try:
        conn = obtener_conexion()  # Abre la conexión
        cursor = conn.cursor()  # Crea el cursor
        cursor.execute("UPDATE usuarios SET usuario = ? WHERE usuario = ?", (nuevo_usuario, usuario_actual))  # Modifica el nombre
        conn.commit()  # Guarda los cambios
        conn.close()  # Cierra la conexión
        return True, "Nombre de usuario actualizado con éxito."  # Retorna éxito
    except sqlite3.IntegrityError:  # En caso de que el nuevo nombre ya esté tomado
        return False, "El nuevo nombre de usuario ya está en uso."  # Retorna error

def obtener_todos_los_usuarios():
    conn = obtener_conexion()  # Abre la conexión a carpinteria.db
    cursor = conn.cursor()  # Crea el cursor SQL
    cursor.execute("SELECT id, usuario FROM usuarios")  # Ejecuta la consulta SQL
    usuarios = cursor.fetchall()  # Obtiene todas las filas resultantes
    conn.close()  # Cierra la conexión
    return usuarios  # Devuelve la lista de usuarios