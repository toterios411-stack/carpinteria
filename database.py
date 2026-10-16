import sqlite3
import hashlib

DB_NAME = "carpinteria.db"

def obtener_conexion():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def encriptar_password(password):
    """Cifra la contraseña usando SHA-256 para seguridad uniforme."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def inicializar_bd():
    """Inicializa las tablas relacionales del sistema y el admin cifrado."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla Usuarios con Rol (Módulo 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'Operario'
    )
    """)

    # Tabla Clientes
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

    # Tabla Materiales e Insumos (Módulo 3 - Stock de Cedro)
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

    # Usuario admin por defecto con contraseña cifrada
    pwd_admin = encriptar_password("1234")
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (usuario, clave, rol) 
    VALUES ('admin', ?, 'Administrador')
    """, (pwd_admin,))

    conn.commit()
    conn.close()

# --- MÓDULO 2: USUARIOS Y ROLES (LOGIN SEGURO) ---
def validar_login_con_rol(usuario, clave):
    """Valida el ingreso comparando el hash SHA-256 y devuelve el rol."""
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        clave_segura = encriptar_password(clave)
        
        cursor.execute("SELECT usuario, rol FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave_segura))
        res = cursor.fetchone()
        if res:
            return True, res[1]
        return False, None
    except Exception as e:
        return False, None
    finally:
        if conn:
            conn.close()

def registrar_usuario(usuario, clave, rol="Operario"):
    """Registra un nuevo usuario cifrando obligatoriamente su contraseña."""
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        clave_segura = encriptar_password(clave)
        
        cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)", (usuario, clave_segura, rol))
        conn.commit()
        return True, f"Usuario '{usuario}' registrado con éxito."
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe."
    except Exception as e:
        return False, f"Error al registrar: {str(e)}"
    finally:
        if conn:
            conn.close()

def obtener_todos_los_usuarios():
    """Retorna la lista completa de usuarios con sus roles."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, rol FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def actualizar_rol_usuario(usuario, nuevo_rol):
    """Modifica el rol de un usuario existente."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET rol = ? WHERE usuario = ?", (nuevo_rol, usuario))
    modificados = cursor.rowcount
    conn.commit()
    conn.close()
    if modificados > 0:
        return True, "Rol actualizado con éxito."
    return False, "Usuario no encontrado."

def eliminar_usuario(usuario):
    """Elimina una cuenta de usuario de la base de datos por su nombre."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
        filas_afectadas = cursor.rowcount
        conn.commit()
        conn.close()
        if filas_afectadas > 0:
            return True, f"El usuario '{usuario}' fue eliminado con éxito."
        return False, "No se encontró el usuario en la base de datos."
    except Exception as e:
        return False, f"Error al eliminar usuario: {str(e)}"

# --- MÓDULO 3: INVENTARIO Y MADERAS (CEDRO) ---
def registrar_material(codigo, nombre, tipo, unidad, stock, stock_min, precio):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO materiales (codigo, nombre, tipo, unidad_medida, stock_actual, stock_minimo, precio_unitario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nombre, tipo, unidad, stock, stock_min, precio))
        conn.commit()
        conn.close()
        return True, "Material registrado en inventario."
    except sqlite3.IntegrityError:
        return False, "El código de material ya existe."

def obtener_materiales():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nombre, tipo, unidad_medida, stock_actual, stock_minimo, precio_unitario FROM materiales")
    mat = cursor.fetchall()
    conn.close()
    return mat

def obtener_materiales_stock_bajo():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nombre, stock_actual, stock_minimo FROM materiales WHERE stock_actual <= stock_minimo")
    criticos = cursor.fetchall()
    conn.close()
    return criticos

# --- MÓDULO CLIENTES ---
def registrar_cliente(ruc_cedula, nombre, telefono, direccion, email=""):
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

def obtener_todos_los_clientes():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT ruc_cedula, nombre_razon_social, telefono, direccion FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def actualizar_cliente(ruc_cedula, nombre, telefono, direccion):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE clientes 
        SET nombre_razon_social = ?, telefono = ?, direccion = ?
        WHERE ruc_cedula = ? OR nombre_razon_social = ?
        """, (nombre, telefono, direccion, ruc_cedula, nombre))
        
        filas_afectadas = cursor.rowcount
        conn.commit()
        conn.close()
        
        if filas_afectadas > 0:
            return True, "Datos del cliente actualizados correctamente."
        return False, "No se encontró el registro del cliente a actualizar."
    except Exception as e:
        return False, f"Error al actualizar cliente: {str(e)}"

# --- MÓDULO 3: PEDIDOS Y STOCK DE CEDRO ---
def inicializar_tabla_pedidos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_cedro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        trabajo TEXT NOT NULL,
        cant_cedro INTEGER NOT NULL,
        plazo_dias INTEGER DEFAULT 15,
        estado TEXT NOT NULL DEFAULT 'Pendiente'
    )
    """)
    cursor.execute("PRAGMA table_info(pedidos_cedro)")
    columnas = [col[1] for col in cursor.fetchall()]
    if "plazo_dias" not in columnas:
        cursor.execute("ALTER TABLE pedidos_cedro ADD COLUMN plazo_dias INTEGER DEFAULT 15")
    conn.commit()
    conn.close()

def registrar_pedido_cedro(cliente_nombre, trabajo, plazo_dias, ruc="", telefono="", direccion=""):
    try:
        inicializar_tabla_pedidos()
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE nombre_razon_social = ?", (cliente_nombre,))
        cliente_existe = cursor.fetchone()
        
        if not cliente_existe and cliente_nombre.strip():
            cursor.execute("""
            INSERT INTO clientes (ruc_cedula, nombre_razon_social, telefono, direccion, email)
            VALUES (?, ?, ?, ?, '')
            """, (ruc if ruc else "S/D", cliente_nombre, telefono, direccion))

        trabajo_lower = trabajo.lower()
        if "4 cuerpos" in trabajo_lower:
            cant_cedro = 12
        elif "3 cuerpos" in trabajo_lower:
            cant_cedro = 9
        elif "2 cuerpos" in trabajo_lower:
            cant_cedro = 6
        elif "1 cuerpo" in trabajo_lower:
            cant_cedro = 4
        elif "comedor" in trabajo_lower:
            cant_cedro = 10
        else:
            cant_cedro = 5

        cursor.execute("""
        INSERT INTO pedidos_cedro (cliente, trabajo, cant_cedro, plazo_dias, estado)
        VALUES (?, ?, ?, ?, 'Pendiente')
        """, (cliente_nombre, trabajo, cant_cedro, plazo_dias))
        
        conn.commit()
        conn.close()
        return True, f"Pedido registrado con éxito. Cliente '{cliente_nombre}' guardado."
    except Exception as e:
        return False, f"Error al registrar el pedido: {str(e)}"

def obtener_todos_los_pedidos_cedro():
    inicializar_tabla_pedidos()
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente, trabajo, cant_cedro, plazo_dias, estado FROM pedidos_cedro ORDER BY id DESC")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def actualizar_pedido_cedro(pedido_id, trabajo, plazo_dias, estado):
    try:
        trabajo_lower = trabajo.lower()
        if "4 cuerpos" in trabajo_lower:
            cant_cedro = 12
        elif "3 cuerpos" in trabajo_lower:
            cant_cedro = 9
        elif "2 cuerpos" in trabajo_lower:
            cant_cedro = 6
        elif "1 cuerpo" in trabajo_lower:
            cant_cedro = 4
        elif "comedor" in trabajo_lower:
            cant_cedro = 10
        else:
            cant_cedro = 5

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE pedidos_cedro 
        SET trabajo = ?, cant_cedro = ?, plazo_dias = ?, estado = ?
        WHERE id = ?
        """, (trabajo, cant_cedro, plazo_dias, estado, pedido_id))
        conn.commit()
        conn.close()
        return True, "Pedido actualizado con éxito."
    except Exception as e:
        return False, f"Error al actualizar el pedido: {str(e)}"

def eliminar_pedido_cedro(pedido_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos_cedro WHERE id = ?", (pedido_id,))
        conn.commit()
        conn.close()
        return True, "Pedido eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar el pedido: {str(e)}"

# --- MÓDULO 3: CATÁLOGO DE MUEBLES / TRABAJOS ---
def inicializar_tabla_muebles():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_muebles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)
    muebles_base = [
        ("Ropero de 4 cuerpos",),
        ("Ropero de 3 cuerpos",),
        ("Ropero de 2 cuerpos",),
        ("Ropero de 1 cuerpo",),
        ("Juego de Comedor",),
        ("Puerta Placa de Cedro",)
    ]
    cursor.executemany("INSERT OR IGNORE INTO tipos_muebles (nombre) VALUES (?)", muebles_base)
    conn.commit()
    conn.close()

def obtener_tipos_muebles():
    inicializar_tabla_muebles()
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM tipos_muebles ORDER BY nombre ASC")
    muebles = [r[0] for r in cursor.fetchall()]
    conn.close()
    return muebles

def registrar_nuevo_mueble(nombre):
    try:
        inicializar_tabla_muebles()
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO tipos_muebles (nombre) VALUES (?)", (nombre,))
        conn.commit()
        conn.close()
    except Exception:
        pass