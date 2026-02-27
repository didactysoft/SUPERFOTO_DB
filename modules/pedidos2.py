import customtkinter as ctk
from tkinter import messagebox
from modules.database_manager import ejecutar_consulta, ejecutar_accion
from datetime import datetime

class PedidosFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Estado del pedido actual
        self.id_cliente_sel = None
        self.lista_items = []
        self.abono_total = 0.0

        # Contenedor Principal (Estilo Imagen)
        self.main_container = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # --- CABECERA ROJA ---
        header = ctk.CTkFrame(self.main_container, fg_color="#D32F2F", height=50, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(header, text="Agregar nuevo trabajo", text_color="white", font=("Arial", 18, "bold")).pack(pady=10)

        # --- CUERPO DIVIDIDO ---
        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        body.grid_columnconfigure(0, weight=1) # Columna Clientes
        body.grid_columnconfigure(1, weight=3) # Columna Formulario

        # ==========================================
        # COLUMNA IZQUIERDA: DATOS DE CLIENTE
        # ==========================================
        frame_cliente = ctk.CTkFrame(body, fg_color="white", border_width=1, border_color="#E0E0E0")
        frame_cliente.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(frame_cliente, text="Datos de cliente", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.info_cliente_txt = ctk.CTkLabel(frame_cliente, text="Cédula/NIT:\nNombre:\nTeléfono:\nDirección:", 
                                             justify="left", anchor="w", font=("Arial", 12), text_color="gray")
        self.info_cliente_txt.pack(fill="x", padx=10, pady=10)

        # Buscador
        search_f = ctk.CTkFrame(frame_cliente, fg_color="transparent")
        search_f.pack(fill="x", padx=10)
        self.ent_bus_cli = ctk.CTkEntry(search_f, placeholder_text="Cédula / Nombre / Tel", height=35)
        self.ent_bus_cli.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(search_f, text="🔍", width=40, fg_color="white", border_width=1, text_color="black", 
                      command=self.buscar_clientes).pack(side="left", padx=2)

        self.scroll_cli = ctk.CTkScrollableFrame(frame_cliente, height=200, fg_color="#F9F9F9")
        self.scroll_cli.pack(fill="x", padx=10, pady=10)

        # ==========================================
        # COLUMNA DERECHA: ITEMS Y PAGOS
        # ==========================================
        frame_form = ctk.CTkScrollableFrame(body, fg_color="white")
        frame_form.grid(row=0, column=1, sticky="nsew")

        # Título y Observaciones
        ctk.CTkLabel(frame_form, text="Título: *").pack(anchor="w", padx=20)
        self.ent_titulo = ctk.CTkEntry(frame_form, placeholder_text="Nombre del trabajo"); self.ent_titulo.pack(fill="x", padx=20, pady=5)
        
        # Sección Items
        ctk.CTkLabel(frame_form, text="Items del trabajo", font=("Arial", 14, "bold")).pack(pady=10)
        
        f_add_item = ctk.CTkFrame(frame_form, fg_color="#F5F5F5")
        f_add_item.pack(fill="x", padx=20, pady=5)
        
        self.cb_prod = ctk.CTkComboBox(f_add_item, values=self.obtener_productos(), width=200)
        self.cb_prod.grid(row=0, column=0, padx=5, pady=5)
        
        self.en_cant = ctk.CTkEntry(f_add_item, placeholder_text="Cant", width=60); self.en_cant.grid(row=0, column=1, padx=5)
        self.en_desc_manual = ctk.CTkEntry(f_add_item, placeholder_text="Descripción (si no está registrado)", width=250); self.en_desc_manual.grid(row=0, column=2, padx=5)
        self.en_precio_man = ctk.CTkEntry(f_add_item, placeholder_text="Valor Unit.", width=100); self.en_precio_man.grid(row=0, column=3, padx=5)
        
        ctk.CTkButton(f_add_item, text="Agregar", fg_color="#D32F2F", command=self.agregar_item_lista).grid(row=0, column=4, padx=5)

        # Tabla de Items agregados
        self.frame_lista_items = ctk.CTkFrame(frame_form, fg_color="transparent")
        self.frame_lista_items.pack(fill="x", padx=20, pady=10)

        # Totales y Pagos
        self.lbl_resumen_finan = ctk.CTkLabel(frame_form, text="Total items: $0\nTotal abonos: $0\nSaldo: $0", 
                                              justify="right", font=("Arial", 14, "bold"), text_color="#D32F2F")
        self.lbl_resumen_finan.pack(anchor="e", padx=20, pady=10)

        # Sección Abonos
        f_abono = ctk.CTkFrame(frame_form, fg_color="#E8F5E9")
        f_abono.pack(fill="x", padx=20, pady=10)
        self.en_abono = ctk.CTkEntry(f_abono, placeholder_text="Monto Abono $"); self.en_abono.pack(side="left", padx=10, pady=10)
        ctk.CTkButton(f_abono, text="💵 Registrar Abono", fg_color="#2E7D32", command=self.registrar_abono).pack(side="left", padx=10)

        # Tiempos de Entrega
        f_entrega = ctk.CTkFrame(frame_form, fg_color="transparent")
        f_entrega.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(f_entrega, text="Fecha Entrega:").grid(row=0, column=0)
        self.ent_f_ent = ctk.CTkEntry(f_entrega, placeholder_text="AAAA-MM-DD"); self.ent_f_ent.grid(row=0, column=1, padx=10)
        ctk.CTkLabel(f_entrega, text="Hora:").grid(row=0, column=2)
        self.ent_h_ent = ctk.CTkEntry(f_entrega, placeholder_text="HH:MM"); self.ent_h_ent.grid(row=0, column=3, padx=10)

        # Botón Guardar
        ctk.CTkButton(frame_form, text="💾 GUARDAR PEDIDO", height=50, fg_color="#1F6AA5", command=self.guardar_db).pack(fill="x", padx=20, pady=20)

    # ==========================================
    # LÓGICA OPERATIVA
    # ==========================================

    def obtener_productos(self):
        res = ejecutar_consulta("SELECT nombre FROM producto")
        return [r[0] for r in res] + ["-- SERVICIO PERSONALIZADO --"]

    def buscar_clientes(self):
        dato = self.ent_bus_cli.get()
        query = "SELECT id_cliente, nombre, cedula_nit, telefono FROM cliente"
        params = ()
        if dato:
            query += " WHERE nombre LIKE ? OR cedula_nit LIKE ? OR telefono LIKE ?"
            params = (f"%{dato}%", f"%{dato}%", f"%{dato}%")
        
        for w in self.scroll_cli.winfo_children(): w.destroy()
        
        for cid, nom, nit, tel in ejecutar_consulta(query, params):
            ctk.CTkButton(self.scroll_cli, text=f"{nom} ({nit})", fg_color="transparent", text_color="black", anchor="w",
                          command=lambda c=cid, n=nom, ni=nit, t=tel: self.seleccionar_cliente(c, n, ni, t)).pack(fill="x")

    def seleccionar_cliente(self, cid, nom, nit, tel):
        self.id_cliente_sel = cid
        self.info_cliente_txt.configure(text=f"Cédula/NIT: {nit}\nNombre: {nom}\nTeléfono: {tel}\nID: {cid}", text_color="black")

    def agregar_item_lista(self):
        prod_nom = self.cb_prod.get()
        try:
            cant = int(self.en_cant.get() or 1)
            desc = self.en_desc_manual.get()
            
            if prod_nom == "-- SERVICIO PERSONALIZADO --":
                id_p = None
                precio = float(self.en_precio_man.get())
                nombre = desc if desc else "Servicio manual"
            else:
                res = ejecutar_consulta("SELECT id_producto, precio FROM producto WHERE nombre=?", (prod_nom,))
                id_p, precio = res[0]
                nombre = prod_nom

            self.lista_items.append({'id': id_p, 'nom': nombre, 'pre': precio, 'cant': cant, 'desc': desc})
            self.actualizar_vista_items()
        except:
            messagebox.showerror("Error", "Ingrese precio y cantidad válidos")

    def registrar_abono(self):
        try:
            self.abono_total += float(self.en_abono.get() or 0)
            self.en_abono.delete(0, 'end')
            self.actualizar_vista_items()
        except: messagebox.showerror("Error", "Monto inválido")

    def actualizar_vista_items(self):
        for w in self.frame_lista_items.winfo_children(): w.destroy()
        total = 0
        for i, it in enumerate(self.lista_items):
            sub = it['pre'] * it['cant']
            total += sub
            f = ctk.CTkFrame(self.frame_lista_items, fg_color="#F9F9F9")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{it['nom']} x{it['cant']}").pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"${sub:,.2f}", font=("Arial", 12, "bold")).pack(side="right", padx=20)
            ctk.CTkButton(f, text="X", width=20, fg_color="red", command=lambda idx=i: [self.lista_items.pop(idx), self.actualizar_vista_items()]).pack(side="right")
        
        saldo = total - self.abono_total
        self.lbl_resumen_finan.configure(text=f"Total items: ${total:,.2f}\nTotal abonos: ${self.abono_total:,.2f}\nSaldo: ${saldo:,.2f}")

    def guardar_db(self):
        if not self.id_cliente_sel or not self.lista_items:
            return messagebox.showerror("Error", "Faltan datos (Cliente o Items)")
        
        id_user = 1 # Placeholder: Aquí debe ir el ID del usuario logueado
        f_ped = datetime.now().strftime("%Y-%m-%d")
        h_ped = datetime.now().strftime("%H:%M")
        
        sql_p = "INSERT INTO pedido (id_cliente, id_usuario, fecha_pedido, hora_pedido, fecha_entrega, hora_entrega, estado) VALUES (?,?,?,?,?,?,?)"
        if ejecutar_accion(sql_p, (self.id_cliente_sel, id_user, f_ped, h_ped, self.ent_f_ent.get(), self.ent_h_ent.get(), "Pendiente")):
            id_ped = ejecutar_consulta("SELECT last_insert_rowid()")[0][0]
            for i, it in enumerate(self.lista_items):
                abono_ins = self.abono_total if i == 0 else 0 # Se asigna el abono al primer registro
                sql_d = "INSERT INTO detallepedido (id_pedido, id_producto, precio_unidad, cantidad, abono, descripcion) VALUES (?,?,?,?,?,?)"
                ejecutar_accion(sql_d, (id_ped, it['id'], it['pre'], it['cant'], abono_ins, it['desc']))
            
            messagebox.showinfo("Éxito", "Trabajo guardado")
            self.main_container.destroy() # O limpiar campos