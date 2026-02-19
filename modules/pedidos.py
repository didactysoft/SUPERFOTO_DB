import customtkinter as ctk

class PedidosFrame(ctk.CTkFrame):
    """Módulo de Pedidos y Trabajos (Jobs/Orders)."""
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

        ctk.CTkButton(frame_controls, text="➕ Nuevo Pedido", fg_color="#1F6AA5", hover_color="#185686").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="📊 Ver Reporte", fg_color="#4CAF50", hover_color="#388E3C").grid(row=0, column=1, padx=10)
        
        ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Cliente o ID...", width=300).grid(row=0, column=3, padx=(100, 10), sticky="e")

        # --- Área de la Tabla (Fila 2) ---
        self.create_table_simulation(frame_content)

    def create_table_simulation(self, parent):
        # Frame para simular la tabla con scrollbar
        frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Pedidos Activos (Últimos 30 días)", label_text_color="#333")
        frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Cabeceras de la tabla
        headers = ["ID", "Cliente", "Fecha Pedido", "Total", "Estado", "Acciones"]
        for i, header in enumerate(headers):
            # Las cabeceras ya usan un color oscuro
            ctk.CTkLabel(frame_table, text=header, font=("Arial", 14, "bold"), width=150, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

        # Datos de ejemplo (Mock Data)
        pedidos_data = [
            (1001, "Juan Pérez", "2025-10-25", "$150.00", "En Producción", ["Editar", "Pagar", "Ver"]),
            (1002, "María López", "2025-10-26", "$45.50", "Finalizado", ["Ver", "Facturar"]),
            (1003, "FotoMundo SA", "2025-10-27", "$320.00", "Pendiente Pago", ["Editar", "Pagar"]),
            (1004, "Roberto G.", "2025-10-28", "$89.99", "Entregado", ["Ver"]),
            (1005, "Laura V.", "2025-10-29", "$12.00", "Cancelado", ["Ver"]),
        ]

        # Llenar la tabla
        for row_index, (id, client, date, total, status, actions) in enumerate(pedidos_data, start=1):
            # Se ha añadido text_color="#333" a todas las etiquetas de datos para asegurar visibilidad.
            ctk.CTkLabel(frame_table, text=str(id), width=150, anchor="w", text_color="#333").grid(row=row_index, column=0, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=client, width=150, anchor="w", text_color="#333").grid(row=row_index, column=1, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=date, width=150, anchor="w", text_color="#333").grid(row=row_index, column=2, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=total, width=150, anchor="e", text_color="#333").grid(row=row_index, column=3, padx=5, pady=2)
            
            # Etiqueta de estado con color (el texto aquí ya es blanco para contrastar con el color de fondo del estado)
            color = {"En Producción": "#FFC107", "Finalizado": "#4CAF50", "Pendiente Pago": "#F44336", "Entregado": "#2196F3", "Cancelado": "#607D8B"}.get(status, "#607D8B")
            ctk.CTkLabel(frame_table, text=status, width=150, anchor="center", fg_color=color, corner_radius=5, text_color="white").grid(row=row_index, column=4, padx=5, pady=2)

            # Botones de acción
            action_frame = ctk.CTkFrame(frame_table, fg_color="transparent")
            action_frame.grid(row=row_index, column=5, padx=5, pady=2, sticky="w")
            for col_index, action in enumerate(actions):
                ctk.CTkButton(action_frame, text=action, width=60, height=25, font=("Arial", 10), fg_color="#9E9E9E", hover_color="#757575").grid(row=0, column=col_index, padx=2)