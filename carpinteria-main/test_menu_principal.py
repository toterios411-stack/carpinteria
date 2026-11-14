import unittest
import database

class TestMenuPrincipalLogica(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.inicializar_bd()

    def test_calculo_precio_mueble(self):
        """Verifica que el sistema obtenga precios correctos para cotizaciones."""
        precio = database.obtener_precio_mueble("ROPERO DE 4 CUERPOS")
        self.assertIsInstance(precio, (int, float))
        self.assertGreaterEqual(precio, 0)

    def test_estructura_estadisticas_reporte(self):
        """Verifica que los datos para los reportes generales estén disponibles."""
        stats = database.obtener_estadisticas_generales()
        self.assertIn("terminados", stats)
        self.assertIn("pendientes", stats)

if __name__ == "__main__":
    unittest.main()