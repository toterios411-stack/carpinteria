import tkinter as tk
from tkinter import messagebox, ttk
import database

class MenuPrincipal(tk.Toplevel):
    def __init__(self, parent, rol_usuario="Operario"):
        super().__init__(parent)
        self.parent = parent
        self.rol_usuario = rol_usuario
        self.title("Sistema de Gestión para Carpintería - Panel Principal")
        self.geometry("850x550")
        self.resizable(False, False)

        # Encabezado
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

        # Botones de Módulos
        btn_frame = tk.Frame(self)
        btn_frame.pack(expand=True)

        tk.Button(
            btn_frame, 
            text="👥 Gestión de Clientes", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            command=self.abrir_clientes
        ).grid(row=0, column=0, padx=15, pady=15)

        tk.Button(
            btn_frame, 
            text="🪵 Pedidos y Stock de Cedro (Módulo 3)", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            command=self.abrir_inventario
        ).grid(row=0, column=1, padx=15, pady=15)
        
        # Módulo 2 accesible para Administradores
        if self.rol_usuario == "Administrador":
            tk.Button(
                btn_frame, 
                text="⚙️ Gestión de Usuarios y Roles (Módulo 2)", 
                font=("Arial", 11, "bold"), 
                width=32, 
                height=2, 
                bg="#2980B9", 
                fg="white", 
                command=self.abrir_usuarios
            ).grid(row=1, column=0, padx=15, pady=15)
        else:
            tk.Button(
                btn_frame, 
                text="⚙️ Gestión de Usuarios (Solo Admin)", 
                font=("Arial", 11), 
                width=32, 
                height=2, 
                state=tk.DISABLED
            ).grid(row=1, column=0, padx=15, pady=15)

        tk.Button(
            btn_frame, 
            text="📋 Órdenes y Presupuestos", 
            font=("Arial", 11), 
            width=32, 
            height=2, 
            command=self.modulo_construccion
        ).grid(row=1, column=1, padx=15, pady=15)

        # Botón Cerrar Sesión
        tk.Button(
            self, 
            text="🔒 Cerrar Sesión", 
            font=("Arial", 10, "bold"), 
            bg="#C0392B", 
            fg="white", 
            command=self.cerrar_sesion
        ).pack(pady=20)

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

    def modulo_construccion(self):
        messagebox.showinfo("Información", "Módulo programado para la siguiente entrega.")


# --- VENTANA MÓDULO 2: GESTIÓN DE USUARIOS Y ROLES ---
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
        self.tree.heading("Rol", text="Rol / Permiso Asignado")
        
        self.tree.column("Usuario", width=250, anchor="center")
        self.tree.column("Rol", width=250, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar_usuarios()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)

        tk.Button(
            btn_frame, 
            text="➕ Nuevo Usuario", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=14,
            command=self.abrir_crear_usuario
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, 
            text="🔄 Actualizar", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=12,
            command=self.cargar_usuarios
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, 
            text="🗑️ Eliminar", 
            bg="#D35400", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=12,
            command=self.eliminar_usuario_seleccionado
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, 
            text="❌ Salir", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=10,
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def cargar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = database.obtener_todos_los_usuarios()
        for u in usuarios:
            self.tree.insert("", tk.END, values=(u[0], u[1]))

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

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea borrar al usuario '{usuario}' del sistema?")
        if confirmar:
            exito, msg = database.eliminar_usuario(usuario)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", msg)


# --- VENTANA EMERGENTE PARA REGISTRAR NUEVO USUARIO ---
class VentanaRegistroUsuario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Nuevo Usuario")
        self.geometry("340x260")
        self.resizable(False, False)

        tk.Label(self, text="Crear Nueva Cuenta", font=("Arial", 12, "bold"), fg="#2C3E50").pack(pady=12)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_nuevo_user = tk.Entry(form, width=20)
        self.txt_nuevo_user.grid(row=0, column=1, padx=5, pady=5)
        self.txt_nuevo_user.focus()

        tk.Label(form, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_nueva_clave = tk.Entry(form, show="*", width=20)
        self.txt_nueva_clave.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Rol:").grid(row=2, column=0, sticky="e", pady=5)
        self.combo_rol = ttk.Combobox(form, values=["Administrador", "Operario"], state="readonly", width=17)
        self.combo_rol.set("Operario")
        self.combo_rol.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            self, 
            text="Guardar Usuario", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 10, "bold"),
            command=self.guardar_usuario
        ).pack(pady=15)

    def guardar_usuario(self):
        user = self.txt_nuevo_user.get().strip()
        clave = self.txt_nueva_clave.get().strip()
        rol = self.combo_rol.get()

        if not user or not clave:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        exito, msg = database.registrar_usuario(user, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", f"Usuario '{user}' registrado como {rol}.")
            self.destroy()
            # Recarga la tabla de la ventana de gestión si está abierta
            if hasattr(self.master, "cargar_usuarios"):
                self.master.cargar_usuarios()
        else:
            messagebox.showerror("Error", msg)


# --- VENTANA MÓDULO 3: PEDIDOS CON REGISTRO INTEGRADO DE CLIENTES NUEVOS ---
class VentanaInventario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo 3: Pedidos de Clientes y Disponibilidad de Cedro")
        self.geometry("820x660")
        self.resizable(False, False)

        self.pedido_seleccionado_id = None

        header = tk.Frame(self, bg="#4A2E10", height=50)
        header.pack(fill=tk.X)
        
        lbl_titulo = tk.Label(
            header, 
            text="🪵 Gestión de Pedidos y Alta de Clientes Nuevos", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#4A2E10"
        )
        lbl_titulo.pack(pady=12)

        frame_form = tk.LabelFrame(self, text=" Datos del Pedido y Cliente ", font=("Arial", 9, "bold"), padx=12, pady=8)
        frame_form.pack(fill=tk.X, padx=15, pady=8)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="e", pady=4)
        self.combo_cliente = ttk.Combobox(frame_form, width=24)
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=4)
        self.combo_cliente.bind("<<ComboboxSelected>>", self.evaluar_cliente_nuevo)
        self.combo_cliente.bind("<KeyRelease>", self.evaluar_cliente_nuevo)

        tk.Label(frame_form, text="Trabajo / Mueble:").grid(row=0, column=2, sticky="e", pady=4)
        self.combo_trabajo = ttk.Combobox(frame_form, width=24)
        self.combo_trabajo.grid(row=0, column=3, padx=5, pady=4)

        self.lbl_ruc = tk.Label(frame_form, text="RUC / Cédula:")
        self.lbl_ruc.grid(row=1, column=0, sticky="e", pady=4)
        self.txt_ruc = tk.Entry(frame_form, width=26)
        self.txt_ruc.grid(row=1, column=1, padx=5, pady=4)

        self.lbl_tel = tk.Label(frame_form, text="Teléfono:")
        self.lbl_tel.grid(row=1, column=2, sticky="e", pady=4)
        self.txt_tel = tk.Entry(frame_form, width=26)
        self.txt_tel.grid(row=1, column=3, padx=5, pady=4)

        self.lbl_dir = tk.Label(frame_form, text="Dirección:")
        self.lbl_dir.grid(row=2, column=0, sticky="e", pady=4)
        self.txt_dir = tk.Entry(frame_form, width=26)
        self.txt_dir.grid(row=2, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Plazo Entrega (Días):").grid(row=2, column=2, sticky="e", pady=4)
        self.txt_plazo_dias = tk.Entry(frame_form, width=26)
        self.txt_plazo_dias.insert(0, "15")
        self.txt_plazo_dias.grid(row=2, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Estado del Trabajo:").grid(row=3, column=0, sticky="e", pady=4)
        self.combo_estado = ttk.Combobox(
            frame_form, 
            values=["Pendiente", "En Proceso", "Terminado", "Cancelado"], 
            state="readonly", 
            width=24
        )
        self.combo_estado.set("Pendiente")
        self.combo_estado.grid(row=3, column=1, padx=5, pady=4)

        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=4, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_form_frame, 
            text="📋 Registrar Pedido", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.guardar_pedido
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="✏️ Guardar Cambios", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.guardar_edicion
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="🗑️ Eliminar", 
            bg="#D35400", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.eliminar_pedido_seleccionado
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="🧹 Limpiar Campos", 
            bg="#7F8C8D", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=5)

        frame_tabla = tk.LabelFrame(self, text=" Registro de Pedidos en Taller ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Cliente", "Trabajo", "CedroEst", "Plazo", "Estado"), show="headings", height=5)
        self.tree.heading("ID", text="N°")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Trabajo", text="Trabajo / Mueble")
        self.tree.heading("CedroEst", text="Cedro Estimado")
        self.tree.heading("Plazo", text="Plazo (Días)")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=35, anchor="center")
        self.tree.column("Cliente", width=170, anchor="w")
        self.tree.column("Trabajo", width=220, anchor="w")
        self.tree.column("CedroEst", width=100, anchor="center")
        self.tree.column("Plazo", width=85, anchor="center")
        self.tree.column("Estado", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pedido)

        self.cargar_opciones_combos()
        self.cargar_pedidos()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, 
            text="❌ Salir", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=16,
            command=self.destroy
        ).pack()

    def cargar_opciones_combos(self):
        clientes_bd = database.obtener_todos_los_clientes()
        self.lista_clientes_nombres = [c[1] for c in clientes_bd]
        
        opciones_combo = ["-- NUEVO CLIENTE --"] + self.lista_clientes_nombres
        self.combo_cliente['values'] = opciones_combo
        self.combo_cliente.set(opciones_combo[0])

        muebles_bd = database.obtener_tipos_muebles()
        self.combo_trabajo['values'] = muebles_bd
        if muebles_bd:
            self.combo_trabajo.set(muebles_bd[0])

        self.evaluar_cliente_nuevo()

    def evaluar_cliente_nuevo(self, event=None):
        val = self.combo_cliente.get().strip()
        if val == "-- NUEVO CLIENTE --" or (val and val not in self.lista_clientes_nombres):
            self.txt_ruc.config(state="normal")
            self.txt_tel.config(state="normal")
            self.txt_dir.config(state="normal")
        else:
            self.txt_ruc.delete(0, tk.END)
            self.txt_tel.delete(0, tk.END)
            self.txt_dir.delete(0, tk.END)
            self.txt_ruc.config(state="disabled")
            self.txt_tel.config(state="disabled")
            self.txt_dir.config(state="disabled")

    def cargar_pedidos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        pedidos = database.obtener_todos_los_pedidos_cedro()
        for p in pedidos:
            self.tree.insert("", tk.END, values=(p[0], p[1], p[2], f"~{p[3]} tablas", f"{p[4]} días", p[5]))

    def seleccionar_pedido(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item['values']
            
            self.pedido_seleccionado_id = val[0]
            self.combo_cliente.set(str(val[1]))
            self.combo_cliente.config(state="disabled")
            self.evaluar_cliente_nuevo()

            self.combo_trabajo.set(str(val[2]))
            
            plazo_str = str(val[4]).replace(" días", "").strip()
            self.txt_plazo_dias.delete(0, tk.END)
            self.txt_plazo_dias.insert(0, plazo_str)
            
            self.combo_estado.set(str(val[5]))

    def limpiar_campos(self):
        self.pedido_seleccionado_id = None
        self.combo_cliente.config(state="normal")
        self.txt_ruc.config(state="normal")
        self.txt_tel.config(state="normal")
        self.txt_dir.config(state="normal")

        self.txt_ruc.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.txt_dir.delete(0, tk.END)

        self.cargar_opciones_combos()
        self.txt_plazo_dias.delete(0, tk.END)
        self.txt_plazo_dias.insert(0, "15")
        self.combo_estado.set("Pendiente")

    def guardar_pedido(self):
        self.combo_cliente.config(state="normal")
        cli = self.combo_cliente.get().strip()
        trab = self.combo_trabajo.get().strip()
        plazo = self.txt_plazo_dias.get().strip()

        ruc = self.txt_ruc.get().strip()
        tel = self.txt_tel.get().strip()
        direccion = self.txt_dir.get().strip()

        if cli == "-- NUEVO CLIENTE --" or not cli:
            messagebox.showwarning("Atención", "Por favor ingrese o seleccione el nombre del cliente.")
            return

        if not trab or not plazo:
            messagebox.showwarning("Atención", "Complete el trabajo y el plazo de entrega.")
            return

        try:
            plazo_int = int(plazo)
        except ValueError:
            messagebox.showwarning("Atención", "El plazo de entrega debe ser un número entero de días.")
            return

        exito, msg = database.registrar_pedido_cedro(cli, trab, plazo_int, ruc, tel, direccion)
        if exito:
            database.registrar_nuevo_mueble(trab)
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", msg)

    def guardar_edicion(self):
        if not self.pedido_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista para modificarlo.")
            return

        trab = self.combo_trabajo.get().strip()
        plazo = self.txt_plazo_dias.get().strip()
        estado = self.combo_estado.get()

        if not trab or not plazo:
            messagebox.showwarning("Atención", "El trabajo y el plazo de entrega no pueden estar vacíos.")
            return

        try:
            plazo_int = int(plazo)
        except ValueError:
            messagebox.showwarning("Atención", "El plazo de entrega debe ser un número entero de días.")
            return

        exito, msg = database.actualizar_pedido_cedro(self.pedido_seleccionado_id, trab, plazo_int, estado)
        if exito:
            database.registrar_nuevo_mueble(trab)
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_pedido_seleccionado(self):
        if not self.pedido_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista para eliminar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            "¿Está seguro de que desea borrar este pedido del registro?"
        )
        
        if confirmar:
            exito, msg = database.eliminar_pedido_cedro(self.pedido_seleccionado_id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_campos()
                self.cargar_pedidos()
            else:
                messagebox.showerror("Error", msg)


# --- VENTANA MÓDULO: GESTIÓN DE CLIENTES CON EDICIÓN Y CONSULTA ---
class VentanaClientes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión y Edición de Clientes - SGC")
        self.geometry("650x560")
        self.resizable(False, False)

        tk.Label(self, text="Gestión y Administración de Clientes", font=("Arial", 14, "bold")).pack(pady=10)

        frame_form = tk.LabelFrame(self, text=" Datos del Cliente ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_form.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(frame_form, text="RUC/Cédula:").grid(row=0, column=0, sticky="e", pady=4)
        self.txt_ruc = tk.Entry(frame_form, width=18)
        self.txt_ruc.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="e", pady=4)
        self.txt_nombre = tk.Entry(frame_form, width=22)
        self.txt_nombre.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Teléfono:").grid(row=1, column=0, sticky="e", pady=4)
        self.txt_tel = tk.Entry(frame_form, width=18)
        self.txt_tel.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Dirección:").grid(row=1, column=2, sticky="e", pady=4)
        self.txt_dir = tk.Entry(frame_form, width=22)
        self.txt_dir.grid(row=1, column=3, padx=5, pady=4)

        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=2, column=0, columnspan=4, pady=8)

        tk.Button(
            btn_form_frame, 
            text="💾 Guardar Nuevo", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.guardar_cliente
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="✏️ Guardar Cambios", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.guardar_edicion
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="🧹 Limpiar Campos", 
            bg="#7F8C8D", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=5)

        frame_tabla = tk.LabelFrame(self, text=" Clientes Registrados (Haga clic en uno para editar) ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("RUC", "Nombre", "Teléfono", "Dirección"), show="headings", height=7)
        self.tree.heading("RUC", text="RUC / Cédula")
        self.tree.heading("Nombre", text="Nombre / Razón Social")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Dirección", text="Dirección")

        self.tree.column("RUC", width=110, anchor="center")
        self.tree.column("Nombre", width=190, anchor="w")
        self.tree.column("Teléfono", width=110, anchor="center")
        self.tree.column("Dirección", width=160, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)
        self.cargar_clientes()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, 
            text="❌ Salir", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=14, 
            command=self.destroy
        ).pack()

    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for c in database.obtener_todos_los_clientes():
            self.tree.insert("", tk.END, values=(c[0], c[1], c[2], c[3]))

    def seleccionar_cliente(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            valores = item['values']
            
            self.limpiar_campos()
            self.txt_ruc.insert(0, str(valores[0]))
            self.txt_nombre.insert(0, str(valores[1]))
            self.txt_tel.insert(0, str(valores[2]))
            self.txt_dir.insert(0, str(valores[3]))
            
            self.txt_ruc.config(state="disabled")

    def limpiar_campos(self):
        self.txt_ruc.config(state="normal")
        self.txt_ruc.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.txt_dir.delete(0, tk.END)

    def guardar_cliente(self):
        self.txt_ruc.config(state="normal")
        ruc = self.txt_ruc.get().strip()
        nom = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        direccion = self.txt_dir.get().strip()

        if not ruc or not nom:
            messagebox.showwarning("Atención", "RUC/Cédula y Nombre son obligatorios.")
            return

        exito, msg = database.registrar_cliente(ruc, nom, tel, direccion, "")
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", msg)

    def guardar_edicion(self):
        ruc = self.txt_ruc.get().strip()
        nom = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        direccion = self.txt_dir.get().strip()

        if not nom:
            messagebox.showwarning("Atención", "El nombre o razón social es obligatorio.")
            return

        exito, msg = database.actualizar_cliente(ruc, nom, tel, direccion)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else: 
            messagebox.showerror("Error", msg)