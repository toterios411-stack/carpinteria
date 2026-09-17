import tkinter as tk  # Librería para la interfaz gráfica (GUI)
from tkinter import messagebox  # Módulo para cuadros emergentes
import database  # Importa las funciones de la base de datos
from menu_principal import abrir_menu_principal  # Importa la ventana del Menú Principal

def intentar_login():
    usuario = entry_usuario.get()  # Lee el texto ingresado en el campo Usuario
    clave = entry_clave.get()  # Lee el texto ingresado en el campo Contraseña
    
    if database.validar_login(usuario, clave):  # Consulta las credenciales en la BD
        messagebox.showinfo("Éxito", "¡Inicio de sesión correcto!")  # Muestra mensaje de éxito
        abrir_menu_principal(usuario, root_login)  # Abre el Menú Principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")  # Muestra mensaje de error

def ventana_nuevo_usuario():
    win_nuevo = tk.Toplevel(root_login)  # Crea una ventana secundaria emergente
    win_nuevo.title("Nuevo Usuario")  # Título de la ventana emergente
    win_nuevo.geometry("300x220")  # Dimensiones de la ventana
    
    tk.Label(win_nuevo, text="Crear Nueva Cuenta", font=("Arial", 11, "bold")).pack(pady=10)  # Encabezado
    
    tk.Label(win_nuevo, text="Nuevo Usuario:").pack()  # Etiqueta Usuario
    entry_new_user = tk.Entry(win_nuevo)  # Campo para escribir nuevo usuario
    entry_new_user.pack(pady=2)  # Posiciona la entrada
    
    tk.Label(win_nuevo, text="Contraseña:").pack()  # Etiqueta Contraseña
    entry_new_pass = tk.Entry(win_nuevo, show="*")  # Campo para contraseña (oculta)
    entry_new_pass.pack(pady=2)  # Posiciona la entrada
    
    def guardar():
        u, p = entry_new_user.get(), entry_new_pass.get()  # Lee los datos ingresados
        if u and p:  # Verifica que los campos no estén vacíos
            exito, msg = database.registrar_usuario(u, p)  # Registra el usuario en la BD
            if exito:
                messagebox.showinfo("Éxito", msg, parent=win_nuevo)  # Alerta éxito
                win_nuevo.destroy()  # Cierra la ventana emergente
            else:
                messagebox.showerror("Error", msg, parent=win_nuevo)  # Alerta error
        else:
            messagebox.showwarning("Advertencia", "Complete todos los campos", parent=win_nuevo)  # Alerta incompleto
            
    tk.Button(win_nuevo, text="Guardar Usuario", command=guardar, bg="#3498db", fg="white").pack(pady=15)  # Botón guardar

def iniciar_interfaz():
    global root_login, entry_usuario, entry_clave  # Variables globales
    database.inicializar_bd()  # Inicializa la BD y crea las tablas si no existen
    
    root_login = tk.Tk()  # Crea la ventana principal de Login
    root_login.title("Acceso al Sistema")  # Título de la ventana
    root_login.geometry("320x280")  # Tamaño de la ventana
    
    tk.Label(root_login, text="Inicio de Sesión", font=("Arial", 12, "bold")).pack(pady=10)  # Título
    
    tk.Label(root_login, text="Usuario:").pack()  # Etiqueta Usuario
    entry_usuario = tk.Entry(root_login)  # Campo de texto para Usuario
    entry_usuario.pack(pady=2)  # Posiciona campo
    
    tk.Label(root_login, text="Contraseña:").pack()  # Etiqueta Contraseña
    entry_clave = tk.Entry(root_login, show="*")  # Campo de texto para Contraseña
    entry_clave.pack(pady=2)  # Posiciona campo
    
    tk.Button(root_login, text="Ingresar", command=intentar_login, bg="#2ecc71", fg="white", width=15).pack(pady=10)  # Botón Ingresar
    tk.Button(root_login, text="Crear Nuevo Usuario", command=ventana_nuevo_usuario, bg="#3498db", fg="white", width=18).pack()  # Botón Registrar
    
    root_login.mainloop()  # Mantiene la ventana activa alineado dentro de iniciar_interfaz()