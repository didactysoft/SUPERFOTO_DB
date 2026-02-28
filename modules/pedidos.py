import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime
from modules.database_manager import ejecutar_consulta, ejecutar_accion, obtener_conexion

class PedidosFrame(ctk.CTkFrame):
    """Módulo de Pedidos y Trabajos (Jobs/Orders)."""
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
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Control ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_controls.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(frame_controls, text="➕ Nuevo Pedido", fg_color="#1F6AA5", hover_color="#185686", 
                      command=self.abrir_form_pedido).grid(row=0, column=0, padx=10)
        
        self.ent_busqueda = ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Cliente o ID...", width=300)
        self.ent_busqueda.grid(row=0, column=4, padx=10, sticky="e")
        self.ent_busqueda.bind("<Return>", lambda e: self.cargar_datos_pedidos())
        ctk.CTkButton(frame_controls, text="🔍 Buscar", fg_color="#555", width=80, 
                      command=self.cargar_datos_pedidos).grid(row=0, column=5, padx=(0, 10), sticky="e")

        # --- Área de la Tabla ---
        self.create_table_structure(frame_content)
        self.cargar_datos_pedidos()

    def create_table_structure(self, parent):
        self.frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0")
        self.frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        headers = ["ID", "Cliente", "Recepción", "Entrega", "Total", "Abono", "Saldo", "Estado", "Acciones"]
        anchos = [40, 160, 100, 100, 90, 90, 90, 110, 80]
        
        for i, (header, ancho) in enumerate(zip(headers, anchos)):
            ctk.CTkLabel(self.frame_table, text=header, font=("Arial", 13, "bold"), width=ancho, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

    def cargar_datos_pedidos(self):
        # Limpiar tabla
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: 
                widget.destroy()
                
        busqueda = self.ent_busqueda.get().strip()
        
        query = """
            SELECT 
                p.id_pedido, 
                IFNULL(c.nombre, 'Sin Cliente') AS cliente, 
                p.fecha_pedido, 
                IFNULL(p.fecha_entrega, 'N/A'),
                COALESCE(SUM((dp.precio_unidad * dp.cantidad) - IFNULL(dp.descuento, 0)), 0) AS total, 
                COALESCE(SUM(dp.abono), 0) AS abono,
                IFNULL(p.estado, 'Pendiente') AS estado,
                c.id_cliente
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
            LEFT JOIN detallepedido dp ON p.id_pedido = dp.id_pedido
        """
        
        if busqueda:
            if busqueda.isdigit(): query += f" WHERE p.id_pedido = {busqueda}"
            else: query += f" WHERE c.nombre LIKE '%{busqueda}%'"
                
        query += " GROUP BY p.id_pedido ORDER BY p.id_pedido DESC"
        resultados = ejecutar_consulta(query)
        
        anchos = [40, 160, 100, 100, 90, 90, 90, 110]
        
        for row_index, datos in enumerate(resultados, start=1):
            id_ped, cliente, f_recep, f_ent, total, abono, estado, id_cliente = datos
            saldo = total - abono
            
            valores = [
                str(id_ped), cliente, f_recep, f_ent, 
                f"${total:,.0f}", f"${abono:,.0f}", f"${saldo:,.0f}"
            ]
            
            for col, (val, ancho) in enumerate(zip(valores, anchos[:7])):
                align = "e" if col >= 4 else "w"
                ctk.CTkLabel(self.frame_table, text=val, width=ancho, anchor=align, text_color="#333").grid(row=row_index, column=col, padx=5, pady=2)
            
            # Etiqueta de estado
            color_estado = {"En Producción": "#FFC107", "Finalizado": "#4CAF50", "Pendiente": "#F44336", "Entregado": "#2196F3", "Cancelado": "#607D8B"}.get(estado, "#607D8B")
            ctk.CTkLabel(self.frame_table, text=estado, width=anchos[7], anchor="center", fg_color=color_estado, corner_radius=5, text_color="white").grid(row=row_index, column=7, padx=5, pady=2)

            # Botones
            action_frame = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            action_frame.grid(row=row_index, column=8, padx=5, pady=2, sticky="w")
            ctk.CTkButton(action_frame, text="📝", width=30, fg_color="#F39C12", hover_color="#D68910", command=lambda d=datos: self.abrir_form_pedido(d)).pack(side="left", padx=2)
            ctk.CTkButton(action_frame, text="🗑️", width=30, fg_color="#E74C3C", hover_color="#C0392B", command=lambda i=id_ped: self.eliminar_pedido(i)).pack(side="left", padx=2)

    def abrir_form_pedido(self, datos_edicion=None):
        win = ctk.CTkToplevel(self)
        win.title("Editar Pedido" if datos_edicion else "Nuevo Pedido")
        win.geometry("800x650")
        win.grab_set()

        self.carrito_productos = [] # Lista para almacenar los detalles del pedido

        # --- Frame Superior: Cliente y Fechas ---
        f_top = ctk.CTkFrame(win, fg_color="transparent")
        f_top.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(f_top, text="Cliente:").grid(row=0, column=0, sticky="w", padx=5)
        cb_cliente = ctk.CTkComboBox(f_top, width=250)
        cb_cliente.grid(row=1, column=0, padx=5, pady=5)
        
        # Botón para registrar un nuevo cliente sin salir
        ctk.CTkButton(f_top, text="➕ Nuevo Cliente", width=120, fg_color="#27AE60", hover_color="#2ECC71", 
                      command=lambda: self.abrir_form_cliente(cb_cliente)).grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(f_top, text="Fecha Recepción:").grid(row=0, column=2, sticky="w", padx=15)
        e_fecha_recep = ctk.CTkEntry(f_top, width=120)
        e_fecha_recep.grid(row=1, column=2, padx=15, pady=5)

        ctk.CTkLabel(f_top, text="Fecha Entrega:").grid(row=0, column=3, sticky="w", padx=5)
        e_fecha_ent = ctk.CTkEntry(f_top, width=120)
        e_fecha_ent.grid(row=1, column=3, padx=5, pady=5)

        # --- Frame Medio: Agregar Productos ---
        f_mid = ctk.CTkFrame(win, fg_color="#EAEAEA", corner_radius=10)
        f_mid.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(f_mid, text="Producto/Servicio:").grid(row=0, column=0, padx=5, pady=(5,0), sticky="w")
        cb_producto = ctk.CTkComboBox(f_mid, width=200)
        cb_producto.grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkLabel(f_mid, text="Cant:").grid(row=0, column=1, padx=5, pady=(5,0), sticky="w")
        e_cant = ctk.CTkEntry(f_mid, width=60)
        e_cant.grid(row=1, column=1, padx=5, pady=5)
        e_cant.insert(0, "1")

        ctk.CTkLabel(f_mid, text="Precio Unid:").grid(row=0, column=2, padx=5, pady=(5,0), sticky="w")
        e_precio = ctk.CTkEntry(f_mid, width=90)
        e_precio.grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(f_mid, text="Abono:").grid(row=0, column=3, padx=5, pady=(5,0), sticky="w")
        e_abono = ctk.CTkEntry(f_mid, width=90)
        e_abono.grid(row=1, column=3, padx=5, pady=5)
        e_abono.insert(0, "0")

        ctk.CTkLabel(f_mid, text="Detalle/Descrip:").grid(row=0, column=4, padx=5, pady=(5,0), sticky="w")
        e_desc = ctk.CTkEntry(f_mid, width=160)
        e_desc.grid(row=1, column=4, padx=5, pady=5)

        # Listbox Visual (Textbox) para el carrito
        tb_carrito = ctk.CTkTextbox(win, height=150)
        tb_carrito.pack(fill="x", padx=20, pady=5)
        tb_carrito.configure(state="disabled")

        # Labels de Totales
        f_totales = ctk.CTkFrame(win, fg_color="transparent")
        f_totales.pack(fill="x", padx=20, pady=5)
        lbl_resumen = ctk.CTkLabel(f_totales, text="Total: $0 | Abono: $0 | Saldo: $0", font=("Arial", 16, "bold"), text_color="#C0392B")
        lbl_resumen.pack(side="right", padx=10)

        ctk.CTkLabel(f_totales, text="Estado:").pack(side="left")
        cb_estado = ctk.CTkComboBox(f_totales, values=["Pendiente", "En Producción", "Finalizado", "Entregado", "Cancelado"])
        cb_estado.pack(side="left", padx=10)

        # Cargar Listas (Clientes y Productos)
        clientes_db = ejecutar_consulta("SELECT id_cliente, nombre FROM cliente ORDER BY nombre")
        nombres_cli = [c[1] for c in clientes_db] if clientes_db else ["Sin clientes"]
        cb_cliente.configure(values=nombres_cli)
        
        prods_db = ejecutar_consulta("SELECT id_producto, nombre, precio FROM producto ORDER BY nombre")
        nombres_prod = [p[1] for p in prods_db] if prods_db else ["Sin productos"]
        cb_producto.configure(values=nombres_prod)

        # Función para actualizar UI del carrito
        def actualizar_vista_carrito():
            tb_carrito.configure(state="normal")
            tb_carrito.delete("1.0", "end")
            total = abono = 0
            for i, p in enumerate(self.carrito_productos):
                subtotal = p['cantidad'] * p['precio']
                total += subtotal
                abono += p['abono']
                linea = f"[{i+1}] {p['nombre']} | Cant: {p['cantidad']} | P.Unit: ${p['precio']} | SubT: ${subtotal} | Abono: ${p['abono']} | Desc: {p['descripcion']}\n"
                tb_carrito.insert("end", linea)
            tb_carrito.configure(state="disabled")
            saldo = total - abono
            lbl_resumen.configure(text=f"Total: ${total:,.0f} | Abono: ${abono:,.0f} | Saldo: ${saldo:,.0f}")

        # Función para añadir producto a la lista temporal
        def agregar_al_carrito():
            idx_p = nombres_prod.index(cb_producto.get()) if cb_producto.get() in nombres_prod else -1
            if idx_p == -1: return messagebox.showerror("Error", "Seleccione un producto válido.")
            try:
                c = int(e_cant.get())
                p = float(e_precio.get())
                a = float(e_abono.get())
            except ValueError:
                return messagebox.showerror("Error", "Cant, Precio y Abono deben ser numéricos.")
            
            self.carrito_productos.append({
                "id_producto": prods_db[idx_p][0], "nombre": prods_db[idx_p][1],
                "cantidad": c, "precio": p, "abono": a, "descripcion": e_desc.get()
            })
            actualizar_vista_carrito()
            e_cant.delete(0, 'end'); e_cant.insert(0, "1")
            e_abono.delete(0, 'end'); e_abono.insert(0, "0")
            e_desc.delete(0, 'end')

        ctk.CTkButton(f_mid, text="➕ Añadir", command=agregar_al_carrito).grid(row=1, column=5, padx=10, pady=5)

        # Autocompletar precio al cambiar producto
        def on_prod_change(choice):
            idx = nombres_prod.index(choice)
            e_precio.delete(0, 'end'); e_precio.insert(0, str(prods_db[idx][2]))
        cb_producto.configure(command=on_prod_change)
        if prods_db: on_prod_change(nombres_prod[0])

        # --- Precargar datos si es edición ---
        if datos_edicion:
            id_pedido_edit = datos_edicion[0]
            cb_cliente.set(datos_edicion[1])
            e_fecha_recep.insert(0, datos_edicion[2])
            e_fecha_ent.insert(0, datos_edicion[3])
            cb_estado.set(datos_edicion[6])
            
            # Cargar detalles existentes
            detalles = ejecutar_consulta("SELECT dp.id_producto, p.nombre, dp.cantidad, dp.precio_unidad, dp.abono, dp.descripcion FROM detallepedido dp JOIN producto p ON dp.id_producto = p.id_producto WHERE dp.id_pedido = ?", (id_pedido_edit,))
            for d in detalles:
                self.carrito_productos.append({"id_producto": d[0], "nombre": d[1], "cantidad": d[2], "precio": d[3], "abono": d[4], "descripcion": d[5]})
            actualizar_vista_carrito()
        else:
            e_fecha_recep.insert(0, date.today().strftime("%Y-%m-%d"))
            if nombres_cli: cb_cliente.set(nombres_cli[0])

        # Función Guardar en Base de Datos
        def guardar_pedido_db():
            if not self.carrito_productos:
                return messagebox.showwarning("Atención", "Debes agregar al menos un producto al pedido.")
            
            nom_cli = cb_cliente.get()
            id_cliente = next((c[0] for c in clientes_db if c[1] == nom_cli), None)
            if not id_cliente: return messagebox.showerror("Error", "Cliente no válido.")

            f_rec = e_fecha_recep.get()
            f_ent = e_fecha_ent.get()
            est = cb_estado.get()
            
            # Usar SQLite crudo para manejar la Transacción y obtener lastrowid
            conn = obtener_conexion()
            cursor = conn.cursor()
            try:
                if datos_edicion:
                    cursor.execute("UPDATE pedido SET id_cliente=?, fecha_pedido=?, fecha_entrega=?, estado=? WHERE id_pedido=?", (id_cliente, f_rec, f_ent, est, datos_edicion[0]))
                    cursor.execute("DELETE FROM detallepedido WHERE id_pedido=?", (datos_edicion[0],))
                    id_pedido = datos_edicion[0]
                else:
                    hora = datetime.now().strftime("%H:%M")
                    cursor.execute("INSERT INTO pedido (id_cliente, fecha_pedido, hora_pedido, fecha_entrega, estado) VALUES (?, ?, ?, ?, ?)", (id_cliente, f_rec, hora, f_ent, est))
                    id_pedido = cursor.lastrowid
                
                for item in self.carrito_productos:
                    cursor.execute("INSERT INTO detallepedido (id_pedido, id_producto, precio_unidad, cantidad, abono, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
                                   (id_pedido, item['id_producto'], item['precio'], item['cantidad'], item['abono'], item['descripcion']))
                conn.commit()
                win.destroy()
                self.cargar_datos_pedidos()
                messagebox.showinfo("Éxito", "Pedido guardado correctamente.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error BD", f"Error al guardar: {e}")
            finally:
                conn.close()

        ctk.CTkButton(win, text="💾 Guardar Pedido Completo", command=guardar_pedido_db, fg_color="#1F6AA5", font=("Arial", 14, "bold"), height=40).pack(pady=20)

    def abrir_form_cliente(self, combo_referencia):
        """Ventana rápida para crear cliente sin salir del pedido."""
        win_cli = ctk.CTkToplevel(self)
        win_cli.title("Registrar Nuevo Cliente")
        win_cli.geometry("350x380")
        win_cli.grab_set()

        ctk.CTkLabel(win_cli, text="Documento:").pack(pady=(10,0))
        e_doc = ctk.CTkEntry(win_cli, width=250)
        e_doc.pack()

        ctk.CTkLabel(win_cli, text="Nombre Completo:").pack(pady=(10,0))
        e_nom = ctk.CTkEntry(win_cli, width=250)
        e_nom.pack()

        ctk.CTkLabel(win_cli, text="Teléfono:").pack(pady=(10,0))
        e_tel = ctk.CTkEntry(win_cli, width=250)
        e_tel.pack()
        
        ctk.CTkLabel(win_cli, text="Correo (Opcional):").pack(pady=(10,0))
        e_cor = ctk.CTkEntry(win_cli, width=250)
        e_cor.pack()

        def guardar_cliente_rapido():
            doc, nom, tel, cor = e_doc.get().strip(), e_nom.get().strip(), e_tel.get().strip(), e_cor.get().strip()
            if not doc or not nom: return messagebox.showerror("Error", "Documento y Nombre son obligatorios.")
            
            if ejecutar_accion("INSERT INTO cliente (documento, nombre, telefono, correo) VALUES (?, ?, ?, ?)", (doc, nom, tel, cor)):
                # Refrescar el Combobox de la ventana de Pedidos
                clientes_nuevos = ejecutar_consulta("SELECT id_cliente, nombre FROM cliente ORDER BY nombre")
                lista_nombres = [c[1] for c in clientes_nuevos]
                combo_referencia.configure(values=lista_nombres)
                combo_referencia.set(nom) # Seleccionar automáticamente el que acabamos de crear
                win_cli.destroy()
                messagebox.showinfo("Éxito", f"Cliente {nom} registrado.")
            else:
                messagebox.showerror("Error", "No se pudo registrar (¿Documento duplicado?)")

        ctk.CTkButton(win_cli, text="💾 Guardar Cliente", command=guardar_cliente_rapido).pack(pady=25)

    def eliminar_pedido(self, id_pedido):
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el pedido #{id_pedido}?"):
            # Usar SQLite crudo para borrar en cascada de forma segura
            conn = obtener_conexion()
            try:
                conn.execute("DELETE FROM detallepedido WHERE id_pedido = ?", (id_pedido,))
                conn.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido,))
                conn.commit()
                self.cargar_datos_pedidos()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            finally:
                conn.close()