import sqlite3

# Datos a registrar
USUARIOS_VALIDOS = {
    "12345678": "admin123",
    "98765432": "pass456",
    "11111111": "luiscarlitos"
}

try:
    # Conexión a la base de datos creada previamente
    conn = sqlite3.connect('superfoto.db')
    cursor = conn.cursor()

    # 1. Opcional: Crear un rol por defecto para estos usuarios si no existen
    cursor.execute("INSERT OR IGNORE INTO rol (id_rol, nombre, descripcion) VALUES (1, 'Administrador', 'Acceso total')")

    # 2. Insertar los usuarios
    for nombre, clave in USUARIOS_VALIDOS.items():
        # Usamos INSERT OR REPLACE por si vuelves a correr el script
        cursor.execute('''
            INSERT OR REPLACE INTO usuario (nombre_usuario, contraseña, id_rol) 
            VALUES (?, ?, ?)
        ''', (nombre, clave, 1))

    conn.commit()
    print("EXITO: Usuarios registrados correctamente.")

    # 3. Verificación: Mostrar lo que se guardó
    cursor.execute("SELECT * FROM usuario")
    print("\nListado de usuarios en la DB:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Usuario: {row[1]} | Rol: {row[3]}")

except sqlite3.Error as e:
    print(f"ERROR DE SQLITE: {e}")
finally:
    if conn:
        conn.close()