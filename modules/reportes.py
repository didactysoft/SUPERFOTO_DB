import customtkinter as ctk

class ReportesFrame(ctk.CTkFrame):
    """Módulo de Generación y Visualización de Reportes."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1) # Fila del área de visualización expandible

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Opciones de Reporte (Fila 1) ---
        frame_options = ctk.CTkFrame(frame_content, fg_color="#F0F0F0")
        frame_options.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_options.grid_columnconfigure(0, weight=1)
        frame_options.grid_columnconfigure(1, weight=1)

        # Columna 1: Tipo de Reporte y Generar
        frame_col1 = ctk.CTkFrame(frame_options, fg_color="transparent")
        frame_col1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        ctk.CTkLabel(frame_col1, text="Tipo de Reporte:", font=("Arial", 16, "bold"), text_color="#333").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        report_types = ["Ventas por Mes", "Productos Más Vendidos", "Pedidos por Estado", "Clientes Top", "Rentabilidad"]
        report_combobox = ctk.CTkComboBox(frame_col1, values=report_types, width=250)
        report_combobox.set("Ventas por Mes")
        report_combobox.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkButton(frame_col1, text="📈 Generar Reporte", fg_color="#1F6AA5", hover_color="#185686", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="w")


        # Columna 2: Rango de Fechas
        frame_col2 = ctk.CTkFrame(frame_options, fg_color="transparent")
        frame_col2.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(frame_col2, text="Rango de Fechas:", font=("Arial", 16, "bold"), text_color="#333").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_col2, text="Inicio:", text_color="#333").grid(row=1, column=0, padx=5, sticky="w")
        ctk.CTkEntry(frame_col2, placeholder_text="YYYY-MM-DD", width=150).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_col2, text="Fin:", text_color="#333").grid(row=2, column=0, padx=5, sticky="w")
        ctk.CTkEntry(frame_col2, placeholder_text="YYYY-MM-DD", width=150).grid(row=2, column=1, padx=5, pady=5, sticky="w")


        # --- Área de Visualización (Fila 2) ---
        # Simulación de Gráfico/Resultado - Un gran área para mostrar los datos
        ctk.CTkLabel(frame_content, 
                     text="[Área de Visualización de Gráficos/Gráficas y Tablas del Reporte Generado]", 
                     font=("Arial", 20), text_color="#9E9E9E", height=300, fg_color="#E0E0E0", corner_radius=10,
                     justify="center").grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        frame_content.grid_rowconfigure(2, weight=4) # Asegura que el área de visualización se expanda