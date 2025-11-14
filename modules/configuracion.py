import customtkinter as ctk

class ConfiguracionFrame(ctk.CTkFrame):
    """Marco para Ajustes de Usuario, Precios, Logotipos y otros ajustes."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Título ---
        ctk.CTkLabel(self, text="⚙️ Módulo de Configuración",
                     font=("Arial", 28, "bold"), text_color="#6c757d").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Controles ---
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkButton(control_frame, text="👤 Gestión de Usuarios", fg_color="#007bff").pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="🏷️ Precios y Servicios", fg_color="#ffc107").pack(side="left", padx=10)

        # --- Área de Contenido ---
        content_area = ctk.CTkFrame(self)
        content_area.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        ctk.CTkLabel(content_area, text="[Aquí se editarán los parámetros generales del sistema y la información de la tienda.]",
                     font=("Arial", 16), text_color="#666666").pack(padx=50, pady=50)