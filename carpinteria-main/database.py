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

        pwd_admin = encriptar_password("1234")
        cursor.execute("""
        INSERT OR IGNORE INTO usuarios (usuario, clave, rol) 
        VALUES ('admin', ?, 'ADMINISTRADOR (Administrador)')
        """, (pwd_admin,))

        conn.commit()
    finally:
        conn.close()
    
    inicializar_tabla_muebles()
    inicializar_tabla_pedidos()

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

def buscar_clientes(termino):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        termino_upper = termino.strip().upper()
        cursor.execute("""
            SELECT id, UPPER(nombre_razon_social), ruc_cedula, telefono, direccion 
            FROM clientes 
            WHERE UPPER(nombre_razon_social) LIKE ? OR ruc_cedula LIKE ?
            ORDER BY id ASC
        """, (f"%{termino_upper}%", f"%{termino_upper}%"))
        return cursor.fetchall()
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
        
        cursor.execute("SELECT id FROM clientes WHERE ruc_cedula = ? OR UPPER(nombre_razon_social) = ?", (ruc_cedula, cli_mayus))
        if not cursor.fetchone():
            return False, f"El cliente '{cli_mayus}' no está registrado en el sistema."

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

def buscar_pedidos(termino):
    inicializar_tabla_pedidos()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        t = f"%{termino.strip().upper()}%"
        cursor.execute("""
            SELECT id, UPPER(cliente), ruc_cedula, UPPER(trabajo), cantidad, plazo_dias, UPPER(estado) 
            FROM pedidos 
            WHERE UPPER(cliente) LIKE ? OR ruc_cedula LIKE ? OR UPPER(trabajo) LIKE ?
            ORDER BY id DESC
        """, (t, t, t))
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

# --- CATÁLOGOS DE MUEBLES CON PRECIOS ---
def inicializar_tabla_muebles():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_muebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            precio REAL DEFAULT 0
        )
        """)
        cursor.execute("PRAGMA table_info(tipos_muebles)")
        columnas = [col[1] for col in cursor.fetchall()]
        if "precio" not in columnas:
            cursor.execute("ALTER TABLE tipos_muebles ADD COLUMN precio REAL DEFAULT 0")

        muebles_base = [
            ("ROPERO DE 4 CUERPOS", 2200000),
            ("ROPERO DE 3 CUERPOS", 1500000),
            ("ROPERO DE 2 CUERPOS", 1100000),
            ("ROPERO DE 1 CUERPO", 750000),
            ("JUEGO DE COMEDOR", 2500000),
            ("PUERTA PLACA DE CEDRO", 850000)
        ]
        cursor.executemany("INSERT OR IGNORE INTO tipos_muebles (nombre, precio) VALUES (?, ?)", muebles_base)
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

def obtener_todos_los_muebles_con_precio():
    inicializar_tabla_muebles()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, UPPER(nombre), precio FROM tipos_muebles ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        conn.close()

def obtener_precio_mueble(nombre):
    inicializar_tabla_muebles()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT precio FROM tipos_muebles WHERE UPPER(nombre) = ?", (nombre.strip().upper(),))
        res = cursor.fetchone()
        return res[0] if res and res[0] is not None else 0.0
    finally:
        conn.close()

def registrar_mueble_con_precio(nombre, precio):
    if not nombre or not nombre.strip():
        return False, "El nombre del mueble es obligatorio."
    inicializar_tabla_muebles()
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tipos_muebles (nombre, precio) VALUES (?, ?)", (nombre.strip().upper(), float(precio)))
        conn.commit()
        return True, "Mueble y precio registrados con éxito."
    except sqlite3.IntegrityError:
        return False, "Ese mueble ya existe en el catálogo."
    except Exception as e:
        return False, f"Error al registrar mueble: {str(e)}"
    finally:
        conn.close()

def actualizar_mueble_con_precio(mueble_id, nombre, precio):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tipos_muebles 
            SET nombre = ?, precio = ?
            WHERE id = ?
        """, (nombre.strip().upper(), float(precio), mueble_id))
        conn.commit()
        return True, "Mueble y precio actualizados correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe otro mueble con ese mismo nombre."
    except Exception as e:
        return False, f"Error al actualizar mueble: {str(e)}"
    finally:
        conn.close()

def eliminar_mueble_por_id(mueble_id):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipos_muebles WHERE id = ?", (mueble_id,))
        conn.commit()
        return True, "Mueble eliminado del catálogo."
    except Exception as e:
        return False, f"Error al eliminar mueble: {str(e)}"
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
            cursor.execute("INSERT OR IGNORE INTO tipos_muebles (nombre, precio) VALUES (?, 0)", (nombre.strip().upper(),))
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass

# --- REPORTES Y ESTADÍSTICAS ---
def obtener_estadisticas_generales():
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE UPPER(estado) = 'TERMINADO'")
        pedidos_terminados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE UPPER(estado) = 'PENDIENTE'")
        pedidos_pendientes = cursor.fetchone()[0]

        cursor.execute("SELECT trabajo, cantidad FROM pedidos")
        pedidos_lista = cursor.fetchall()
        
        ingreso_total = 0.0
        for trabajo, cantidad in pedidos_lista:
            precio = obtener_precio_mueble(trabajo)
            ingreso_total += precio * cantidad

        return {
            "clientes": total_clientes,
            "pedidos": total_pedidos,
            "terminados": pedidos_terminados,
            "pendientes": pedidos_pendientes,
            "ingresos": ingreso_total
        }
    finally:
        conn.close()