import tkinter as tk
from tkinter import messagebox, ttk
import database

class MenuPrincipal(tk.Toplevel):
    def __init__(self, parent, rol_usuario="CARPINTERO (Operario)"):
        super().__init__(parent)
        self.parent = parent
        self.rol_usuario = rol_usuario.upper()
        self.title("Sistema de Gestión para Carpintería - Panel Principal")
        self.geometry("850x550")
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
            text="🪵 Registro y Pedidos de Taller", 
            font=("Arial", 11, "bold"), 
            width=32, 
            height=2, 
            command=self.abrir_inventario
        ).grid(row=0, column=1, padx=15, pady=15)
        
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

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea borrar al usuario '{usuario}' del sistema?")
        if confirmar:
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
        self.combo_permisos = ttk.Combobox(
            form, 
            values=["ADMINISTRADOR", "OPERARIO"], 
            state="readonly", 
            width=20
        )
        self.combo_permisos.set("OPERARIO")
        self.combo_permisos.grid(row=3, column=1, padx=5, pady=6)

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
        rol_cargo = self.txt_rol.get().strip()
        permisos = self.combo_permisos.get().strip()

        if not user or not clave:
            messagebox.showwarning("Atención", "El usuario y la contraseña son obligatorios.")
            return

        if not rol_cargo:
            messagebox.showwarning("Atención", "El campo de Rol (Cargo) no puede estar vacío.")
            return

        if len(rol_cargo.split()) > 1 or " " in rol_cargo:
            messagebox.showwarning("Atención", "El Rol (Cargo) debe ser estrictamente UNA SOLA PALABRA (sin espacios).")
            return

        rol_cargo_formateado = rol_cargo.upper()
        rol_final = f"{rol_cargo_formateado} ({permisos})"

        exito, msg = database.registrar_usuario(user, clave, rol_final)
        
        if exito:
            messagebox.showinfo("Éxito", f"Usuario '{user}' registrado como '{rol_cargo_formateado}' con permisos de {permisos}.")
            self.destroy()
            if hasattr(self.master, "cargar_usuarios"):
                self.master.cargar_usuarios()
        else:
            messagebox.showerror("Error", msg)


# --- MÓDULO: PEDIDOS Y GESTIÓN DE TALLER ---
class VentanaInventario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo de Pedidos - Taller de Carpintería")
        self.geometry("900x660")
        self.resizable(False, False)

        self.pedido_seleccionado_id = None

        header = tk.Frame(self, bg="#4A2E10", height=50)
        header.pack(fill=tk.X)
        
        lbl_titulo = tk.Label(
            header, 
            text="🪵 Registro y Gestión de Pedidos de Clientes", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#4A2E10"
        )
        lbl_titulo.pack(pady=12)

        # --- FORMULARIO DE PEDIDO ---
        frame_form = tk.LabelFrame(self, text=" Datos del Pedido ", font=("Arial", 9, "bold"), padx=12, pady=8)
        frame_form.pack(fill=tk.X, padx=15, pady=8)

        # Fila 0: RUC / Cédula y Nombre de Cliente Automático
        tk.Label(frame_form, text="RUC / Cédula:").grid(row=0, column=0, sticky="e", pady=6)
        self.txt_ruc = tk.Entry(frame_form, width=22)
        self.txt_ruc.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.txt_ruc.bind("<KeyRelease>", self.actualizar_nombre_cliente_por_ruc)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=2, sticky="e", pady=6)
        self.lbl_cliente_nombre = tk.Label(frame_form, text="[Ingrese RUC]", fg="gray", font=("Arial", 9, "italic"), anchor="w", width=30)
        self.lbl_cliente_nombre.grid(row=0, column=3, padx=5, pady=6, sticky="w")

        # Fila 1: Trabajo (Ancho ampliado a width=32 y botón de borrar catálogo) y Cantidad
        tk.Label(frame_form, text="Trabajo / Mueble:").grid(row=1, column=0, sticky="e", pady=6)
        
        frame_trabajo = tk.Frame(frame_form)
        frame_trabajo.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        self.combo_trabajo = ttk.Combobox(frame_trabajo, width=32)
        self.combo_trabajo.pack(side=tk.LEFT)
        self.combo_trabajo.bind("<KeyRelease>", self.autocompletar_trabajo)

        tk.Button(
            frame_trabajo, 
            text="🗑️", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 8, "bold"), 
            command=self.eliminar_mueble_catalogo,
            relief="flat"
        ).pack(side=tk.LEFT, padx=3)

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=2, sticky="e", pady=6)
        self.txt_cantidad = tk.Entry(frame_form, width=20)
        self.txt_cantidad.insert(0, "1")
        self.txt_cantidad.grid(row=1, column=3, padx=5, pady=6, sticky="w")

        # Fila 2: Plazo y Estado
        tk.Label(frame_form, text="Plazo Entrega (Días):").grid(row=2, column=0, sticky="e", pady=6)
        self.txt_plazo_dias = tk.Entry(frame_form, width=22)
        self.txt_plazo_dias.insert(0, "15")
        self.txt_plazo_dias.grid(row=2, column=1, padx=5, pady=6, sticky="w")

        tk.Label(frame_form, text="Estado del Trabajo:").grid(row=2, column=2, sticky="e", pady=6)
        self.combo_estado = ttk.Combobox(
            frame_form, 
            values=["PENDIENTE", "EN PROCESO", "TERMINADO", "CANCELADO"], 
            state="readonly", 
            width=23
        )
        self.combo_estado.set("PENDIENTE")
        self.combo_estado.grid(row=2, column=3, padx=5, pady=6, sticky="w")

        # Botonera de Acciones
        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=3, column=0, columnspan=4, pady=12)

        tk.Button(
            btn_form_frame, 
            text="📋 Registrar Pedido", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.guardar_pedido
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_form_frame, 
            text="✏️ Guardar Cambios", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.guardar_edicion
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_form_frame, 
            text="🗑️ Eliminar", 
            bg="#D35400", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.eliminar_pedido_seleccionado
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_form_frame, 
            text="🧹 Limpiar Campos", 
            bg="#7F8C8D", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=6)

        # --- BUSCADOR DE PEDIDOS ---
        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(frame_busqueda, text="🔍 Buscar Pedido (Exacto: RUC, Cliente o Mueble):", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.txt_buscar_pedido = tk.Entry(frame_busqueda, width=28, font=("Arial", 10))
        self.txt_buscar_pedido.pack(side=tk.LEFT, padx=5)
        self.txt_buscar_pedido.bind("<KeyRelease>", self.filtrar_pedidos)

        # --- TABLA DE PEDIDOS ---
        frame_tabla = tk.LabelFrame(self, text=" Listado de Pedidos en Taller ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Cliente", "RUC", "Trabajo", "Cantidad", "Plazo", "Estado"), show="headings", height=7)
        self.tree.heading("ID", text="N°")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("RUC", text="RUC / Cédula")
        self.tree.heading("Trabajo", text="Trabajo / Mueble")
        self.tree.heading("Cantidad", text="Cant.")
        self.tree.heading("Plazo", text="Plazo")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=35, anchor="center")
        self.tree.column("Cliente", width=160, anchor="w")
        self.tree.column("RUC", width=100, anchor="center")
        self.tree.column("Trabajo", width=200, anchor="w")
        self.tree.column("Cantidad", width=50, anchor="center")
        self.tree.column("Plazo", width=75, anchor="center")
        self.tree.column("Estado", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pedido)

        self.cargar_opciones_combos()
        self.cargar_pedidos()

        tk.Button(
            self, 
            text="❌ Salir", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=16,
            command=self.destroy
        ).pack(pady=10)

    def cargar_opciones_combos(self):
        muebles_bd = database.obtener_tipos_muebles()
        self.lista_muebles = muebles_bd
        self.combo_trabajo['values'] = muebles_bd

    def autocompletar_trabajo(self, event):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down", "Return"):
            return
        texto_tipeado = self.combo_trabajo.get().strip().upper()
        if not texto_tipeado:
            return
        for mueble in self.lista_muebles:
            if mueble.startswith(texto_tipeado):
                self.combo_trabajo.delete(0, tk.END)
                self.combo_trabajo.insert(0, mueble)
                self.combo_trabajo.select_range(len(texto_tipeado), tk.END)
                break

    def eliminar_mueble_catalogo(self):
        mueble = self.combo_trabajo.get().strip().upper()
        if not mueble:
            messagebox.showwarning("Atención", "Seleccione o escriba el trabajo que desea eliminar del catálogo.")
            return
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar '{mueble}' de los trabajos disponibles?")
        if confirmar:
            exito, msg = database.eliminar_tipo_mueble(mueble)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_opciones_combos()
                self.combo_trabajo.set("")
            else:
                messagebox.showerror("Error", msg)

    def actualizar_nombre_cliente_por_ruc(self, event=None):
        ruc_ingresado = self.txt_ruc.get().strip().upper()
        if not ruc_ingresado:
            self.lbl_cliente_nombre.config(text="[Ingrese RUC]", fg="gray", font=("Arial", 9, "italic"))
            return
        
        clientes = database.obtener_todos_los_clientes()
        encontrado = False
        for c in clientes:
            if c[2] and ruc_ingresado == c[2].strip().upper():
                self.lbl_cliente_nombre.config(text=c[1].upper(), fg="black", font=("Arial", 9, "bold"))
                encontrado = True
                break
        if not encontrado:
            self.lbl_cliente_nombre.config(text="[Cliente no registrado]", fg="red", font=("Arial", 9, "italic"))

    def cargar_pedidos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        pedidos = database.obtener_todos_los_pedidos()
        for p in pedidos:
            cliente_nombre = p[1].upper() if p[1] else ""
            ruc = p[2] if p[2] and p[2] != "None" else "S/D"
            trabajo = p[3].upper() if p[3] else ""
            cantidad = p[4]
            plazo = p[5]
            estado = p[6].upper() if p[6] else ""
            self.tree.insert("", tk.END, values=(p[0], cliente_nombre, ruc, trabajo, cantidad, f"{plazo} días", estado))

    def filtrar_pedidos(self, event=None):
        termino = self.txt_buscar_pedido.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not termino:
            self.cargar_pedidos()
            return
            
        pedidos = database.buscar_pedidos(termino)
        for p in pedidos:
            cliente_nombre = p[1].upper() if p[1] else ""
            ruc = p[2] if p[2] and p[2] != "None" else "S/D"
            trabajo = p[3].upper() if p[3] else ""
            cantidad = p[4]
            plazo = p[5]
            estado = p[6].upper() if p[6] else ""
            self.tree.insert("", tk.END, values=(p[0], cliente_nombre, ruc, trabajo, cantidad, f"{plazo} días", estado))

    def seleccionar_pedido(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item['values']
            
            self.pedido_seleccionado_id = val[0]
            ruc_val = str(val[2])
            self.txt_ruc.delete(0, tk.END)
            self.txt_ruc.insert(0, ruc_val)
            self.actualizar_nombre_cliente_por_ruc()

            self.combo_trabajo.set(str(val[3]).upper())
            
            self.txt_cantidad.delete(0, tk.END)
            self.txt_cantidad.insert(0, str(val[4]))

            plazo_str = str(val[5]).replace(" días", "").strip()
            self.txt_plazo_dias.delete(0, tk.END)
            self.txt_plazo_dias.insert(0, plazo_str)
            
            self.combo_estado.set(str(val[6]).upper())

    def limpiar_campos(self):
        self.pedido_seleccionado_id = None
        self.txt_ruc.delete(0, tk.END)
        self.lbl_cliente_nombre.config(text="[Ingrese RUC]", fg="gray", font=("Arial", 9, "italic"))
        self.combo_trabajo.set("")
        self.txt_cantidad.delete(0, tk.END)
        self.txt_cantidad.insert(0, "1")
        self.txt_plazo_dias.delete(0, tk.END)
        self.txt_plazo_dias.insert(0, "15")
        self.combo_estado.set("PENDIENTE")
        self.txt_buscar_pedido.delete(0, tk.END)
        self.cargar_pedidos()

    def guardar_pedido(self):
        ruc = self.txt_ruc.get().strip().upper()
        trab = self.combo_trabajo.get().strip().upper()
        cant = self.txt_cantidad.get().strip()
        plazo = self.txt_plazo_dias.get().strip()

        if not ruc:
            messagebox.showwarning("Atención", "Debe ingresar el RUC o Cédula del cliente.")
            return

        clientes = database.obtener_todos_los_clientes()
        cli_encontrado = None
        for c in clientes:
            if c[2] and ruc == c[2].strip().upper():
                cli_encontrado = c[1].upper()
                break

        if not cli_encontrado:
            messagebox.showerror("Error", "El RUC o Cédula ingresado no está registrado en el sistema. Debe registrar al cliente primero en 'Gestión de Clientes'.")
            return

        if not trab or not cant or not plazo:
            messagebox.showwarning("Atención", "Complete el trabajo, la cantidad y el plazo de entrega.")
            return

        try:
            cant_int = int(cant)
            plazo_int = int(plazo)
        except ValueError:
            messagebox.showwarning("Atención", "La cantidad y el plazo de entrega deben ser números enteros.")
            return

        exito, msg = database.registrar_pedido(cli_encontrado, ruc, trab, cant_int, plazo_int)
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
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista para modificarlo.")
            return

        trab = self.combo_trabajo.get().strip().upper()
        cant = self.txt_cantidad.get().strip()
        plazo = self.txt_plazo_dias.get().strip()
        estado = self.combo_estado.get().strip().upper()

        if not trab or not cant or not plazo:
            messagebox.showwarning("Atención", "Todos los campos del pedido son obligatorios.")
            return

        try:
            cant_int = int(cant)
            plazo_int = int(plazo)
        except ValueError:
            messagebox.showwarning("Atención", "La cantidad y el plazo deben ser números enteros.")
            return

        exito, msg = database.actualizar_pedido(self.pedido_seleccionado_id, trab, cant_int, plazo_int, estado)
        if exito:
            database.registrar_nuevo_mueble(trab)
            messagebox.showinfo("Éxito", "Pedido actualizado con éxito.")
            self.limpiar_campos()
            self.cargar_pedidos()
            self.cargar_opciones_combos()
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
            exito, msg = database.eliminar_pedido(self.pedido_seleccionado_id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_campos()
                self.cargar_pedidos()
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
        
        lbl_titulo = tk.Label(
            header, 
            text="👥 Módulo de Gestión de Clientes", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#2C3E50"
        )
        lbl_titulo.pack(pady=12)

        frame_form = tk.LabelFrame(self, text=" Datos del Cliente ", font=("Arial", 9, "bold"), padx=12, pady=8)
        frame_form.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_form, text="Nombre / Razón Social:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_nombre = tk.Entry(frame_form, width=28)
        self.txt_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.txt_nombre.focus()

        tk.Label(frame_form, text="RUC / Cédula (máx 10):").grid(row=0, column=2, sticky="e", pady=5)
        self.txt_ruc = tk.Entry(frame_form, width=22)
        self.txt_ruc.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Teléfono (máx 10 nros):").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_tel = tk.Entry(frame_form, width=28)
        self.txt_tel.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Dirección:").grid(row=1, column=2, sticky="e", pady=5)
        self.txt_dir = tk.Entry(frame_form, width=22)
        self.txt_dir.grid(row=1, column=3, padx=5, pady=5)

        btn_form_frame = tk.Frame(frame_form)
        btn_form_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_form_frame, 
            text="➕ Registrar Cliente", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.registrar_nuevo_cliente
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="✏️ Guardar Cambios", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.guardar_edicion_cliente
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="🗑️ Eliminar", 
            bg="#D35400", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.eliminar_cliente
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_form_frame, 
            text="🧹 Limpiar Campos", 
            bg="#7F8C8D", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=5)

        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(frame_busqueda, text="🔍 Buscar (Nombre o RUC):", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.txt_buscar = tk.Entry(frame_busqueda, width=35, font=("Arial", 10))
        self.txt_buscar.pack(side=tk.LEFT, padx=5)
        self.txt_buscar.bind("<KeyRelease>", self.filtrar_clientes)

        frame_tabla = tk.LabelFrame(self, text=" Listado de Clientes en Sistema ", font=("Arial", 9, "bold"), padx=10, pady=8)
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

        tk.Button(
            self, 
            text="❌ Salir", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            width=14,
            command=self.destroy
        ).pack(pady=10)

    def validar_datos(self, nombre, ruc, tel):
        if not nombre:
            messagebox.showwarning("Atención", "El nombre o razón social es obligatorio.")
            return False

        if ruc:
            if len(ruc) > 10:
                messagebox.showwarning("Atención", "El RUC / Cédula no puede tener más de 10 caracteres.")
                return False
            if not all(c.isdigit() or c == '-' for c in ruc):
                messagebox.showwarning("Atención", "El RUC / Cédula solo debe contener números y opcionalmente un guión (-).")
                return False

        if tel:
            if not tel.isdigit() or len(tel) > 10:
                messagebox.showwarning("Atención", "El teléfono debe contener únicamente números y un máximo de 10 dígitos.")
                return False

        return True

    def registrar_nuevo_cliente(self):
        nombre = self.txt_nombre.get().strip().upper()
        ruc = self.txt_ruc.get().strip()
        tel = self.txt_tel.get().strip()
        dir_cli = self.txt_dir.get().strip().upper()

        if not self.validar_datos(nombre, ruc, tel):
            return

        exito, msg = database.registrar_cliente(ruc if ruc else "S/D", nombre, tel, dir_cli)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", msg)

    def guardar_edicion_cliente(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un cliente de la lista para modificar.")
            return

        nombre = self.txt_nombre.get().strip().upper()
        ruc = self.txt_ruc.get().strip()
        tel = self.txt_tel.get().strip()
        dir_cli = self.txt_dir.get().strip().upper()

        if not self.validar_datos(nombre, ruc, tel):
            return

        exito, msg = database.actualizar_cliente_por_id(self.cliente_seleccionado_id, ruc, nombre, tel, dir_cli)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_cliente(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un cliente de la lista para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este cliente del sistema?")
        if confirmar:
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
            item = self.tree.item(selected[0])
            val = item['values']
            
            self.cliente_seleccionado_id = val[0]
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, str(val[1]).upper())
            
            self.txt_ruc.delete(0, tk.END)
            self.txt_ruc.insert(0, str(val[2]))
            
            self.txt_tel.delete(0, tk.END)
            self.txt_tel.insert(0, str(val[3]))
            
            self.txt_dir.delete(0, tk.END)
            self.txt_dir.insert(0, str(val[4]).upper())

    def limpiar_campos(self):
        self.cliente_seleccionado_id = None
        self.txt_nombre.delete(0, tk.END)
        self.txt_ruc.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.txt_dir.delete(0, tk.END)
        self.txt_nombre.focus()

    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        clientes = database.obtener_todos_los_clientes()
        for c in clientes:
            self.tree.insert("", tk.END, values=(c[0], c[1].upper(), c[2], c[3], c[4].upper()))

    def filtrar_clientes(self, event=None):
        termino = self.txt_buscar.get().strip().upper()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        clientes = database.buscar_clientes(termino)
        for c in clientes:
            self.tree.insert("", tk.END, values=(c[0], c[1].upper(), c[2], c[3], c[4].upper()))