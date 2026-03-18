import customtkinter as ctk
from PIL import Image
import importlib
import sys
import os
import json
from modules.database_manager import ejecutar_consulta

# --- Configuración inicial de usuario para ejecución directa ---
usuario_global = sys.argv[1] if len(sys.argv) > 1 else "Prueba"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(PROJECT_ROOT)

def inicializar_apariencia():
    archivo_config = os.path.join(PROJECT_ROOT, "config_sistema.json")
    tema = "Light" 
    if os.path.exists(archivo_config):
        try:
            with open(archivo_config, "r", encoding="utf-8") as f:
                tema = json.load(f).get("tema", "Light")
        except Exception:
            pass
    ctk.set_appearance_mode(tema)

inicializar_apariencia()

# =======================================================
# 📌 CLASE BASE PARA MÓDULOS (Plantilla de error)
# =======================================================
class BaseModuleFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.pack(fill="both", expand=True) # Uso pack en lugar de grid para el contenedor principal
        
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_content, text=f"MÓDULO: {title}", font=("Arial", 32, "bold"), text_color="#050404").pack(pady=(50, 20))
        ctk.CTkLabel(frame_content, text=f"Si ve este mensaje, el módulo '{title}' aún no está implementado.", font=("Arial", 16), text_color="gray").pack(pady=10)

# =======================================================
# 📌 CLASE PRINCIPAL: MainApp 
# =======================================================
class MainApp(ctk.CTk):
    def __init__(self, usuarioid):
        super().__init__()
        
        self.title("SUPERFOTO DB - Panel de Control")
        self.after(0, lambda: self.state('zoomed'))
        
        ruta_icono = os.path.join(PROJECT_ROOT, "assets", "logo.ico")
        if os.path.exists(ruta_icono):
            self.after(200, lambda: self.iconbitmap(ruta_icono))

        # --- Obtener Nombre de Usuario ---
        query = """
        SELECT e.nombre FROM usuario u
        INNER JOIN empleado e ON u.id_empleado = e.id_empleado
        WHERE u.usuario = ?
        """
        res = ejecutar_consulta(query, (usuarioid,))
        self.username = res[0][0] if res else "Usuario"

        # --- Layout Principal ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_module = None
        self.modules = {
            "Pedidos/Trabajos": "modules.pedidos.PedidosFrame",
            "Ventas/Facturación": "modules.ventas.VentasFrame",
            "Clientes": "modules.clientes.ClientesFrame",
            "Empleados": "modules.empleado.EmpleadosFrame",
            "Usuarios": "modules.usuario.UsuariosFrame",
            "Inventario": "modules.inventario.InventarioFrame",
            "Reportes": "modules.reportes.ReportesFrame",
            "Configuración": "modules.configuracion.ConfiguracionFrame",
            "Respaldo DB": "modules.backup.BackupFrame"
        }

        self.create_sidebar()
        self.create_content_frame()
        self.select_module("Pedidos/Trabajos")

    def get_ctk_image(self, filename, size):
        """Retorna un objeto CTkImage o None si falla."""
        ruta = os.path.join(PROJECT_ROOT, "assets", filename)
        if os.path.exists(ruta):
            return ctk.CTkImage(Image.open(ruta), size=size)
        return None

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#202020")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(len(self.modules) + 3, weight=1) # Empuja hacia abajo

        # Logos y Saludo
        img_logo = self.get_ctk_image("logo.png", (200, 60))
        ctk.CTkLabel(self.sidebar_frame, image=img_logo, text="[Logo]" if not img_logo else "").grid(row=0, column=0, padx=20, pady=(20, 10))
        
        ctk.CTkLabel(self.sidebar_frame, text=f"Hola, {self.username}", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=0, pady=10)
        
        # Generar Botones Dinámicamente
        self.module_buttons = {}
        for i, name in enumerate(self.modules.keys(), start=2):
            btn = ctk.CTkButton(self.sidebar_frame, text=name, anchor="w", fg_color="transparent", hover_color="#A30000",
                                command=lambda n=name: self.select_module(n))
            btn.grid(row=i, column=0, padx=15, pady=4, sticky="ew")
            self.module_buttons[name] = btn

        # Footer Sidebar
        img_sfdb = self.get_ctk_image("logosfdb.png", (200, 60))
        row_footer = len(self.modules) + 4
        ctk.CTkLabel(self.sidebar_frame, image=img_sfdb, text="[Logo DB]" if not img_sfdb else "").grid(row=row_footer, column=0, pady=(20, 0))
        
        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", fg_color="#A30000", hover_color="#800000", 
                      command=self.logout).grid(row=row_footer + 1, column=0, padx=20, pady=20)

    def create_content_frame(self):
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent") 
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def select_module(self, module_name):
        if self.current_module == module_name: return

        if self.current_module:
            self.module_buttons[self.current_module].configure(fg_color="transparent")
        self.module_buttons[module_name].configure(fg_color="#A30000")

        # Limpiar contenedor principal
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Cargar módulo
        try:
            modulo, clase = self.modules[module_name].rsplit('.', 1)
            mod_importado = importlib.import_module(modulo)
            InstanciaClase = getattr(mod_importado, clase)
            
            # Instanciar y mostrar el frame del módulo
            frame = InstanciaClase(self.content_frame, title=module_name)
            frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            ctk.CTkLabel(self.content_frame, text=f"Error al cargar {module_name}:\n{e}", text_color="red", font=("Arial", 16)).grid(row=0, column=0)

        self.current_module = module_name

    def logout(self):
        self.destroy()
        # Aquí podrías usar subprocess para volver a lanzar el login si fuera necesario.

if __name__ == "__main__":
    app = MainApp(usuario_global)
    app.mainloop()