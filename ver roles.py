import os
import sys

# Ajuste de ruta para subir desde 'modules' a la raíz
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from modules.database_manager import ejecutar_consulta

def diagnostico_roles():
    print("\n🔍 --- INICIANDO DIAGNÓSTICO DE TABLA 'ROL' ---")
    
    # 1. Verificar si la tabla existe y ver sus columnas
    try:
        info_columnas = ejecutar_consulta("PRAGMA table_info(rol)")
        if not info_columnas:
            print("❌ ERROR: La tabla 'rol' no existe en la base de datos.")
            return
        
        print("✅ Estructura encontrada:")
        columnas = []
        for col in info_columnas:
            # col[1] es el nombre de la columna en SQLite
            print(f"   - Columna: {col[1]} ({col[2]})")
            columnas.append(col[1])
        
        # 2. Intentar leer los datos usando los nombres reales encontrados
        nombre_col = columnas[1] if len(columnas) > 1 else columnas[0]
        id_col = columnas[0]
        
        print(f"\nREADING: SELECT {id_col}, {nombre_col} FROM rol...")
        datos = ejecutar_consulta(f"SELECT {id_col}, {nombre_col} FROM rol")
        
        if datos:
            print("\n🎭 ROLES ENCONTRADOS:")
            print("-" * 25)
            for fila in datos:
                print(f"ID: {fila[0]} | Rol: {fila[1]}")
        else:
            print("\n⚠️ La tabla existe pero NO tiene datos insertados.")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    diagnostico_roles()