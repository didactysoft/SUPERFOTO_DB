import customtkinter as ctk
# ⚠️ IMPORTANTE: Volvemos a importar ImageTk para usarlo de forma explícita
from PIL import Image, ImageTk 
import importlib
import sys
import os

# --- Definición de Rutas Clave ---
# 1. Ruta del directorio actual (e.g., .../SUPERFOTO_DB/modules)
MAINAPP_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 2. La raíz del proyecto (e.g., .../SUPERFOTO_DB)
PROJECT_ROOT = os.path.dirname(MAINAPP_DIR) 

# Agrega la raíz del proyecto al sys.path para la carga de módulos
sys.path.append(PROJECT_ROOT)

# =======================================================
# 📌 CLASE BASE PARA MÓDULOS
# =======================================================
class BaseModuleFrame(ctk.CTkFrame):
    """Clase base de la que deben heredar todos los módulos cargados dinámicamente."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central con esquinas redondeadas para el contenido
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title}", 
                     font=("Arial", 32, "bold"), 
                     text_color="#CC0000").pack(pady=(50, 20))
        
        ctk.CTkLabel(frame_content, 
                     text=f"Si ve este mensaje, el módulo '{title}' aún no está implementado o falló al cargar.", 
                     font=("Arial", 16)).pack(pady=10)


# =======================================================
# 📌 CLASE PRINCIPAL: MainApp 
# =======================================================
class MainApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        # --- Variables de Referencia ---
        # ATRIBUTO CLAVE PARA LA PERSISTENCIA DE LA IMAGEN
        self.logo_image_ref = None 
        
        # --- Configuración de la Ventana Principal ---
        self.title("SUPERFOTO DB - Panel de Control")
        self.state("zoomed")
        self.configure(fg_color=("#F0F0F0", "gray10")) 
        
        # 1. Configuración del Layout (Grid de 2 columnas)
        self.grid_columnconfigure(0, weight=0) # Menú: tamaño fijo
        self.grid_columnconfigure(1, weight=1) # Contenido: expandible
        self.grid_rowconfigure(0, weight=1)

        self.username = username
        self.current_module = None

        # --- Lista de Módulos ---
        self.modules = {
            "Clientes": "modules.clientes.ClientesFrame",
            "Ventas/Facturación": "modules.ventas.VentasFrame",
            "Pedidos/Trabajos": "modules.pedidos.PedidosFrame",
            "Inventario": "modules.inventario.InventarioFrame",
            "Reportes": "modules.reportes.ReportesFrame",
            "Configuración": "modules.configuracion.ConfiguracionFrame",
            "Respaldo DB": "modules.backup.BackupFrame",
        }

        # --- Creación de la Interfaz ---
        self.create_sidebar()
        self.create_content_frame()
        
        # Iniciar con el módulo de Clientes
        self.select_module("Clientes")


    # =======================================================
    # 🔧 Método para Cargar Imágenes (SOLUCIÓN FORZADA DE PERSISTENCIA)
    # =======================================================
    def load_logo(self, parent_frame, filename, size):
        """Carga un logo de la carpeta 'assets' forzando la persistencia de PhotoImage."""
        try:
            # Construcción de la ruta ABSOLUTA
            assets_path = os.path.join(PROJECT_ROOT, "assets")
            ruta = os.path.join(assets_path, filename)
            
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"Archivo de logo NO ENCONTRADO en: {ruta}")

            # 1. Abrir la imagen con PIL
            img_pil = Image.open(ruta).resize(size, Image.LANCZOS)
            
            # --- PASO CRÍTICO: CREAR Y GUARDAR EXPLÍCITAMENTE EL PhotoImage ---
            # Esto es lo que CustomTkinter y Tkinter necesitan para que la imagen persista
            img_tk = ImageTk.PhotoImage(img_pil) 
            self.logo_image_ref = img_tk # Guardamos la referencia en la clase

            # 2. Crear la etiqueta y USAR el objeto img_tk (PhotoImage)
            # NOTA: Usamos el argumento 'image' directo, lo cual puede generar la advertencia
            # de CustomTkinter, pero es la forma de resolver el error de recolección de basura.
            label = ctk.CTkLabel(parent_frame, image=img_tk, text="", fg_color="transparent")
            
            # 3. Guardamos la referencia en el widget para una doble capa de protección
            label.image = img_tk 

            print("DEBUG: Logo cargado exitosamente (Solución forzada de PhotoImage).")

            return label
        except FileNotFoundError as fnfe:
            print(f"ERROR: Fallo al cargar la imagen: {fnfe}")
            return ctk.CTkLabel(parent_frame, text="[LOGO SFDB - NO ENCONTRADO]", text_color="white", font=("Arial", 14, "bold"))
        except Exception as e:
            # Cambiamos el mensaje de error para ayudar a identificar la causa si persiste
            print(f"ERROR: Fallo general al cargar la imagen con PhotoImage: {e}") 
            return ctk.CTkLabel(parent_frame, text="[LOGO SFDB - ERROR GENERAL]", text_color="white", font=("Arial", 14, "bold"))


    # -----------------------------------------------------------------
    # --- 1. Menú Lateral (Sidebar) ---
    # -----------------------------------------------------------------
    def create_sidebar(self):
        # Frame for the sidebar menu (column 0)
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#CC0000") # Rojo SUPERFOTO
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Permite que el botón de Cerrar Sesión se pegue al fondo
        self.sidebar_frame.grid_rowconfigure(len(self.modules) + 3, weight=1) 

        # --- SUPERFOTO DB Logo (Usando grid para consistencia) ---
        logo_label = self.load_logo(self.sidebar_frame, "logosfdb.png", (180, 50))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        ctk.CTkLabel(self.sidebar_frame, text="Admin DB",
                     font=("Arial", 10), text_color="#F0F0F0").grid(row=1, column=0, padx=20, pady=(0, 10))

        # Saludo al usuario
        ctk.CTkLabel(self.sidebar_frame, text=f"Hola, {self.username}",
                     font=("Arial", 12), text_color="white").grid(row=2, column=0, padx=20, pady=(0, 20))
        
        # Botones de Módulos
        self.module_buttons = {}
        for i, module_name in enumerate(self.modules.keys()):
            # Row index increased to account for logo and greeting
            button = ctk.CTkButton(self.sidebar_frame, text=module_name,
                                   command=lambda name=module_name: self.select_module(name),
                                   width=180, height=40,
                                   fg_color="transparent", hover_color="#A30000", # Rojo hover
                                   anchor="w", font=("Arial", 14))
            button.grid(row=i + 3, column=0, padx=20, pady=5)
            self.module_buttons[module_name] = button

        # Botón de Cerrar Sesión (al final de la barra)
        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión",
                      command=self.logout, width=180, height=40,
                      fg_color="#A30000", hover_color="#800000").grid(row=len(self.modules) + 4, column=0, padx=20, pady=(40, 20), sticky="s")


    # -----------------------------------------------------------------
    # --- 2. Marco de Contenido ---
    # -----------------------------------------------------------------
    def create_content_frame(self):
        # Frame for the main content (column 1)
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#F0F0F0") 
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)


    # -----------------------------------------------------------------
    # --- 3. Funcionalidades del Menú (Carga Dinámica) ---
    # -----------------------------------------------------------------
    def select_module(self, module_name):
        # 1. Si el módulo ya está seleccionado, no hacemos nada
        if self.current_module == module_name:
            return

        # 2. Desactivar y activar el resalte del botón
        if self.current_module and self.current_module in self.module_buttons:
            self.module_buttons[self.current_module].configure(fg_color="transparent")

        self.module_buttons[module_name].configure(fg_color="#A30000") # Resaltar en rojo oscuro

        # 3. Limpiar Contenido Anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # 4. Importar y Cargar Dinámicamente el Nuevo Frame
        module_file_name = None
        try:
            # Obtener la ruta y nombre de la clase
            module_path = self.modules[module_name] 
            parts = module_path.split('.')
            module_file_name = parts[1] 
            class_name = parts[-1] 

            # --- Carga DIRECTA de módulos ---
            # Intenta importar el módulo (ej: modules.clientes) y obtener la clase (ClientesFrame)
            module = importlib.import_module(f"modules.{module_file_name}")
            ModuleClass = getattr(module, class_name)
            
            # Instanciar el frame del módulo
            new_module_frame = ModuleClass(self.content_frame)
            new_module_frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            # Si la carga falla (ej: el archivo no existe o la clase no está definida), muestra error
            error_message = f"🚨 ERROR AL CARGAR EL MÓDULO: {module_name}\n\n"
            error_message += f"Asegúrese de que exista el archivo 'modules/{module_file_name}.py' y contenga la clase '{class_name}'.\n\n"
            error_message += f"Detalles del error: {e}"
            
            ctk.CTkLabel(self.content_frame, 
                         text=error_message,
                         font=("Arial", 20, "bold"), text_color="red", justify="left").grid(row=0, column=0, padx=50, pady=50)

        # 5. Actualizar el estado
        self.current_module = module_name


    def logout(self):
        """Destruye la ventana principal y simula el regreso a la ventana de login."""
        self.destroy()
        print("Sesión cerrada. Volviendo al login...")

# -----------------------------------------------------------------
# --- Ejecución (Para Pruebas) ---
# -----------------------------------------------------------------
if __name__ == "__main__":
    # Prueba la ventana principal de forma independiente.
    ctk.set_appearance_mode("Light") 

    # IMPORTANTE: El constructor espera el nombre de usuario/cédula
    app = MainApp(username="admin_test_1234")
    app.mainloop()