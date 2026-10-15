import unittest
import database

class TestSprint2Carpinteria(unittest.TestCase):

    def setUp(self):
        """Inicializa la estructura de la base de datos antes de cada test."""
        database.inicializar_bd()

    # --- PRUEBAS MÓDULO USUARIOS / ROLES ---
    def test_01_registro_usuario_con_rol(self):
        """Prueba la inserción de usuario asignando un rol específico."""
        exito, msg = database.registrar_usuario("operario_juan", "pass123", "Operario")
        self.assertTrue(exito)
        self.assertIn("registrado exitosamente", msg)

    def test_02_modificar_rol_usuario(self):
        """Prueba la actualización de rol a un usuario registrado."""
        database.registrar_usuario("pedro_carpintero", "1234", "Operario")
        exito, msg = database.actualizar_rol_usuario("pedro_carpintero", "Administrador")
        self.assertTrue(exito)

    def test_03_login_rol_valido(self):
        """Valida que la autenticación devuelva el rol correcto."""
        database.registrar_usuario("maria_admin", "admin123", "Administrador")
        usuario_valido, rol = database.validar_login_con_rol("maria_admin", "admin123")
        self.assertTrue(usuario_valido)
        self.assertEqual(rol, "Administrador")

    # --- PRUEBAS MÓDULO INVENTARIO Y MADERAS ---
    def test_04_registrar_material_inventario(self):
        """Prueba el alta de una madera en el inventario."""
        exito, msg = database.registrar_material("MAD-LAP-01", "Lapacho Macizo 2x4", "Madera", "Pie Tablar", 150.0, 20.0, 35000.0)
        self.assertTrue(exito)

    def test_05_material_codigo_duplicado(self):
        """Verifica que no se permitan códigos de inventario duplicados."""
        database.registrar_material("MAD-CED-01", "Cedro 1x6", "Madera", "Pie Tablar", 50.0, 10.0, 28000.0)
        exito, msg = database.registrar_material("MAD-CED-01", "Cedro Repetido", "Madera", "Pie Tablar", 10.0, 5.0, 28000.0)
        self.assertFalse(exito)

    def test_06_alerta_stock_critico(self):
        """Verifica que el sistema identifique materiales bajo el stock mínimo."""
        database.registrar_material("HER-TORN-01", "Tornillos 2 pulgadas", "Herraje", "Unidad", 5.0, 50.0, 150.0)
        materiales_criticos = database.obtener_materiales_stock_bajo()
        self.assertGreaterEqual(len(materiales_criticos), 1)

if __name__ == "__main__":
    unittest.main()