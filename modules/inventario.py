import customtkinter as ctk

class InventarioFrame(ctk.CTkFrame):
    """Módulo de Gestión de Inventario (Suministros y Productos)."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1) # Fila de la tabla expandible

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Control (Fila 1) ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_controls.grid_columnconfigure(4, weight=1) # Espacio vacío

        ctk.CTkButton(frame_controls, text="➕ Nuevo Artículo", fg_color="#1F6AA5", hover_color="#185686").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="📉 Alertas de Stock", fg_color="#FF4500", hover_color="#CD3700").grid(row=0, column=1, padx=10)
        
        ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Nombre o Código...", width=300).grid(row=0, column=3, padx=(100, 10), sticky="e")

        # --- Área de la Tabla (Fila 2) ---
        self.create_inventory_table(frame_content)

    def create_inventory_table(self, parent):
        # Frame para simular la tabla con scrollbar
        frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Suministros y Productos en Stock", label_text_color="#333")
        frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Cabeceras de la tabla
        headers = ["Código", "Nombre del Artículo", "Stock Actual", "Mínimo Stock", "Ubicación", "Precio Compra"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(frame_table, text=header, font=("Arial", 14, "bold"), width=150, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

        # Datos de ejemplo (Mock Data)
        inventory_data = [
            ("P-4x6-GL", "Papel Fotográfico 4x6 Brillo", 500, 100, "Estante A1", "$0.10"),
            ("T-C-893", "Tinta Cyan para Plotter", 2, 5, "Almacén", "$45.00"), # Stock bajo
            ("M-10x15-B", "Marco de Madera 10x15 Negro", 45, 20, "Estante B3", "$2.50"),
            ("P-8x10-MT", "Papel Fotográfico 8x10 Mate", 90, 50, "Estante A2", "$0.30"),
            ("P-6x8-MT", "Papel Fotográfico 6x8 Mate", 48, 50, "Estante A2", "$0.20"), # Stock bajo
            ("T-M-893", "Tinta Magenta para Plotter", 10, 5, "Almacén", "$45.00"),
        ]

        # Llenar la tabla
        for row_index, (code, name, stock, min_stock, location, price) in enumerate(inventory_data, start=1):
            ctk.CTkLabel(frame_table, text=code, width=150, anchor="w", text_color="#333").grid(row=row_index, column=0, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=name, width=150, anchor="w", text_color="#333").grid(row=row_index, column=1, padx=5, pady=2)
            
            # Lógica para resaltar stock bajo (stock < min_stock)
            text_color = "red" if stock < min_stock else "#333"
            ctk.CTkLabel(frame_table, text=str(stock), width=150, anchor="center", text_color=text_color, font=("Arial", 14, "bold")).grid(row=row_index, column=2, padx=5, pady=2)
            
            ctk.CTkLabel(frame_table, text=str(min_stock), width=150, anchor="center", text_color="#333").grid(row=row_index, column=3, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=location, width=150, anchor="w", text_color="#333").grid(row=row_index, column=4, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=price, width=150, anchor="e", text_color="#333").grid(row=row_index, column=5, padx=5, pady=2)