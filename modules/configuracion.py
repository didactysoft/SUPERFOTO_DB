import customtkinter as ctk

class ConfiguracionFrame(ctk.CTkFrame):
    """Módulo de Configuración del Sistema."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(1, weight=1) # Fila del área de opciones expandible

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Opciones (Scrollable) ---
        frame_options = ctk.CTkScrollableFrame(frame_content, fg_color="#F0F0F0", label_text="Opciones del Sistema", label_text_color="#333")
        frame_options.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_options.grid_columnconfigure(0, weight=1)

        # -------------------
        # 1. Configuración General
        # -------------------
        self.create_settings_section(frame_options, "Datos de la Empresa", 0, [
            ("Nombre de la Empresa:", "SUPERFOTO S.A.S.", "entry"),
            ("NIT/RUC:", "900.123.456-7", "entry"),
            ("Dirección:", "Calle 10 # 5-20, Centro", "entry"),
            ("Teléfono Contacto:", "607-6789012", "entry"),
            ("Moneda Predeterminada:", ["COP (Peso Colombiano)", "USD (Dólar)", "EUR (Euro)"], "combo", "COP (Peso Colombiano)"),
        ])

        # -------------------
        # 2. Preferencias de Usuario
        # -------------------
        self.create_settings_section(frame_options, "Preferencias de Usuario", 1, [
            ("Modo de Apariencia:", ["Light", "Dark", "System"], "combo", "Light"),
            ("Idioma:", ["Español", "Inglés"], "combo", "Español"),
            ("Mostrar Alertas de Stock:", "Activado", "switch"),
            ("Notificaciones por Email:", "Desactivado", "switch"),
        ])

        # -------------------
        # 3. Impresión y Facturación
        # -------------------
        self.create_settings_section(frame_options, "Configuración de Impresión y Documentos", 2, [
            ("Impresora Predeterminada:", ["Plotter Canon", "Epson L3110", "Laser B/N"], "combo", "Plotter Canon"),
            ("Formato de Factura:", ["Estándar A4", "Térmico 80mm"], "combo", "Estándar A4"),
            ("Prefijo de Factura (EJ: SF-):", "SF-", "entry"),
        ])
        
        # Botón Guardar
        ctk.CTkButton(frame_content, text="💾 Guardar Cambios", fg_color="#4CAF50", hover_color="#388E3C", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=20, pady=10, sticky="e")


    def create_settings_section(self, parent, title, row_start, settings_list):
        """
        Helper para crear secciones de configuración con título y controles.
        settings_list: Lista de tuplas (Label, DefaultValue/Values, ControlType, DefaultSelection*)
        """
        frame_section = ctk.CTkFrame(parent, fg_color="white", corner_radius=8, border_width=1, border_color="#D0D0D0")
        frame_section.grid(row=row_start, column=0, padx=15, pady=15, sticky="ew")
        frame_section.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_section, text=title, font=("Arial", 18, "bold"), text_color="#1F6AA5").grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 10), sticky="w")

        for i, setting in enumerate(settings_list, start=1):
            label_text = setting[0]
            default_value = setting[1]
            control_type = setting[2]
            default_selection = setting[3] if control_type == "combo" and len(setting) > 3 else None

            ctk.CTkLabel(frame_section, text=label_text, anchor="w", width=200, text_color="#333").grid(row=i, column=0, padx=15, pady=5, sticky="w")
            
            # Control
            if control_type == "entry":
                control = ctk.CTkEntry(frame_section, width=300)
                control.insert(0, default_value)
            elif control_type == "combo":
                control = ctk.CTkComboBox(frame_section, values=default_value, width=300)
                if default_selection:
                    control.set(default_selection)
            elif control_type == "switch":
                is_checked = default_value == "Activado"
                control = ctk.CTkSwitch(frame_section, text="", onvalue="Activado", offvalue="Desactivado")
                if is_checked:
                    control.select()
                
            # Asignar el control a la cuadrícula
            control.grid(row=i, column=1, padx=15, pady=5, sticky="ew")