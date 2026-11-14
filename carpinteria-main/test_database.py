import unittest
import database

class TestSistemaCarpinteriaCompleto(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta al inicio para inicializar la base de datos y sus tablas principales."""
        database.inicializar_bd()

    def test_01_modulo_usuarios(self):
        """MÓDULO 1: Prueba la encriptación, registro, login con rol y eliminación de usuarios."""
        user_test = "operario_test"
        clave_test = "secreto123"
        rol_test = "CARPINTERO (OPERARIO)"
        
        # Limpieza previa
        database.eliminar_usuario(user_test)
        
        # Probar registro y encriptación
        exito, msg = database.registrar_usuario(user_test, clave_test, rol_test)
        self.assertTrue(exito, f"Error al registrar usuario: {msg}")
        
        # Probar login con rol
        valido, rol_obtenido = database.validar_login_con_rol(user_test, clave_test)
        self.assertTrue(valido, "El login con credenciales correctas debe ser exitoso.")
        self.assertIn("CARPINTERO", rol_obtenido)
        
        # Probar eliminación
        exito_del, _ = database.eliminar_usuario(user_test)
        self.assertTrue(exito_del, "El usuario debe eliminarse correctamente.")

    def test_02_modulo_clientes(self):
        """MÓDULO 2: Prueba el registro, búsqueda exacta y gestión de clientes."""
        ruc_test = "999999-9"
        nombre_test = "CLIENTES DEL ESTE S.A."
        
        # Limpieza previa
        for c in database.obtener_todos_los_clientes():
            if c[2] == ruc_test:
                database.eliminar_cliente_por_id(c[0])

        # Probar registro
        exito, msg = database.registrar_cliente(ruc_test, nombre_test, "0981112233", "RUTA 2 KM 20", "info@este.com")
        self.assertTrue(exito, f"Error al registrar cliente: {msg}")
        
        # Probar búsqueda exacta
        res = database.buscar_clientes(ruc_test)
        self.assertTrue(len(res) > 0, "La búsqueda por RUC debe arrojar resultados.")
        
        # Obtener ID para eliminar
        cliente_id = res[0][0]
        exito_del, _ = database.eliminar_cliente_por_id(cliente_id)
        self.assertTrue(exito_del, "El cliente debe eliminarse correctamente.")

    def test_03_modulo_catalogo_muebles(self):
        """MÓDULO 3: Prueba la consulta en el catálogo de muebles."""
        muebles = database.obtener_tipos_muebles()
        self.assertIsInstance(muebles, list, "El catálogo de muebles debe retornar una lista.")

    def test_04_modulo_pedidos(self):
        """MÓDULO 4: Prueba la validación y registro de pedidos en el sistema."""
        ruc_cli = "555444-3"
        nombre_cli = "JUAN PÉREZ PEDIDOS"
        
        database.registrar_cliente(ruc_cli, nombre_cli, "0971555444", "CENTRO")
        
        # Ajustado a los 5 parámetros que requiere tu función registrar_pedido
        exito, msg = database.registrar_pedido(nombre_cli, ruc_cli, "ROPERO DE 3 CUERPOS", 1, 1800000)
        self.assertTrue(exito, f"Error al registrar pedido: {msg}")

    def test_05_modulo_ordenes_trabajo(self):
        """MÓDULO 5: Prueba la obtención y gestión de órdenes de trabajo y pedidos."""
        pedidos = database.obtener_todos_los_pedidos()
        self.assertIsInstance(pedidos, list, "Debe retornar una lista de pedidos/órdenes.")

    def test_06_estadisticas_generales(self):
        """MÓDULO 6: Prueba que el módulo de reportes devuelva métricas válidas."""
        stats = database.obtener_estadisticas_generales()
        self.assertIsInstance(stats, dict)
        self.assertIn("clientes", stats)
        self.assertIn("pedidos", stats)
        self.assertIn("ingresos", stats)


if __name__ == "__main__":
    unittest.main()