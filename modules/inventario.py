import customtkinter as ctk
from tkinter import messagebox
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class InventarioFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, text=f"GESTIÓN DE {title.upper()}", 
                     font=("Arial", 24, "bold"), text_color="#CC0000").grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # --- Panel de Controles ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(frame_controls, text="📦 Nuevo Producto", command=self.abrir_form_producto, fg_color="#1F6AA5").grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_controls, text="📁 Categorías", command=self.ventana_ver_categorias, fg_color="#2E8B57").grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_controls, text="🤝 Proveedores", command=self.ventana_previa_nit, fg_color="#8B4513").grid(row=0, column=2, padx=5)
        
        self.entry_busqueda = ctk.CTkEntry(frame_controls, placeholder_text="Buscar producto...", width=250)
        self.entry_busqueda.grid(row=0, column=3, padx=20, sticky="e")
        self.entry_busqueda.bind("<Return>", lambda e: self.cargar_datos_inventario())

        # --- Tabla Principal ---
        self.create_inventory_table(frame_content)
        self.cargar_datos_inventario()

    def create_inventory_table(self, parent):
        self.frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Stock de Productos")
        self.frame_table.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        headers = ["ID", "Producto", "Stock", "Precio", "Categoría", "Proveedor", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_table, text=h, font=("Arial", 13, "bold"), text_color="black").grid(row=0, column=i, padx=10, pady=5)

    def cargar_datos_inventario(self):
        """Carga productos con JOIN para ver nombres en lugar de IDs."""
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: widget.destroy()

        query = """
            SELECT p.id_producto, p.nombre, p.cantidad, p.precio, c.nombre, prov.nombre
            FROM producto p
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            LEFT JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor
        """
        for row_idx, (id_p, nom, cant, prec, cat, prov) in enumerate(ejecutar_consulta(query), start=1):
            ctk.CTkLabel(self.frame_table, text=id_p, text_color="black").grid(row=row_idx, column=0)
            ctk.CTkLabel(self.frame_table, text=nom, text_color="black", anchor="w").grid(row=row_idx, column=1)
            color_stock = "red" if (cant or 0) < 5 else "black"
            ctk.CTkLabel(self.frame_table, text=cant, text_color=color_stock, font=("Arial", 12, "bold")).grid(row=row_idx, column=2)
            ctk.CTkLabel(self.frame_table, text=f"${prec:.2f}", text_color="black").grid(row=row_idx, column=3)
            ctk.CTkLabel(self.frame_table, text=cat or "N/A", text_color="black").grid(row=row_idx, column=4)
            ctk.CTkLabel(self.frame_table, text=prov or "N/A", text_color="black").grid(row=row_idx, column=5)
            ctk.CTkButton(self.frame_table, text="🗑️", width=30, fg_color="#F44336", 
                          command=lambda id_p=id_p: self.eliminar_item("producto", "id_producto", id_p)).grid(row=row_idx, column=6)

    # --- LÓGICA DE PROVEEDORES ---

    def ventana_previa_nit(self):
        """Ventana de validación similar a clientes."""
        self.win_v = ctk.CTkToplevel(self)
        self.win_v.title("Validar Proveedor")
        self.win_v.geometry("400x300")
        self.win_v.grab_set()

        ctk.CTkButton(self.win_v, text="📋 Seleccionar del Listado", fg_color="#555", 
                      command=self.ventana_lista_proveedores).pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(self.win_v, text="O ingrese NIT para validar:").pack()
        self.ent_nit_val = ctk.CTkEntry(self.win_v, width=200); self.ent_nit_val.pack(pady=5)

        ctk.CTkButton(self.win_v, text="Validar NIT", command=self.validar_nit_manual, fg_color="#8B4513").pack(pady=20)

    def ventana_lista_proveedores(self):
        """Muestra lista y permite elegir uno."""
        win_list = ctk.CTkToplevel(self)
        win_list.title("Seleccionar Proveedor")
        win_list.geometry("600x400")
        win_list.grab_set()

        scroll = ctk.CTkScrollableFrame(win_list, fg_color="#EEE")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        provs = ejecutar_consulta("SELECT * FROM proveedor")
        for i, p in enumerate(provs):
            ctk.CTkLabel(scroll, text=f"{p[1]} - {p[2]}", text_color="black").grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkButton(scroll, text="Elegir", width=60, 
                          command=lambda datos=p: self.seleccionar_y_abrir(datos, win_list)).grid(row=i, column=1)

    def seleccionar_y_abrir(self, datos, win_list):
        win_list.destroy()
        if hasattr(self, 'win_v'): self.win_v.destroy()
        self.abrir_form_proveedor(datos_edicion=datos)

    def validar_nit_manual(self):
        nit = self.ent_nit_val.get().strip()
        if not nit: return
        res = ejecutar_consulta("SELECT * FROM proveedor WHERE documento_nit = ?", (nit,))
        self.win_v.destroy()
        if res: self.abrir_form_proveedor(datos_edicion=res[0])
        else: self.abrir_form_proveedor(nuevo_nit=nit)

    def abrir_form_proveedor(self, datos_edicion=None, nuevo_nit=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Formulario Proveedor")
        ventana.geometry("400x500")
        ventana.grab_set()

        campos = ["NIT", "Nombre", "Dirección", "Teléfono", "Correo", "Web"]
        self.ents = {}
        # Mapeo según SQL: id(0), nit(1), nombre(2), dir(3), tel(4), correo(5), web(6)
        for i, campo in enumerate(campos):
            ctk.CTkLabel(ventana, text=campo).pack()
            entry = ctk.CTkEntry(ventana, width=300); entry.pack(pady=2)
            if datos_edicion: entry.insert(0, str(datos_edicion[i+1] or ""))
            elif campo == "NIT": entry.insert(0, nuevo_nit); entry.configure(state="disabled")
            self.ents[campo] = entry

        def guardar():
            vals = [self.ents[c].get() for c in campos[1:]]
            nit = self.ents["NIT"].get()
            if datos_edicion:
                ejecutar_accion("UPDATE proveedor SET nombre=?, direccion=?, telefono=?, correo=?, web=? WHERE documento_nit=?", (*vals, nit))
            else:
                ejecutar_accion("INSERT INTO proveedor (documento_nit, nombre, direccion, telefono, correo, web) VALUES (?,?,?,?,?,?)", (nit, *vals))
            messagebox.showinfo("Éxito", "Proveedor guardado"); ventana.destroy()

        ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=20)

    # --- CATEGORÍAS Y PRODUCTOS ---

    def ventana_ver_categorias(self):
        win = ctk.CTkToplevel(self); win.title("Categorías"); win.geometry("400x400"); win.grab_set()
        ctk.CTkButton(win, text="+ Nueva", command=self.abrir_form_categoria).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        for i, c in enumerate(ejecutar_consulta("SELECT * FROM categoria")):
            ctk.CTkLabel(scroll, text=f"{c[0]} - {c[1]}").grid(row=i, column=0, padx=20)

    def abrir_form_categoria(self):
        win = ctk.CTkToplevel(self); win.geometry("300x200"); win.grab_set()
        ent = ctk.CTkEntry(win, placeholder_text="Nombre"); ent.pack(pady=20)
        def g():
            if ent.get() and ejecutar_accion("INSERT INTO categoria (nombre) VALUES (?)", (ent.get(),)):
                win.destroy()
        ctk.CTkButton(win, text="Guardar", command=g).pack()

    def abrir_form_producto(self):
        cats = ejecutar_consulta("SELECT id_categoria, nombre FROM categoria")
        provs = ejecutar_consulta("SELECT id_proveedor, nombre FROM proveedor")
        if not cats or not provs: 
            messagebox.showwarning("Aviso", "Registre categorías y proveedores primero."); return

        win = ctk.CTkToplevel(self); win.geometry("400x550"); win.grab_set()
        ctk.CTkLabel(win, text="Nombre:").pack()
        e_nom = ctk.CTkEntry(win, width=300); e_nom.pack()
        ctk.CTkLabel(win, text="Cantidad:").pack()
        e_cant = ctk.CTkEntry(win, width=300); e_cant.pack()
        ctk.CTkLabel(win, text="Precio:").pack()
        e_prec = ctk.CTkEntry(win, width=300); e_prec.pack()
        
        cb_cat = ctk.CTkComboBox(win, values=[c[1] for c in cats], width=300); cb_cat.pack(pady=10)
        cb_prov = ctk.CTkComboBox(win, values=[p[1] for p in provs], width=300); cb_prov.pack(pady=10)

        def g():
            try:
                id_c = cats[[c[1] for c in cats].index(cb_cat.get())][0]
                id_p = provs[[p[1] for p in provs].index(cb_prov.get())][0]
                if ejecutar_accion("INSERT INTO producto (nombre, cantidad, precio, id_categoria, id_proveedor) VALUES (?,?,?,?,?)", 
                                   (e_nom.get(), int(e_cant.get()), float(e_prec.get()), id_c, id_p)):
                    win.destroy(); self.cargar_datos_inventario()
            except: messagebox.showerror("Error", "Datos inválidos")
        ctk.CTkButton(win, text="Guardar Producto", command=g).pack(pady=20)

    def eliminar_item(self, tabla, campo_id, valor_id):
        if messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            if ejecutar_accion(f"DELETE FROM {tabla} WHERE {campo_id} = ?", (valor_id,)):
                self.cargar_datos_inventario()