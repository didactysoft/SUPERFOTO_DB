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

        self.entry_busqueda = ctk.CTkEntry(frame_tools, placeholder_text="Buscar por nombre...", width=300)
        self.entry_busqueda.grid(row=0, column=1, padx=20)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.cargar_tabla())

        self.frame_tabla = None
        self.cargar_tabla()

    def cargar_tabla(self):
        if self.frame_tabla: self.frame_tabla.destroy()
        self.frame_tabla = ctk.CTkScrollableFrame(self)
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure((1,2), weight=1)

        headers = ["ID", "Documento", "Nombre", "Cargo", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_tabla, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, pady=10)

        filtro = f"%{self.entry_busqueda.get()}%"
        query = "SELECT id_empleado, documento, nombre, cargo FROM empleado WHERE nombre LIKE ?"
        
        for row_idx, (eid, doc, nom, car) in enumerate(ejecutar_consulta(query, (filtro,)), start=1):
            ctk.CTkLabel(self.frame_tabla, text=eid).grid(row=row_idx, column=0)
            ctk.CTkLabel(self.frame_tabla, text=doc).grid(row=row_idx, column=1)
            ctk.CTkLabel(self.frame_tabla, text=nom).grid(row=row_idx, column=2)
            ctk.CTkLabel(self.frame_tabla, text=car).grid(row=row_idx, column=3)
            
            # Botones de Acción
            btn_f = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
            btn_f.grid(row=row_idx, column=4)
            ctk.CTkButton(btn_f, text="✏️", width=30, fg_color="#FFB300", text_color="black",
                          command=lambda i=eid: self.abrir_formulario(i)).pack(side="left", padx=2)
            ctk.CTkButton(btn_f, text="🗑️", width=30, fg_color="#E74C3C",
                          command=lambda i=eid: self.eliminar_empleado(i)).pack(side="left", padx=2)

    def abrir_formulario(self, empleado_id=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Formulario Empleado")
        ventana.geometry("400x450")
        ventana.grab_set()

        datos = ["", "", ""]
        if empleado_id:
            res = ejecutar_consulta("SELECT documento, nombre, cargo FROM empleado WHERE id_empleado = ?", (empleado_id,))
            if res: datos = res[0]

        ctk.CTkLabel(ventana, text="Documento:").pack(pady=(20,0))
        ent_doc = ctk.CTkEntry(ventana, width=250); ent_doc.pack(); ent_doc.insert(0, datos[0])
        
        ctk.CTkLabel(ventana, text="Nombre:").pack(pady=10)
        ent_nom = ctk.CTkEntry(ventana, width=250); ent_nom.pack(); ent_nom.insert(0, datos[1])
        
        ctk.CTkLabel(ventana, text="Cargo:").pack(pady=10)
        ent_car = ctk.CTkEntry(ventana, width=250); ent_car.pack(); ent_car.insert(0, datos[2])

        def guardar():
            d, n, c = ent_doc.get(), ent_nom.get(), ent_car.get()
            if not d or not n: return messagebox.showwarning("Error", "Campos obligatorios vacíos")
            
            if empleado_id:
                sql = "UPDATE empleado SET documento=?, nombre=?, cargo=? WHERE id_empleado=?"
                params = (d, n, c, empleado_id)
            else:
                sql = "INSERT INTO empleado (documento, nombre, cargo) VALUES (?,?,?)"
                params = (d, n, c)
            
            if ejecutar_accion(sql, params):
                messagebox.showinfo("Éxito", "Empleado guardado")
                ventana.destroy()
                self.cargar_tabla()

        ctk.CTkButton(ventana, text="💾 Guardar Cambios", command=guardar).pack(pady=30)

    def eliminar_empleado(self, eid):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este empleado permanentemente?"):
            if ejecutar_accion("DELETE FROM empleado WHERE id_empleado=?", (eid,)):
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se puede eliminar: tiene registros vinculados.")