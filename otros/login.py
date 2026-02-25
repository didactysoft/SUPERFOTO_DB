import customtkinter as ctk
from PIL import Image, ImageTk
import sys, os
#from mainapp import MainApp
import subprocess

# La ruta del proyecto es necesaria para las importaciones relativas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) 
# Añadir la carpeta 'modules' al path para poder importar módulos internos
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))


# --- Configuración inicial ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Base de datos simulada ---
USUARIOS_VALIDOS = {
    "12345678": "admin123",
    "98765432": "pass456",
    "11111111": "luiscarlitos"
}

# =======================================================
# 📌 CLASE DE LOGIN
# =======================================================
class LoginApp(ctk.CTk):
    # Atributo para mantener la referencia del logo (previene el error pyimage)
    logo_image_ref = None 

    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.state("zoomed")
        self.configure(fg_color="#CC0000")  # Fondo rojo

        # --- FRAME PRINCIPAL BLANCO (TODAS LAS ESQUINAS REDONDEADAS) ---
        self.login_frame = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.login_frame.grid_propagate(False)

        # Espacio superior
        self.login_line = ctk.CTkLabel(self.login_frame, text=" ", height=1,width=400, fg_color="white")
        self.login_line.pack(pady=(15, 10))
 
        # --- LOGO SUPERFOTO DB ---
        self.load_logo(self.login_frame, "logosfdb.png", (230, 70))
        
        ctk.CTkLabel(self.login_frame, text="Sistema de administración para estudios fotográficos",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 10))
        
        # Línea divisoria
        ctk.CTkFrame(self.login_frame, height=1, fg_color="gray70", corner_radius=0).pack(fill="x", padx=40, pady=(5, 15))


        ctk.CTkLabel(self.login_frame, text="Accede a tu cuenta",
                     font=("Arial", 18, "bold"), text_color="black").pack(pady=(0, 15))
        
        
        # --- LOGO SUPERFOTO  ---
        self.load_logo(self.login_frame, "logo.png", (230, 70))
        
    
        # --- CAMPOS DE ENTRADA ---
        self.cedula_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Cédula",
                                         width=280, height=45, corner_radius=20,
                                         border_color="#CC0000", border_width=2,
                                         text_color="black", fg_color="white")
        self.cedula_entry.pack(pady=(10, 10))

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña",
                                           show="*", width=280, height=45, corner_radius=20,
                                           border_color="#CC0000", border_width=2,
                                           text_color="black", fg_color="white")
        self.password_entry.pack(pady=(0, 30))

        # --- BOTÓN DE LOGIN ---
        self.login_button = ctk.CTkButton(self.login_frame, text="Iniciar Sesión",
                                          command=self.login_action,
                                          width=200, height=50, corner_radius=25,
                                          fg_color="#CC0000", hover_color="#A30000",
                                          text_color="white", font=("Arial", 16, "bold"))
        self.login_button.pack(pady=(0, 5))

      

        ctk.CTkLabel(self.login_frame, text="DIDACTYSOFT",
                     font=("Arial", 10), text_color="gray").pack(pady=(10, 5))

        # ENTER -> ejecutar login
        self.cedula_entry.bind("<Return>", lambda e: self.login_action())
        self.password_entry.bind("<Return>", lambda e: self.login_action())

    # =======================================================
    # 🔧 Función para cargar imágenes desde assets/
    # =======================================================
    def load_logo(self, parent_frame, filename, size):
        """Carga un logo desde la carpeta 'assets' y lo muestra."""
        try:
            # Construye la ruta absoluta dentro de la carpeta 'assets'
            base_path = os.path.join(PROJECT_ROOT, "assets")
            ruta = os.path.join(base_path, filename)
            
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

            img = Image.open(ruta)
            img = img.resize(size, Image.LANCZOS)
            # Creamos el objeto PhotoImage
            logo_img = ImageTk.PhotoImage(img)

            # Guardamos la referencia en la clase y en el widget para la persistencia
            LoginApp.logo_image_ref = logo_img 

            # Colocamos la imagen en el frame padre
            label = ctk.CTkLabel(parent_frame, image=logo_img, text="")
            label.image = logo_img  # CRÍTICO: Mantener la referencia
            label.pack(pady=10)
        except Exception as e:
            print(f"⚠️ Error al cargar logo {filename}: {e}") 
            ctk.CTkLabel(parent_frame, text=f"[{filename} no encontrado]",
                         text_color="#CC0000", font=("Arial", 14, "bold")).pack(pady=10)

    # =======================================================
    # 🔐 Validación de login
    # =======================================================
    def login_action(self):
        cedula = self.cedula_entry.get()
        password = self.password_entry.get()

        if not cedula or not password:
            # Usamos una etiqueta temporal para notificar
            ctk.CTkLabel(self.login_frame, text="Debe ingresar Cédula y Contraseña.", text_color="#CC0000").pack(pady=(5, 0))
            return

        if cedula in USUARIOS_VALIDOS and USUARIOS_VALIDOS[cedula] == password:
            self.withdraw()  # Oculta la ventana de login
            
            # 🔗 Abre la ventana principal
            #main_app = MainApp(cedula)
            # Manejar el cierre de MainApp
            # main_app.protocol("WM_DELETE_WINDOW", lambda: self.show_login_on_main_close(main_app))
            # main_app.mainloop()
            #os.system('python mainapp.py')
            cedula_L = cedula
            subprocess.run(['python', 'mainapp.py', cedula_L])
        else:
            ctk.CTkLabel(self.login_frame, text="Cédula o Contraseña incorrecta.", text_color="#CC0000").pack(pady=(5, 0))
            self.password_entry.delete(0, ctk.END)

    def show_login_on_main_close(self, main_app_instance):
        """Función llamada al cerrar la ventana principal."""
        main_app_instance.destroy()
        self.cedula_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.deiconify()  # Vuelve a mostrar la ventana de Login
        self.cedula_entry.focus_set() # Poner el foco en la cédula

# =======================================================
# 🔁 Lanzar aplicación
# =======================================================
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()