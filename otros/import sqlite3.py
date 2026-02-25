import sqlite3
import os
from modules.database_manager import obtener_conexion

def actualizar_estructura_y_datos():
    conn = obtener_conexion()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # 1. Intentar agregar la columna 'usuario' si no existe
        try:
            cursor.execute("ALTER TABLE usuario ADD COLUMN usuario VARCHAR(50);")
            print("Columna 'usuario' creada.")
        except sqlite3.OperationalError:
            print("La columna 'usuario' ya existia, procediendo a actualizar datos.")

        # 2. Datos a insertar/actualizar
        # Formato: (Cédula/Usuario, Nuevo Nombre Usuario, Password)
        datos_nuevos = [
            ("12345678", "admin", "admin123"),
            ("98765432", "carlos villalba", "pass456"),
            ("11111111", "luis carlos villalba", "luiscarlitos")
        ]

        # 3. Aplicar los cambios
        for cedula, nombre, password in datos_nuevos:
            # Primero intentamos ver si el registro existe por su ID o nombre previo
            # Actualizamos: usuario = cedula, nombre_usuario = nombre, contraseña = password
            query = """
                UPDATE usuario 
                SET usuario = ?, nombre_usuario = ?, contraseña = ?
                WHERE nombre_usuario = ? OR usuario = ?
            """
            cursor.execute(query, (cedula, nombre, password, cedula, cedula))
            
            # Si no se actualizó nada (porque el registro es nuevo), lo insertamos
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO usuario (usuario, nombre_usuario, contraseña, id_rol)
                    VALUES (?, ?, ?, 1)
                """, (cedula, nombre, password))

        conn.commit()
        print("✅ Base de datos actualizada con éxito.")
        
        # Verificación rápida
        print("\nEstado actual de la tabla:")
        cursor.execute("SELECT usuario, nombre_usuario, contraseña FROM usuario")
        for fila in cursor.fetchall():
            print(f"Usuario(Cedula): {fila[0]} | Nombre: {fila[1]} | Pass: {fila[2]}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    actualizar_estructura_y_datos()