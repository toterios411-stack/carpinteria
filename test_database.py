import unittest
import database

class TestDatabaseCompleto(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez al inicio para asegurar que las tablas estén inicializadas."""
        database.inicializar_bd()
        database.inicializar_tabla_pedidos()
        database.inicializar_tabla_muebles()

    def test_01_encriptar_password(self):
        """Prueba la función: encriptar_password"""
        hash1 = database.encriptar_password("1234")
        hash2 = database.encriptar_password("1234")
        self.assertEqual(hash1, hash2, "El hash de la misma contraseña debe ser idéntico.")
        self.assertNotEqual(hash1, database.encriptar_password("otra_clave"))

    def test_02_modulo_usuarios(self):
        """Prueba las funciones de usuarios: registrar_usuario, validar_login_con_rol, obtener_todos_los_usuarios y eliminar_usuario"""
        user_test = "operario_prueba"
        clave_test = "12345"
        rol_test = "CARPINTERO (OPERARIO)"
        
        # Limpieza previa por si existía
        database.eliminar_usuario(user_test)
        
        # 1. Probar registrar_usuario
        exito, msg = database.registrar_usuario(user_test, clave_test, rol_test)
        self.assertTrue(exito, f"Error al registrar usuario: {msg}")
        
        # 2. Probar validar_login_con_rol
        valido, rol_obtenido = database.validar_login_con_rol(user_test, clave_test)
        self.assertTrue(valido, "El login con credenciales correctas debe ser exitoso.")
        self.assertIn("CARPINTERO", rol_obtenido)
        
        # 3. Probar obtener_todos_los_usuarios
        usuarios = database.obtener_todos_los_usuarios()
        self.assertTrue(any(u[0] == user_test for u in usuarios), "El usuario creado debe estar en la lista.")
        
        # 4. Probar eliminar_usuario
        exito_del, _ = database.eliminar_usuario(user_test)
        self.assertTrue(exito_del, "El usuario debe eliminarse correctamente.")

    def test_03_modulo_clientes(self):
        """Prueba las funciones de clientes: registrar_cliente, obtener_todos_los_clientes, buscar_clientes, actualizar_cliente_por_id y eliminar_cliente_por_id"""
        ruc_test = "555555-5"
        nombre_test = "MUEBLES DEL NORTE"
        
        # Limpieza previa
        clientes = database.obtener_todos_los_clientes()
        for c in clientes:
            if c[2] == ruc_test:
                database.eliminar_cliente_por_id(c[0])

        # 1. Probar registrar_cliente
        exito, msg = database.registrar_cliente(ruc_test, nombre_test, "0981999999", "AVENIDA SUR", "contacto@norte.com")
        self.assertTrue(exito, f"Error al registrar cliente: {msg}")
        
        # 2. Probar obtener_todos_los_clientes
        clientes_todos = database.obtener_todos_los_clientes()
        cliente_creado = next((c for c in clientes_todos if c[2] == ruc_test), None)
        self.assertIsNotNone(cliente_creado)
        cliente_id = cliente_creado[0]
        
        # 3. Probar buscar_clientes (Búsqueda exacta)
        res_busqueda = database.buscar_clientes(ruc_test)
        self.assertTrue(len(res_busqueda) > 0, "La búsqueda exacta por RUC debe retornar resultados.")
        
        # 4. Probar actualizar_cliente_por_id
        exito_act, _ = database.actualizar_cliente_por_id(cliente_id, ruc_test, "MUEBLES DEL SUR S.A.", "0982888888", "RUTA 2")
        self.assertTrue(exito_act, "La actualización del cliente debe ser exitosa.")
        
        # 5. Probar eliminar_cliente_por_id
        exito_del, _ = database.eliminar_cliente_por_id(cliente_id)
        self.assertTrue(exito_del, "El cliente debe eliminarse correctamente.")

    def test_04_modulo_catalogo_muebles(self):
        """Prueba las funciones del catálogo: registrar_nuevo_mueble, obtener_tipos_muebles y eliminar_tipo_mueble"""
        mueble_test = "MESADA DE GRANITO"
        
        # Limpieza previa
        database.eliminar_tipo_mueble(mueble_test)
        
        # 1. Probar registrar_nuevo_mueble
        database.registrar_nuevo_mueble(mueble_test)
        
        # 2. Probar obtener_tipos_muebles
        muebles = database.obtener_tipos_muebles()
        self.assertIn(mueble_test, muebles, "El mueble nuevo debe aparecer en el catálogo.")
        
        # 3. Probar eliminar_tipo_mueble
        exito_del, _ = database.eliminar_tipo_mueble(mueble_test)
        self.assertTrue(exito_del, "El mueble debe eliminarse del catálogo correctamente.")

    def test_05_modulo_pedidos(self):
        """Prueba las funciones de pedidos: registrar_pedido, obtener_todos_los_pedidos, buscar_pedidos, actualizar_pedido y eliminar_pedido"""
        ruc_cli = "444444-4"
        nombre_cli = "CLIENTE PEDIDO TEST"
        
        # Aseguramos que el cliente exista previamente (requisito de validación estricta)
        database.registrar_cliente(ruc_cli, nombre_cli, "0971234567", "CENTRO")
        
        # 1. Probar registrar_pedido
        exito, msg = database.registrar_pedido(nombre_cli, ruc_cli, "ROPERO DE 4 CUERPOS", 2, 15)
        self.assertTrue(exito, f"Error al registrar pedido: {msg}")
        
        # 2. Probar obtener_todos_los_pedidos
        pedidos = database.obtener_todos_los_pedidos()
        pedido_creado = next((p for p in pedidos if p[2] == ruc_cli), None)
        self.assertIsNotNone(pedido_creado)
        pedido_id = pedido_creado[0]
        
        # 3. Probar buscar_pedidos (Búsqueda exacta)
        res_pedidos = database.buscar_pedidos(ruc_cli)
        self.assertTrue(len(res_pedidos) > 0, "La búsqueda exacta de pedidos debe arrojar resultados.")
        
        # 4. Probar actualizar_pedido
        exito_upd, _ = database.actualizar_pedido(pedido_id, "ROPERO MODIFICADO", 1, 10, "TERMINADO")
        self.assertTrue(exito_upd, "La actualización del pedido debe ser exitosa.")
        
        # 5. Probar eliminar_pedido
        exito_del, _ = database.eliminar_pedido(pedido_id)
        self.assertTrue(exito_del, "El pedido debe eliminarse correctamente.")

if __name__ == "__main__":
    unittest.main()