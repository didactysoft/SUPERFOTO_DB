import customtkinter as ctk
from tkinter import messagebox
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class ClientesFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # --- Cabecera ---
        self.label_titulo = ctk.CTkLabel(self, text=f"GESTIÓN DE {title.upper()}", 
                                         font=("Arial", 24, "bold"), text_color="#CC0000")
        self.label_titulo.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # --- Panel de Controles ---
        frame_controls = ctk.CTkFrame(self, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Botón Nuevo Cliente con ventana de validación previa
        ctk.CTkButton(frame_controls, text="➕ Nuevo Cliente", 
                      command=self.ventana_previa_documento, 
                      fg_color="#1F6AA5").grid(row=0, column=0, padx=5)
        
        self.search_entry = ctk.CTkEntry(frame_controls, 
                                         placeholder_text="Buscar en cualquier campo y presiona Enter...", 
                                         width=300)
        self.search_entry.grid(row=0, column=1, padx=10)
        
        # Habilitar búsqueda con la tecla Enter
        self.search_entry.bind("<Return>", lambda event: self.cargar_datos_clientes())
        
        ctk.CTkButton(frame_controls, text="Buscar", 
                      command=self.cargar_datos_clientes).grid(row=0, column=2, padx=5)

        # --- Tabla de Datos ---
        self.create_clients_table()
        self.cargar_datos_clientes()

    def create_clients_table(self):
        self.frame_table = ctk.CTkScrollableFrame(self, fg_color="#F0F0F0", label_text="Clientes Registrados")
        self.frame_table.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Distribución de columnas
        self.frame_table.grid_columnconfigure((0,1,2,3,4), weight=2)
        self.frame_table.grid_columnconfigure(5, weight=1) 
        
        headers = ["Documento", "Nombre", "Teléfono", "Correo", "Dirección", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_table, text=h, font=("Arial", 13, "bold"), 
                         text_color="black").grid(row=0, column=i, pady=5)

    def cargar_datos_clientes(self):
        """Limpia la tabla y carga los datos evitando duplicados visuales."""
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: 
                widget.destroy()

        termino = self.search_entry.get().strip()
        query = "SELECT documento, nombre, telefono, correo, direccion FROM cliente"
        params = ()
        
        if termino:
            query += """ WHERE documento LIKE ? OR nombre LIKE ? OR telefono LIKE ? 
                         OR correo LIKE ? OR direccion LIKE ?"""
            params = (f"%{termino}%", f"%{termino}%", f"%{termino}%", f"%{termino}%", f"%{termino}%")

        for row_idx, datos in enumerate(ejecutar_consulta(query, params), start=1):
            for col_idx, val in enumerate(datos):
                ctk.CTkLabel(self.frame_table, text=val, text_color="black").grid(row=row_idx, column=col_idx, pady=2)
            
            btn_frame = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            btn_frame.grid(row=row_idx, column=5, sticky="nsew")
            btn_frame.grid_columnconfigure((0,1), weight=1)

            ctk.CTkButton(btn_frame, text="✏️", width=30, anchor="center", fg_color="#4CAF50", 
                          command=lambda d=datos: self.abrir_formulario(datos_edicion=d)).grid(row=0, column=0, padx=2, pady=2)
            
            ctk.CTkButton(btn_frame, text="🗑️", width=30, anchor="center", fg_color="#F44336", 
                          command=lambda doc=datos[0]: self.confirmar_borrado(doc)).grid(row=0, column=1, padx=2, pady=2)

    def ventana_previa_documento(self):
        """Ventana intermedia para validar si el documento ya existe."""
        self.win_valida = ctk.CTkToplevel(self)
        self.win_valida.title("Validar Documento")
        self.win_valida.geometry("350x220")
        self.win_valida.grab_set()
        self.win_valida.resizable(False, False)

        ctk.CTkLabel(self.win_valida, text="Ingrese el Documento del Cliente:", 
                     font=("Arial", 13, "bold")).pack(pady=20)
        
        self.ent_doc_valida = ctk.CTkEntry(self.win_valida, width=220)
        self.ent_doc_valida.pack(pady=5)
        self.ent_doc_valida.focus_set()

        btn_validar = ctk.CTkButton(self.win_valida, text="Validar y Continuar", 
                                    command=self.procesar_validacion_previa)
        btn_validar.pack(pady=25)
        
        self.ent_doc_valida.bind("<Return>", lambda e: self.procesar_validacion_previa())

    def procesar_validacion_previa(self):
        """Consulta la base de datos y decide el flujo a seguir."""
        doc = self.ent_doc_valida.get().strip()
        
        if not doc:
            messagebox.showwarning("Atención", "Debe ingresar un número de documento.")
            return

        query = "SELECT documento, nombre, telefono, correo, direccion FROM cliente WHERE documento = ?"
        resultado = ejecutar_consulta(query, (doc,))

        self.win_valida.destroy() # Cerramos la ventana de validación

        if resultado:
            messagebox.showinfo("Registro Encontrado", 
                                f"El documento {doc} ya existe. Cargando datos para actualización.")
            self.abrir_formulario(datos_edicion=resultado[0])
        else:
            self.abrir_formulario(nuevo_doc=doc)

    def abrir_formulario(self, datos_edicion=None, nuevo_doc=None):
        """Carga el formulario en modo registro o actualización."""
        self.ventana_form = ctk.CTkToplevel(self)
        self.ventana_form.title("Formulario de Cliente")
        self.ventana_form.geometry("420x580")
        self.ventana_form.grab_set() 

        main_form_frame = ctk.CTkFrame(self.ventana_form, fg_color="transparent")
        main_form_frame.pack(fill="both", expand=True, padx=35, pady=25)

        campos = ["Documento", "Nombre", "Teléfono", "Correo", "Dirección"]
        self.entries = {}

        for i, campo in enumerate(campos):
            ctk.CTkLabel(main_form_frame, text=campo, font=("Arial", 12, "bold"), 
                         anchor="w").pack(fill="x", pady=(10, 0))
            
            entry = ctk.CTkEntry(main_form_frame, width=320)
            entry.pack(fill="x", pady=5)
            
            # Lógica de autocompletado y bloqueo de documento
            if datos_edicion:
                entry.insert(0, datos_edicion[i])
            elif campo == "Documento" and nuevo_doc:
                entry.insert(0, nuevo_doc)
            
            if campo == "Documento" and (datos_edicion or nuevo_doc):
                entry.configure(state="disabled") # No permitir cambiar el documento validado

            self.entries[campo] = entry
            entry.bind("<Return>", lambda e: self.validar_y_guardar(datos_edicion is not None))

        btn_txt = "Actualizar Información" if datos_edicion else "Registrar Nuevo Cliente"
        ctk.CTkButton(main_form_frame, text=btn_txt, font=("Arial", 13, "bold"),
                      command=lambda: self.validar_y_guardar(datos_edicion is not None),
                      height=45, fg_color="#1F6AA5").pack(fill="x", pady=35)

    def validar_y_guardar(self, es_edicion):
        """Procesa el INSERT o UPDATE en la base de datos."""
        # Se usa normal para el documento ya que está deshabilitado en el widget
        doc_val = self.entries["Documento"].get() 
        datos = [doc_val] + [self.entries[c].get().strip() for c in ["Nombre", "Dirección", "Teléfono", "Correo"]]
        
        if not doc_val or not datos[1]:
            messagebox.showerror("Campos Incompletos", "Documento y Nombre son obligatorios.")
            return

        if messagebox.askyesno("Confirmar", "¿Desea guardar los cambios en la base de datos?"):
            if es_edicion:
                # Query de actualización
                query = "UPDATE cliente SET nombre=?, direccion=?, telefono=?, correo=? WHERE documento=?"
                params = (datos[1], datos[2], datos[3], datos[4], datos[0])
            else:
                # Query de inserción respetando el UNIQUE
                query = "INSERT INTO cliente (documento, nombre, direccion, telefono, correo) VALUES (?,?,?,?,?)"
                params = tuple(datos)

            if ejecutar_accion(query, params):
                messagebox.showinfo("Éxito", "Datos guardados correctamente.")
                self.ventana_form.destroy()
                self.cargar_datos_clientes()

    def confirmar_borrado(self, documento):
        if messagebox.askyesno("Atención", f"¿Eliminar permanentemente al cliente {documento}?\nEsta acción es irreversible."):
            if ejecutar_accion("DELETE FROM cliente WHERE documento = ?", (documento,)):
                messagebox.showinfo("Eliminado", "El registro ha sido removido.")
                self.cargar_datos_clientes()