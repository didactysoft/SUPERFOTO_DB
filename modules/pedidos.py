import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from modules.database_manager import ejecutar_consulta, ejecutar_accion
from datetime import datetime

class PedidosFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Variables de control de estado
        self.id_cliente_sel = None
        self.lista_items = []
        self.abono_total = 0.0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- CONTENEDOR PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(1, weight=3)
        self.main_container.grid_rowconfigure(1, weight=1)

        # --- CABECERA ---
        header = ctk.CTkFrame(self.main_container, fg_color="#A30000", height=60, corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(header, text=f"GESTIÓN DE {title.upper()}", text_color="white", 
                     font=("Arial", 22, "bold")).pack(pady=15)

        # ==========================================
        # COLUMNA IZQUIERDA: BUSCADOR DE CLIENTES
        # ==========================================
        frame_left = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5", width=320)
        frame_left.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        
        ctk.CTkLabel(frame_left, text="Buscar Cliente", font=("Arial", 16, "bold"), text_color="#333").pack(pady=10)
        
        self.ent_bus_cli = ctk.CTkEntry(frame_left, placeholder_text="Nombre, NIT o Tel...", height=35)
        self.ent_bus_cli.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkButton(frame_left, text="🔍 Buscar", command=self.buscar_clientes, 
                      fg_color="#333", hover_color="#555").pack(pady=10, padx=15)
        
        # Lista de resultados
        self.scroll_cli = ctk.CTkScrollableFrame(frame_left, height=300, fg_color="white")
        self.scroll_cli.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.lbl_info_cli = ctk.CTkLabel(frame_left, text="⚠️ Cliente no seleccionado", 
                                         text_color="#A30000", font=("Arial", 12, "bold"), wraplength=250)
        self.lbl_info_cli.pack(pady=15)

        # ==========================================
        # COLUMNA DERECHA: FORMULARIO DE PEDIDO
        # ==========================================
        frame_right = ctk.CTkScrollableFrame(self.main_container, fg_color="white")
        frame_right.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)

        # 1. FECHA DE ENTREGA (USANDO TKCALENDAR)
        ctk.CTkLabel(frame_right, text="DATOS DE ENTREGA", font=("Arial", 14, "bold"), text_color="gray").pack(anchor="w", pady=(0,10))
        f_entrega = ctk.CTkFrame(frame_right, fg_color="#F9F9F9", corner_radius=10)
        f_entrega.pack(fill="x", pady=5)
        
        ctk.CTkLabel(f_entrega, text="📅 Fecha Prometida:", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=15)
        self.cal_entrega = DateEntry(f_entrega, width=12, background='#A30000', foreground='white', 
                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        self.cal_entrega.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(f_entrega, text="⏰ Hora:").grid(row=0, column=2, padx=20)
        self.ent_h_ent = ctk.CTkEntry(f_entrega, width=80, placeholder_text="HH:MM")
        self.ent_h_ent.grid(row=0, column=3, padx=5)

        # 2. SECCIÓN DE ÍTEMS
        ctk.CTkLabel(frame_right, text="PRODUCTOS / SERVICIOS", font=("Arial", 14, "bold"), text_color="gray").pack(anchor="w", pady=(20,10))
        f_items = ctk.CTkFrame(frame_right, fg_color="#F2F2F2", border_width=1, border_color="#DDD")
        f_items.pack(fill="x", pady=5)
        
        self.cb_prod = ctk.CTkComboBox(f_items, values=self.cargar_productos_db(), width=220)
        self.cb_prod.grid(row=0, column=0, padx=10, pady=10)
        
        self.en_cant = ctk.CTkEntry(f_items, width=60, placeholder_text="Cant")
        self.en_cant.grid(row=0, column=1, padx=5)
        
        self.en_val = ctk.CTkEntry(f_items, width=100, placeholder_text="$ Unitario")
        self.en_val.grid(row=0, column=2, padx=5)
        
        self.en_desc = ctk.CTkEntry(f_items, placeholder_text="Descripción o notas específicas del trabajo...")
        self.en_desc.grid(row=1, column=0, columnspan=3, padx=10, pady=(0,10), sticky="ew")
        
        ctk.CTkButton(f_items, text="➕ Añadir", command=self.agregar_item, 
                      fg_color="#1F6AA5", font=("Arial", 12, "bold")).grid(row=0, column=3, rowspan=2, padx=10)

        # 3. LISTADO VISUAL DE ITEMS
        self.frame_lista_visual = ctk.CTkFrame(frame_right, fg_color="transparent")
        self.frame_lista_visual.pack(fill="x", pady=10)

        # 4. ABONOS Y TOTALES
        f_totales = ctk.CTkFrame(frame_right, fg_color="#E8F5E9", corner_radius=10)
        f_totales.pack(fill="x", pady=20)
        
        self.en_abono = ctk.CTkEntry(f_totales, placeholder_text="Registrar Abono $", width=150)
        self.en_abono.pack(side="left", padx=20, pady=15)
        ctk.CTkButton(f_totales, text="💵 Abonar", fg_color="#2E7D32", width=100, command=self.registrar_abono).pack(side="left")
        
        self.lbl_totales = ctk.CTkLabel(f_totales, text="TOTAL: $0.00 | SALDO: $0.00", 
                                        font=("Arial", 18, "bold"), text_color="#1B5E20")
        self.lbl_totales.pack(side="right", padx=20)

        # 5. BOTÓN FINAL
        ctk.CTkButton(frame_right, text="💾 GUARDAR TODO Y FINALIZAR", height=55, 
                      fg_color="#A30000", font=("Arial", 16, "bold"), 
                      command=self.guardar_pedido_final).pack(fill="x", pady=20)

    # --- FUNCIONES OPERATIVAS ---

    def cargar_productos_db(self):
        try:
            res = ejecutar_consulta("SELECT nombre FROM producto")
            return [r[0] for r in res] + ["-- OTRO SERVICIO --"]
        except: return ["-- OTRO SERVICIO --"]

    def buscar_clientes(self):
        dato = self.ent_bus_cli.get()
        query = "SELECT id_cliente, nombre, cedula_nit FROM cliente"
        params = ()
        if dato:
            query += " WHERE nombre LIKE ? OR cedula_nit LIKE ? OR telefono LIKE ?"
            params = (f"%{dato}%", f"%{dato}%", f"%{dato}%")
        
        for w in self.scroll_cli.winfo_children(): w.destroy()
        
        resultados = ejecutar_consulta(query + " LIMIT 15", params)
        for cid, nom, nit in resultados:
            btn = ctk.CTkButton(self.scroll_cli, text=f"{nom}\nNIT: {nit}", fg_color="transparent", 
                                text_color="black", anchor="w", font=("Arial", 11),
                                command=lambda c=cid, n=nom: self.seleccionar_cliente(c, n))
            btn.pack(fill="x", pady=2)

    def seleccionar_cliente(self, cid, nom):
        self.id_cliente_sel = cid
        self.lbl_info_cli.configure(text=f"✅ CLIENTE:\n{nom}", text_color="green")

    def agregar_item(self):
        try:
            nombre = self.cb_prod.get()
            cant = int(self.en_cant.get() or 1)
            precio = float(self.en_val.get() or 0)
            if precio <= 0: raise ValueError
            
            # Obtener ID de producto si existe
            res = ejecutar_consulta("SELECT id_producto FROM producto WHERE nombre=?", (nombre,))
            id_p = res[0][0] if res else None
            
            self.lista_items.append({'id_p': id_p, 'nom': nombre, 'pre': precio, 'cant': cant, 'desc': self.en_desc.get()})
            
            # Limpiar campos
            self.en_cant.delete(0, 'end'); self.en_val.delete(0, 'end'); self.en_desc.delete(0, 'end')
            self.renderizar_items()
        except:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos en Precio y Cantidad.")

    def registrar_abono(self):
        try:
            monto = float(self.en_abono.get() or 0)
            self.abono_total += monto
            self.en_abono.delete(0, 'end')
            self.renderizar_items()
        except: messagebox.showerror("Error", "Monto de abono inválido.")

    def renderizar_items(self):
        for w in self.frame_lista_visual.winfo_children(): w.destroy()
        total_acum = 0
        for i, it in enumerate(self.lista_items):
            sub = it['pre'] * it['cant']
            total_acum += sub
            f = ctk.CTkFrame(self.frame_lista_visual, fg_color="#F8F8F8")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"• {it['nom']} x{it['cant']} ({it['desc']})").pack(side="left", padx=15, pady=5)
            ctk.CTkLabel(f, text=f"${sub:,.2f}", font=("Arial", 12, "bold")).pack(side="right", padx=40)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color="#E74C3C", 
                          command=lambda idx=i: [self.lista_items.pop(idx), self.renderizar_items()]).pack(side="right", padx=5)
        
        saldo = total_acum - self.abono_total
        self.lbl_totales.configure(text=f"TOTAL: ${total_acum:,.2f} | SALDO: ${saldo:,.2f}")

    def guardar_pedido_final(self):
        if not self.id_cliente_sel: return messagebox.showerror("Error", "Seleccione un cliente de la lista izquierda.")
        if not self.lista_items: return messagebox.showerror("Error", "El pedido no tiene productos.")

        try:
            # 1. Insertar Pedido Principal
            f_ent = self.cal_entrega.get()
            h_ent = self.ent_h_ent.get()
            f_hoy = datetime.now().strftime("%Y-%m-%d")
            h_hoy = datetime.now().strftime("%H:%M")
            
            # id_usuario = 1 (Ajustar según sesión)
            sql_p = "INSERT INTO pedido (id_cliente, id_usuario, fecha_pedido, hora_pedido, fecha_entrega, hora_entrega, estado) VALUES (?,?,?,?,?,?,?)"
            if ejecutar_accion(sql_p, (self.id_cliente_sel, 1, f_hoy, h_hoy, f_ent, h_ent, "Pendiente")):
                id_ped = ejecutar_consulta("SELECT last_insert_rowid()")[0][0]
                
                # 2. Insertar Detalles
                for i, it in enumerate(self.lista_items):
                    abono_item = self.abono_total if i == 0 else 0 # Abono se registra en el primer item
                    sql_d = "INSERT INTO detallepedido (id_pedido, id_producto, precio_unidad, cantidad, abono, descripcion) VALUES (?,?,?,?,?,?)"
                    ejecutar_accion(sql_d, (id_ped, it['id_p'], it['pre'], it['cant'], abono_item, it['desc']))
                
                messagebox.showinfo("Éxito", f"Pedido #{id_ped} guardado correctamente.")
                self.limpiar_todo()
        except Exception as e:
            messagebox.showerror("Error Crítico", f"No se pudo guardar: {e}")

    def limpiar_todo(self):
        self.lista_items = []; self.abono_total = 0; self.id_cliente_sel = None
        self.lbl_info_cli.configure(text="⚠️ Cliente no seleccionado", text_color="#A30000")
        self.renderizar_items()