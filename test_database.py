import unittest
import os
import database

class TestDatabaseCarpinteria(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba para asegurar el entorno base."""
        database.inicializar_bd()

    def test_01_registro_usuario_exitoso(self):
        """Prueba la inserción de un usuario nuevo."""
        usuario_test = "carpintero_test"
        clave_test = "password123"
        exito, msg = database.registrar_usuario(usuario_test, clave_test)
        self.assertTrue(exito)
        self.assertIn("registrado exitosamente", msg)

    def test_02_usuario_duplicado(self):
        """Verifica que el sistema rechace usuarios duplicados."""
        usuario_test = "admin" # Usuario creado en la inicialización
        exito, msg = database.registrar_usuario(usuario_test, "1234")
        self.assertFalse(exito)
        self.assertIn("ya existe", msg)

    def test_03_login_correcto(self):
        """Valida que las credenciales correctas permitan el acceso."""
        self.assertTrue(database.validar_login("admin", "1234"))

    def test_04_login_incorrecto(self):
        """Valida que credenciales erróneas sean rechazadas."""
        self.assertFalse(database.validar_login("admin", "clave_erronea"))

if __name__ == "__main__":
    unittest.main()