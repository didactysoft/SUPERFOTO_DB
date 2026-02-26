import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class InventarioFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.rango_alerta = 5
        
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1)

        # --- CABECERA ---
        header = ctk.CTkFrame(frame_content, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(header, text="CONTROL DE INVENTARIO", 
                     font=("Arial", 24, "bold"), text_color="#CC0000").pack(side="left")
        
        ctk.CTkButton(header, text="⚙️ Alertas", width=100, fg_color="#555",
                      command=self.configurar_alerta).pack(side="right")

        # --- PANEL DE CONTROLES ---
        frame_ctrls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_ctrls.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(frame_ctrls, text="📦 Nuevo Producto", command=self.abrir_form_producto, fg_color="#1F6AA5").grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_ctrls, text="📁 Categorías", command=self.ventana_ver_categorias, fg_color="#2E8B57").grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_ctrls, text="🤝 Proveedores", command=self.ventana_previa_nit, fg_color="#8B4513").grid(row=0, column=2, padx=5)
        
        self.ent_busqueda = ctk.CTkEntry(frame_ctrls, placeholder_text="Buscar producto...", width=250)
        self.ent_busqueda.grid(row=0, column=3, padx=20, sticky="e")
        self.ent_busqueda.bind("<Return>", lambda e: self.cargar_datos_inventario())

        # --- TABLA PRINCIPAL ---
        self.create_inventory_table(frame_content)
        self.cargar_datos_inventario()

    def create_inventory_table(self, parent):
        self.frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Stock de Productos")
        self.frame_table.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        headers = ["ID", "Producto", "Stock", "Ajuste", "Precio", "Proveedor", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_table, text=h, font=("Arial", 12, "bold"), text_color="black").grid(row=0, column=i, padx=10, pady=5)

    def cargar_datos_inventario(self):
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: widget.destroy()
        busqueda = self.ent_busqueda.get().strip()
        query = "SELECT p.id_producto, p.nombre, p.cantidad, p.precio, prov.nombre, p.id_categoria, p.id_proveedor FROM producto p LEFT JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor"
        if busqueda: query += f" WHERE p.nombre LIKE '%{busqueda}%'"
        for row_idx, datos in enumerate(ejecutar_consulta(query), start=1):
            id_p, nom, cant, prec, prov = datos[0], datos[1], datos[2], datos[3], datos[4]
            ctk.CTkLabel(self.frame_table, text=id_p, text_color="black").grid(row=row_idx, column=0)
            ctk.CTkLabel(self.frame_table, text=nom, text_color="black", anchor="w").grid(row=row_idx, column=1)
            color = "red" if (cant or 0) <= self.rango_alerta else "#006400"
            ctk.CTkLabel(self.frame_table, text=str(cant), text_color=color, font=("Arial", 12, "bold")).grid(row=row_idx, column=2)
            f_ajuste = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            f_ajuste.grid(row=row_idx, column=3)
            ctk.CTkButton(f_ajuste, text="-", width=25, fg_color="#E74C3C", command=lambda i=id_p, c=cant: self.ajustar_stock(i, c, -1)).pack(side="left", padx=1)
            ctk.CTkButton(f_ajuste, text="+", width=25, fg_color="#2ECC71", command=lambda i=id_p, c=cant: self.ajustar_stock(i, c, 1)).pack(side="left", padx=1)
            ctk.CTkLabel(self.frame_table, text=f"${prec:.2f}", text_color="black").grid(row=row_idx, column=4)
            ctk.CTkLabel(self.frame_table, text=prov or "N/A", text_color="black").grid(row=row_idx, column=5)
            f_acc = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            f_acc.grid(row=row_idx, column=6)
            ctk.CTkButton(f_acc, text="📝", width=30, fg_color="#F39C12", command=lambda d=datos: self.abrir_form_producto(d)).pack(side="left", padx=2)
            ctk.CTkButton(f_acc, text="🗑️", width=30, fg_color="#AAA", command=lambda i=id_p: self.eliminar_item("producto", "id_producto", i)).pack(side="left", padx=2)

    def ajustar_stock(self, id_p, actual, cambio):
        if ejecutar_accion("UPDATE producto SET cantidad = ? WHERE id_producto = ?", (max(0, actual + cambio), id_p)):
            self.cargar_datos_inventario()

    def configurar_alerta(self):
        res = simpledialog.askinteger("Configurar", "Stock mínimo para alerta:", initialvalue=self.rango_alerta)
        if res is not None: self.rango_alerta = res; self.cargar_datos_inventario()

    # --- CATEGORÍAS ---
    def ventana_ver_categorias(self):
        win = ctk.CTkToplevel(self); win.title("Categorías"); win.geometry("500x450"); win.grab_set()
        ctk.CTkButton(win, text="+ Nueva Categoría", fg_color="#2E8B57", command=lambda: self.abrir_form_categoria(win_p=win)).pack(pady=15)
        scroll = ctk.CTkScrollableFrame(win, fg_color="#EEE"); scroll.pack(fill="both", expand=True, padx=10, pady=10)
        for i, c in enumerate(ejecutar_consulta("SELECT * FROM categoria"), start=1):
            ctk.CTkLabel(scroll, text=f"{c[1]}", text_color="black").grid(row=i, column=0, padx=20, sticky="w")
            ctk.CTkButton(scroll, text="📝", width=35, fg_color="#F39C12", command=lambda d=c: self.abrir_form_categoria(d, win)).grid(row=i, column=1, padx=5)
            ctk.CTkButton(scroll, text="🗑️", width=35, fg_color="#E74C3C", command=lambda id_c=c[0], n=c[1]: self.eliminar_categoria(id_c, n, win)).grid(row=i, column=2, padx=5)

    def abrir_form_categoria(self, datos=None, win_p=None):
        f = ctk.CTkToplevel(self); f.geometry("300x250"); f.grab_set()
        ctk.CTkLabel(f, text="Nombre:").pack(pady=5)
        ent = ctk.CTkEntry(f, width=200); ent.pack(pady=20)
        if datos: ent.insert(0, datos[1])
        def guardar():
            nom = ent.get().strip()
            if not nom: return
            q = "UPDATE categoria SET nombre=? WHERE id_categoria=?" if datos else "INSERT INTO categoria (nombre) VALUES (?)"
            p = (nom, datos[0]) if datos else (nom,)
            if ejecutar_accion(q, p): f.destroy(); win_p.destroy(); self.ventana_ver_categorias()
        ctk.CTkButton(f, text="Guardar", command=guardar).pack()

    def eliminar_categoria(self, id_cat, nombre, win_p):
        conteo = ejecutar_consulta("SELECT COUNT(*) FROM producto WHERE id_categoria = ?", (id_cat,))
        if conteo and conteo[0][0] > 0:
            messagebox.showerror("Error", f"La categoría '{nombre}' tiene productos asociados.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar categoría '{nombre}'?"):
            if ejecutar_accion("DELETE FROM categoria WHERE id_categoria = ?", (id_cat,)):
                win_p.destroy(); self.ventana_ver_categorias()

    # --- PROVEEDORES ---
    def ventana_previa_nit(self):
        v = ctk.CTkToplevel(self); v.title("Proveedores"); v.geometry("400x350"); v.grab_set()
        ctk.CTkButton(v, text="📋 Ver Listado Completo", command=self.ventana_lista_proveedores, fg_color="#555").pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(v, text="O ingrese NIT para Nuevo/Editar:").pack()
        ent = ctk.CTkEntry(v, placeholder_text="NIT"); ent.pack(pady=10)
        def val():
            res = ejecutar_consulta("SELECT * FROM proveedor WHERE documento_nit = ?", (ent.get(),))
            v.destroy(); self.abrir_form_proveedor(datos=res[0] if res else None, nit=ent.get() if not res else None)
        ctk.CTkButton(v, text="Validar NIT", command=val, fg_color="#8B4513").pack(pady=10)

    def ventana_lista_proveedores(self):
        w = ctk.CTkToplevel(self); w.title("Listado Proveedores"); w.geometry("650x450"); w.grab_set()
        s = ctk.CTkScrollableFrame(w, fg_color="#EEE"); s.pack(fill="both", expand=True, padx=10, pady=10)
        for i, p in enumerate(ejecutar_consulta("SELECT * FROM proveedor"), start=1):
            ctk.CTkLabel(s, text=f"{p[1]} | {p[2]}", text_color="black").grid(row=i, column=0, padx=10, sticky="w")
            ctk.CTkButton(s, text="📝", width=35, fg_color="#F39C12", command=lambda d=p: [w.destroy(), self.abrir_form_proveedor(datos=d)]).grid(row=i, column=1, padx=5)
            ctk.CTkButton(s, text="🗑️", width=35, fg_color="#E74C3C", command=lambda id_p=p[0], n=p[2]: self.eliminar_proveedor(id_p, n, w)).grid(row=i, column=2, padx=5)

    def eliminar_proveedor(self, id_prov, nombre, win_p):
        conteo = ejecutar_consulta("SELECT COUNT(*) FROM producto WHERE id_proveedor = ?", (id_prov,))
        if conteo and conteo[0][0] > 0:
            messagebox.showerror("Error", f"El proveedor '{nombre}' tiene productos en el inventario.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar proveedor '{nombre}'?"):
            if ejecutar_accion("DELETE FROM proveedor WHERE id_proveedor = ?", (id_prov,)):
                win_p.destroy(); self.ventana_lista_proveedores()

    def abrir_form_proveedor(self, datos=None, nit=None):
        win = ctk.CTkToplevel(self); win.geometry("400x550"); win.grab_set()
        campos = ["ID", "NIT", "Nombre", "Dirección", "Teléfono", "Correo", "Web"]
        ents = {}
        for i, c in enumerate(campos[1:], start=1):
            ctk.CTkLabel(win, text=c).pack()
            e = ctk.CTkEntry(win, width=300); e.pack()
            if datos:
                e.insert(0, str(datos[i] or ""))
                if c == "NIT": e.configure(state="disabled")
            elif c == "NIT":
                e.insert(0, nit or ""); e.configure(state="disabled")
            ents[c] = e
        def g():
            v = [ents[c].get() for c in campos[2:]]
            if datos: q = "UPDATE proveedor SET nombre=?, direccion=?, telefono=?, correo=?, web=? WHERE documento_nit=?"
            else: q = "INSERT INTO proveedor (documento_nit, nombre, direccion, telefono, correo, web) VALUES (?,?,?,?,?,?)"
            params = (*v, ents["NIT"].get()) if datos else (ents["NIT"].get(), *v)
            if ejecutar_accion(q, params): win.destroy(); self.cargar_datos_inventario()
        ctk.CTkButton(win, text="💾 Guardar Proveedor", command=g, fg_color="#1F6AA5").pack(pady=20)

    # --- PRODUCTOS ---
    def abrir_form_producto(self, datos_edicion=None):
        cats = ejecutar_consulta("SELECT id_categoria, nombre FROM categoria")
        provs = ejecutar_consulta("SELECT id_proveedor, nombre FROM proveedor")
        if not cats or not provs:
            messagebox.showwarning("Aviso", "Registre categorías y proveedores primero.")
            return
        win = ctk.CTkToplevel(self); win.geometry("400x550"); win.grab_set()
        e_nom = ctk.CTkEntry(win, placeholder_text="Nombre", width=300); e_nom.pack(pady=10)
        e_cant = ctk.CTkEntry(win, placeholder_text="Cantidad", width=300); e_cant.pack(pady=10)
        e_prec = ctk.CTkEntry(win, placeholder_text="Precio", width=300); e_prec.pack(pady=10)
        cb_cat = ctk.CTkComboBox(win, values=[c[1] for c in cats], width=300); cb_cat.pack(pady=10)
        cb_prov = ctk.CTkComboBox(win, values=[p[1] for p in provs], width=300); cb_prov.pack(pady=10)
        if datos_edicion:
            e_nom.insert(0, datos_edicion[1]); e_cant.insert(0, str(datos_edicion[2])); e_prec.insert(0, str(datos_edicion[3]))
            for c in cats: 
                if c[0] == datos_edicion[5]: cb_cat.set(c[1])
            for p in provs: 
                if p[0] == datos_edicion[6]: cb_prov.set(p[1])
        def guardar():
            try:
                id_c = cats[[c[1] for c in cats].index(cb_cat.get())][0]
                id_p = provs[[p[1] for p in provs].index(cb_prov.get())][0]
                if datos_edicion:
                    q = "UPDATE producto SET nombre=?, cantidad=?, precio=?, id_categoria=?, id_proveedor=? WHERE id_producto=?"
                    par = (e_nom.get(), int(e_cant.get()), float(e_prec.get()), id_c, id_p, datos_edicion[0])
                else:
                    q = "INSERT INTO producto (nombre, cantidad, precio, id_categoria, id_proveedor) VALUES (?,?,?,?,?)"
                    par = (e_nom.get(), int(e_cant.get()), float(e_prec.get()), id_c, id_p)
                if ejecutar_accion(q, par): win.destroy(); self.cargar_datos_inventario()
            except: messagebox.showerror("Error", "Datos inválidos.")
        ctk.CTkButton(win, text="💾 Guardar Producto", command=guardar, fg_color="#1F6AA5").pack(pady=20)

    def eliminar_item(self, tabla, campo_id, valor_id):
        if messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            if ejecutar_accion(f"DELETE FROM {tabla} WHERE {campo_id} = ?", (valor_id,)):
                self.cargar_datos_inventario()