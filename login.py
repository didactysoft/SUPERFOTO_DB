import customtkinter as ctk
from PIL import Image
import sys, os, subprocess
from modules.database_manager import validar_credenciales

# Configuración de rutas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#CC0000")

        # --- FRAME PRINCIPAL BLANCO ---
        frame = ctk.CTkFrame(self, width=420, height=580, corner_radius=20, fg_color="white")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.grid_propagate(False)

        # Encabezado y Logos
        ctk.CTkLabel(frame, text=" ", height=1, width=400).pack(pady=(15, 10))
        self.load_logo(frame, "logosfdb.png", (230, 70))
        ctk.CTkLabel(frame, text="Sistema de administración para estudios fotográficos", font=("Arial", 12), text_color="gray").pack(pady=(0, 10))
        
        # Línea divisoria
        ctk.CTkFrame(frame, height=1, fg_color="gray70", corner_radius=0).pack(fill="x", padx=40, pady=(5, 15))
        
        self.load_logo(frame, "logo0.png", (230, 70))
        ctk.CTkLabel(frame, text="Accede a tu cuenta", font=("Arial", 18, "bold"), text_color="black").pack(pady=(0, 15))

        # --- FORMULARIO ---
        # Diccionario con los estilos compartidos para los Entry
        e_kw = dict(width=280, height=45, corner_radius=20, border_color="#CC0000", border_width=2, text_color="black", fg_color="white")
        
        self.cedula = ctk.CTkEntry(frame, placeholder_text="Cédula", **e_kw)
        self.cedula.pack(pady=(10, 10))
        
        self.clave = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", **e_kw)
        self.clave.pack(pady=(0, 30))

        # Botón y Footer
        ctk.CTkButton(frame, text="Iniciar Sesión", command=self.login_action, width=200, height=50, corner_radius=25, fg_color="#CC0000", hover_color="#A30000", text_color="white", font=("Arial", 16, "bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame, text="DIDACTYSOFT", font=("Arial", 10), text_color="gray").pack(pady=(10, 5))
        
        self.error_label = ctk.CTkLabel(frame, text="", text_color="#CC0000", font=("Arial", 12))
        self.error_label.pack(pady=5)

        # Atajos de teclado
        self.bind("<Return>", lambda e: self.login_action())

    def login_action(self):
        usr, pwd = self.cedula.get(), self.clave.get()

        if not usr or not pwd:
            return self.error_label.configure(text="⚠️ Por favor complete todos los campos")

        if validar_credenciales(usr, pwd):
            self.withdraw()
            subprocess.run(['python', 'mainapp.py', usr])
        else:
            self.error_label.configure(text="❌ Cédula o contraseña incorrecta")
            self.clave.delete(0, "end")

    def load_logo(self, parent, filename, size):
        try:
            ruta = os.path.join(PROJECT_ROOT, "assets", filename)
            img = ctk.CTkImage(Image.open(ruta), size=size)
            ctk.CTkLabel(parent, image=img, text="").pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(parent, text=filename, text_color="black").pack()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()