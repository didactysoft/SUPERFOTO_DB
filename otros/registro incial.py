import sqlite3

# Diccionario de usuarios: "usuario_acceso": "contraseña"
USUARIOS_A_REGISTRAR = {
    "12345678": "admin123",
    "98765432": "pass456",
    "11111111": "luiscarlitos"
}

try:
    # 1. Conexión (Asegúrate de que la ruta al archivo .db sea la correcta)
    conn = sqlite3.connect('database/superfotoDB.db')
    cursor = conn.cursor()

    # 2. Insertar el ROL primero (Requisito por la llave foránea id_rol)
    # La tabla rol tiene: id_rol, nombre, descripcion
    cursor.execute("""
        INSERT OR IGNORE INTO rol (id_rol, nombre, descripcion) 
        VALUES (1, 'Administrador', 'Acceso total al sistema')
    """)

    # 3. Insertar los usuarios
    for login, password in USUARIOS_A_REGISTRAR.items():
        # Query basado en tu estructura: usuario, nombre_usuario, contraseña, id_rol
        query = """
            INSERT OR REPLACE INTO usuario (usuario, nombre_usuario, contraseña, id_rol) 
            VALUES (?, ?, ?, ?)
        """
        # Aquí usamos 'login' tanto para el usuario como para el nombre_usuario
        cursor.execute(query, (login, f"Usuario {login}", password, 1))

    conn.commit()
    print("¡Usuarios registrados con éxito!")

except sqlite3.Error as e:
    print(f"Error de base de datos: {e}")
finally:
    if conn:
        conn.close()