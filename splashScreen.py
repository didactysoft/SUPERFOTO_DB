import customtkinter as ctk
from PIL import Image
import sys
import os
import runpy 

# --- FUNCIÓN CRÍTICA PARA RUTAS EN EL EXE ---
def obtener_ruta_recurso(ruta_relativa):
    """ Obtiene la ruta absoluta para recursos, compatible con PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de ventana
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        # 2. Tamaño y centrado
        width, height = 500, 300
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(fg_color="white")

        # 3. Contenido visual
        try:
            ruta_logo = obtener_ruta_recurso(os.path.join("assets", "logosfdb.png"))
            img_pil = Image.open(ruta_logo)
            self.img_ctk = ctk.CTkImage(img_pil, size=(300, 100))
            self.logo_label = ctk.CTkLabel(self, image=self.img_ctk, text="")
            self.logo_label.pack(expand=True, pady=(40, 0))
        except Exception:
            self.logo_label = ctk.CTkLabel(self, text="SUPERFOTO DB", font=("Arial", 30, "bold"), text_color="#CC0000")
            self.logo_label.pack(expand=True)

        self.loading_label = ctk.CTkLabel(self, text="Iniciando sistema...", font=("Arial", 12), text_color="gray")
        self.loading_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=400, height=10, progress_color="#629f36")
        self.progress.set(0)
        self.progress.pack(pady=(0, 40))

        self._after_id = None # Para rastrear el temporizador
        self.update_progress(0)

    def update_progress(self, val):
        if val <= 1:
            self.progress.set(val)
            # Guardamos el ID del proceso para poder cancelarlo al terminar
            self._after_id = self.after(30, lambda: self.update_progress(val + 0.05))
        else:
            # 1. Cancelamos cualquier actualización pendiente
            if self._after_id:
                self.after_cancel(self._after_id)
            # 2. Detenemos el loop de Tkinter de forma segura
            self.quit()
            # 3. Cerramos la ventana
            self.destroy() 

if __name__ == "__main__":
    app = SplashScreen()
    app.mainloop() 
    
    # --- LANZAMIENTO DEL LOGIN (CON RUNPY) ---
    
    archivo_login = obtener_ruta_recurso("login.py")
    
    if os.path.exists(archivo_login):
        try:
            # Al usar runpy, el entorno de sys.path ya tiene 'modules'
            # porque lo añadimos en el .spec o en los otros archivos.
            runpy.run_path(archivo_login, run_name='__main__')
        except Exception as e:
            print(f"Error al ejecutar el Login: {e}")
            if not getattr(sys, 'frozen', False):
                input("Presiona Enter para salir...")
    else:
        print(f"Error fatal: No se encontró {archivo_login}")
        input("Presiona Enter para salir...")
    
    # Cerramos el proceso principal definitivamente
    sys.exit()