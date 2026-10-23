import sqlite3
import hashlib

DB_NAME = "carpinteria.db"

def obtener_conexion():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def encriptar_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def inicializar_bd():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'CARPINTERO (Operario)'
        )
        """)

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

        pwd_admin = encriptar_password("1234")
        cursor.execute("""
        INSERT OR IGNORE INTO usuarios (usuario, clave, rol) 
        VALUES ('admin', ?, 'ADMINISTRADOR (Administrador)')
        """, (pwd_admin,))

        conn.commit()
    finally:
        conn.close()

# --- MÓDULO: USUARIOS Y ROLES ---
def validar_login_con_rol(usuario, clave):
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
    except Exception:
        return False, None
    finally:
        if conn:
            conn.close()

def registrar_usuario(usuario_nombre, password, rol):
    rol = rol.strip().upper()
    clave_segura = encriptar_password(password)
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario_nombre,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."
            
        cursor.execute("""
        INSERT INTO usuarios (usuario, clave, rol) 
        VALUES (?, ?, ?)
        """, (usuario_nombre, clave_segura, rol))
        
        conn.commit()
        return True, "Usuario registrado con éxito."
    except Exception as e:
        return False, f"Error al registrar: {e}"
    finally:
        conn.close()

def obtener_todos_los_usuarios():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, UPPER(rol) FROM usuarios")
        return cursor.fetchall()
    finally:
        conn.close()

def eliminar_usuario(usuario):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
        filas_afectadas = cursor.rowcount
        conn.commit()
        if filas_afectadas > 0:
            return True, f"El usuario '{usuario}' fue eliminado con éxito."
        return False, "No se encontró el usuario en la base de datos."
    except Exception as e:
        return False, f"Error al eliminar usuario: {str(e)}"
    finally:
        conn.close()

# --- MÓDULO: CLIENTES ---
def registrar_cliente(ruc_cedula, nombre, telefono, direccion, email=""):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clientes (ruc_cedula, nombre_razon_social, telefono, direccion, email)
        VALUES (?, ?, ?, ?, ?)
        """, (ruc_cedula, nombre.upper(), telefono, direccion, email))
        conn.commit()
        return True, "Cliente registrado exitosamente."
    except sqlite3.IntegrityError:
        return False, "El RUC o Cédula ya está registrado."
    except Exception as e:
        return False, f"Error al registrar cliente: {str(e)}"
    finally:
        conn.close()

def obtener_todos_los_clientes():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, UPPER(nombre_razon_social), ruc_cedula, telefono, direccion FROM clientes ORDER BY id ASC")
        return cursor.fetchall()
    finally:
        conn.close()



def actualizar_cliente_por_id(cliente_id, ruc_cedula, nombre, telefono, direccion):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET ruc_cedula = ?, nombre_razon_social = ?, telefono = ?, direccion = ?
            WHERE id = ?
        """, (ruc_cedula if ruc_cedula else "S/D", nombre.upper(), telefono, direccion, cliente_id))
        filas_afectadas = cursor.rowcount
        conn.commit()
        if filas_afectadas > 0:
            return True, "Cliente actualizado correctamente."
        return False, "No se encontró el cliente a actualizar."
    except Exception as e:
        return False, f"Error al actualizar cliente: {str(e)}"
    finally:
        conn.close()

def eliminar_cliente_por_id(cliente_id):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        filas_afectadas = cursor.rowcount
        conn.commit()
        if filas_afectadas > 0:
            return True, "Cliente eliminado correctamente."
        return False, "No se encontró el cliente en la base de datos."
    except Exception as e:
        return False, f"Error al eliminar cliente: {str(e)}"
    finally:
        conn.close()

# --- MÓDULO: PEDIDOS ---
def inicializar_tabla_pedidos():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            ruc_cedula TEXT,
            trabajo TEXT NOT NULL,
            cantidad INTEGER DEFAULT 1,
            plazo_dias INTEGER DEFAULT 15,
            estado TEXT NOT NULL DEFAULT 'PENDIENTE'
        )
        """)
        cursor.execute("PRAGMA table_info(pedidos)")
        columnas = [col[1] for col in cursor.fetchall()]
        if "ruc_cedula" not in columnas:
            cursor.execute("ALTER TABLE pedidos ADD COLUMN ruc_cedula TEXT")
        if "cantidad" not in columnas:
            cursor.execute("ALTER TABLE pedidos ADD COLUMN cantidad INTEGER DEFAULT 1")
        conn.commit()
    finally:
        conn.close()

def registrar_pedido(cliente_nombre, ruc_cedula, trabajo, cantidad, plazo_dias):
    inicializar_tabla_pedidos()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cli_mayus = cliente_nombre.upper()
        trab_mayus = trabajo.upper()
        
        # Verificar estrictamente que el cliente exista antes de registrar el pedido
        cursor.execute("SELECT id FROM clientes WHERE ruc_cedula = ? OR UPPER(nombre_razon_social) = ?", (ruc_cedula, cli_mayus))
        if not cursor.fetchone():
            return False, f"El cliente '{cli_mayus}' no está registrado en el sistema. Debe registrarlo primero en 'Gestión de Clientes'."

        cursor.execute("""
        INSERT INTO pedidos (cliente, ruc_cedula, trabajo, cantidad, plazo_dias, estado)
        VALUES (?, ?, ?, ?, ?, 'PENDIENTE')
        """, (cli_mayus, ruc_cedula, trab_mayus, cantidad, plazo_dias))
        conn.commit()
        return True, f"Pedido registrado con éxito para '{cli_mayus}'."
    except Exception as e:
        return False, f"Error al registrar el pedido: {str(e)}"
    finally:
        conn.close()

def obtener_todos_los_pedidos():
    inicializar_tabla_pedidos()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, UPPER(cliente), ruc_cedula, UPPER(trabajo), cantidad, plazo_dias, UPPER(estado) FROM pedidos ORDER BY id DESC")
        return cursor.fetchall()
    finally:
        conn.close()

# --- MÓDULO: CLIENTES (Búsqueda Exacta) ---
def buscar_clientes(termino):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        termino_upper = termino.strip().upper()
        cursor.execute("""
            SELECT id, UPPER(nombre_razon_social), ruc_cedula, telefono, direccion 
            FROM clientes 
            WHERE UPPER(nombre_razon_social) = ? OR ruc_cedula = ?
            ORDER BY id ASC
        """, (termino_upper, termino_upper))
        return cursor.fetchall()
    finally:
        conn.close()

# --- MÓDULO: PEDIDOS (Búsqueda Exacta) ---
def buscar_pedidos(termino):
    inicializar_tabla_pedidos()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        termino_upper = termino.strip().upper()
        cursor.execute("""
            SELECT id, UPPER(cliente), ruc_cedula, UPPER(trabajo), cantidad, plazo_dias, UPPER(estado) 
            FROM pedidos 
            WHERE UPPER(cliente) = ? OR ruc_cedula = ? OR UPPER(trabajo) = ?
            ORDER BY id DESC
        """, (termino_upper, termino_upper, termino_upper))
        return cursor.fetchall()
    finally:
        conn.close()


def actualizar_pedido(pedido_id, trabajo, cantidad, plazo_dias, estado):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE pedidos 
        SET trabajo = ?, cantidad = ?, plazo_dias = ?, estado = ?
        WHERE id = ?
        """, (trabajo.upper(), cantidad, plazo_dias, estado.upper(), pedido_id))
        conn.commit()
        return True, "Pedido actualizado con éxito."
    except Exception as e:
        return False, f"Error al actualizar el pedido: {str(e)}"
    finally:
        conn.close()

def eliminar_pedido(pedido_id):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
        conn.commit()
        return True, "Pedido eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar el pedido: {str(e)}"
    finally:
        conn.close()

# --- CATÁLOGOS DE MUEBLES ---
def inicializar_tabla_muebles():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_muebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """)
        muebles_base = [
            ("ROPERO DE 4 CUERPOS",),
            ("ROPERO DE 3 CUERPOS",),
            ("ROPERO DE 2 CUERPOS",),
            ("ROPERO DE 1 CUERPO",),
            ("JUEGO DE COMEDOR",),
            ("PUERTA PLACA DE CEDRO",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO tipos_muebles (nombre) VALUES (?)", muebles_base)
        conn.commit()
    finally:
        conn.close()

def obtener_tipos_muebles():
    inicializar_tabla_muebles()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT UPPER(nombre) FROM tipos_muebles ORDER BY nombre ASC")
        return [r[0] for r in cursor.fetchall()]
    finally:
        conn.close()

def registrar_nuevo_mueble(nombre):
    if not nombre or not nombre.strip():
        return
    try:
        inicializar_tabla_muebles()
        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO tipos_muebles (nombre) VALUES (?)", (nombre.strip().upper(),))
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass

def eliminar_tipo_mueble(nombre):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipos_muebles WHERE UPPER(nombre) = ?", (nombre.upper(),))
        filas = cursor.rowcount
        conn.commit()
        if filas > 0:
            return True, "Trabajo eliminado del catálogo correctamente."
        return False, "No se encontró el trabajo en el catálogo."
    except Exception as e:
        return False, f"Error al eliminar del catálogo: {str(e)}"
    finally:
        conn.close()

registrar_pedido_cedro = registrar_pedido
obtener_todos_los_pedidos_cedro = obtener_todos_los_pedidos
actualizar_pedido_cedro = actualizar_pedido
eliminar_pedido_cedro = eliminar_pedido