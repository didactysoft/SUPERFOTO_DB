import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import os
import json
from datetime import datetime

class BackupFrame(ctk.CTkFrame):
    """Módulo de Respaldo y Mantenimiento de la Base de Datos Funcional."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # --- Configuración de Rutas Relativas ---
        # Subimos un nivel (..) desde modules/ para llegar a la raíz
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Ruta a la base de datos: database/superfotoDB.db
        self.DB_PATH = os.path.join(self.BASE_DIR, "database", "superfotoDB.db")
        
        # Carpeta de respaldos en la raíz: Backups/
        self.BACKUP_DIR = os.path.join(self.BASE_DIR, "Backups")
        
        # Archivo de configuración en la raíz
        self.CONFIG_FILE = os.path.join(self.BASE_DIR, "config_backup.json")
        
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Interfaz Gráfica ---
        frame_content = ctk.CTkFrame(self, fg_color=("white", "gray15"), corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame_content, text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), text_color="#A30000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        panel = ctk.CTkScrollableFrame(frame_content, fg_color="transparent")
        panel.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        
        # SECCIÓN 1: RESPALDO MANUAL
        self.create_backup_ui(panel)
        # SECCIÓN 2: RESTAURACIÓN
        self.create_restore_ui(panel)
        # SECCIÓN 3: PROGRAMACIÓN
        self.create_schedule_ui(panel)

        self.cargar_configuracion()

    def create_backup_ui(self, panel):
        section = ctk.CTkFrame(panel, corner_radius=10, border_width=1)
        section.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(section, text="Respaldo Manual", font=("Arial", 18, "bold"), text_color="#1F6AA5").pack(pady=(10, 5))
        
        self.btn_backup = ctk.CTkButton(section, text="⚙️ Generar Respaldo Ahora", 
                                        fg_color="#4CAF50", hover_color="#388E3C", 
                                        font=("Arial", 14, "bold"), command=self.ejecutar_respaldo)
        self.btn_backup.pack(pady=15)
        
        self.lbl_ultimo_respaldo = ctk.CTkLabel(section, text="Último Respaldo: Desconocido", text_color="gray")
        self.lbl_ultimo_respaldo.pack(pady=(0, 10))

    def create_restore_ui(self, panel):
        section = ctk.CTkFrame(panel, corner_radius=10, border_width=1)
        section.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(section, text="Restaurar Base de Datos", font=("Arial", 18, "bold"), text_color="#A30000").pack(pady=(10, 5))
        
        self.path_restaurar = ctk.StringVar()
        f_controls = ctk.CTkFrame(section, fg_color="transparent")
        f_controls.pack(pady=15)
        
        ctk.CTkButton(f_controls, text="📂 Seleccionar Archivo", fg_color="#607D8B", 
                      command=self.seleccionar_archivo_restaurar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(f_controls, text="⚠️ Restaurar DB", fg_color="#F44336", 
                      command=self.ejecutar_restauracion).grid(row=0, column=1, padx=10)

    def create_schedule_ui(self, panel):
        section = ctk.CTkFrame(panel, corner_radius=10, border_width=1)
        section.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(section, text="Programación", font=("Arial", 18, "bold"), text_color="#1F6AA5").pack(pady=(10, 5))
        
        f_sch = ctk.CTkFrame(section, fg_color="transparent")
        f_sch.pack(pady=10)
        self.combo_frecuencia = ctk.CTkComboBox(f_sch, values=["Diario", "Semanal", "Mensual"])
        self.combo_frecuencia.grid(row=0, column=0, padx=5)
        self.entry_hora = ctk.CTkEntry(f_sch, placeholder_text="HH:MM")
        self.entry_hora.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(section, text="Guardar Programación", fg_color="#4CAF50", 
                      command=self.guardar_configuracion).pack(pady=(0, 15))

    # --- LÓGICA DE RUTAS Y ARCHIVOS ---

    def ejecutar_respaldo(self):
        """Copia superfotoDB.db a la carpeta Backups/."""
        if not os.path.exists(self.DB_PATH):
            messagebox.showerror("Error", f"No se encontró la base de datos en:\n{self.DB_PATH}")
            return

        fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_respaldo = f"respaldo_SF_{fecha_str}.db"
        destino = os.path.join(self.BACKUP_DIR, nombre_respaldo)

        try:
            shutil.copy2(self.DB_PATH, destino)
            self.lbl_ultimo_respaldo.configure(text=f"Último Respaldo: {fecha_str}")
            self.guardar_configuracion()
            messagebox.showinfo("Éxito", "Respaldo creado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al copiar: {e}")

    def seleccionar_archivo_restaurar(self):
        archivo = filedialog.askopenfilename(initialdir=self.BACKUP_DIR, filetypes=[("DB files", "*.db")])
        if archivo: self.path_restaurar.set(archivo)

    def ejecutar_restauracion(self):
        ruta_origen = self.path_restaurar.get()
        if not ruta_origen: return
        
        if messagebox.askyesno("Confirmar", "Esto sobrescribirá la base de datos actual. ¿Continuar?"):
            try:
                # Copia de seguridad antes de restaurar
                shutil.copy2(self.DB_PATH, self.DB_PATH + ".bak")
                # Reemplazo
                shutil.copy2(ruta_origen, self.DB_PATH)
                messagebox.showinfo("Éxito", "Base de datos restaurada.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def guardar_configuracion(self):
        config = {
            "frecuencia": self.combo_frecuencia.get(),
            "hora": self.entry_hora.get(),
            "ultimo": self.lbl_ultimo_respaldo.cget("text")
        }
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    def cargar_configuracion(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.combo_frecuencia.set(config.get("frecuencia", "Diario"))
                self.entry_hora.insert(0, config.get("hora", ""))
                self.lbl_ultimo_respaldo.configure(text=config.get("ultimo", "Último Respaldo: Desconocido"))