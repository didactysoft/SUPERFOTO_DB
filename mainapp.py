import customtkinter as ctk
from PIL import Image
import importlib
import sys
import os
from modules.database_manager import ejecutar_consulta

# --- Configuración inicial de usuario para ejecución directa ---
if __name__ == "__main__":
    usuario_global = sys.argv[1] if len(sys.argv) > 1 else "11111111"
else:
    usuario_global = "Usuario"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(PROJECT_ROOT)



# =======================================================
# 📌 CLASE BASE PARA MÓDULOS
# =======================================================
class BaseModuleFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_content, text=f"MÓDULO: {title}", 
                     font=("Arial", 32, "bold"), text_color="#050404").pack(pady=(50, 20))
        
        ctk.CTkLabel(frame_content, 
                     text=f"Si ve este mensaje, el módulo '{title}' aún no está implementado.", 
                     font=("Arial", 16), text_color="gray").pack(pady=10)

# =======================================================
# 📌 CLASE PRINCIPAL: MainApp 
# =======================================================
class MainApp(ctk.CTk):
    def __init__(self, usuarioid):
        super().__init__()

        # --- Configuración de la Ventana ---
        
        self.title("SUPERFOTO DB - Panel de Control")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color=("#F0F0F0", "gray10")) 
        ruta_icono = os.path.join(PROJECT_ROOT, "assets", "logo.ico")

        if os.path.exists(ruta_icono):
            self.after(200, lambda: app.iconbitmap(ruta_icono))
        else:
            print(f"Error: No se encontró el icono en {ruta_icono}") 

        # --- Obtener Datos del Usuario ---
        query = "SELECT nombre_usuario FROM usuario WHERE usuario = ?"
        res = ejecutar_consulta(query, (usuarioid,))
        self.username = res[0][0] if res else "Usuario"

        # --- Layout Principal (SOLO GRID) ---
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Contenido
        self.grid_rowconfigure(0, weight=1)

        self.current_module = None
        self.modules = {
            "Pedidos/Trabajos": "modules.pedidos.PedidosFrame",
            "Ventas/Facturación": "modules.ventas.VentasFrame",
            "Clientes": "modules.clientes.ClientesFrame",
            "Inventario": "modules.inventario.InventarioFrame",
            "Reportes": "modules.reportes.ReportesFrame",
            "Configuración": "modules.configuracion.ConfiguracionFrame",
            "Respaldo DB": "modules.backup.BackupFrame",
        }

        self.create_sidebar()
        self.create_content_frame()
        self.select_module("Pedidos/Trabajos")

    def load_logo(self, parent_frame, filename, size):
        """Carga un logo usando CTkImage para evitar errores de escalado."""
        try:
            ruta = os.path.join(PROJECT_ROOT, "assets", filename)
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"No existe: {ruta}")

            img_pil = Image.open(ruta)
            # CTkImage gestiona la persistencia automáticamente
            logo_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=size)

            label = ctk.CTkLabel(parent_frame, image=logo_ctk, text="")
            return label
        except Exception as e:
            print(f"[WARNING] Error logo {filename}: {e}")
            return ctk.CTkLabel(parent_frame, text=f"[{filename}]", text_color="white")

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#202020")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Logo Principal
        logo_sf = self.load_logo(self.sidebar_frame, "logo.png", (200, 60))
        logo_sf.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Saludo
        ctk.CTkLabel(self.sidebar_frame, text=f"Hola, {self.username}",
                     font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=0, padx=20, pady=10)
        
        # Botones
        self.module_buttons = {}
        for i, module_name in enumerate(self.modules.keys()):
            btn = ctk.CTkButton(self.sidebar_frame, text=module_name,
                                command=lambda n=module_name: self.select_module(n),
                                width=190, height=35, fg_color="transparent",
                                hover_color="#A30000", anchor="w")
            btn.grid(row=i + 2, column=0, padx=15, pady=4)
            self.module_buttons[module_name] = btn

        # Empuje para el botón inferior
        self.sidebar_frame.grid_rowconfigure(len(self.modules) + 2, weight=1)


        logo_sf2 = self.load_logo(self.sidebar_frame, "logosfdb.png", (200, 60))
        logo_sf2.grid(row=9, column=0, padx=20, pady=(20, 0))

        # Botón Cerrar Sesión
        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión",
                      command=self.logout, fg_color="#A30000", 
                      hover_color="#800000").grid(row=len(self.modules) + 3, column=0, padx=20, pady=20)

    def create_content_frame(self):
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent") 
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def select_module(self, module_name):
        if self.current_module == module_name: return

        if self.current_module in self.module_buttons:
            self.module_buttons[self.current_module].configure(fg_color="transparent")
        self.module_buttons[module_name].configure(fg_color="#A30000")

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        try:
            full_path = self.modules[module_name]
            path_parts = full_path.split('.')
            class_name = path_parts[-1]
            module_path = ".".join(path_parts[:-1])

            module = importlib.import_module(module_path)
            ModuleClass = getattr(module, class_name)
            
            frame = ModuleClass(self.content_frame, title=module_name)
            frame.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            print(f"Error cargando {module_name}: {e}")
            ctk.CTkLabel(self.content_frame, text=f"Error al cargar {module_name}\n{e}",
                         text_color="red", font=("Arial", 16)).grid(row=0, column=0)

        self.current_module = module_name

    def logout(self):
        self.destroy()
        print("Regresando al login...")

# --- Ejecución ---
if __name__ == "__main__":
    app = MainApp(usuario_global)
    app.mainloop()