from PIL import Image
import os

def test_image_loading():
    # RUTA CORRECTA
    image_path = "C:/Users/GATOTEC18/Documents/Sublimacion/SUPERFOTO_DB/logo.png"

    print(f"--- Prueba de carga de imagen ---")
    print(f"Ruta que se intentará abrir: {image_path}")
    
    if not os.path.exists(image_path):
        # ... (código para FileNotFoundError)
        return

    print("\n✅ Paso 1: El archivo fue encontrado en la ruta.")

    try:
        img = Image.open(image_path)
        img.load()  # <-- ESTA ES LA CLAVE: Forzar la carga de la imagen en memoria
        
        print("✅ Paso 2: La librería Pillow pudo abrir y cargar el archivo completamente.")
        print(f"   - Formato detectado: {img.format}")
        print(f"   - Tamaño de la imagen: {img.size}")
        
        # Opcional: Intenta guardarla de nuevo
        temp_path = os.path.join(os.path.dirname(image_path), "logo_test_ok.png")
        img.save(temp_path)
        print(f"✅ Paso 3: Se pudo guardar una copia del logo en: {temp_path}")
        print("\n🎉 ÉXITO: La imagen está lista para usarse en CustomTkinter.")

    except Exception as e:
        print(f"\n❌ FALLO: Error al cargar o procesar el archivo: {e}")

if __name__ == "__main__":
    test_image_loading()