import customtkinter as ctk

class VentasFrame(ctk.CTkFrame):
    """Módulo de Ventas y Facturación."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Control ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_controls.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(frame_controls, text="💸 Nueva Venta Directa", fg_color="#1F6AA5", hover_color="#185686").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="🧾 Generar Factura", fg_color="#4CAF50", hover_color="#388E3C").grid(row=0, column=1, padx=10)
        
        ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Factura o Cliente...", width=300).grid(row=0, column=3, padx=(100, 10), sticky="e")

        # --- Área de la Tabla ---
        self.create_sales_table(frame_content)

    def create_sales_table(self, parent):
        frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Historial de Ventas y Facturas", label_text_color="#333")
        frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        headers = ["Factura ID", "Fecha", "Cliente", "Método Pago", "Monto Total", "Estado"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(frame_table, text=header, font=("Arial", 14, "bold"), width=150, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

        sales_data = [
            (5001, "2025-10-29", "Juan Pérez", "Efectivo", "$150.00", "Pagada"),
            (5002, "2025-10-28", "María López", "Tarjeta", "$45.50", "Pagada"),
            (5003, "2025-10-27", "FotoMundo SA", "Crédito", "$320.00", "Pendiente"),
            (5004, "2025-10-26", "Roberto G.", "Transferencia", "$89.99", "Pagada"),
        ]

        for row_index, (id, date, client, method, total, status) in enumerate(sales_data, start=1):
            ctk.CTkLabel(frame_table, text=str(id), width=150, anchor="w", text_color="#333").grid(row=row_index, column=0, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=date, width=150, anchor="w", text_color="#333").grid(row=row_index, column=1, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=client, width=150, anchor="w", text_color="#333").grid(row=row_index, column=2, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=method, width=150, anchor="w", text_color="#333").grid(row=row_index, column=3, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=total, width=150, anchor="e", text_color="#333").grid(row=row_index, column=4, padx=5, pady=2)
            
            color = {"Pagada": "#4CAF50", "Pendiente": "#FF9800", "Anulada": "#F44336"}.get(status, "#607D8B")
            ctk.CTkLabel(frame_table, text=status, width=150, anchor="center", fg_color=color, corner_radius=5, text_color="white").grid(row=row_index, column=5, padx=5, pady=2)