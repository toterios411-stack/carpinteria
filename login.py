import sys
import tkinter as tk
from tkinter import messagebox, ttk
import database
from menu_principal import MenuPrincipal

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("SGC - Inicio de Sesión")
        self.root.geometry("380x280")
        self.root.resizable(False, False)

        # Inicialización de BD
        database.inicializar_bd()

        # Encabezado
        tk.Label(root, text="Sistema de Gestión de Carpintería", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        tk.Label(root, text="Acceso al Sistema", font=("Arial", 10)).pack(pady=(0, 10))

        # Formulario
        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.txt_usuario = tk.Entry(frame, width=22)
        self.txt_usuario.grid(row=0, column=1, padx=5, pady=5)
        self.txt_usuario.focus()
        # Atajo Enter en el campo usuario
        self.txt_usuario.bind('<Return>', lambda event: self.validar_ingreso())

        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.txt_clave = tk.Entry(frame, show="*", width=22)
        self.txt_clave.grid(row=1, column=1, padx=5, pady=5)
        # Atajo Enter en el campo contraseña
        self.txt_clave.bind('<Return>', lambda event: self.validar_ingreso())

        # Botones (Solo Ingresar y Salir)
        btn_frame1 = tk.Frame(root)
        btn_frame1.pack(pady=10)

        tk.Button(
            btn_frame1, 
            text="Ingresar", 
            bg="#27AE60", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=26,
            command=self.validar_ingreso
        ).pack()

        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=5)

        tk.Button(
            btn_frame2, 
            text="❌ Salir del Sistema", 
            bg="#C0392B", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=26,
            command=self.salir_del_sistema
        ).pack()

        self.root.protocol("WM_DELETE_WINDOW", self.salir_del_sistema)

    def validar_ingreso(self):
        usuario = self.txt_usuario.get().strip()
        clave = self.txt_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor complete todos los campos.")
            return

        res = database.validar_login_con_rol(usuario, clave)
        
        if res and res[0]:
            rol = res[1]
            messagebox.showinfo("Bienvenido", f"¡Acceso Correcto!\nUsuario: {usuario}\nRol: {rol}")
            
            # Limpiar entradas
            self.txt_usuario.delete(0, tk.END)
            self.txt_clave.delete(0, tk.END)
            
            # Ocultar login y abrir Menú Principal de forma directa
            self.root.withdraw()
            MenuPrincipal(self.root, rol_usuario=rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def salir_del_sistema(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar el sistema?"):
            self.root.destroy()
            sys.exit(0)


def iniciar_app():
    root = tk.Tk()
    app = VentanaLogin(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()