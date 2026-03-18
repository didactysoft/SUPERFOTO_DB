import customtkinter as ctk
from PIL import Image
import sys, os, runpy
import tkinter.messagebox as msg # Para ver el error real
from modules.database_manager import validar_credenciales

def obtener_ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

# Configurar rutas de módulos
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = sys._MEIPASS
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if os.path.join(PROJECT_ROOT, "modules") not in sys.path:
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "modules"))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#CC0000")
        self.login_exitoso = False # Flag para saber si abrimos el MainApp

        # --- Interfaz (Resumida para brevedad, mantén tu diseño) ---
        self.frame = ctk.CTkFrame(self, width=420, height=580, corner_radius=20, fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.cedula = ctk.CTkEntry(self.frame, placeholder_text="Cédula", width=280, border_color="#CC0000", text_color="black", fg_color="white")
        self.cedula.pack(pady=(120, 10))
        
        self.clave = ctk.CTkEntry(self.frame, placeholder_text="Contraseña", show="*", width=280, border_color="#CC0000", text_color="black", fg_color="white")
        self.clave.pack(pady=(0, 30))

        self.btn = ctk.CTkButton(self.frame, text="Iniciar Sesión", command=self.login_action, fg_color="#CC0000")
        self.btn.pack()
        
        self.error_label = ctk.CTkLabel(self.frame, text="", text_color="#CC0000")
        self.error_label.pack(pady=5)
        self.bind("<Return>", lambda e: self.login_action())

    def login_action(self):
        usr, pwd = self.cedula.get(), self.clave.get()
        if validar_credenciales(usr, pwd):
            os.environ["CURRENT_USER"] = str(usr)
            self.login_exitoso = True # Activamos el permiso para abrir mainapp
            self.quit() # Detiene el mainloop
        else:
            self.error_label.configure(text="❌ Cédula o contraseña incorrecta")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
    
    # --- MOMENTO CRÍTICO: LANZAMIENTO FUERA DEL LOOP ---
    if app.login_exitoso:
        try:
            app.destroy() # Cerramos la ventana completamente
            ruta_main = obtener_ruta_recurso("mainapp.py")
            
            if os.path.exists(ruta_main):
                # Intentamos ejecutar el menú principal
                runpy.run_path(ruta_main, run_name='__main__')
            else:
                msg.showerror("Error de Archivo", f"No se encontró:\n{ruta_main}")
                
        except Exception as e:
            # SI MAINAPP TIENE UN ERROR, ESTO TE DIRÁ CUÁL ES
            import traceback
            error_detallado = traceback.format_exc()
            msg.showerror("Error en MainApp", f"El sistema falló al iniciar:\n\n{error_detallado}")