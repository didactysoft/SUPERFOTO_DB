import os
from modules.database_manager import obtener_conexion

def mostrar_tabla_usuarios():
    conn = obtener_conexion()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conn.cursor()
        
        # Consultamos los campos según tu nueva estructura
        # usuario (Cédula), nombre_usuario (Nombre Real), contraseña
        query = "SELECT usuario, nombre_usuario, contraseña, id_rol FROM usuario"
        cursor.execute(query)
        
        usuarios = cursor.fetchall()

        print("\n" + "="*70)
        print(f"{'CEDULA (usuario)':<20} | {'NOMBRE (nombre_usuario)':<25} | {'PASSWORD':<15}")
        print("-"*70)

        if not usuarios:
            print("La tabla está vacía.")
        else:
            for u in usuarios:
                # u[0] = usuario (cedula), u[1] = nombre_usuario (nombre), u[2] = clave
                print(f"{str(u[0]):<20} | {str(u[1]):<25} | {str(u[2]):<15}")
        
        print("="*70 + "\n")

    except Exception as e:
        print(f"Error al consultar la tabla: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    mostrar_tabla_usuarios()