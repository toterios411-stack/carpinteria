import tkinter as tk
from tkinter import messagebox
import database
from menu_principal import abrir_menu_principal

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Carpintería - Login")
        self.geometry = self.root.geometry("350x280")
        self.root.resizable(False, False)

        # Título
        tk.Label(root, text="Inicio de Sesión", font=("Arial", 14, "bold")).pack(pady=15)

        # Formulario
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_usuario = tk.Entry(frame)
        self.txt_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_clave = tk.Entry(frame, show="*")
        self.txt_clave.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Ingresar", bg="#27AE60", fg="white", font=("Arial", 10, "bold"), command=self.validar_ingreso).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Registrarse", bg="#2980B9", fg="white", font=("Arial", 10, "bold"), command=self.abrir_registro).pack(side=tk.LEFT, padx=5)

    def validar_ingreso(self):
        usuario = self.txt_usuario.get().strip()
        clave = self.txt_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor complete todos los campos.")
            return

        if database.validar_login(usuario, clave):
            messagebox.showinfo("Bienvenido", f"¡Acceso correcto! Bienvenido {usuario}.")
            
            # Limpia los campos
            self.txt_usuario.delete(0, tk.END)
            self.txt_clave.delete(0, tk.END)
            
            self.root.withdraw()  # Oculta la ventana de Login
            
            # Abre el Menú Principal
            abrir_menu_principal(self.root)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        VentanaRegistro(self.root)


class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de Usuario")
        self.geometry("300x220")

        tk.Label(self, text="Registrar Usuario", font=("Arial", 12, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5)
        self.txt_nuevo_user = tk.Entry(form)
        self.txt_nuevo_user.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_nueva_clave = tk.Entry(form, show="*")
        self.txt_nueva_clave.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Guardar", bg="#27AE60", fg="white", command=self.guardar_usuario).pack(pady=10)

    def guardar_usuario(self):
        user = self.txt_nuevo_user.get().strip()
        clave = self.txt_nueva_clave.get().strip()

        if not user or not clave:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        exito, msg = database.registrar_usuario(user, clave)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)


def iniciar_app():
    root = tk.Tk()
    app = VentanaLogin(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()