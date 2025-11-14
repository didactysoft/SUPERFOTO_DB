import customtkinter as ctk

class BackupFrame(ctk.CTkFrame):
    """Marco para el Respaldo (Backup) de la Base de Datos."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Título ---
        ctk.CTkLabel(self, text="💾 Módulo de Respaldo DB",
                     font=("Arial", 28, "bold"), text_color="#1f6aa5").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Controles ---
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkButton(control_frame, text="🚀 Realizar Respaldo Ahora", fg_color="#28a745", height=40).pack(pady=20, padx=20)
        
        # --- Área de Contenido ---
        content_area = ctk.CTkFrame(self)
        content_area.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        ctk.CTkLabel(content_area, text="Último Respaldo Realizado: 2025-11-13 23:00:00\n\n[Aquí se listarán los respaldos anteriores y se configurará la automatización.]",
                     font=("Arial", 16), text_color="#666666").pack(padx=50, pady=50)