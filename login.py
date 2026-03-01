import customtkinter as ctk
from PIL import Image, ImageTk
import sys, os
import subprocess
from modules.database_manager import validar_credenciales

# Configuración de rutas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    logo_image_ref = None 

    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
# Iniciar ventana maximizada
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#CC0000")

        # --- FRAME PRINCIPAL BLANCO ---
        self.login_frame = ctk.CTkFrame(self, width=420, height=580, corner_radius=20, fg_color="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.login_frame.grid_propagate(False)

        self.setup_ui()

    def setup_ui(self):
        self.login_line = ctk.CTkLabel(self.login_frame, text=" ", height=1,width=400, fg_color="white")
        self.login_line.pack(pady=(15, 10))
 
        self.load_logo(self.login_frame, "logosfdb.png", (230, 70))
        ctk.CTkLabel(self.login_frame, text="Sistema de administración para estudios fotográficos",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 10))
        
        # Línea divisoria
        ctk.CTkFrame(self.login_frame, height=1, fg_color="gray70", corner_radius=0).pack(fill="x", padx=40, pady=(5, 15))

       
        # --- LOGO SUPERFOTO  ---
        self.load_logo(self.login_frame, "logo0.png", (230, 70))


        ctk.CTkLabel(self.login_frame, text="Accede a tu cuenta",
                     font=("Arial", 18, "bold"), text_color="black").pack(pady=(0, 15))
        
 
        self.cedula_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Cédula", width=280, height=45, corner_radius=20, border_color="#CC0000", border_width=2, text_color="black", fg_color="white")
        self.cedula_entry.pack(pady=(10, 10))

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*", width=280, height=45, corner_radius=20, border_color="#CC0000", border_width=2, text_color="black", fg_color="white")
        self.password_entry.pack(pady=(0, 30))

        self.login_button = ctk.CTkButton(self.login_frame, text="Iniciar Sesión", command=self.login_action, width=200, height=50, corner_radius=25, fg_color="#CC0000", hover_color="#A30000", text_color="white", font=("Arial", 16, "bold"))
        self.login_button.pack(pady=(0, 5))

        ctk.CTkLabel(self.login_frame, text="DIDACTYSOFT",
                     font=("Arial", 10), text_color="gray").pack(pady=(10, 5))
        # Etiqueta para mensajes de error
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="#CC0000", font=("Arial", 12))
        self.error_label.pack(pady=5)

        # Atajos de teclado
        self.bind("<Return>", lambda e: self.login_action())

    def login_action(self):
        usuario = self.cedula_entry.get()
        clave = self.password_entry.get()

        if not usuario or not clave:
            self.error_label.configure(text="⚠️ Por favor complete todos los campos")
            return

        # Validación real mediante el módulo centralizado
        if validar_credenciales(usuario, clave):
            print(f"Acceso exitoso: {usuario}")
            self.withdraw()
            subprocess.run(['python', 'mainapp.py', usuario])
        else:
            self.error_label.configure(text="❌ Cédula o contraseña incorrecta")
            self.password_entry.delete(0, ctk.END)

    def load_logo(self, parent, filename, size):
        try:
            ruta = os.path.join(PROJECT_ROOT, "assets", filename)
            img = Image.open(ruta)
            img = img.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(parent, image=photo, text="")
            label.image = photo 
            label.pack(pady=5)
        except:
            ctk.CTkLabel(parent, text=filename, text_color="black").pack()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()