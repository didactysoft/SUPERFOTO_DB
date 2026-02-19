import customtkinter as ctk

class BackupFrame(ctk.CTkFrame):
    """Módulo de Respaldo y Mantenimiento de la Base de Datos."""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor central blanco
        frame_content = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_content.grid_columnconfigure(0, weight=1)
        frame_content.grid_rowconfigure(1, weight=1) # Fila del área de panel expandible

        # --- Cabecera ---
        ctk.CTkLabel(frame_content, 
                     text=f"MÓDULO: {title.upper()}", 
                     font=("Arial", 28, "bold"), 
                     text_color="#CC0000").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # --- Panel Principal (Scrollable) ---
        panel = ctk.CTkScrollableFrame(frame_content, fg_color="#F0F0F0")
        panel.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        
        # --- Sección de Respaldo Manual ---
        backup_section = ctk.CTkFrame(panel, fg_color="white", corner_radius=10, border_width=1, border_color="#D0D0D0")
        backup_section.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(backup_section, text="Respaldo Manual de la Base de Datos", font=("Arial", 18, "bold"), text_color="#1F6AA5").pack(pady=(10, 5))
        ctk.CTkLabel(backup_section, text="Genera una copia de seguridad de toda la información de la aplicación.", text_color="#333").pack(pady=5)
        
        ctk.CTkButton(backup_section, text="⚙️ Generar Respaldo Ahora", fg_color="#4CAF50", hover_color="#388E3C", font=("Arial", 14, "bold")).pack(pady=15)
        
        ctk.CTkLabel(backup_section, text="Último Respaldo: 2025-10-30 10:45 AM | Ubicación: C:/SuperFotoDB/Backups/", text_color="#666").pack(pady=(0, 10))

        # --- Sección de Restauración ---
        restore_section = ctk.CTkFrame(panel, fg_color="white", corner_radius=10, border_width=1, border_color="#D0D0D0")
        restore_section.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(restore_section, text="Restaurar Base de Datos", font=("Arial", 18, "bold"), text_color="#FF4500").pack(pady=(10, 5))
        ctk.CTkLabel(restore_section, text="¡ADVERTENCIA! Esta acción reemplazará los datos actuales y no se puede deshacer. Úsala con precaución.", text_color="red").pack(pady=5)
        
        frame_restore_controls = ctk.CTkFrame(restore_section, fg_color="transparent")
        frame_restore_controls.pack(pady=15)
        
        ctk.CTkButton(frame_restore_controls, text="📂 Seleccionar Archivo de Respaldo", fg_color="#9E9E9E", hover_color="#757575").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_restore_controls, text="⚠️ Restaurar DB", fg_color="#F44336", hover_color="#D32F2F").grid(row=0, column=1, padx=10)

        # --- Sección de Respaldo Automático ---
        auto_backup_section = ctk.CTkFrame(panel, fg_color="white", corner_radius=10, border_width=1, border_color="#D0D0D0")
        auto_backup_section.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(auto_backup_section, text="Respaldo Programado (Automático)", font=("Arial", 18, "bold"), text_color="#1F6AA5").pack(pady=(10, 5))
        
        frame_schedule = ctk.CTkFrame(auto_backup_section, fg_color="transparent")
        frame_schedule.pack(pady=10)
        
        ctk.CTkLabel(frame_schedule, text="Frecuencia:", text_color="#333").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkComboBox(frame_schedule, values=["Diario", "Semanal", "Mensual"], width=150).grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_schedule, text="Hora:", text_color="#333").grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkEntry(frame_schedule, placeholder_text="02:00 AM", width=100).grid(row=0, column=3, padx=5, pady=5)
        
        ctk.CTkButton(auto_backup_section, text="Guardar Programación", fg_color="#4CAF50", hover_color="#388E3C").pack(pady=(0, 10))