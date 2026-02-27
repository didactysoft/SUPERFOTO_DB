import customtkinter as ctk
import json
import os

class ConfiguracionFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Ruta del archivo de configuración
        self.archivo_config = "config_sistema.json"
        
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.grid_rowconfigure(1, weight=1)

        # --- TÍTULO ---
        ctk.CTkLabel(self, text=title.upper(), font=("Arial", 24, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(10, 20)
        )

        # --- COLUMNA 1: EMPRESA ---
        self.frame_empresa = self.create_container(0, "🏢 Empresa")
        self.fields_empresa = {}
        campos = ["NIT", "Nombre", "Teléfono", "Correo", "Dirección"]
        for i, campo in enumerate(campos):
            # Guardamos la referencia en el diccionario para acceder luego
            lbl = ctk.CTkLabel(self.frame_empresa, text=f"{campo}:")
            lbl.pack(pady=(5, 0), padx=20, anchor="w")
            entry = ctk.CTkEntry(self.frame_empresa, height=30)
            entry.pack(pady=(0, 10), padx=20, fill="x")
            self.fields_empresa[campo] = entry

        # --- COLUMNA 2: IMPRESORA ---
        self.frame_printer = self.create_container(1, "🖨️ Impresora")
        
        ctk.CTkLabel(self.frame_printer, text="Tamaño de papel:").pack(pady=(5, 0), padx=20, anchor="w")
        self.combo_papel = ctk.CTkComboBox(self.frame_printer, values=["58mm", "80mm", "Carta"])
        self.combo_papel.pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkLabel(self.frame_printer, text="Tipo de impresión:").pack(pady=(5, 0), padx=20, anchor="w")
        self.combo_tipo = ctk.CTkComboBox(self.frame_printer, values=["Térmica", "Láser"])
        self.combo_tipo.pack(pady=(0, 10), padx=20, fill="x")

        self.check_corte = ctk.CTkCheckBox(self.frame_printer, text="Corte automático", 
                                          fg_color="#A30000", hover_color="#800000")
        self.check_corte.pack(pady=20, padx=20, anchor="w")

        # --- COLUMNA 3: SISTEMA ---
        self.frame_app = self.create_container(2, "🎨 Sistema")
        
        ctk.CTkLabel(self.frame_app, text="Tema del sistema:").pack(pady=(5, 0), padx=20, anchor="w")
        self.combo_tema = ctk.CTkComboBox(self.frame_app, values=["Dark", "Light"], 
                                         command=self.cambiar_tema_instante)
        self.combo_tema.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(self.frame_app, text="").pack(expand=True)

        self.btn_guardar = ctk.CTkButton(self.frame_app, text="GUARDAR CAMBIOS", 
                                        fg_color="#A30000", hover_color="#800000",
                                        height=45, font=("Arial", 13, "bold"),
                                        command=self.guardar_configuracion)
        self.btn_guardar.pack(pady=20, padx=20, fill="x")

        # --- CARGAR DATOS AL INICIAR ---
        self.cargar_datos_existentes()

    def create_container(self, col, title):
        frame = ctk.CTkFrame(self, fg_color=("white", "#252525"), corner_radius=15, border_width=1, border_color="#404040")
        frame.grid(row=1, column=col, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=("Arial", 18, "bold"), text_color="#A30000").pack(pady=15)
        return frame

    def cambiar_tema_instante(self, nuevo_tema):
        ctk.set_appearance_mode(nuevo_tema)

    def cargar_datos_existentes(self):
        """Lee el archivo JSON y rellena los campos."""
        if os.path.exists(self.archivo_config):
            try:
                with open(self.archivo_config, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Rellenar Empresa
                    empresa = data.get("empresa", {})
                    for campo, entry in self.fields_empresa.items():
                        entry.insert(0, empresa.get(campo, ""))
                    
                    # Rellenar Impresora
                    imp = data.get("impresora", {})
                    self.combo_papel.set(imp.get("papel", "80mm"))
                    self.combo_tipo.set(imp.get("tipo", "Térmica"))
                    if imp.get("corte"): self.check_corte.select()
                    
                    # Rellenar Tema
                    self.combo_tema.set(data.get("tema", "Dark"))
            except Exception as e:
                print(f"Error cargando config: {e}")

    def guardar_configuracion(self):
        """Recopila datos y los escribe en el JSON."""
        datos = {
            "empresa": {campo: entry.get() for campo, entry in self.fields_empresa.items()},
            "impresora": {
                "papel": self.combo_papel.get(),
                "tipo": self.combo_tipo.get(),
                "corte": self.check_corte.get()
            },
            "tema": self.combo_tema.get()
        }
        
        try:
            with open(self.archivo_config, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            
            # Feedback visual simple
            self.btn_guardar.configure(text="¡GUARDADO!", fg_color="green")
            self.after(2000, lambda: self.btn_guardar.configure(text="GUARDAR CAMBIOS", fg_color="#A30000"))
            
        except Exception as e:
            print(f"Error al guardar: {e}")