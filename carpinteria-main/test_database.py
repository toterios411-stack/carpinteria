import unittest
import database

class TestCarpinteriaDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial antes de ejecutar las pruebas."""
        database.inicializar_bd()

    def test_01_cifrado_password(self):
        """Prueba que el cifrado SHA-256 funcione correctamente."""
        pass_plana = "1234"
        pass_cifrada = database.encriptar_password(pass_plana)
        # El hash SHA-256 de '1234' tiene una longitud específica y no es igual al texto plano
        self.assertNotEqual(pass_plana, pass_cifrada)
        self.assertEqual(len(pass_cifrada), 64)

    def test_02_login_usuario(self):
        """Prueba el inicio de sesión del usuario administrador por defecto."""
        exito, rol = database.validar_login_con_rol("admin", "1234")
        self.assertTrue(exito)
        self.assertIn("ADMINISTRADOR", rol)

    def test_03_gestion_clientes(self):
        """Prueba el registro y búsqueda de un cliente de prueba."""
        ruc_prueba = "999888777-1"
        # Intentamos registrar (si ya existe por pruebas anteriores, no hay problema)
        database.registrar_cliente(ruc_prueba, "CLIENTE PRUEBA S.A.", "0981123456", "Asuncion")
        
        # Verificamos que se pueda buscar
        resultados = database.buscar_clientes("CLIENTE PRUEBA")
        self.assertGreater(len(resultados), 0)

    def test_04_catalogo_muebles(self):
        """Prueba que el catálogo devuelva precios válidos."""
        precio = database.obtener_precio_mueble("ROPERO DE 4 CUERPOS")
        self.assertIsInstance(precio, float)
        self.assertGreater(precio, 0)

    def test_05_estadisticas_generales(self):
        """Prueba que el módulo de reportes y estadísticas devuelva un diccionario válido con ingresos."""
        stats = database.obtener_estadisticas_generales()
        self.assertIsInstance(stats, dict)
        self.assertIn("clientes", stats)
        self.assertIn("pedidos", stats)
        self.assertIn("terminados", stats)
        self.assertIn("pendientes", stats)
        self.assertIn("ingresos", stats)

if __name__ == "__main__":
    unittest.main()