import unittest
import database

class TestLoginModulo(unittest.TestCase):

    def test_login_credenciales_correctas(self):
        """Verifica que las credenciales válidas den acceso de administrador."""
        valido, rol = database.validar_login_con_rol("admin", "1234")
        self.assertTrue(valido)
        self.assertIn("ADMINISTRADOR", rol)

    def test_login_credenciales_incorrectas(self):
        """Verifica que una contraseña errónea rechace el acceso."""
        valido, rol = database.validar_login_con_rol("admin", "clave_falsa")
        self.assertFalse(valido)

    def test_login_usuario_inexistente(self):
        """Verifica que un usuario que no existe en la BD falle en el login."""
        valido, rol = database.validar_login_con_rol("usuario_fantasma", "1234")
        self.assertFalse(valido)

if __name__ == "__main__":
    unittest.main()