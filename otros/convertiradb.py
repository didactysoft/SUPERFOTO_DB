import sqlite3

# Pega el contenido de arriba en un archivo llamado corregido.sql
with open('corregido.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

try:
    conn = sqlite3.connect('superfoto.db')
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    print("Base de datos creada exitosamente.")
except sqlite3.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()