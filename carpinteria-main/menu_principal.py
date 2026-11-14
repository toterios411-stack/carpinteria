import tkinter as tk
from tkinter import messagebox, ttk
import database

class MenuPrincipal(tk.Toplevel):
    def __init__(self, parent, rol_usuario="CARPINTERO (Operario)"):
        super().__init__(parent)
        self.parent = parent
        self.rol_usuario = rol_usuario.upper()
        self.title("Sistema de Gestión para Carpintería - Panel Principal")
        self.geometry("820x520")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#4A2E10", height=60)
        header.pack(fill=tk.X)
        
        lbl_titulo = tk.Label(
            header, 
            text=f"Panel Principal - Rol Activo: {self.rol_usuario}", 
            font=("Arial", 14, "bold"), 
            fg="white", 
            bg="#4A2E10"
        )
        lbl_titulo.pack(pady=15)

        btn_frame = tk.Frame(self)
        btn_frame.pack(expand=True)

        # Botones Principales Operativos
        tk.Button(
            btn_frame, 
            text="👥 Gestión de Clientes", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            command=self.abrir_clientes
        ).grid(row=0, column=0, padx=15, pady=12)

        tk.Button(
            btn_frame, 
            text="🪵 Registro y Pedidos de Taller", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            command=self.abrir_inventario
        ).grid(row=0, column=1, padx=15, pady=12)
        
        # Reportes y Estadísticas
        tk.Button(
            btn_frame, 
            text="📊 Reportes y Estadísticas", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            bg="#8E44AD", 
            fg="white",
            command=self.abrir_reportes
        ).grid(row=1, column=0, padx=15, pady=12)

        # Catálogo y Precios de Muebles
        tk.Button(
            btn_frame, 
            text="🪑 Catálogo y Precios de Muebles", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            bg="#D35400", 
            fg="white",
            command=self.abrir_catalogo_muebles
        ).grid(row=1, column=1, padx=15, pady=12)

        if "ADMINISTRADOR" in self.rol_usuario:
            tk.Button(
                btn_frame, 
                text="⚙️ Gestión de Usuarios y Roles", 
                font=("Arial", 11, "bold"), 
                width=32, 
                height=2, 
                bg="#2980B9", 
                fg="white", 
                command=self.abrir_usuarios
            ).grid(row=2, column=0, padx=15, pady=12)
        else:
            tk.Button(
                btn_frame, 
                text="⚙️ Gestión de Usuarios (Solo Admin)", 
                font=("Arial", 11), 
                width=32, 
                height=2, 
                state=tk.DISABLED
            ).grid(row=2, column=0, padx=15, pady=12)

        tk.Button(
            btn_frame, 
            text="🔒 Cerrar Sesión", 
            font=("Arial", 10, "bold"), 
            bg="#C0392B", 
            fg="white", 
            width=32,
            height=2,
            command=self.cerrar_sesion
        ).grid(row=2, column=1, padx=15, pady=12)

        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)

    def cerrar_sesion(self):
        self.destroy()
        if self.parent:
            self.parent.deiconify()

    def abrir_clientes(self):
        VentanaClientes(self)

    def abrir_inventario(self):
        VentanaInventario(self)

    def abrir_usuarios(self):
        VentanaGestionUsuarios(self)

    def abrir_reportes(self):
        VentanaReportes(self)

    def abrir_catalogo_muebles(self):
        VentanaCatalogoMuebles(self)


# --- VENTANA REPORTES Y ESTADÍSTICAS ---
class VentanaReportes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reportes y Estadísticas de Pedidos e Ingresos")
        self.geometry("560x420")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#8E44AD", height=50)
        header.pack(fill=tk.X)
        tk.Label(
            header, 
            text="📊 Resumen de Pedidos e Ingresos Estimados", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#8E44AD"
        ).pack(pady=12)

        stats = database.obtener_estadisticas_generales()

        frame_stats = tk.LabelFrame(self, text=" Métricas Generales del Taller ", font=("Arial", 10, "bold"), padx=15, pady=15)
        frame_stats.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        lbls = [
            f"👥 Total de Clientes Registrados: {stats['clientes']}",
            f"📋 Total de Pedidos Ingresados: {stats['pedidos']}",
            f"✅ Pedidos Terminados con Éxito: {stats['terminados']}",
            f"⏳ Pedidos en Proceso / Pendientes: {stats['pendientes']}",
            f"💰 Ingresos Totales Estimados (Pedidos): ₲ {stats['ingresos']:,.0f}"
        ]

        for texto in lbls:
            tk.Label(frame_stats, text=texto, font=("Arial", 11), anchor="w").pack(fill=tk.X, pady=8)

        tk.Button(
            self, 
            text="❌ Cerrar", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=20, 
            command=self.destroy
        ).pack(pady=10)


# --- VENTANA CATÁLOGO Y PRECIOS DE MUEBLES ---
class VentanaCatalogoMuebles(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("SGC - Catálogo y Precios de Muebles")
        self.geometry("680x540")
        self.resizable(False, False)

        self.mueble_seleccionado_id = None

        header = tk.Frame(self, bg="#D35400", height=50)
        header.pack(fill=tk.X)
        tk.Label(
            header, 
            text="🪑 Catálogo de Muebles y Lista de Precios (Roperos / Trabajos)", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#D35400"
        ).pack(pady=12)

        frame_form = tk.LabelFrame(self, text=" Datos del Mueble / Roperos ", font=("Arial", 9, "bold"), padx=12, pady=10)
        frame_form.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_form, text="Nombre del Mueble:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_nombre = tk.Entry(frame_form, width=30)
        self.txt_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.txt_nombre.focus()

        tk.Label(frame_form, text="Precio (₲):").grid(row=0, column=2, sticky="e", pady=5)
        self.txt_precio = tk.Entry(frame_form, width=18)
        self.txt_precio.grid(row=0, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(frame_form)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="➕ Agregar Mueble", bg="#27AE60", fg="white", font=("Arial", 9, "bold"), command=self.guardar_mueble).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Modificar Precio / Nombre", bg="#2980B9", fg="white", font=("Arial", 9, "bold"), command=self.actualizar_mueble).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), command=self.eliminar_mueble).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)

        frame_tabla = tk.LabelFrame(self, text=" Muebles y Precios Registrados (Haga clic para editar) ", font=("Arial", 9, "bold"), padx=10, pady=8)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Mueble", "Precio"), show="headings", height=9)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mueble", text="Trabajo / Mueble (Ej. Roperos)")
        self.tree.heading("Precio", text="Precio Unitario (₲)")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Mueble", width=360, anchor="w")
        self.tree.column("Precio", width=180, anchor="e")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_mueble)
        self.cargar_muebles()

        tk.Button(self, text="❌ Salir", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), width=15, command=self.destroy).pack(pady=10)

    def cargar_muebles(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in database.obtener_todos_los_muebles_con_precio():
            precio_val = m[2] if m[2] is not None else 0.0
            precio_formateado = f"₲ {precio_val:,.0f}"
            self.tree.insert("", tk.END, values=(m[0], m[1], precio_formateado))

    def seleccionar_mueble(self, event):
        selected = self.tree.selection()
        if selected:
            val = self.tree.item(selected[0])['values']
            self.mueble_seleccionado_id = val[0]
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, val[1])
            
            precio_limpio = str(val[2]).replace("₲", "").replace(",", "").strip()
            self.txt_precio.delete(0, tk.END)
            self.txt_precio.insert(0, precio_limpio)

    def guardar_mueble(self):
        nombre = self.txt_nombre.get().strip()
        precio_str = self.txt_precio.get().strip().replace(",", "")

        if not nombre or not precio_str:
            messagebox.showwarning("Atención", "Ingrese el nombre del mueble y su precio.")
            return
        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido para el precio.")
            return

        exito, msg = database.registrar_mueble_con_precio(nombre, precio)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_muebles()
        else:
            messagebox.showerror("Error", msg)

    def actualizar_mueble(self):
        if not self.mueble_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un mueble de la tabla para modificarlo.")
            return

        nombre = self.txt_nombre.get().strip()
        precio_str = self.txt_precio.get().strip().replace(",", "")

        if not nombre or not precio_str:
            messagebox.showwarning("Atención", "El nombre y el precio no pueden quedar vacíos.")
            return
        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido.")
            return

        exito, msg = database.actualizar_mueble_con_precio(self.mueble_seleccionado_id, nombre, precio)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_muebles()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_mueble(self):
        if not self.mueble_seleccionado_id:
            selected_items = self.tree.selection()
            if selected_items:
                val = self.tree.item(selected_items[0])['values']
                self.mueble_seleccionado_id = val[0]
            else:
                messagebox.showwarning("Atención", "Seleccione un mueble de la tabla para eliminar.")
                return

        if messagebox.askyesno("Confirmar", "¿Eliminar este mueble del catálogo?"):
            exito, msg = database.eliminar_mueble_por_id(self.mueble_seleccionado_id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_campos()
                self.cargar_muebles()
            else:
                messagebox.showerror("Error", msg)

    def limpiar_campos(self):
        self.mueble_seleccionado_id = None
        self.txt_nombre.delete(0, tk.END)
        self.txt_precio.delete(0, tk.END)
        for item in self.tree.selection():
            self.tree.selection_remove(item)


# --- VENTANA GESTIÓN DE USUARIOS ---
class VentanaGestionUsuarios(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("SGC - Consulta y Administración de Usuarios")
        self.geometry("580x440")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#2C3E50", height=50)
        header.pack(fill=tk.X)
        
        lbl_titulo = tk.Label(
            header, 
            text="👥 Registro y Control de Cuentas del Sistema", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#2C3E50"
        )
        lbl_titulo.pack(pady=12)

        frame_tabla = tk.LabelFrame(self, text=" Cuentas Registradas en Base de Datos ", font=("Arial", 9, "bold"), padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 9), rowheight=25)

        self.tree = ttk.Treeview(frame_tabla, columns=("Usuario", "Rol"), show="headings", height=8)
        self.tree.heading("Usuario", text="Nombre de Usuario")
        self.tree.heading("Rol", text="Rol (Cargo) y Permisos")
        
        self.tree.column("Usuario", width=200, anchor="center")
        self.tree.column("Rol", width=300, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar_usuarios()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)

        tk.Button(
            btn_frame, text="➕ Nuevo Usuario", bg="#27AE60", fg="white", font=("Arial", 9, "bold"), width=14,
            command=self.abrir_crear_usuario
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="🔄 Actualizar", bg="#2980B9", fg="white", font=("Arial", 9, "bold"), width=12,
            command=self.cargar_usuarios
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="🗑️ Eliminar", bg="#D35400", fg="white", font=("Arial", 9, "bold"), width=12,
            command=self.eliminar_usuario_seleccionado
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="❌ Salir", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), width=10,
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def cargar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        usuarios = database.obtener_todos_los_usuarios()
        for u in usuarios:
            self.tree.insert("", tk.END, values=(u[0], u[1].upper()))

    def abrir_crear_usuario(self):
        VentanaRegistroUsuario(self)

    def eliminar_usuario_seleccionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione un usuario de la lista.")
            return
        item = self.tree.item(selected[0])
        usuario = item['values'][0]
        if usuario == "admin":
            messagebox.showerror("Acción no permitida", "No es posible eliminar la cuenta principal de Administrador ('admin').")
            return
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de borrar al usuario '{usuario}'?"):
            exito, msg = database.eliminar_usuario(usuario)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", msg)


class VentanaRegistroUsuario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Nuevo Usuario")
        self.geometry("360x310")
        self.resizable(False, False)

        tk.Label(self, text="Crear Nueva Cuenta", font=("Arial", 12, "bold"), fg="#2C3E50").pack(pady=12)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="Usuario:").grid(row=0, column=0, sticky="e", pady=6)
        self.txt_nuevo_user = tk.Entry(form, width=22)
        self.txt_nuevo_user.grid(row=0, column=1, padx=5, pady=6)
        self.txt_nuevo_user.focus()

        tk.Label(form, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=6)
        self.txt_nueva_clave = tk.Entry(form, show="*", width=22)
        self.txt_nueva_clave.grid(row=1, column=1, padx=5, pady=6)

        tk.Label(form, text="Rol (Cargo):").grid(row=2, column=0, sticky="e", pady=6)
        self.txt_rol = tk.Entry(form, width=22)
        self.txt_rol.insert(0, "CARPINTERO")
        self.txt_rol.grid(row=2, column=1, padx=5, pady=6)

        tk.Label(form, text="Permisos (Nivel):").grid(row=3, column=0, sticky="e", pady=6)
        self.combo_permisos = ttk.Combobox(form, values=["ADMINISTRADOR", "OPERARIO"], state="readonly", width=20)
        self.combo_permisos.set("OPERARIO")
        self.combo_permisos.grid(row=3, column=1, padx=5, pady=6)

        tk.Button(
            self, text="Guardar Usuario", bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
            command=self.guardar_usuario
        ).pack(pady=15)

    def guardar_usuario(self):
        user = self.txt_nuevo_user.get().strip()
        clave = self.txt_nueva_clave.get().strip()
        rol_cargo = self.txt_rol.get().strip().upper()
        permisos = self.combo_permisos.get().strip()

        if not user or not clave or not rol_cargo:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        if " " in rol_cargo:
            messagebox.showwarning("Atención", "El Rol debe ser una sola palabra.")
            return

        exito, msg = database.registrar_usuario(user, clave, f"{rol_cargo} ({permisos})")
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.destroy()
            if hasattr(self.master, "cargar_usuarios"):
                self.master.cargar_usuarios()
        else:
            messagebox.showerror("Error", msg)


# --- VENTANA GESTIÓN DE CLIENTES ---
class VentanaClientes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("750x600")
        self.resizable(False, False)

        self.cliente_seleccionado_id = None

        header = tk.Frame(self, bg="#2C3E50", height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="👥 Módulo de Gestión de Clientes", font=("Arial", 11, "bold"), fg="white", bg="#2C3E50").pack(pady=12)

        frame_form = tk.LabelFrame(self, text=" Datos del Cliente ", font=("Arial", 9, "bold"), padx=12, pady=8)
        frame_form.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_form, text="Nombre / Razón Social:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_nombre = tk.Entry(frame_form, width=28)
        self.txt_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.txt_nombre.focus()

        tk.Label(frame_form, text="RUC / Cédula:").grid(row=0, column=2, sticky="e", pady=5)
        self.txt_ruc = tk.Entry(frame_form, width=22)
        self.txt_ruc.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Teléfono:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_tel = tk.Entry(frame_form, width=28)
        self.txt_tel.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Dirección:").grid(row=1, column=2, sticky="e", pady=5)
        self.txt_dir = tk.Entry(frame_form, width=22)
        self.txt_dir.grid(row=1, column=3, padx=5, pady=5)

        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(btn_form_frame, text="➕ Registrar", bg="#27AE60", fg="white", font=("Arial", 9, "bold"), command=self.registrar_nuevo_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_form_frame, text="✏️ Actualizar", bg="#2980B9", fg="white", font=("Arial", 9, "bold"), command=self.guardar_edicion_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_form_frame, text="🗑️ Eliminar", bg="#D35400", fg="white", font=("Arial", 9, "bold"), command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_form_frame, text="🧹 Limpiar", bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)

        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(frame_busqueda, text="🔍 Buscar (Nombre o RUC):", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.txt_buscar = tk.Entry(frame_busqueda, width=35, font=("Arial", 10))
        self.txt_buscar.pack(side=tk.LEFT, padx=5)
        self.txt_buscar.bind("<KeyRelease>", self.filtrar_clientes)

        frame_tabla = tk.LabelFrame(self, text=" Listado de Clientes ", font=("Arial", 9, "bold"), padx=10, pady=8)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "RUC", "Teléfono", "Dirección"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre / Razón Social")
        self.tree.heading("RUC", text="RUC / Cédula")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Dirección", text="Dirección")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=180, anchor="w")
        self.tree.column("RUC", width=110, anchor="center")
        self.tree.column("Teléfono", width=100, anchor="center")
        self.tree.column("Dirección", width=160, anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)
        self.cargar_clientes()

        tk.Button(self, text="❌ Salir", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), width=14, command=self.destroy).pack(pady=10)

    def registrar_nuevo_cliente(self):
        nombre = self.txt_nombre.get().strip().upper()
        ruc = self.txt_ruc.get().strip()
        tel = self.txt_tel.get().strip()
        dir_cli = self.txt_dir.get().strip().upper()

        if not nombre or not ruc:
            messagebox.showwarning("Atención", "El nombre y el RUC son obligatorios.")
            return

        exito, msg = database.registrar_cliente(ruc, nombre, tel, dir_cli)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", msg)

    def guardar_edicion_cliente(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un cliente.")
            return
        nombre = self.txt_nombre.get().strip().upper()
        ruc = self.txt_ruc.get().strip()
        tel = self.txt_tel.get().strip()
        dir_cli = self.txt_dir.get().strip().upper()

        exito, msg = database.actualizar_cliente_por_id(self.cliente_seleccionado_id, ruc, nombre, tel, dir_cli)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_cliente(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un cliente.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente seleccionado?"):
            exito, msg = database.eliminar_cliente_por_id(self.cliente_seleccionado_id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_campos()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", msg)

    def seleccionar_cliente(self, event):
        selected = self.tree.selection()
        if selected:
            val = self.tree.item(selected[0])['values']
            self.cliente_seleccionado_id = val[0]
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, val[1])
            self.txt_ruc.delete(0, tk.END)
            self.txt_ruc.insert(0, val[2])
            self.txt_tel.delete(0, tk.END)
            self.txt_tel.insert(0, val[3])
            self.txt_dir.delete(0, tk.END)
            self.txt_dir.insert(0, val[4])

    def limpiar_campos(self):
        self.cliente_seleccionado_id = None
        self.txt_nombre.delete(0, tk.END)
        self.txt_ruc.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.txt_dir.delete(0, tk.END)

    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in database.obtener_todos_los_clientes():
            self.tree.insert("", tk.END, values=c)

    def filtrar_clientes(self, event=None):
        termino = self.txt_buscar.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in database.buscar_clientes(termino):
            self.tree.insert("", tk.END, values=c)


# --- MÓDULO: PEDIDOS Y TALLER ---
class VentanaInventario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo de Pedidos - Taller de Carpintería")
        self.geometry("950x670")
        self.resizable(False, False)
        self.pedido_seleccionado_id = None

        header = tk.Frame(self, bg="#4A2E10", height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="🪵 Registro y Gestión de Pedidos de Clientes", font=("Arial", 11, "bold"), fg="white", bg="#4A2E10").pack(pady=12)

        frame_form = tk.LabelFrame(self, text=" Datos del Pedido ", font=("Arial", 9, "bold"), padx=12, pady=8)
        frame_form.pack(fill=tk.X, padx=15, pady=8)

        tk.Label(frame_form, text="RUC / Cédula:").grid(row=0, column=0, sticky="e", pady=6)
        self.txt_ruc = tk.Entry(frame_form, width=22)
        self.txt_ruc.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.txt_ruc.bind("<KeyRelease>", self.actualizar_nombre_cliente_por_ruc)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=2, sticky="e", pady=6)
        self.lbl_cliente_nombre = tk.Label(frame_form, text="[Ingrese RUC]", fg="gray", font=("Arial", 9, "italic"), anchor="w", width=30)
        self.lbl_cliente_nombre.grid(row=0, column=3, padx=5, pady=6, sticky="w")

        tk.Label(frame_form, text="Trabajo / Mueble:").grid(row=1, column=0, sticky="e", pady=6)
        frame_trabajo = tk.Frame(frame_form)
        frame_trabajo.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        self.combo_trabajo = ttk.Combobox(frame_trabajo, width=24)
        self.combo_trabajo.pack(side=tk.LEFT)

        tk.Button(
            frame_trabajo, text="💲 Precios", bg="#D35400", fg="white", font=("Arial", 8, "bold"),
            command=lambda: VentanaCatalogoMuebles(self)
        ).pack(side=tk.LEFT, padx=4)

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=2, sticky="e", pady=6)
        self.txt_cantidad = tk.Entry(frame_form, width=10)
        self.txt_cantidad.insert(0, "1")
        self.txt_cantidad.grid(row=1, column=3, padx=5, pady=6, sticky="w")

        self.lbl_precio_estimado = tk.Label(frame_form, text="Unit.: ₲ 0 | Total: ₲ 0", fg="#16A085", font=("Arial", 9, "bold"))
        self.lbl_precio_estimado.grid(row=1, column=4, padx=5, pady=6, sticky="w")

        self.combo_trabajo.bind("<<ComboboxSelected>>", self.calcular_precio_pedido)
        self.combo_trabajo.bind("<KeyRelease>", self.calcular_precio_pedido)
        self.txt_cantidad.bind("<KeyRelease>", self.calcular_precio_pedido)

        tk.Label(frame_form, text="Plazo Entrega (Días):").grid(row=2, column=0, sticky="e", pady=6)
        self.txt_plazo_dias = tk.Entry(frame_form, width=22)
        self.txt_plazo_dias.insert(0, "15")
        self.txt_plazo_dias.grid(row=2, column=1, padx=5, pady=6, sticky="w")

        tk.Label(frame_form, text="Estado del Trabajo:").grid(row=2, column=2, sticky="e", pady=6)
        self.combo_estado = ttk.Combobox(frame_form, values=["PENDIENTE", "EN PROCESO", "TERMINADO", "CANCELADO"], state="readonly", width=23)
        self.combo_estado.set("PENDIENTE")
        self.combo_estado.grid(row=2, column=3, padx=5, pady=6, sticky="w")

        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=3, column=0, columnspan=5, pady=12)

        tk.Button(btn_form_frame, text="📋 Registrar", bg="#27AE60", fg="white", font=("Arial", 9, "bold"), command=self.guardar_pedido).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_form_frame, text="✏️ Actualizar", bg="#2980B9", fg="white", font=("Arial", 9, "bold"), command=self.guardar_edicion).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_form_frame, text="🗑️ Eliminar", bg="#D35400", fg="white", font=("Arial", 9, "bold"), command=self.eliminar_pedido_seleccionado).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_form_frame, text="🧹 Limpiar", bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), command=self.limpiar_campos).pack(side=tk.LEFT, padx=6)

        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(frame_busqueda, text="🔍 Buscar Pedido:", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.txt_buscar_pedido = tk.Entry(frame_busqueda, width=28, font=("Arial", 10))
        self.txt_buscar_pedido.pack(side=tk.LEFT, padx=5)
        self.txt_buscar_pedido.bind("<KeyRelease>", self.filtrar_pedidos)

        frame_tabla = tk.LabelFrame(self, text=" Listado de Pedidos en Taller ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Cliente", "RUC", "Trabajo", "Cantidad", "Total", "Plazo", "Estado"), show="headings", height=7)
        self.tree.heading("ID", text="N°")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("RUC", text="RUC / Cédula")
        self.tree.heading("Trabajo", text="Trabajo / Mueble")
        self.tree.heading("Cantidad", text="Cant.")
        self.tree.heading("Total", text="Total Est.")
        self.tree.heading("Plazo", text="Plazo")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=35, anchor="center")
        self.tree.column("Cliente", width=150, anchor="w")
        self.tree.column("RUC", width=95, anchor="center")
        self.tree.column("Trabajo", width=190, anchor="w")
        self.tree.column("Cantidad", width=45, anchor="center")
        self.tree.column("Total", width=105, anchor="e")
        self.tree.column("Plazo", width=70, anchor="center")
        self.tree.column("Estado", width=90, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pedido)
        self.cargar_opciones_combos()
        self.cargar_pedidos()

        tk.Button(self, text="❌ Salir", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), width=16, command=self.destroy).pack(pady=10)

    def calcular_precio_pedido(self, event=None):
        mueble = self.combo_trabajo.get().strip()
        precio_unit = database.obtener_precio_mueble(mueble)
        try:
            cant = int(self.txt_cantidad.get().strip())
        except ValueError:
            cant = 1
        total = precio_unit * cant
        self.lbl_precio_estimado.config(text=f"Unit.: ₲ {precio_unit:,.0f} | Total: ₲ {total:,.0f}")

    def cargar_opciones_combos(self):
        self.combo_trabajo['values'] = database.obtener_tipos_muebles()

    def actualizar_nombre_cliente_por_ruc(self, event=None):
        ruc = self.txt_ruc.get().strip().upper()
        if not ruc:
            self.lbl_cliente_nombre.config(text="[Ingrese RUC]", fg="gray")
            return
        for c in database.obtener_todos_los_clientes():
            if c[2] and ruc == c[2].strip().upper():
                self.lbl_cliente_nombre.config(text=c[1], fg="black")
                return
        self.lbl_cliente_nombre.config(text="[No registrado]", fg="red")

    def cargar_pedidos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in database.obtener_todos_los_pedidos():
            precio_u = database.obtener_precio_mueble(p[3])
            total_est = f"₲ {precio_u * p[4]:,.0f}"
            self.tree.insert("", tk.END, values=(p[0], p[1], p[2], p[3], p[4], total_est, f"{p[5]} días", p[6]))

    def filtrar_pedidos(self, event=None):
        termino = self.txt_buscar_pedido.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in database.buscar_pedidos(termino):
            precio_u = database.obtener_precio_mueble(p[3])
            total_est = f"₲ {precio_u * p[4]:,.0f}"
            self.tree.insert("", tk.END, values=(p[0], p[1], p[2], p[3], p[4], total_est, f"{p[5]} días", p[6]))

    def seleccionar_pedido(self, event):
        selected = self.tree.selection()
        if selected:
            val = self.tree.item(selected[0])['values']
            self.pedido_seleccionado_id = val[0]
            self.txt_ruc.delete(0, tk.END)
            self.txt_ruc.insert(0, str(val[2]))
            self.actualizar_nombre_cliente_por_ruc()
            self.combo_trabajo.set(str(val[3]))
            self.txt_cantidad.delete(0, tk.END)
            self.txt_cantidad.insert(0, str(val[4]))
            self.txt_plazo_dias.delete(0, tk.END)
            self.txt_plazo_dias.insert(0, str(val[6]).replace(" días", ""))
            self.combo_estado.set(str(val[7]))
            self.calcular_precio_pedido()

    def limpiar_campos(self):
        self.pedido_seleccionado_id = None
        self.txt_ruc.delete(0, tk.END)
        self.lbl_cliente_nombre.config(text="[Ingrese RUC]", fg="gray")
        self.combo_trabajo.set("")
        self.txt_cantidad.delete(0, tk.END)
        self.txt_cantidad.insert(0, "1")
        self.txt_plazo_dias.delete(0, tk.END)
        self.txt_plazo_dias.insert(0, "15")
        self.combo_estado.set("PENDIENTE")
        self.lbl_precio_estimado.config(text="Unit.: ₲ 0 | Total: ₲ 0")

    def guardar_pedido(self):
        ruc = self.txt_ruc.get().strip()
        trab = self.combo_trabajo.get().strip()
        cant = self.txt_cantidad.get().strip()
        plazo = self.txt_plazo_dias.get().strip()

        if not ruc or not trab:
            messagebox.showwarning("Atención", "RUC y Trabajo son obligatorios.")
            return

        cli_nombre = self.lbl_cliente_nombre.cget("text")
        if cli_nombre in ("[Ingrese RUC]", "[No registrado]"):
            messagebox.showerror("Error", "El cliente debe estar registrado.")
            return

        exito, msg = database.registrar_pedido(cli_nombre, ruc, trab, int(cant), int(plazo))
        if exito:
            database.registrar_nuevo_mueble(trab)
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_pedidos()
            self.cargar_opciones_combos()
        else:
            messagebox.showerror("Error", msg)

    def guardar_edicion(self):
        if not self.pedido_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un pedido.")
            return
        trab = self.combo_trabajo.get().strip()
        exito, msg = database.actualizar_pedido(self.pedido_seleccionado_id, trab, int(self.txt_cantidad.get()), int(self.txt_plazo_dias.get()), self.combo_estado.get())
        if exito:
            database.registrar_nuevo_mueble(trab)
            messagebox.showinfo("Éxito", "Pedido actualizado con éxito.")
            self.limpiar_campos()
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_pedido_seleccionado(self):
        if not self.pedido_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un pedido.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar pedido seleccionado?"):
            exito, msg = database.eliminar_pedido(self.pedido_seleccionado_id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_campos()
                self.cargar_pedidos()
            else:
                messagebox.showerror("Error", msg)