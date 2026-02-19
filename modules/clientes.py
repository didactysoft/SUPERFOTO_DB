import customtkinter as ctk

class ClientesFrame(ctk.CTkFrame):
    """Módulo de Gestión de Clientes."""
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

        ctk.CTkButton(frame_controls, text="➕ Añadir Cliente", fg_color="#1F6AA5", hover_color="#185686").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="📧 Enviar Mailing", fg_color="#FF9800", hover_color="#E65100").grid(row=0, column=1, padx=10)
        
        ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Nombre o Cédula...", width=300).grid(row=0, column=3, padx=(100, 10), sticky="e")

        # --- Área de la Tabla ---
        self.create_clients_table(frame_content)

    def create_clients_table(self, parent):
        frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Lista de Clientes Registrados", label_text_color="#333")
        frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        headers = ["ID/Cédula", "Nombre Completo", "Teléfono", "Email", "Última Compra", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(frame_table, text=header, font=("Arial", 14, "bold"), width=150, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

        clients_data = [
            ("12345678", "Juan Pérez", "3001234567", "juan@mail.com", "2025-10-29", ["Editar", "Ver Historial"]),
            ("87654321", "María López", "3009876543", "maria@mail.com", "2025-10-28", ["Editar", "Ver Historial"]),
            ("99887766", "FotoMundo SA", "6076543210", "contacto@fotomundo.co", "2025-10-27", ["Editar", "Ver Historial"]),
            ("22334455", "Carlos A. Rivas", "3154456789", "carlos@ejemplo.com", "2025-10-25", ["Editar", "Ver Historial"]),
            ("55667788", "Diana García", "3209988776", "diana@mail.net", "2025-10-20", ["Editar", "Ver Historial"]),
        ]

        for row_index, (doc, name, phone, email, last_buy, actions) in enumerate(clients_data, start=1):
            ctk.CTkLabel(frame_table, text=doc, width=150, anchor="w", text_color="#333").grid(row=row_index, column=0, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=name, width=150, anchor="w", text_color="#333").grid(row=row_index, column=1, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=phone, width=150, anchor="w", text_color="#333").grid(row=row_index, column=2, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=email, width=150, anchor="w", text_color="#333").grid(row=row_index, column=3, padx=5, pady=2)
            ctk.CTkLabel(frame_table, text=last_buy, width=150, anchor="w", text_color="#333").grid(row=row_index, column=4, padx=5, pady=2)
            
            action_frame = ctk.CTkFrame(frame_table, fg_color="transparent")
            action_frame.grid(row=row_index, column=5, padx=5, pady=2, sticky="w")
            for col_index, action in enumerate(actions):
                ctk.CTkButton(action_frame, text=action, width=80, height=25, font=("Arial", 10), fg_color="#9E9E9E", hover_color="#757575").grid(row=0, column=col_index, padx=2)