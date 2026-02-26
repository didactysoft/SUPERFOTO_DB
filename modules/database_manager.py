import sqlite3
import os

# Configuración de rutas relativas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "superfotoDB.db")

def obtener_conexion():
    """Establece conexión con la base de datos SQLite."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        # Activamos las llaves foráneas para mantener la integridad de tu script SQL
        conn.execute("PRAGMA foreign_keys = ON;") 
        return conn
    except sqlite3.Error as e:
        print(f"Error de conexión: {e}")
        return None

def validar_credenciales(usuario, clave):
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            # IMPORTANTE: Coincide con tu SQL (nombre_usuario y contraseña)
            query = "SELECT usuario FROM usuario WHERE usuario = ? AND contraseña = ?"
            cursor.execute(query, (usuario, clave))
            resultado = cursor.fetchone()
            return resultado is not None
        finally:
            conn.close()
    return False

def ejecutar_consulta(query, params=()):
    conn = obtener_conexion() # Cambiado de get_connection a obtener_conexion
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    return []

def ejecutar_accion(query, params=()):
    conn = obtener_conexion() # Cambiado de get_connection a obtener_conexion
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        finally:
            conn.close()
    return False