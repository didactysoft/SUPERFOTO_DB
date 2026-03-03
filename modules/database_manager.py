import sqlite3
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "superfotoDB.db")

def obtener_conexion():
    """Establece conexión con la base de datos SQLite y confirma el éxito."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;") 
        # print(f"Conexión exitosa a: {os.path.basename(DB_PATH)}") # Descomentar si deseas ver el log
        return conn
    except sqlite3.Error as e:
        print(f"Error de conexión: {e}")
        return None

def validar_credenciales(usuario, clave):
    """Valida el usuario reutilizando la función ejecutar_consulta."""
    query = "SELECT 1 FROM usuario WHERE usuario = ? AND contraseña = ?"
    # Si la lista tiene resultados es True, si está vacía [] es False
    return bool(ejecutar_consulta(query, (usuario, clave)))

def ejecutar_consulta(query, params=()):
    """Ejecuta un SELECT y retorna los resultados."""
    conn = obtener_conexion()
    if not conn: return []
    
    try:
        # conn.execute crea el cursor automáticamente
        return conn.execute(query, params).fetchall()
    except sqlite3.Error as e:
        print(f"Error en consulta: {e}")
        return []
    finally:
        conn.close()

def ejecutar_accion(query, params=()):
    """Ejecuta un INSERT, UPDATE o DELETE (con auto-commit)."""
    conn = obtener_conexion()
    if not conn: return False
    
    try:
        # El bloque 'with conn:' hace commit automáticamente si todo sale bien, 
        # o hace rollback si ocurre un error.
        with conn:
            conn.execute(query, params)
        return True
    except sqlite3.Error as e:
        print(f"Error en acción: {e}")
        return False
    finally:
        conn.close()