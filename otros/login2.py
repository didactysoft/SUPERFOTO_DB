import customtkinter as ctk
from PIL import Image, ImageTk
import sys, os
import sqlite3  # Importamos la librería para la base de datos
import subprocess

# La ruta del proyecto es necesaria para las importaciones relativas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

# --- Configuración de la ruta de la base de datos ---
DB_PATH = os.path.join(PROJECT_ROOT, "database", "superfoto.db")

# --- Configuración inicial ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    logo_image_ref = None 

    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.state("zoomed")
        self.configure(fg_color="#CC0000")

        # --- FRAME PRINCIPAL ---
        self.login_frame = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.login_frame.grid_propagate(False)

        # (Se mantiene el resto de tu diseño de interfaz...)
        self.setup_ui()

    def setup_ui(self):
        """Organiza los elementos visuales extraídos de tu código original"""
        self.login_line = ctk.CTkLabel(self.login_frame, text=" ", height=1,width=400, fg_color="white")
        self.login_line.pack(pady=(15, 10))
 
        self.load_logo(self.login_frame, "logosfdb.png", (230, 70))
        ctk.CTkLabel(self.login_frame, text="Sistema de administración para estudios fotográficos",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 10))
        
        # Línea divisoria
        ctk.CTkFrame(self.login_frame, height=1, fg_color="gray70", corner_radius=0).pack(fill="x", padx=40, pady=(5, 15))

       
        # --- LOGO SUPERFOTO  ---
        self.load_logo(self.login_frame, "logo.png", (230, 70))


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

    # =======================================================
    # 🔐 VALIDACIÓN CON BASE DE DATOS REAL
    # =======================================================
    def check_credentials(self, cedula, password):
        """Consulta la base de datos para validar el usuario."""
        try:
            # Conexión a la carpeta database/superfoto.db
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Consultamos si existe el nombre_usuario con esa contraseña
            query = "SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ? AND contraseña = ?"
            cursor.execute(query, (cedula, password))
            
            user = cursor.fetchone()
            conn.close()

            return user is not None # Retorna True si encontró coincidencia
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False

    def login_action(self):
        cedula = self.cedula_entry.get()
        password = self.password_entry.get()

        if not cedula or not password:
            self.error_label.configure(text="Debe ingresar Cédula y Contraseña.")
            return

        # Validación mediante la función de base de datos
        if self.check_credentials(cedula, password):
            print(f"Acceso concedido a: {cedula}")
            self.withdraw()
            subprocess.run(['python', 'mainapp.py', cedula])
        else:
            self.error_label.configure(text="Cédula o Contraseña incorrecta.")
            self.password_entry.delete(0, ctk.END)

    def load_logo(self, parent_frame, filename, size):
        # (Tu función load_logo original se mantiene igual)
        try:
            base_path = os.path.join(PROJECT_ROOT, "assets")
            ruta = os.path.join(base_path, filename)
            img = Image.open(ruta)
            img = img.resize(size, Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            LoginApp.logo_image_ref = logo_img 
            label = ctk.CTkLabel(parent_frame, image=logo_img, text="")
            label.image = logo_img 
            label.pack(pady=10)
        except Exception: pass

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()