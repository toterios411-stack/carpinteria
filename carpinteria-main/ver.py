import database

# Obtiene y muestra los usuarios
usuarios = database.obtener_todos_los_usuarios()

print("\n--- USUARIOS REGISTRADOS ---")
for u in usuarios:
    print(f"ID: {u['id']} | Usuario: {u['usuario']}")
print("----------------------------\n")