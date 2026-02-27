import os
from modules.database_manager import ejecutar_accion

def llenar_datos_iniciales():
    print("--- INICIANDO CARGA DE DATOS PARA SUPERFOTO ---")

    # 1. INSERTAR CATEGORÍAS
    categorias = [
        ("Papelería", "Papel fotográfico y suministros de impresión"),
        ("Tintas", "Tintas GI-190, T544 y cartuchos varios"),
        ("Marcos", "Marcos de madera, aluminio y vidrio"),
        ("Cámaras", "Cámaras réflex, Mirrorless y accesorios ópticos"),
        ("Servicios", "Impresiones, restauraciones y sesiones")
    ]
    for cat in categorias:
        ejecutar_accion("INSERT INTO categoria (nombre, descripcion) VALUES (?,?)", cat)
    print("✓ Categorías cargadas.")

    # 2. INSERTAR PROVEEDORES
    # Formato: documento_nit, nombre, direccion, telefono, correo, web
    proveedores = [
        ("900123456-1", "Canon Colombia", "Calle 100 #15-20, Bogotá", "3001234567", "ventas@canon.co", "www.canon.co"),
        ("860456789-2", "Epson S.A.", "Av. El Dorado, Bogotá", "3109876543", "soporte@epson.com", "www.epson.com.co"),
        ("700888999-0", "Distribuidora Pamplona", "Carrera 5 #4-10, Pamplona", "3154445566", "distri.pamplona@gmail.com", "")
    ]
    for prov in proveedores:
        ejecutar_accion("INSERT INTO proveedor (documento_nit, nombre, direccion, telefono, correo, web) VALUES (?,?,?,?,?,?)", prov)
    print("✓ Proveedores cargados.")

    # 3. INSERTAR 10 PRODUCTOS
    # Formato: nombre, cantidad, precio, id_categoria, id_proveedor
    # Nota: Los IDs (1, 2, 3...) dependen del orden de inserción anterior
    productos = [
        ("Papel Foto 10x15 Brillo (100h)", 45, 38000, 1, 3),
        ("Tinta Canon GI-190 Black", 3, 42000, 2, 1),        # SALE EN ROJO (Stock bajo)
        ("Marco Madera 20x30 Premium", 15, 18500, 3, 3),
        ("Cámara Canon EOS R100", 2, 2800000, 4, 1),         # SALE EN ROJO (Stock bajo)
        ("Tinta Epson T544 Cyan", 12, 35000, 2, 2),
        ("Trípode Profesional Pro-Z", 6, 95000, 4, 3),
        ("Batería Canon LP-E17", 4, 150000, 4, 1),           # SALE EN ROJO (Stock bajo)
        ("Papel Plotter Mate 61cm", 8, 115000, 1, 2),
        ("Kit Limpieza Lentes", 20, 15000, 4, 3),
        ("Álbum Fotográfico 200 fotos", 10, 45000, 1, 3)
    ]
    for prod in productos:
        ejecutar_accion("INSERT INTO producto (nombre, cantidad, precio, id_categoria, id_proveedor) VALUES (?,?,?,?,?)", prod)
    print("✓ 10 Productos cargados.")

    print("\n[ÉXITO] Base de datos en 'database/superfotoDB.db' lista para usar.")

if __name__ == "__main__":
    llenar_datos_iniciales()