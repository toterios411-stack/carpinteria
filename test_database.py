import unittest
import os
import database

class TestSprint2Carpinteria(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        database.DB_NAME = "carpinteria_test.db"
        # Si la base de datos de prueba anterior existe, la borramos para empezar totalmente limpios
        if os.path.exists("carpinteria_test.db"):
            try:
                os.remove("carpinteria_test.db")
            except PermissionError:
                pass  # Si está ocupada, continuamos
        database.inicializar_bd()

    def test_01_registro_usuario_con_rol(self):
        """Prueba la inserción de usuario asignando un rol específico."""
        database.eliminar_usuario("operario_juan")
        exito, msg = database.registrar_usuario("operario_juan", "clave123", "Operario")
        self.assertTrue(exito)
        self.assertIn("registrado con éxito", msg)

    def test_02_login_administrador(self):
        """Prueba el inicio de sesión correcto del admin con SHA-256."""
        exito, rol = database.validar_login_con_rol("admin", "1234")
        self.assertTrue(exito)
        self.assertEqual(rol, "Administrador")

    def test_03_login_fallido(self):
        """Prueba que un login con contraseña errónea falle."""
        exito, rol = database.validar_login_con_rol("admin", "clave_falsa")
        self.assertFalse(exito)
        self.assertIsNone(rol)

    def test_04_registrar_material_inventario(self):
        """Prueba el alta de una madera en el inventario."""
        exito, msg = database.registrar_material("CED-TEST-1", "Tablón Test", "Madera", "Metros", 50, 10, 150000)
        self.assertTrue(exito)

if __name__ == '__main__':
    unittest.main()