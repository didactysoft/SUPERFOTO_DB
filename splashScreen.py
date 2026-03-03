import customtkinter as ctk
from PIL import Image
import os

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, callback):
        super().__init__()
        
        # 1. Configuración de ventana sin bordes (Splash)
        self.overrideredirect(True)  # Elimina la barra de título y bordes
        self.attributes("-topmost", True) # Siempre al frente
        
        # 2. Tamaño y centrado
        width, height = 500, 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.configure(fg_color="white") # Fondo limpio

        # 3. Contenido visual
        # Logo (Asegúrate de que la ruta sea correcta)
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "assets", "logosfdb.png")
            img = ctk.CTkImage(Image.open(ruta_logo), size=(300, 100))
            self.logo_label = ctk.CTkLabel(self, image=img, text="")
            self.logo_label.pack(expand=True, pady=(40, 0))
        except:
            self.logo_label = ctk.CTkLabel(self, text="SUPERFOTO DB", font=("Arial", 30, "bold"), text_color="#CC0000")
            self.logo_label.pack(expand=True)

        # Texto de carga
        self.loading_label = ctk.CTkLabel(self, text="Iniciando sistema...", font=("Arial", 12), text_color="gray")
        self.loading_label.pack(pady=10)

        # Barra de progreso estética
        self.progress = ctk.CTkProgressBar(self, width=400, height=10, progress_color="#CC0000")
        self.progress.set(0)
        self.progress.pack(pady=(0, 40))

        # 4. Lógica de temporizador
        self.callback = callback
        self.update_progress(0)

    def update_progress(self, val):
        if val <= 1:
            self.progress.set(val)
            # Simular carga (puedes ajustar el tiempo aquí)
            self.after(30, lambda: self.update_progress(val + 0.02))
        else:
            self.destroy() # Cerramos el Splash
            self.callback() # Ejecutamos la función para abrir el Login

# --- INTEGRACIÓN CON TU LOGIN ---

def iniciar_aplicacion():
    # Aquí importas y lanzas tu clase LoginApp
    from main import LoginApp # Asumiendo que tu login está en main.py
    app = LoginApp()
    app.mainloop()

if __name__ == "__main__":
    # Necesitamos una ventana raíz invisible para que el Splash funcione correctamente
    root = ctk.CTk()
    root.withdraw() # Ocultamos la raíz principal
    
    splash = SplashScreen(iniciar_aplicacion)
    root.mainloop()