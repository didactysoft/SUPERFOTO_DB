import sqlite3
import os
import sys

def obtener_ruta_db():
    """
    Determina la ruta de la base de datos.
    Para ADSO: La base de datos DEBE ser externa al EXE para que sea persistente.
    """
    # Detectar si el script está corriendo como un ejecutable (.exe)
    if getattr(sys, 'frozen', False):
        # Si es el EXE, la DB debe estar en la carpeta donde el usuario guardó el EXE
        base_dir = os.path.dirname(sys.executable)
    else:
        # Si es desarrollo (VS Code), subimos un nivel desde 'modules' a la raíz
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # IMPORTANTE: Asegúrate de que la carpeta se llame 'database' en tu proyecto
    ruta_final = os.path.join(base_dir, "database", "superfotoDB.db")
    return ruta_final

# Asignamos la ruta calculada al inicio
DB_PATH = obtener_ruta_db()

def obtener_conexion():
    """Establece conexión con SQLite y crea la carpeta si no existe."""
    try:
        # Crea la carpeta 'database' automáticamente si no existe en la PC de destino
        directorio_db = os.path.dirname(DB_PATH)
        if not os.path.exists(directorio_db):
            os.makedirs(directorio_db, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;") 
        # Configurar timeout para evitar errores de "database is locked" con procesos separados
        conn.execute("PRAGMA busy_timeout = 3000;") 
        return conn
    except sqlite3.Error as e:
        print(f"Error de conexión crítica: {e}")
        return None

def validar_credenciales(usuario, clave):
    """Valida el acceso del usuario."""
    query = "SELECT 1 FROM usuario WHERE usuario = ? AND contraseña = ?"
    resultado = ejecutar_consulta(query, (usuario, clave))
    return bool(resultado)

def ejecutar_consulta(query, params=()):
    """Ejecuta SELECT y maneja el cierre de conexión."""
    conn = obtener_conexion()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error en consulta SELECT: {e}")
        return []
    finally:
        conn.close()

def ejecutar_accion(query, params=()):
    """Ejecuta INSERT, UPDATE o DELETE."""
    conn = obtener_conexion()
    if not conn: return False
    try:
        with conn:
            conn.execute(query, params)
        return True
    except sqlite3.Error as e:
        print(f"Error en acción (I/U/D): {e}")
        return False
    finally:
        conn.close()