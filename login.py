import customtkinter as ctk
from PIL import Image
import sys, os, runpy
import tkinter.messagebox as msg
import traceback
from modules.database_manager import validar_credenciales

# --- CONFIGURACIÓN DE RUTAS ---
def obtener_ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS  # Carpeta temporal del EXE
    except Exception:
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, ruta_relativa)

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = sys._MEIPASS
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if os.path.join(PROJECT_ROOT, "modules") not in sys.path:
    sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#CC0000")
        
        self.autorizado = False

        # --- FRAME PRINCIPAL ---
        frame = ctk.CTkFrame(self, width=420, height=580, corner_radius=20, fg_color="white")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.grid_propagate(False)

        # Logos y Encabezado
        ctk.CTkLabel(frame, text=" ", height=1, width=400).pack(pady=(15, 10))
        self.load_logo(frame, "logosfdb.png", (300, 80))
        ctk.CTkLabel(frame, text="Administración para estudios fotográficos", font=("Arial", 11), text_color="gray").pack(pady=(0, 10))
        ctk.CTkFrame(frame, height=1, fg_color="gray70", corner_radius=0).pack(fill="x", padx=40, pady=(5, 15))
        
        self.load_logo(frame, "logo0.png", (230, 70))
        ctk.CTkLabel(frame, text="Accede a tu cuenta", font=("Arial", 18, "bold"), text_color="black").pack(pady=(0, 15))

        # --- FORMULARIO ---
        e_kw = dict(width=280, height=45, corner_radius=20, border_color="#CC0000", border_width=2, text_color="black", fg_color="white")
        
        self.usuario = ctk.CTkEntry(frame, placeholder_text="Usuario", **e_kw)
        self.usuario.pack(pady=(10, 10))
        
        self.clave = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", **e_kw)
        self.clave.pack(pady=(0, 30))

        # Botón
        ctk.CTkButton(frame, text="Iniciar Sesión", command=self.login_action, 
                      width=200, height=50, corner_radius=25, fg_color="#CC0000", 
                      hover_color="#A30000", text_color="white", font=("Arial", 16, "bold")).pack(pady=(0, 5))
        
        ctk.CTkLabel(frame, text="DIDACTYSOFT", font=("Arial", 10), text_color="gray").pack(pady=(10, 5))
        
        self.error_label = ctk.CTkLabel(frame, text="", text_color="#CC0000", font=("Arial", 12))
        self.error_label.pack(pady=5)

        self.bind("<Return>", lambda e: self.login_action())

    def login_action(self):
        usr, pwd = self.usuario.get(), self.clave.get()

        if not usr or not pwd:
            return self.error_label.configure(text="⚠️ Por favor complete todos los campos")

        if validar_credenciales(usr, pwd):
            # Guardamos el usuario para MainApp
            os.environ["CURRENT_USER"] = str(usr) 
            self.autorizado = True
            
            # --- CIERRE SEGURO ---
            # Ocultamos la ventana primero para que las animaciones de CTK terminen
            self.withdraw()
            self.after(200, self.quit) 
        else:
            self.error_label.configure(text="❌ Usuario o contraseña incorrecta")
            self.clave.delete(0, "end")

    def load_logo(self, parent, filename, size):
        try:
            ruta = obtener_ruta_recurso(os.path.join("assets", filename))
            img = ctk.CTkImage(Image.open(ruta), size=size)
            ctk.CTkLabel(parent, image=img, text="").pack(pady=5)
        except Exception:
            ctk.CTkLabel(parent, text=filename, text_color="black").pack()

# --- LANZAMIENTO SEGURO ---
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
    
    # Si salió del mainloop porque se validó correctamente
    if app.autorizado:
        try:
            app.destroy() # Destrucción final de la ventana de login
            
            ruta_main = obtener_ruta_recurso("mainapp.py")
            if os.path.exists(ruta_main):
                # Lanzamos MainApp en el mismo proceso del EXE
                runpy.run_path(ruta_main, run_name='__main__')
            else:
                msg.showerror("Error", f"No se encontró el archivo:\n{ruta_main}")
        except Exception:
            # Si mainapp.py tiene un error, esto te lo mostrará en pantalla
            msg.showerror("Error crítico en Menú", traceback.format_exc())
    
    sys.exit()