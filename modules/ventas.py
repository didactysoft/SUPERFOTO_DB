import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from modules.database_manager import ejecutar_consulta, ejecutar_accion, obtener_conexion

class VentasFrame(ctk.CTkFrame):
    """Módulo de Ventas y Facturación (Punto de Venta)."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.crear_tablas_si_no_existen()
        
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Control ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_controls.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(frame_controls, text="💸 Nueva Venta Directa", fg_color="#1F6AA5", hover_color="#185686", 
                      command=self.abrir_form_venta).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="🧾 Generar Reporte", fg_color="#4CAF50", hover_color="#388E3C").grid(row=0, column=1, padx=10)
        
        self.ent_busqueda = ctk.CTkEntry(frame_controls, placeholder_text="Buscar por N° Venta o Cliente...", width=300)
        self.ent_busqueda.grid(row=0, column=3, padx=10, sticky="e")
        self.ent_busqueda.bind("<Return>", lambda e: self.cargar_datos_ventas())
        ctk.CTkButton(frame_controls, text="🔍 Buscar", fg_color="#555", width=80, 
                      command=self.cargar_datos_ventas).grid(row=0, column=4, padx=(0, 10), sticky="w")

        # --- Área de la Tabla ---
        self.create_sales_table(frame_content)
        self.cargar_datos_ventas()

    def crear_tablas_si_no_existen(self):
        """Crea las tablas de ventas si es la primera vez que se abre el módulo."""
        query_venta = """CREATE TABLE IF NOT EXISTS venta (
                            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_cliente INT,
                            fecha_venta TEXT,
                            hora_venta TEXT,
                            metodo_pago TEXT,
                            estado TEXT DEFAULT 'Pagada',
                            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                         )"""
        query_detalle = """CREATE TABLE IF NOT EXISTS detalleventa (
                            id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_venta INT,
                            id_producto INT,
                            cantidad INT,
                            precio_unidad REAL,
                            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
                            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
                           )"""
        ejecutar_accion(query_venta)
        ejecutar_accion(query_detalle)

    def create_sales_table(self, parent):
        self.frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Historial de Ventas Directas", label_text_color="#333")
        self.frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        headers = ["Factura N°", "Fecha y Hora", "Cliente", "Método Pago", "Monto Total", "Estado", "Acciones"]
        anchos = [80, 150, 160, 120, 120, 100, 80]
        for i, (header, ancho) in enumerate(zip(headers, anchos)):
            ctk.CTkLabel(self.frame_table, text=header, font=("Arial", 14, "bold"), width=ancho, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

    def cargar_datos_ventas(self):
        # Limpiar tabla
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: widget.destroy()

        busqueda = self.ent_busqueda.get().strip()
        
        query = """
            SELECT 
                v.id_venta, 
                v.fecha_venta || ' ' || v.hora_venta AS fecha_hora,
                IFNULL(c.nombre, 'Cliente Mostrador') AS cliente, 
                v.metodo_pago,
                COALESCE(SUM(dv.precio_unidad * dv.cantidad), 0) AS total,
                v.estado
            FROM venta v
            LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
            LEFT JOIN detalleventa dv ON v.id_venta = dv.id_venta
        """
        if busqueda:
            if busqueda.isdigit(): query += f" WHERE v.id_venta = {busqueda}"
            else: query += f" WHERE c.nombre LIKE '%{busqueda}%'"
                
        query += " GROUP BY v.id_venta ORDER BY v.id_venta DESC"
        resultados = ejecutar_consulta(query)
        
        anchos = [80, 150, 160, 120, 120]
        for row_index, datos in enumerate(resultados, start=1):
            id_venta, fecha_hora, cliente, metodo, total, estado = datos
            
            valores = [str(id_venta), fecha_hora, cliente, metodo, f"${total:,.0f}"]
            for col, (val, ancho) in enumerate(zip(valores, anchos)):
                align = "e" if col == 4 else "w"
                ctk.CTkLabel(self.frame_table, text=val, width=ancho, anchor=align, text_color="#333").grid(row=row_index, column=col, padx=5, pady=2)
            
            # Etiqueta de estado
            color = {"Pagada": "#4CAF50", "Pendiente": "#FF9800", "Anulada": "#F44336"}.get(estado, "#607D8B")
            ctk.CTkLabel(self.frame_table, text=estado, width=100, anchor="center", fg_color=color, corner_radius=5, text_color="white").grid(row=row_index, column=5, padx=5, pady=2)
            
            # Acciones
            action_frame = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            action_frame.grid(row=row_index, column=6, padx=5, pady=2, sticky="w")
            ctk.CTkButton(action_frame, text="🗑️ Anular", width=60, fg_color="#E74C3C", hover_color="#C0392B", 
                          command=lambda i=id_venta: self.anular_venta(i)).pack(side="left", padx=2)

    def abrir_form_venta(self):
        """Abre la ventana del Punto de Venta (POS)."""
        win = ctk.CTkToplevel(self)
        win.title("Nueva Venta Directa")
        win.geometry("800x600")
        win.grab_set()

        self.carrito_ventas = []

        # --- Frame Superior (Datos de la venta) ---
        f_top = ctk.CTkFrame(win, fg_color="transparent")
        f_top.pack(fill="x", padx=20, pady=10)

        # Clientes
        ctk.CTkLabel(f_top, text="Cliente:").grid(row=0, column=0, sticky="w", padx=5)
        clientes_db = ejecutar_consulta("SELECT id_cliente, nombre FROM cliente ORDER BY nombre")
        nombres_cli = ["Cliente Mostrador (Anónimo)"] + [c[1] for c in clientes_db] if clientes_db else ["Cliente Mostrador (Anónimo)"]
        cb_cliente = ctk.CTkComboBox(f_top, values=nombres_cli, width=250)
        cb_cliente.grid(row=1, column=0, padx=5, pady=5)
        cb_cliente.set("Cliente Mostrador (Anónimo)")

        # Método de Pago
        ctk.CTkLabel(f_top, text="Método de Pago:").grid(row=0, column=1, sticky="w", padx=15)
        cb_metodo = ctk.CTkComboBox(f_top, values=["Efectivo", "Nequi / Daviplata", "Transferencia Bancaria", "Tarjeta Crédito/Débito"], width=180)
        cb_metodo.grid(row=1, column=1, padx=15, pady=5)

        # --- Frame Medio (Agregar Productos) ---
        f_mid = ctk.CTkFrame(win, fg_color="#EAEAEA", corner_radius=10)
        f_mid.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(f_mid, text="Producto:").grid(row=0, column=0, padx=5, pady=(5,0), sticky="w")
        
        # Cargar productos con su stock
        prods_db = ejecutar_consulta("SELECT id_producto, nombre, precio, cantidad FROM producto WHERE cantidad > 0 ORDER BY nombre")
        nombres_prod = [f"{p[1]} (Stock: {p[3]})" for p in prods_db] if prods_db else ["Sin productos disponibles"]
        cb_producto = ctk.CTkComboBox(f_mid, values=nombres_prod, width=300)
        cb_producto.grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkLabel(f_mid, text="Cantidad:").grid(row=0, column=1, padx=5, pady=(5,0), sticky="w")
        e_cant = ctk.CTkEntry(f_mid, width=70)
        e_cant.grid(row=1, column=1, padx=5, pady=5); e_cant.insert(0, "1")

        ctk.CTkLabel(f_mid, text="Precio:").grid(row=0, column=2, padx=5, pady=(5,0), sticky="w")
        e_precio = ctk.CTkEntry(f_mid, width=100)
        e_precio.grid(row=1, column=2, padx=5, pady=5)

        tb_carrito = ctk.CTkTextbox(win, height=180)
        tb_carrito.pack(fill="x", padx=20, pady=5); tb_carrito.configure(state="disabled")

        lbl_total = ctk.CTkLabel(win, text="TOTAL A COBRAR: $0", font=("Arial", 22, "bold"), text_color="#27AE60")
        lbl_total.pack(pady=5)

        def actualizar_vista_carrito():
            tb_carrito.configure(state="normal")
            tb_carrito.delete("1.0", "end")
            total = 0
            for i, p in enumerate(self.carrito_ventas):
                subtotal = p['cantidad'] * p['precio']
                total += subtotal
                linea = f"[{i+1}] {p['nombre_limpio']} | Cantidad: {p['cantidad']} | P.Unit: ${p['precio']:,.0f} | SubTotal: ${subtotal:,.0f}\n"
                tb_carrito.insert("end", linea)
            tb_carrito.configure(state="disabled")
            lbl_total.configure(text=f"TOTAL A COBRAR: ${total:,.0f}")

        def agregar_al_carrito():
            sel_prod = cb_producto.get()
            idx_p = nombres_prod.index(sel_prod) if sel_prod in nombres_prod else -1
            if idx_p == -1: return messagebox.showerror("Error", "Seleccione un producto válido.")
            try:
                c, p = int(e_cant.get()), float(e_precio.get())
                stock_disponible = int(prods_db[idx_p][3])
                if c > stock_disponible:
                    return messagebox.showwarning("Stock Insuficiente", f"Solo hay {stock_disponible} unidades disponibles de este producto.")
                if c <= 0: return messagebox.showwarning("Error", "La cantidad debe ser mayor a 0.")
            except ValueError: return messagebox.showerror("Error", "Cantidad y Precio deben ser números.")
            
            self.carrito_ventas.append({
                "id_producto": prods_db[idx_p][0], 
                "nombre_limpio": prods_db[idx_p][1],
                "cantidad": c, 
                "precio": p
            })
            actualizar_vista_carrito()
            e_cant.delete(0, 'end'); e_cant.insert(0, "1")

        ctk.CTkButton(f_mid, text="🛒 Añadir al Carrito", command=agregar_al_carrito, fg_color="#F39C12", hover_color="#D68910").grid(row=1, column=3, padx=15, pady=5)

        def on_prod_change(choice):
            idx = nombres_prod.index(choice)
            e_precio.delete(0, 'end'); e_precio.insert(0, str(prods_db[idx][2]))
        cb_producto.configure(command=on_prod_change)
        if prods_db: on_prod_change(nombres_prod[0])

        def procesar_venta_db():
            if not self.carrito_ventas: return messagebox.showwarning("Atención", "El carrito está vacío.")
            
            nom_cli = cb_cliente.get()
            id_cliente = None
            if nom_cli != "Cliente Mostrador (Anónimo)":
                id_cliente = next((c[0] for c in clientes_db if c[1] == nom_cli), None)

            f_actual = datetime.now().strftime("%Y-%m-%d")
            h_actual = datetime.now().strftime("%H:%M:%S")
            metodo = cb_metodo.get()
            
            conn = obtener_conexion(); cursor = conn.cursor()
            try:
                # 1. Insertar Venta
                cursor.execute("INSERT INTO venta (id_cliente, fecha_venta, hora_venta, metodo_pago, estado) VALUES (?, ?, ?, ?, 'Pagada')", 
                               (id_cliente, f_actual, h_actual, metodo))
                id_venta = cursor.lastrowid
                
                # 2. Insertar Detalles y Descontar Inventario
                for item in self.carrito_ventas:
                    cursor.execute("INSERT INTO detalleventa (id_venta, id_producto, cantidad, precio_unidad) VALUES (?, ?, ?, ?)", 
                                   (id_venta, item['id_producto'], item['cantidad'], item['precio']))
                    # Actualizar Stock en inventario
                    cursor.execute("UPDATE producto SET cantidad = cantidad - ? WHERE id_producto = ?", (item['cantidad'], item['id_producto']))
                
                conn.commit(); win.destroy(); self.cargar_datos_ventas()
                messagebox.showinfo("Éxito", f"Venta #{id_venta} procesada correctamente.")
            except Exception as e:
                conn.rollback(); messagebox.showerror("Error BD", f"Error al procesar venta: {e}")
            finally:
                conn.close()

        ctk.CTkButton(win, text="✅ Confirmar y Cobrar", command=procesar_venta_db, fg_color="#27AE60", hover_color="#2ECC71", font=("Arial", 16, "bold"), height=50).pack(pady=20)

    def anular_venta(self, id_venta):
        if messagebox.askyesno("Confirmar Anulación", f"¿Estás seguro de anular la venta #{id_venta}?\nEsto devolverá los productos al inventario."):
            conn = obtener_conexion()
            try:
                cursor = conn.cursor()
                # Verificar si ya está anulada
                cursor.execute("SELECT estado FROM venta WHERE id_venta = ?", (id_venta,))
                estado = cursor.fetchone()[0]
                if estado == 'Anulada': return messagebox.showinfo("Aviso", "Esta venta ya está anulada.")

                # Devolver stock al inventario
                detalles = cursor.execute("SELECT id_producto, cantidad FROM detalleventa WHERE id_venta = ?", (id_venta,)).fetchall()
                for d in detalles:
                    cursor.execute("UPDATE producto SET cantidad = cantidad + ? WHERE id_producto = ?", (d[1], d[0]))
                
                # Marcar como anulada (no la borramos para mantener el historial contable)
                cursor.execute("UPDATE venta SET estado = 'Anulada' WHERE id_venta = ?", (id_venta,))
                conn.commit(); self.cargar_datos_ventas()
                messagebox.showinfo("Éxito", "Venta anulada correctamente.")
            except Exception as e:
                conn.rollback(); messagebox.showerror("Error", f"No se pudo anular: {e}")
            finally:
                conn.close()