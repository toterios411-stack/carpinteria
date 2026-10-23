# 🪵 Sistema de Gestión para Taller de Carpintería (Sprint 2)

Proyecto académico desarrollado para el control integral de operaciones en un taller de carpintería, abarcando gestión de usuarios con control de acceso por roles (RBAC), control de clientes, catálogo de muebles y sistema de pedidos con validaciones estrictas de calidad (QA).

---

## 🚀 Requisitos del Sistema y Tecnologías
* **Lenguaje:** Python 3.12+
* **Base de Datos:** SQLite3 (`carpinteria.db`)
* **Interfaz Gráfica:** Tkinter
* **Control de Versiones:** Git & GitHub (con soporte para TAGs)
* **Pruebas Unitarias:** Framework nativo `unittest`
* **Documentación Automática:** Generada mediante `pdoc`

---

## 📂 Estructura del Proyecto

```text
carpinteria/
│
├── database.py             # Capa de datos y lógica de negocio (CRUD y SQLite)
├── menu_principal.py       # Interfaz gráfica principal (Tkinter) y navegación por roles
├── login.py                # Módulo de autenticación y control de accesos
├── main.py                 # Punto de entrada de la aplicación
├── test_database.py        # Pruebas unitarias automatizadas para cada función (def)
├── Doxyfile                # Configuración de documentación
├── documentacion/          # Carpeta con la documentación automática en HTML
├── carpinteria.db          # Base de datos principal del sistema
└── README.md               # Documentación y guía del repositorio
```

---

## 🛠️ Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd carpinteria
   ```

2. **Ejecutar la aplicación principal:**
   ```bash
   python main.py
   ```

---

## 🧪 Ejecución de Pruebas Unitarias (PUN)
Para verificar el correcto funcionamiento de cada función (`def`) de la base de datos de manera automatizada, ejecute el siguiente comando en la terminal:
```bash
python -m unittest test_database.py
```

---

## 📚 Documentación Automática (PDO)
La documentación técnica del código fuente se genera automáticamente utilizando herramientas de análisis estático. Para actualizarla o regenerarla, ejecute:
```bash
pdoc database.py menu_principal.py test_database.py -o documentacion
```

---

## 📋 Resumen de Cumplimiento (Sprint 2)
* **SCC:** Sistema de control de cambios montado en Git con commits descriptivos y **TAGs** de entrega oficial (`sprint2`).
* **PUN:** Cobertura total de pruebas unitarias sobre los módulos de base de datos.
* **PDO:** Documentación HTML autogenerada y estructurada en la carpeta `documentacion/`.
* **ALC:** Módulos funcionales de Usuarios/Roles, Clientes, Catálogo de Muebles y Pedidos con validaciones estrictas.
* **QA:** Código limpio, estructurado por capas y validado mediante pruebas automatizadas.