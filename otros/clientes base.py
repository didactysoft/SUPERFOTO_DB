import sys
import os

# Asegura que Python encuentre la carpeta 'modules'
# os.path.dirname(os.path.abspath(__file__)) obtiene la ruta del script actual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Se importa la función ejecutar_accion desde el módulo database_manager
from modules.database_manager import ejecutar_accion

def insertar_clientes_ejemplo():
    # Datos basados en tu esquema SQL: documento, nombre, direccion, telefono, correo
    clientes = [
        ("1098765432", "Carlos Alberto Restrepo", "Calle 45 #12-34, Bucaramanga", "3105551234", "carlos.res@email.com"),
        ("1015432109", "Ana María Valencia", "Av. Santander #5-10, Pamplona", "3154449876", "ana.valencia@estudio.co"),
        ("900123456", "Variedades El Parque", "Carrera 8 #4-22, Cúcuta", "6075712233", "contacto@elparque.com"),
        ("1020304050", "Diego Fernando Ruiz", "Transversal 15 #30-45, Girón", "3208884567", "diego.ruiz@mail.net"),
        ("1050607080", "Lucía Fernanda Gómez", "Calle 10 #15-08, Floridablanca", "3112223344", "lucia.gomez@gmail.com")
    ]

    # Query SQL ajustado a los nombres de columna de tu tabla cliente
    query = """INSERT INTO cliente (documento, nombre, direccion, telefono, correo) 
               VALUES (?, ?, ?, ?, ?)"""

    print("--- Iniciando insercion de clientes ---")
    
    for cliente in clientes:
        # Se intenta ejecutar la inserción en la base de datos
        exito = ejecutar_accion(query, cliente)
        
        # Se reemplazan los emojis por texto para evitar errores de codificación en Windows
        if exito:
            print(f"EXITO - Cliente insertado: {cliente[1]}")
        else:
            print(f"ERROR - No se pudo insertar: {cliente[1]}")

if __name__ == "__main__":
    insertar_clientes_ejemplo()