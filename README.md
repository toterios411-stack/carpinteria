# Sistema de Gestión de Carpintería (SGC)

Sistema de gestión desarrollado en Python (Tkinter) y SQLite para el control operativo, clientes, inventario y usuarios en taller de carpintería.

---

## 📌 Entrega: Sprint 1
- **Estructura Base del Proyecto:** Configuración de la base de datos relacional SQLite (`database.py`) e interfaz gráfica principal.
- **Inicio de Sesión Basico:** Pantalla de autenticación y estructura de tablas iniciales.

---

## 📌 Entrega: Sprint 2

### 📋 Criterios de Evaluación
- **SCC (Sistema de Control de Cambios - 3p):** Repositorio Git en funcionamiento con etiquetado formal mediante TAGs (`v2.0`).
- **PUN (Pruebas Unitarias - 5p):** Cobertura de pruebas unitarias configuradas en `test_database.py` verificando cifrado SHA-256, login y funciones de base de datos.
- **PDO (Documentación Automática - 5p):** Documentación técnica del código fuente generada automáticamente mediante `pdoc` en el directorio `./documentacion`.
- **ALC (Alcance del Proyecto - 16p):**
  - **Módulo 2 (Usuarios / Roles - 8p):** Control de acceso seguro (cifrado SHA-256), atajo rápido con tecla **Enter**, asignación de roles (Administrador / Operario) y gestión/registro de cuentas trasladado exclusivamente al Menú Principal.
  - **Módulo 3 (Pedidos y Stock de Cedro / Clientes - 8p):** Registro de pedidos de muebles con estimación automática de madera de cedro, plazos de entrega en días y alta integrada de clientes nuevos.
- **QA (Calidad de Software - 6p):** Manejo estricto de excepciones (`try-except`), validación visual de entradas vacías/errores (`messagebox`) e interfaz fluida con controles deshabilitados según permisos.

---

## 🚀 Instrucciones de Ejecución

1. **Iniciar la Aplicación:**
   ```bash
   python main.py