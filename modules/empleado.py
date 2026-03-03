import customtkinter as ctk
from tkinter import messagebox
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class EmpleadosFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        ctk.CTkLabel(self, text=f"GESTIÓN DE {title.upper()}", 
                     font=("Arial", 24, "bold"), text_color="#A30000").grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        frame_tools = ctk.CTkFrame(self, fg_color="transparent")
        frame_tools.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkButton(frame_tools, text="➕ Nuevo Empleado", fg_color="#2ECC71", 
                      command=self.abrir_formulario).grid(row=0, column=0, padx=5)

        self.entry_busqueda = ctk.CTkEntry(frame_tools, placeholder_text="Buscar por nombre o documento...", width=300)
        self.entry_busqueda.grid(row=0, column=1, padx=20)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.cargar_tabla())

        self.frame_tabla = None
        self.cargar_tabla()

    def cargar_tabla(self):
        if self.frame_tabla: self.frame_tabla.destroy()
        self.frame_tabla = ctk.CTkScrollableFrame(self)
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Ajustamos columnas para que la tabla se vea equilibrada
        self.frame_tabla.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)

        # Actualización de encabezados
        headers = ["ID", "Documento", "Nombre", "Cargo", "Teléfono", "Correo", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_tabla, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=10)

        filtro = f"%{self.entry_busqueda.get()}%"
        # SQL actualizado para traer los campos nuevos
        query = "SELECT id_empleado, documento, nombre, cargo, telefono, correo FROM empleado WHERE nombre LIKE ? OR documento LIKE ?"
        
        for row_idx, (eid, doc, nom, car, tel, cor) in enumerate(ejecutar_consulta(query, (filtro, filtro)), start=1):
            ctk.CTkLabel(self.frame_tabla, text=eid).grid(row=row_idx, column=0)
            ctk.CTkLabel(self.frame_tabla, text=doc).grid(row=row_idx, column=1)
            ctk.CTkLabel(self.frame_tabla, text=nom).grid(row=row_idx, column=2)
            ctk.CTkLabel(self.frame_tabla, text=car).grid(row=row_idx, column=3)
            ctk.CTkLabel(self.frame_tabla, text=tel).grid(row=row_idx, column=4)
            ctk.CTkLabel(self.frame_tabla, text=cor).grid(row=row_idx, column=5)
            
            # Botones de Acción
            btn_f = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
            btn_f.grid(row=row_idx, column=6)
            ctk.CTkButton(btn_f, text="✏️", width=30, fg_color="#FFB300", text_color="black",
                          command=lambda i=eid: self.abrir_formulario(i)).pack(side="left", padx=2)
            ctk.CTkButton(btn_f, text="🗑️", width=30, fg_color="#E74C3C",
                          command=lambda i=eid: self.eliminar_empleado(i)).pack(side="left", padx=2)

    def abrir_formulario(self, empleado_id=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Formulario Empleado")
        ventana.geometry("450x650") # Aumentamos altura para los nuevos campos
        ventana.grab_set()

        # Datos por defecto (vacíos) - 6 campos ahora
        datos = ["", "", "", "", "", ""]
        if empleado_id:
            sql = "SELECT documento, nombre, cargo, direccion, telefono, correo FROM empleado WHERE id_empleado = ?"
            res = ejecutar_consulta(sql, (empleado_id,))
            if res: datos = res[0]

        # --- Interfaz del Formulario ---
        def crear_campo(label_text, default_val):
            ctk.CTkLabel(ventana, text=label_text).pack(pady=(10, 0))
            entry = ctk.CTkEntry(ventana, width=300)
            entry.pack()
            entry.insert(0, default_val)
            return entry

        ent_doc = crear_campo("Documento:", datos[0])
        ent_nom = crear_campo("Nombre Completo:", datos[1])
        ent_car = crear_campo("Cargo:", datos[2])
        ent_dir = crear_campo("Dirección:", datos[3])
        ent_tel = crear_campo("Teléfono:", datos[4])
        ent_cor = crear_campo("Correo Electrónico:", datos[5])

        def guardar():
            d, n, c = ent_doc.get(), ent_nom.get(), ent_car.get()
            di, t, co = ent_dir.get(), ent_tel.get(), ent_cor.get()
            
            if not d or not n: 
                return messagebox.showwarning("Error", "Documento y Nombre son obligatorios")
            
            if empleado_id:
                # SQL UPDATE actualizado
                sql = """UPDATE empleado SET documento=?, nombre=?, cargo=?, 
                         direccion=?, telefono=?, correo=? WHERE id_empleado=?"""
                params = (d, n, c, di, t, co, empleado_id)
            else:
                # SQL INSERT actualizado
                sql = """INSERT INTO empleado (documento, nombre, cargo, direccion, telefono, correo) 
                         VALUES (?,?,?,?,?,?)"""
                params = (d, n, c, di, t, co)
            
            if ejecutar_accion(sql, params):
                messagebox.showinfo("Éxito", "Empleado guardado correctamente")
                ventana.destroy()
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos")

        ctk.CTkButton(ventana, text="💾 Guardar Cambios", fg_color="#2874A6",
                      command=guardar).pack(pady=30)

    def eliminar_empleado(self, eid):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este empleado permanentemente?"):
            if ejecutar_accion("DELETE FROM empleado WHERE id_empleado=?", (eid,)):
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se puede eliminar: tiene registros vinculados en otras tablas.")