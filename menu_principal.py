import tkinter as tk
from tkinter import messagebox, ttk
import database

class MenuPrincipal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Referencia a la ventana de Login
        self.title("Sistema de Gestión para Carpintería (SGC)")
        self.geometry("800x500")
        self.resizable(False, False)

        # Encabezado
        header_frame = tk.Frame(self, bg="#4A2E10", height=60)
        header_frame.pack(fill=tk.X)
        
        lbl_titulo = tk.Label(header_frame, text="Panel Principal - Carpintería", font=("Arial", 16, "bold"), fg="white", bg="#4A2E10")
        lbl_titulo.pack(pady=15)

        # Panel de Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(expand=True)

        tk.Button(btn_frame, text="👥 Gestión de Clientes (RF04)", font=("Arial", 11), width=30, height=2, command=self.abrir_clientes).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="🪵 Inventario y Maderas (RF06)", font=("Arial", 11), width=30, height=2, command=self.modulo_en_construccion).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="📋 Ordenes y Presupuestos (RF10)", font=("Arial", 11), width=30, height=2, command=self.modulo_en_construccion).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="📊 Reportes y Comprobantes (RF15)", font=("Arial", 11), width=30, height=2, command=self.modulo_en_construccion).grid(row=1, column=1, padx=10, pady=10)

        # Botón Cerrar Sesión (vuelve al Login)
        tk.Button(self, text="Cerrar Sesión", font=("Arial", 10, "bold"), bg="#C0392B", fg="white", command=self.cerrar_sesion).pack(pady=20)

        # Si cierra la ventana desde la 'X', se vuelve a mostrar el login
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)

    def cerrar_sesion(self):
        """Cierra el Panel Principal y vuelve a desplegar el Login."""
        self.destroy()
        if self.parent:
            self.parent.deiconify()  # Muestra nuevamente la ventana de login

    def abrir_clientes(self):
        VentanaClientes(self)

    def modulo_en_construccion(self):
        messagebox.showinfo("Información", "Módulo programado según la planificación del proyecto.")


class VentanaClientes(tk.Toplevel):
    """Módulo para cumplimiento de RF04 y RF05."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("500x350")

        tk.Label(self, text="Registro de Clientes", font=("Arial", 14, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="RUC/Cédula:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_ruc = tk.Entry(form, width=25)
        self.txt_ruc.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Nombre/Razón Social:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_nombre = tk.Entry(form, width=25)
        self.txt_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Teléfono:").grid(row=2, column=0, sticky="e", pady=5)
        self.txt_tel = tk.Entry(form, width=25)
        self.txt_tel.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Guardar Cliente", bg="#27AE60", fg="white", font=("Arial", 10, "bold"), command=self.guardar_cliente).pack(pady=15)

    def guardar_cliente(self):
        ruc = self.txt_ruc.get().strip()
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()

        if not ruc or not nombre:
            messagebox.showwarning("Atención", "RUC/Cédula y Nombre son obligatorios.")
            return

        exito, msg = database.registrar_cliente(ruc, nombre, tel, "", "")
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)


def abrir_menu_principal(parent):
    """Función para ser llamada desde login.py."""
    return MenuPrincipal(parent)