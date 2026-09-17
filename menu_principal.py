import tkinter as tk  # Librería para la interfaz gráfica (GUI)

def abrir_menu_principal(usuario, ventana_login=None):
    if ventana_login:
        ventana_login.destroy()  # Cierra la ventana de Login al ingresar
        
    menu = tk.Tk()  # Crea la ventana del Menú Principal
    menu.title("Menú Principal")  # Título de la ventana
    menu.geometry("500x300")  # Tamaño compacto (Ancho x Alto)
    
    # --- Mensaje Único de Bienvenida ---
    tk.Label(
        menu, 
        text=f"¡Bienvenido/a, {usuario}!", 
        font=("Arial", 14, "bold"), 
        fg="#2c3e50"
    ).pack(expand=True)  # Centra el texto vertical y horizontalmente
    
    menu.mainloop()  # Mantiene activa la ventana del Menú Principal