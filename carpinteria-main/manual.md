# Manual de Usuario - Sistema de Gestión para Taller de Carpintería (SGC)

## 1. Introducción
El **Sistema de Gestión de Carpintería (SGC)** es una aplicación de escritorio desarrollada en Python y SQLite diseñada para administrar de forma integral las operaciones de un taller, abarcando el control de acceso por roles, clientes, pedidos de taller, proveedores, compras de insumos y reportes gerenciales.

---

## 2. Requisitos del Sistema
* **Lenguaje:** Python 3.12 o superior.
* **Base de Datos:** SQLite3 (archivo local `carpinteria.db`).
* **Interfaz Gráfica:** Tkinter.

---

## 3. Inicio de Sesión y Control de Accesos (Login)
Al ejecutar la aplicación (`python main.py`), se presentará la ventana de autenticación.
* **Credenciales por defecto de Administrador:**
  * **Usuario:** `admin`
  * **Contraseña:** `1234`
* **Roles del Sistema:**
  * **Administrador:** Tiene acceso total al sistema, incluyendo la administración de cuentas de usuario, control de roles, clientes, pedidos, proveedores y reportes.
  * **Operario / Carpintero:** Limitado exclusivamente a la toma y consulta de pedidos y clientes, cumpliendo con los protocolos de seguridad de roles.

---

## 4. Módulos del Sistema

### 4.1. Módulo de Clientes
* Permite registrar nuevos clientes indicando Razón Social, Ruc/Cédula, Teléfono y Dirección.
* Incluye validación estricta de campos obligatorios y un buscador en tiempo real por nombre o RUC.
* Permite actualizar datos y eliminar registros seleccionados de la tabla.

### 4.2. Módulo de Pedidos y Taller
* Permite registrar trabajos asignados a clientes previamente cargados mediante la validación de su RUC.
* Gestiona catálogos de muebles (roperos, comedores, puertas, etc.) con opción de autocompletado y eliminación de ítems del catálogo.
* Controla el estado del pedido: `PENDIENTE`, `EN PROCESO`, `TERMINADO` o `CANCELADO`, junto con el plazo de entrega en días y la cantidad.

### 4.3. Módulo 4: Proveedores y Compras de Insumos
* Administra la base de datos de proveedores de maderas, herrajes e insumos (RUC, Razón Social, Teléfono, Dirección e Insumo Principal).
* Permite registrar las compras u órdenes de adquisición a dichos proveedores especificando descripción, costo en Guaraníes (₲) y fecha.

### 4.4. Módulo 5: Reportes y Estadísticas del Taller
* Panel gerencial que calcula y muestra en tiempo real métricas clave del negocio:
  * Total de clientes registrados.
  * Total de pedidos ingresados y su desglose (terminados vs. pendientes).
  * Proveedores activos.
  * Inversión y gastos totales en compras de insumos.

---

## 5. Mantenimiento y Comandos de Soporte
* **Ejecutar Pruebas Unitarias (PUN):**
  ```bash
  python -m unittest test_database.py