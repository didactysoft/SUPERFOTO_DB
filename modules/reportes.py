import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import csv
import os
from modules.database_manager import ejecutar_consulta

class ReportesFrame(ctk.CTkFrame):
    """Módulo de Generación y Visualización de Reportes."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel de Opciones de Reporte (Fila 1) ---
        frame_options = ctk.CTkFrame(frame_content, fg_color="#F0F0F0")
        frame_options.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        frame_options.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Columna 1: Tipo de Reporte
        f_tipo = ctk.CTkFrame(frame_options, fg_color="transparent")
        f_tipo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(f_tipo, text="Tipo de Reporte:", font=("Arial", 16, "bold"), text_color="#333").pack(anchor="w", pady=(0,5))
        
        self.cb_tipo_reporte = ctk.CTkComboBox(f_tipo, values=["Ventas Directas", "Pedidos y Trabajos", "Inventario Actual"], width=200)
        self.cb_tipo_reporte.pack()

        # Columna 2: Rango de Fechas
        f_fechas = ctk.CTkFrame(frame_options, fg_color="transparent")
        f_fechas.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(f_fechas, text="Rango de Fechas:", font=("Arial", 16, "bold"), text_color="#333").pack(anchor="w", pady=(0,5))
        
        f_fechas_inputs = ctk.CTkFrame(f_fechas, fg_color="transparent")
        f_fechas_inputs.pack()
        
        ctk.CTkLabel(f_fechas_inputs, text="Desde:", text_color="#333").grid(row=0, column=0, padx=(0,5))
        # Fecha inicio (por defecto, hace 30 días)
        hace_un_mes = datetime.now() - timedelta(days=30)
        self.de_inicio = DateEntry(f_fechas_inputs, width=12, background='#1F6AA5', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.de_inicio.set_date(hace_un_mes.date())
        self.de_inicio.grid(row=0, column=1, padx=(0,15))
        
        ctk.CTkLabel(f_fechas_inputs, text="Hasta:", text_color="#333").grid(row=0, column=2, padx=(0,5))
        self.de_fin = DateEntry(f_fechas_inputs, width=12, background='#1F6AA5', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.de_fin.grid(row=0, column=3)

        # Columna 3: Botones de Acción
        f_botones = ctk.CTkFrame(frame_options, fg_color="transparent")
        f_botones.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        ctk.CTkButton(f_botones, text="📊 Generar", fg_color="#1F6AA5", hover_color="#185686", height=40,
                      command=self.generar_reporte).pack(side="left", padx=5)
        ctk.CTkButton(f_botones, text="💾 Exportar a CSV", fg_color="#27AE60", hover_color="#2ECC71", height=40,
                      command=self.exportar_csv).pack(side="left", padx=5)

        # --- Área de Visualización (Fila 2) ---
        self.frame_viewer = ctk.CTkScrollableFrame(frame_content, fg_color="#FAFAFA", border_width=1, border_color="#DDD")
        self.frame_viewer.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # --- Resumen Totalizador (Fila 3) ---
        self.f_resumen = ctk.CTkFrame(frame_content, fg_color="#FFF9C4", height=50) # Amarillo clarito
        self.f_resumen.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.lbl_resumen = ctk.CTkLabel(self.f_resumen, text="Genera un reporte para ver los totales.", font=("Arial", 16, "bold"), text_color="#333")
        self.lbl_resumen.pack(pady=10)

        self.datos_actuales = [] # Para almacenar lo que se va a exportar
        self.headers_actuales = []

    def limpiar_tabla(self):
        for widget in self.frame_viewer.winfo_children():
            widget.destroy()

    def generar_reporte(self):
        self.limpiar_tabla()
        tipo = self.cb_tipo_reporte.get()
        f_inicio = self.de_inicio.get_date().strftime("%Y-%m-%d")
        f_fin = self.de_fin.get_date().strftime("%Y-%m-%d")

        if f_inicio > f_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor a la fecha de fin.")
            return

        if tipo == "Ventas Directas":
            self.reporte_ventas(f_inicio, f_fin)
        elif tipo == "Pedidos y Trabajos":
            self.reporte_pedidos(f_inicio, f_fin)
        elif tipo == "Inventario Actual":
            self.reporte_inventario()

    def dibujar_tabla(self, headers, datos, anchos, alinear_derecha_desde=3):
        self.headers_actuales = headers
        self.datos_actuales = datos

        # Dibujar cabeceras
        for i, (header, ancho) in enumerate(zip(headers, anchos)):
            ctk.CTkLabel(self.frame_viewer, text=header, font=("Arial", 14, "bold"), width=ancho, text_color="#1F6AA5", anchor="w" if i < alinear_derecha_desde else "e").grid(row=0, column=i, padx=5, pady=10)

        if not datos:
            ctk.CTkLabel(self.frame_viewer, text="No se encontraron registros en este rango de fechas.", text_color="#555").grid(row=1, column=0, columnspan=len(headers), pady=20)
            return

        # Dibujar filas
        for row_index, fila in enumerate(datos, start=1):
            for col_index, (valor, ancho) in enumerate(zip(fila, anchos)):
                align = "e" if col_index >= alinear_derecha_desde else "w"
                ctk.CTkLabel(self.frame_viewer, text=str(valor), width=ancho, anchor=align, text_color="#333").grid(row=row_index, column=col_index, padx=5, pady=2)

    def reporte_ventas(self, inicio, fin):
        query = """
            SELECT 
                v.id_venta, v.fecha_venta, IFNULL(c.nombre, 'Cliente Mostrador'), v.metodo_pago,
                COALESCE(SUM(dv.precio_unidad * dv.cantidad), 0) AS total, v.estado
            FROM venta v
            LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
            LEFT JOIN detalleventa dv ON v.id_venta = dv.id_venta
            WHERE v.fecha_venta BETWEEN ? AND ?
            GROUP BY v.id_venta ORDER BY v.fecha_venta DESC, v.id_venta DESC
        """
        resultados = ejecutar_consulta(query, (inicio, fin))
        
        # Formatear datos
        datos_formateados = []
        suma_total = 0
        for r in resultados:
            estado = r[5]
            total = r[4]
            if estado != 'Anulada':
                suma_total += total
            datos_formateados.append((r[0], r[1], r[2], r[3], f"${total:,.0f}", estado))

        headers = ["N° Venta", "Fecha", "Cliente", "Método", "Total", "Estado"]
        anchos = [80, 100, 200, 120, 100, 100]
        self.dibujar_tabla(headers, datos_formateados, anchos, alinear_derecha_desde=4)
        
        self.lbl_resumen.configure(text=f"Total Ventas (Sin anuladas): ${suma_total:,.0f} | Registros: {len(resultados)}")

    def reporte_pedidos(self, inicio, fin):
        query = """
            SELECT 
                p.id_pedido, p.fecha_pedido, IFNULL(c.nombre, 'Sin Cliente'), p.estado,
                COALESCE(SUM((dp.precio_unidad * dp.cantidad) - IFNULL(dp.descuento, 0)), 0) AS total,
                COALESCE(SUM(dp.abono), 0) AS abono
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
            LEFT JOIN detallepedido dp ON p.id_pedido = dp.id_pedido
            WHERE p.fecha_pedido BETWEEN ? AND ?
            GROUP BY p.id_pedido ORDER BY p.fecha_pedido DESC, p.id_pedido DESC
        """
        resultados = ejecutar_consulta(query, (inicio, fin))
        
        datos_formateados = []
        suma_total, suma_abonos = 0, 0
        for r in resultados:
            estado = r[3]
            total, abono = r[4], r[5]
            if estado != 'Cancelado':
                suma_total += total
                suma_abonos += abono
            saldo = total - abono
            datos_formateados.append((r[0], r[1], r[2], estado, f"${total:,.0f}", f"${abono:,.0f}", f"${saldo:,.0f}"))

        headers = ["N° Pedido", "Fecha", "Cliente", "Estado", "Total", "Abonado", "Saldo Pendiente"]
        anchos = [80, 100, 200, 120, 100, 100, 120]
        self.dibujar_tabla(headers, datos_formateados, anchos, alinear_derecha_desde=4)

        self.lbl_resumen.configure(text=f"Total Pedidos: ${suma_total:,.0f} | Cobrado (Abonos): ${suma_abonos:,.0f} | Por Cobrar: ${(suma_total - suma_abonos):,.0f}")

    def reporte_inventario(self):
        # El inventario no depende de fechas, mostramos el stock actual
        query = """
            SELECT p.id_producto, p.nombre, p.cantidad, p.precio, IFNULL(c.nombre, 'Sin Categoría')
            FROM producto p
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            ORDER BY p.cantidad ASC
        """
        resultados = ejecutar_consulta(query)
        
        datos_formateados = []
        valor_inventario = 0
        para_agotar = 0
        for r in resultados:
            cant = r[2]
            precio = r[3]
            valor_inventario += (cant * precio)
            if cant <= 5: para_agotar += 1
            datos_formateados.append((r[0], r[1], r[4], cant, f"${precio:,.0f}", f"${(cant * precio):,.0f}"))

        headers = ["ID", "Producto", "Categoría", "Stock", "Precio Costo", "Valor Total"]
        anchos = [60, 250, 150, 80, 100, 120]
        self.dibujar_tabla(headers, datos_formateados, anchos, alinear_derecha_desde=3)

        self.lbl_resumen.configure(text=f"Valor Total en Inventario: ${valor_inventario:,.0f} | Productos por agotarse (<= 5): {para_agotar}")

    def exportar_csv(self):
        if not self.datos_actuales:
            messagebox.showwarning("Atención", "No hay datos generados para exportar. Haz clic en 'Generar' primero.")
            return

        tipo = self.cb_tipo_reporte.get().replace(" ", "_")
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        nombre_sugerido = f"Reporte_{tipo}_{fecha}.csv"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=nombre_sugerido,
            title="Guardar Reporte Como",
            filetypes=[("Archivos CSV (Excel)", "*.csv"), ("Todos los archivos", "*.*")]
        )

        if filepath:
            try:
                # Escribir el CSV
                with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';') # Usamos punto y coma para que Excel en español lo abra directo en columnas
                    # Escribir Cabeceras
                    writer.writerow(self.headers_actuales)
                    # Escribir Filas
                    for fila in self.datos_actuales:
                        writer.writerow(fila)
                
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")