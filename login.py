import customtkinter as ctk
from PIL import Image, ImageTk
import sys, os
from tkinter import messagebox

# La ruta del proyecto es necesaria para las importaciones relativas
PROJECT_ROOT = os.path.dirname(__file__)
# Añadir la carpeta 'modules' al path para poder importar MainApp
sys.path.append(os.path.join(PROJECT_ROOT, "modules"))

try:
    from mainapp import MainApp  # 🔗 Importa la pantalla principal desde modules/
except ImportError:
    # Manejo de error si el archivo MainApp no está donde se espera
    print("Error: No se encontró 'mainapp.py'. Asegúrese de que esté dentro de la carpeta 'modules'.")
    # Nota: No usamos messagebox aquí para evitar errores si la app aún no se ha lanzado completamente.
    sys.exit()

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
    def __init__(self):
        super().__init__()
        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.geometry("800x600")
        self.state("zoomed")
        self.configure(fg_color="#CC0000")  # Fondo rojo

        # --- FRAME PRINCIPAL BLANCO (TODAS LAS ESQUINAS REDONDEADAS) ---
        # Se asegura un corner_radius alto y un solo frame para el redondeo consistente.
        self.login_frame = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.login_frame.grid_propagate(False)

        # --- LOGO SUPERIOR ---
        self.load_logo(self.login_frame, "logo.png", (220, 80))

        # --- TEXTO PRINCIPAL ---
        ctk.CTkLabel(self.login_frame, text="SUPERFOTO DB",
                     font=("Arial", 26, "bold"), text_color="#CC0000").pack(pady=(5, 0))

        ctk.CTkLabel(self.login_frame, text="Sistema de administración para estudios fotográficos",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        ctk.CTkLabel(self.login_frame, text="Accede a tu cuenta",
                     font=("Arial", 18, "bold"), text_color="black").pack(pady=(0, 10))
        # Línea divisoria
        self.login_line = ctk.CTkLabel(self.login_frame, text="_______________________________________________________________________________________", font=("Arial", 10, "bold"), text_color="white")
        self.login_line.pack(pady=(0, 15))

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
        self.login_button.pack(pady=(0, 20))

        # --- LOGO INFERIOR ---
        self.load_logo(self.login_frame, "logosfdb.png", (200, 70))

        ctk.CTkLabel(self.login_frame, text="DIDACTYSOFT",
                     font=("Arial", 10), text_color="gray").pack(pady=(5, 0))

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
            logo_img = ImageTk.PhotoImage(img)

            # Colocamos las imágenes en el frame padre
            label = ctk.CTkLabel(parent_frame, image=logo_img, text="")
            label.image = logo_img  # CRÍTICO: Mantener la referencia
            label.pack(pady=10)
        except Exception as e:
            # print(f"⚠️ Error al cargar logo {filename}: {e}") # Descomentar para debug
            ctk.CTkLabel(parent_frame, text=f"[{filename} no encontrado]",
                         text_color="#CC0000", font=("Arial", 14, "bold")).pack(pady=10)

    # =======================================================
    # 🔐 Validación de login
    # =======================================================
    def login_action(self):
        cedula = self.cedula_entry.get()
        password = self.password_entry.get()

        if not cedula or not password:
            messagebox.showerror("Error de Login", "Debe ingresar Cédula y Contraseña.")
            return

        if cedula in USUARIOS_VALIDOS and USUARIOS_VALIDOS[cedula] == password:
            self.withdraw()  # Oculta la ventana de login
            
            # 🔗 Abre la ventana principal
            main_app = MainApp(cedula)
            # Pasamos la referencia de la ventana de login a MainApp para que pueda cerrarla si es necesario
            main_app.protocol("WM_DELETE_WINDOW", lambda: self.show_login_on_main_close(main_app))
            main_app.mainloop()
            
            # La ventana de login se muestra automáticamente al cerrar MainApp
            self.password_entry.delete(0, ctk.END) # Limpiar el password al regresar
            self.cedula_entry.focus_set() # Poner el foco en la cédula
            
        else:
            messagebox.showerror("Error de Login", "Cédula o Contraseña incorrecta.")
            self.password_entry.delete(0, ctk.END)

    def show_login_on_main_close(self, main_app_instance):
        """Función llamada al cerrar la ventana principal."""
        main_app_instance.destroy()
        self.deiconify() # Vuelve a mostrar la ventana de Login

# =======================================================
# 🔁 Lanzar aplicación
# =======================================================
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()