import customtkinter as ctk
import importlib
import sys
import os

# Agregamos la carpeta superior al path para permitir la importación de 'modules'
# Esto es necesario si ejecutas main_app.py directamente dentro de SUPERFOTO_DB/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class MainApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("SUPERFOTO DB - Principal")
        self.state("zoomed")
        
        # 1. Configuración del Layout (Grid de 2 columnas)
        self.grid_columnconfigure(0, weight=0)  # Menú: tamaño fijo
        self.grid_columnconfigure(1, weight=1)  # Contenido: expandible
        self.grid_rowconfigure(0, weight=1)

        self.username = username
        self.current_module = None

        # --- Lista de Módulos ---
        # Formato: "Nombre en Menú": "ruta.del.modulo.NombreDeClase"
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


# -----------------------------------------------------------------
# --- 1. Menú Lateral (Sidebar) ---
# -----------------------------------------------------------------
    def create_sidebar(self):
        # Marco para el menú lateral (columna 0)
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#333333")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Permite que los elementos superiores estén fijos y los inferiores se peguen al fondo
        self.sidebar_frame.grid_rowconfigure(len(self.modules) + 3, weight=1) 

        # Título/Logo
        ctk.CTkLabel(self.sidebar_frame, text="SUPERFOTO DB",
                     font=("Arial", 20, "bold"), text_color="#FF0000").grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Saludo al usuario
        ctk.CTkLabel(self.sidebar_frame, text=f"Hola, {self.username}",
                     font=("Arial", 12), text_color="white").grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Botones de Módulos
        self.module_buttons = {}
        for i, module_name in enumerate(self.modules.keys()):
            button = ctk.CTkButton(self.sidebar_frame, text=module_name,
                                   command=lambda name=module_name: self.select_module(name),
                                   width=180, height=40,
                                   fg_color="transparent", hover_color="#555555",
                                   anchor="w", font=("Arial", 14))
            button.grid(row=i + 2, column=0, padx=20, pady=5)
            self.module_buttons[module_name] = button

        # Botón de Cerrar Sesión (al final de la barra)
        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión",
                      command=self.logout, width=180, height=40,
                      fg_color="#CC0000", hover_color="#A30000").grid(row=len(self.modules) + 4, column=0, padx=20, pady=(40, 20), sticky="s")


# -----------------------------------------------------------------
# --- 2. Marco de Contenido ---
# -----------------------------------------------------------------
    def create_content_frame(self):
        # Marco para el contenido principal (columna 1)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#f0f0f0") # Un color claro para diferenciar
        self.content_frame.grid(row=0, column=1, sticky="nsew")
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

        self.module_buttons[module_name].configure(fg_color="#FF0000") # Resaltar en rojo

        # 3. Limpiar Contenido Anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # 4. Importar y Cargar Dinámicamente el Nuevo Frame
        try:
            # Obtener la ruta y nombre de la clase
            module_path = self.modules[module_name] 
            parts = module_path.split('.')
            module_file_name = parts[1] # Ej: 'clientes'
            class_name = parts[-1]      # Ej: 'ClientesFrame'

            # Importar el módulo (Ej: from modules import clientes)
            module = importlib.import_module(f"modules.{module_file_name}")
            
            # Obtener la clase (Ej: ClientesFrame)
            ModuleClass = getattr(module, class_name)
            
            # Instanciar el frame del módulo
            new_module_frame = ModuleClass(self.content_frame, fg_color="transparent")
            new_module_frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            # Mostrar un mensaje de error si la carga falla
            ctk.CTkLabel(self.content_frame, 
                         text=f"🚨 ERROR AL CARGAR EL MÓDULO: {module_name}\n\nDetalles: {e}",
                         font=("Arial", 20, "bold"), text_color="red").grid(row=0, column=0, padx=50, pady=50)

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
    # Nota: Asegúrate de tener la carpeta 'modules' con los archivos .py
    # antes de ejecutar esto.
    
    # ctk.set_appearance_mode("Dark") # Opcional: para un tema oscuro

    app = MainApp("Administrador_SFDB")
    app.mainloop()