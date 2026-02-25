import sys, os
from modules.database_manager import obtener_conexion, ejecutar_accion

# Configuración de rutas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

def agregar_columna_usuario():
    print("--- Iniciando actualización de base de datos ---")
    
    # Intentamos agregar la columna
    # VARCHAR(50) para el nombre/alias del usuario
    query = "ALTER TABLE usuario ADD COLUMN usuario VARCHAR(50);"
    
    try:
        # Usamos ejecutar_accion que ya definimos en tu gestor
        exito = ejecutar_accion(query)
        
        if exito:
            print("✅ Columna 'usuario' agregada con éxito.")
            # Opcional: Llenar un dato de prueba
            ejecutar_accion("UPDATE usuario SET usuario = 'Administrador' WHERE nombre_usuario = '12345678'")
            print("📝 Dato de prueba actualizado para el admin.")
        else:
            print("⚠️ No se pudo agregar la columna. Es probable que ya exista.")
            
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")

if __name__ == "__main__":
    agregar_columna_usuario()