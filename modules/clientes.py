import customtkinter as ctk

class ClientesFrame(ctk.CTkFrame):
    """
    Marco para la gestión de Clientes (CRUD: Crear, Leer, Actualizar, Borrar).
    Este frame se carga dentro de la ventana principal (MainApp).
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Asegura que el contenido se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Fila 2 para la tabla/lista principal

        # --- Título del Módulo ---
        ctk.CTkLabel(self, text="👤 Módulo de Gestión de Clientes",
                     font=("Arial", 28, "bold"), text_color="#1F6AA5").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Barra de Búsqueda y Botones ---
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        control_frame.grid_columnconfigure((0, 1), weight=1) # Para centrar los widgets

        # Búsqueda
        search_entry = ctk.CTkEntry(control_frame, placeholder_text="Buscar cliente (Nombre, ID, Teléfono...)", width=400)
        search_entry.pack(side="left", padx=(0, 15))

        # Botón Nuevo Cliente
        ctk.CTkButton(control_frame, text="➕ Nuevo Cliente", 
                      command=self.open_new_client_window, 
                      fg_color="#00A859", hover_color="#008044").pack(side="right")
        
        # --- Área de Listado de Clientes (Simulación) ---
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(list_frame, text="[Aquí se mostrará la tabla o lista de clientes]",
                     font=("Arial", 16), text_color="#666666").grid(row=0, column=0, padx=50, pady=50)

    def open_new_client_window(self):
        """Función placeholder para abrir una ventana de creación de cliente."""
        print("Abriendo ventana para crear un nuevo cliente...")
        # En una aplicación real, aquí se llamaría a una CTkTopLevel para el formulario.

# --- Ejemplo de ejecución (opcional, para probar el frame individualmente) ---
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Prueba de Módulo Clientes")
    
    # El frame del módulo ocupa toda la ventana de prueba
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    
    clientes_view = ClientesFrame(app)
    clientes_view.grid(row=0, column=0, sticky="nsew")
    
    app.mainloop()