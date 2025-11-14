import customtkinter as ctk
from PIL import Image, ImageTk
import os 
from tkinter import messagebox # Necesario para mostrar mensajes de error

# --- Configuraciones Iniciales ---
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

# --- SIMULACIÓN DE USUARIOS VÁLIDOS (Base de Datos) ---
# Un diccionario simple donde la clave es la Cédula y el valor es la Contraseña
USUARIOS_VALIDOS = {
    "12345678": "admin123", # Usuario de ejemplo 1
    "98765432": "pass456",  # Usuario de ejemplo 2
    "11111111": "luiscarlitos" # Usuario de ejemplo 3
}

# =======================================================
# 📌 CLASE DE LA VENTANA PRINCIPAL (MainApp)
# =======================================================

class MainApp(ctk.CTk):
    """Representa la pantalla principal del sistema después de un login exitoso."""
    def __init__(self, username):
        super().__init__()

        self.title("SUPERFOTO DB - Pantalla Principal")
        self.geometry("1024x768")
        self.state('zoomed')
        self.configure(fg_color="#FF0000") # Un color de fondo diferente

        # Saludo en la pantalla principal
        self.welcome_label = ctk.CTkLabel(
            self, 
            text=f"¡Bienvenido/a, {username}!", 
            font=("Arial", 30, "bold"), 
            text_color="white"
        )
        self.welcome_label.pack(pady=50, padx=20)
        
        self.info_label = ctk.CTkLabel(
            self, 
            text="Esta es la pantalla principal del sistema SUPERFOTO DB.\nAquí irá la interfaz de administración.", 
            font=("Arial", 16), 
            text_color="white"
        )
        self.info_label.pack(pady=20, padx=20)

        # Botón de Cierre de Sesión
        self.logout_button = ctk.CTkButton(
            self,
            text="Cerrar Sesión",
            command=self.logout,
            width=150,
            height=40,
            fg_color="#CC0000",
            hover_color="#A30000",
            font=("Arial", 14, "bold")
        )
        self.logout_button.pack(pady=40)

    def logout(self):
        """Cierra la sesión y vuelve a la ventana de Login."""
        self.destroy() # Destruye la ventana principal
        # Llamar a la función principal para relanzar la aplicación de login
        # (Esto se maneja fuera de la clase en el bloque if __name__ == "__main__":)
        print("Sesión cerrada. Volviendo a la pantalla de login.")


# =======================================================
# 📌 CLASE DE LA VENTANA DE LOGIN (LoginApp)
# =======================================================

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Accede a tu cuenta - SUPERFOTO DB")
        self.geometry("800x600") 
        self.state('zoomed') 

        # --- Fondo de color rojo ---
        self.configure(fg_color="#CC0000")

        # --- Frame principal blanco para el contenido del login ---
        self.login_frame = ctk.CTkFrame(self, width=400, height=520, corner_radius=20, fg_color="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.login_frame.grid_propagate(False)
        self.load_logo("logo.png", (200,80), 1)

        # Texto "SUPERFOTO DB"
        self.company_name = ctk.CTkLabel(self.login_frame, text="SUPERFOTO BD", font=("Arial", 26, "bold"), text_color="#CC0000")
        #self.company_name.pack(pady=(0, 0))

        self.tagline = ctk.CTkLabel(self.login_frame, text="Sistema de administración para estudios Fotográficos", font=("Arial", 12), text_color="gray")
        
        
        # Texto "Accede a tu cuenta"
        self.login_title = ctk.CTkLabel(self.login_frame, text="Accede a tu cuenta", font=("Arial", 18, "bold"), text_color="black")
        self.login_title.pack(pady=(10, 0))

        # Línea divisoria
        self.login_line = ctk.CTkLabel(self.login_frame, text="_______________________________________________________________________________________", font=("Arial", 10, "bold"), text_color="white")
        self.login_line.pack(pady=(0, 15))

        # Campo de entrada para Cédula
        self.cedula_entry = ctk.CTkEntry(
            self.login_frame, 
            placeholder_text="Cédula", 
            width=250, 
            height=45, 
            corner_radius=20,
            fg_color="white",
            border_color="#CC0000", 
            border_width=2,
            text_color="black"
        )
        self.cedula_entry.pack(pady=(0, 15))

        # Campo de entrada para Contraseña
        self.password_entry = ctk.CTkEntry(
            self.login_frame, 
            placeholder_text="Contraseña", 
            #show="*", 
            width=250, 
            height=45, 
            corner_radius=20,
            fg_color="white",
            border_color="#CC0000", 
            border_width=2,
            text_color="black"
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Asociar la tecla ENTER al evento de login en ambos campos
        self.cedula_entry.bind('<Return>', lambda event: self.login_action())
        self.password_entry.bind('<Return>', lambda event: self.login_action())

        # Botón "Iniciar Sesión"
        self.login_button = ctk.CTkButton(
            self.login_frame, 
            text="Iniciar Sesión", 
            command=self.login_action,
            width=180, 
            height=50, 
            corner_radius=25,
            fg_color="#CC0000", 
            hover_color="#A30000", 
            text_color="white",
            font=("Arial", 16, "bold")
        )
        self.login_button.pack(pady=(0, 30))

        # --- Carga de Logo 2 ---
        self.load_logo("logosfdb.png", (250, 80), 2)
        self.tagline.pack(pady=(0, 20))
        # Texto "Didactysoft - Desarrollo de Software"
        self.footer_label = ctk.CTkLabel(self.login_frame, text="DIDACTYSOFT", font=("Arial", 10), text_color="gray")
        self.footer_label.pack(pady=(0, 10))

    def load_logo(self, path, size, index):
        """Función auxiliar para cargar logos de forma segura."""
        try:
            # Usar una ruta relativa para mayor portabilidad
            original_image = Image.open(path)
            original_image.load() 
            
            resized_image = original_image.resize(size, Image.LANCZOS)
            
            # Guardamos la referencia de la imagen en un atributo diferente para cada logo
            if index == 1:
                self.logo_img1 = ImageTk.PhotoImage(resized_image)
                logo_label = ctk.CTkLabel(self.login_frame, image=self.logo_img1, text="")
            else:
                self.logo_img2 = ImageTk.PhotoImage(resized_image)
                logo_label = ctk.CTkLabel(self.login_frame, image=self.logo_img2, text="")
                
            logo_label.pack(pady=(20, 5) if index == 1 else (0, 5), padx=20)
            
        except FileNotFoundError:
            error_text = f"[LOGO {index} NO ENCONTRADO]"
            logo_label = ctk.CTkLabel(self.login_frame, text=error_text, font=("Arial", 16, "bold"), text_color="#CC0000")
            logo_label.pack(pady=(20, 5), padx=20)
            print(f"ERROR: Archivo no encontrado en la ruta: {path}")
            
        except Exception as e:
            error_text = f"[ERROR DE CARGA DE IMAGEN {index}]"
            logo_label = ctk.CTkLabel(self.login_frame, text=error_text, font=("Arial", 14, "bold"), text_color="#CC0000")
            logo_label.pack(pady=(20, 5), padx=20)
            print(f"Error crítico al procesar el logo {index}: {e}")

    def login_action(self):
        """
        Valida las credenciales de usuario y realiza la transición de pantalla.
        """
        cedula = self.cedula_entry.get()
        password = self.password_entry.get()
        
        print(f"Intento de login - Cédula: {cedula}")
        
        # 1. Validación de campos vacíos
        if not cedula or not password:
            messagebox.showerror("Error de Login", "Debe ingresar Cédula y Contraseña.")
            return

        # 2. Validación contra la "base de datos" (diccionario)
        if cedula in USUARIOS_VALIDOS and USUARIOS_VALIDOS[cedula] == password:
            # --- ÉXITO DEL LOGIN ---
            print("Login exitoso. Iniciando aplicación principal.")
            
            # 3. Destruir la ventana actual (Login)
            self.destroy() 
            
            # 4. Iniciar la ventana principal
            main_app = MainApp(cedula) # Le pasamos la cédula como 'username' de ejemplo
            main_app.mainloop()

        else:
            # --- FALLO DEL LOGIN ---
            messagebox.showerror("Error de Login", "Cédula o Contraseña incorrecta. Intente de nuevo.")
            # Opcional: Limpiar el campo de contraseña
            self.password_entry.delete(0, ctk.END)


if __name__ == "__main__":
    # La función main_loop nos permite relanzar la aplicación de login
    # si el usuario cierra la MainApp con el botón "Cerrar Sesión".
    def main_loop():
        # Aseguramos que solo haya una instancia de CTk en la memoria
        if ctk.get_appearance_mode() == "System":
            ctk.set_appearance_mode("light") # Reiniciar por si acaso

        app = LoginApp()
        app.mainloop()
        
        # Si la MainApp se cerró (con self.destroy()), app.mainloop() habrá terminado. 
        # Si queremos que MainApp nos devuelva al Login, necesitamos reiniciar el ciclo.
        # En este caso, el ciclo se reiniciará si el usuario presiona "Cerrar Sesión" 
        # y la MainApp fue lanzada por esta parte del código.
        
    main_loop()