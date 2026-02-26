import sqlite3
import os

# 1. Obtener la ruta de la carpeta donde está este script (otros)
dir_actual = os.path.dirname(os.path.abspath(__file__))

# 2. Subir un nivel (a la raíz SUPERFOTO_DB) y buscar el SQL
# Si el SQL está en la raíz, usamos '..' para subir. 
# Si el SQL está en la misma carpeta 'otros', quita el os.path.join(..., '..', ...)
ruta_sql = os.path.abspath(os.path.join(dir_actual, '..', 'supefotoDB.sql'))
ruta_db = os.path.abspath(os.path.join(dir_actual, '..', 'database', 'superfoto.db'))

# Asegurar que la carpeta database existe
os.makedirs(os.path.dirname(ruta_db), exist_ok=True)

try:
    print(f"Buscando archivo en: {ruta_sql}")
    with open(ruta_sql, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    print("Ejecutando script SQL...")
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    print("¡Base de datos creada exitosamente en la carpeta database!")

except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo {ruta_sql}")
    print("Asegúrate de que el nombre del archivo sea exacto (supefotoDB.sql)")
except Exception as e:
    print(f"Ocurrió un error: {e}")