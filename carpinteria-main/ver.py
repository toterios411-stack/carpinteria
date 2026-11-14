import database

def mostrar_lista_usuarios():
    """Consulta la base de datos e imprime en consola los usuarios registrados."""
    # Asegura que la BD exista
    database.inicializar_bd()
    
    usuarios = database.obtener_todos_los_usuarios()

    print("\n==========================================")
    print("        USUARIOS REGISTRADOS EN BD        ")
    print("==========================================")
    
    if not usuarios:
        print("No hay usuarios registrados.")
    else:
        for u in usuarios:
            # u[0] es 'usuario', u[1] es 'rol'
            print(f"• Usuario: {u[0]:<15} | Rol: {u[1]}")
            
    print("==========================================\n")

if __name__ == "__main__":
    mostrar_lista_usuarios()