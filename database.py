import sqlite3

DB_NAME = "carpinteria.db"

def obtener_conexion():
    """Establece y devuelve la conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_bd():
    """Crea la estructura de tablas para todos los módulos del sistema si no existen."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla 1: Usuarios (RF01, RF02, RF03)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'Operario'
    )
    """)

    # Tabla 2: Clientes (RF04, RF05)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ruc_cedula TEXT UNIQUE NOT NULL,
        nombre_razon_social TEXT NOT NULL,
        telefono TEXT,
        direccion TEXT,
        email TEXT
    )
    """)

    # Tabla 3: Materiales e Insumos (RF06, RF07, RF08, RF09)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        unidad_medida TEXT NOT NULL,
        stock_actual REAL DEFAULT 0,
        stock_minimo REAL DEFAULT 0,
        precio_unitario REAL DEFAULT 0
    )
    """)

    # Tabla 4: Proveedores (RF14)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ruc TEXT UNIQUE NOT NULL,
        nombre_empresa TEXT NOT NULL,
        contacto TEXT,
        telefono TEXT
    )
    """)

    # Tabla 5: Pedidos y Presupuestos (RF10, RF11, RF12, RF13, RF15)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        mueble_descripcion TEXT NOT NULL,
        dimensiones TEXT,
        costo_estimado REAL NOT NULL,
        monto_sena REAL DEFAULT 0,
        estado TEXT DEFAULT 'Presupuesto',
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_cliente) REFERENCES clientes (id)
    )
    """)

    # Usuario administrador por defecto
    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, clave, rol) VALUES ('admin', '1234', 'Administrador')")

    conn.commit()
    conn.close()

# --- FUNCIONES DE AUTENTICACIÓN Y USUARIOS ---
def validar_login(usuario, clave):
    """Valida si el usuario y la contraseña coinciden en la base de datos."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def registrar_usuario(usuario, clave, rol="Operario"):
    """Registra un nuevo usuario en el sistema."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)", (usuario, clave, rol))
        conn.commit()
        conn.close()
        return True, "Usuario registrado exitosamente."
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe."

def obtener_todos_los_usuarios():
    """Devuelve la lista completa de usuarios registrados para las pruebas unitarias."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, rol FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# --- FUNCIONES DE CLIENTES ---
def registrar_cliente(ruc_cedula, nombre, telefono, direccion, email):
    """Registra un cliente en la base de datos."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clientes (ruc_cedula, nombre_razon_social, telefono, direccion, email)
        VALUES (?, ?, ?, ?, ?)
        """, (ruc_cedula, nombre, telefono, direccion, email))
        conn.commit()
        conn.close()
        return True, "Cliente registrado exitosamente."
    except sqlite3.IntegrityError:
        return False, "El RUC o Cédula ya está registrado."

def obtener_clientes():
    """Retorna el listado completo de clientes."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos e infraestructura de tablas actualizadas.")