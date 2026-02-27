import os
import sys

# 1. Configuración de rutas para acceder a database_manager
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from modules.database_manager import ejecutar_consulta

def rellenar_roles_manual():
    print("🚀 Insertando información detallada en la tabla 'rol'...")
    
    # 2. Definimos los datos con los 3 campos: (id_rol, nombre, descripcion)
    roles = [
        (2, "Superadministrador", "Acceso total al sistema, configuración y gestión de usuarios."),
        (3, "Empleado", "Acceso limitado a ventas, registro de clientes y pedidos.")
    ]
    
    try:
        # 3. Consulta que incluye el id_rol manualmente
        # Usamos INSERT OR REPLACE para que si el ID ya existe, se actualice la información
        query = "INSERT OR REPLACE INTO rol (id_rol, nombre, descripcion) VALUES (?, ?, ?)"
        
        for r in roles:
            # r es la tupla completa: (1, "Nombre", "Desc...")
            ejecutar_consulta(query, r)
            print(f"✅ Rol ID {r[0]} ({r[1]}) guardado correctamente.")
            
        print("\n✨ Carga de roles finalizada con éxito.")
        
        # 4. Verificación en consola
        print("\n📋 REGISTROS EN LA BASE DE DATOS:")
        print(f"{'ID':<5} | {'NOMBRE':<20} | {'DESCRIPCIÓN'}")
        print("-" * 70)
        
        resultado = ejecutar_consulta("SELECT * FROM rol")
        if resultado:
            for id_r, nom, desc in resultado:
                print(f"{id_r:<5} | {nom:<20} | {desc}")
        else:
            print("La tabla sigue vacía. Revisa la conexión en database_manager.py")

    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    rellenar_roles_manual()