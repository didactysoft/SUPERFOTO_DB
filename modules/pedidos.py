import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class PedidosFrame(ctk.CTkFrame):
    """Módulo de Pedidos y Trabajos (Jobs/Orders)."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1) # Fila de la tabla expandible

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Control (Fila 1) ---
        frame_controls = ctk.CTkFrame(frame_content, fg_color="transparent")
        frame_controls.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_controls.grid_columnconfigure(4, weight=1) # Espacio vacío

        ctk.CTkButton(frame_controls, text="➕ Nuevo Pedido", fg_color="#1F6AA5", hover_color="#185686", 
                      command=self.abrir_form_pedido).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_controls, text="📊 Ver Reporte", fg_color="#4CAF50", hover_color="#388E3C").grid(row=0, column=1, padx=10)
        
        self.ent_busqueda = ctk.CTkEntry(frame_controls, placeholder_text="Buscar por Cliente o ID...", width=300)
        self.ent_busqueda.grid(row=0, column=3, padx=(100, 10), sticky="e")
        self.ent_busqueda.bind("<Return>", lambda e: self.cargar_datos_pedidos())

        # --- Área de la Tabla (Fila 2) ---
        self.create_table_structure(frame_content)
        self.cargar_datos_pedidos()

    def create_table_structure(self, parent):
        # Frame para la tabla con scrollbar
        self.frame_table = ctk.CTkScrollableFrame(parent, fg_color="#F0F0F0", label_text="Pedidos Activos", label_text_color="#333")
        self.frame_table.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Cabeceras de la tabla
        headers = ["ID", "Cliente", "Fecha Pedido", "Total", "Estado", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(self.frame_table, text=header, font=("Arial", 14, "bold"), width=130, text_color="#333").grid(row=0, column=i, padx=5, pady=5)

    def cargar_datos_pedidos(self):
        # Limpiar tabla (excepto cabeceras)
        for widget in self.frame_table.winfo_children():
            if int(widget.grid_info()["row"]) > 0: 
                widget.destroy()
                
        busqueda = self.ent_busqueda.get().strip()
        
        # Consulta actualizada para coincidir con la base de datos
        query = """
            SELECT 
                p.id_pedido, 
                IFNULL(c.nombre, 'Sin Cliente') AS cliente, 
                p.fecha_pedido, 
                COALESCE((SELECT SUM((dp.precio_unidad * dp.cantidad) - IFNULL(dp.descuento, 0)) 
                          FROM detallepedido dp WHERE dp.id_pedido = p.id_pedido), 0) AS total, 
                IFNULL(p.estado, 'Pendiente') AS estado,
                c.id_cliente
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
        """
        
        if busqueda:
            if busqueda.isdigit():
                query += f" WHERE p.id_pedido = {busqueda}"
            else:
                query += f" WHERE c.nombre LIKE '%{busqueda}%'"
                
        query += " ORDER BY p.id_pedido DESC"
        
        resultados = ejecutar_consulta(query)
        
        for row_index, datos in enumerate(resultados, start=1):
            id_ped, cliente, fecha, total, estado, id_cliente = datos
            
            ctk.CTkLabel(self.frame_table, text=str(id_ped), width=130, anchor="w", text_color="#333").grid(row=row_index, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.frame_table, text=cliente, width=130, anchor="w", text_color="#333").grid(row=row_index, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.frame_table, text=fecha, width=130, anchor="w", text_color="#333").grid(row=row_index, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.frame_table, text=f"${total:.2f}", width=130, anchor="e", text_color="#333").grid(row=row_index, column=3, padx=5, pady=2)
            
            # Etiqueta de estado con color
            color_estado = {"En Producción": "#FFC107", "Finalizado": "#4CAF50", "Pendiente": "#F44336", "Entregado": "#2196F3", "Cancelado": "#607D8B"}.get(estado, "#607D8B")
            ctk.CTkLabel(self.frame_table, text=estado, width=130, anchor="center", fg_color=color_estado, corner_radius=5, text_color="white").grid(row=row_index, column=4, padx=5, pady=2)

            # Botones de acción
            action_frame = ctk.CTkFrame(self.frame_table, fg_color="transparent")
            action_frame.grid(row=row_index, column=5, padx=5, pady=2, sticky="w")
            
            ctk.CTkButton(action_frame, text="📝", width=30, height=25, fg_color="#F39C12", hover_color="#D68910", 
                          command=lambda d=datos: self.abrir_form_pedido(d)).grid(row=0, column=0, padx=2)
            ctk.CTkButton(action_frame, text="🗑️", width=30, height=25, fg_color="#E74C3C", hover_color="#C0392B", 
                          command=lambda i=id_ped: self.eliminar_pedido(i)).grid(row=0, column=1, padx=2)

    def abrir_form_pedido(self, datos_edicion=None):
        win = ctk.CTkToplevel(self)
        win.title("Editar Pedido" if datos_edicion else "Nuevo Pedido")
        win.geometry("400x350")
        win.grab_set()

        # Obtener lista de clientes de la base de datos
        clientes = ejecutar_consulta("SELECT id_cliente, nombre FROM cliente ORDER BY nombre")
        nombres_clientes = [c[1] for c in clientes] if clientes else ["No hay clientes"]

        ctk.CTkLabel(win, text="Cliente:").pack(pady=(15, 0))
        cb_cliente = ctk.CTkComboBox(win, values=nombres_clientes, width=300)
        cb_cliente.pack(pady=(0, 10))

        ctk.CTkLabel(win, text="Estado:").pack(pady=(10, 0))
        estados_disponibles = ["Pendiente", "En Producción", "Finalizado", "Entregado", "Cancelado"]
        cb_estado = ctk.CTkComboBox(win, values=estados_disponibles, width=300)
        cb_estado.pack(pady=(0, 10))
        
        # Info de solo lectura para el Total (No se edita aquí, se edita en Detalles de Pedido)
        if datos_edicion:
            ctk.CTkLabel(win, text=f"Total Actual: ${datos_edicion[3]:.2f}\n(Añade productos para alterar el total)", text_color="#666").pack(pady=5)

        # Precargar datos si es edición
        if datos_edicion:
            cb_cliente.set(datos_edicion[1])
            cb_estado.set(datos_edicion[4])
        else:
            if nombres_clientes:
                cb_cliente.set(nombres_clientes[0])
            cb_estado.set("Pendiente")

        def guardar_pedido():
            nombre_seleccionado = cb_cliente.get()
            estado = cb_estado.get()

            # Buscar el ID del cliente seleccionado
            id_cliente = None
            for c in clientes:
                if c[1] == nombre_seleccionado:
                    id_cliente = c[0]
                    break
            
            if not id_cliente:
                messagebox.showerror("Error", "Debes seleccionar un cliente válido.")
                return

            if datos_edicion:
                query = "UPDATE pedido SET id_cliente=?, estado=? WHERE id_pedido=?"
                params = (id_cliente, estado, datos_edicion[0])
            else:
                fecha_actual = date.today().strftime("%Y-%m-%d")
                hora_actual = datetime.now().strftime("%H:%M")
                query = "INSERT INTO pedido (id_cliente, fecha_pedido, hora_pedido, estado) VALUES (?, ?, ?, ?)"
                params = (id_cliente, fecha_actual, hora_actual, estado)

            if ejecutar_accion(query, params):
                win.destroy()
                self.cargar_datos_pedidos()
            else:
                messagebox.showerror("Error", "No se pudo guardar el pedido en la base de datos.")

        ctk.CTkButton(win, text="💾 Guardar Pedido", command=guardar_pedido, fg_color="#1F6AA5").pack(pady=25)

    def eliminar_pedido(self, id_pedido):
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el pedido #{id_pedido}?"):
            # Opcional: Eliminar primero los detalles para no dejar datos huérfanos
            ejecutar_accion("DELETE FROM detallepedido WHERE id_pedido = ?", (id_pedido,))
            if ejecutar_accion("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido,)):
                self.cargar_datos_pedidos()