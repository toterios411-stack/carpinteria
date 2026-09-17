import unittest
import os
import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Inicializa la base de datos antes de cada prueba."""
        database.inicializar_bd()

    def test_validar_login_correcto(self):
        """Prueba la validación con credenciales correctas."""
        self.assertTrue(database.validar_login("admin", "1234"))

    def test_validar_login_incorrecto(self):
        """Prueba el rechazo de credenciales inválidas."""
        self.assertFalse(database.validar_login("admin", "clave_erronea"))

    def test_registrar_usuario_nuevo(self):
        """Prueba el registro de un nuevo usuario en la BD."""
        exito, msg = database.registrar_usuario("usuario_prueba", "pass123")
        self.assertTrue(exito)

    def test_obtener_usuarios(self):
        """Prueba la consulta de lista de usuarios."""
        usuarios = database.obtener_todos_los_usuarios()
        self.assertGreater(len(usuarios), 0)

if __name__ == '__main__':
    unittest.main()