import customtkinter as ctk

class InventarioFrame(ctk.CTkFrame):
    """Marco para el Control de Insumos y Materiales (Inventario)."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Título ---
        ctk.CTkLabel(self, text="📦 Módulo de Inventario",
                     font=("Arial", 28, "bold"), text_color="#fd7e14").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Controles ---
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkButton(control_frame, text="➕ Agregar Material", fg_color="#17a2b8").pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="📉 Productos Bajos en Stock", fg_color="#dc3545").pack(side="left", padx=10)

        # --- Área de Contenido ---
        content_area = ctk.CTkFrame(self)
        content_area.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        ctk.CTkLabel(content_area, text="[Aquí se mostrará la lista de stock, precios de compra y alerta de mínimos.]",
                     font=("Arial", 16), text_color="#666666").pack(padx=50, pady=50)