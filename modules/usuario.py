import customtkinter as ctk
from tkinter import messagebox
from modules.database_manager import ejecutar_consulta, ejecutar_accion

class UsuariosFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="GESTIÓN DE ACCESOS", font=("Arial", 24, "bold"), text_color="#1F6AA5").grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        ctk.CTkButton(self, text="🔑 Crear Nuevo Acceso", fg_color="#1F6AA5", 
                      command=self.abrir_ventana_usuario).grid(row=1, column=0, padx=20, pady=(0,10), sticky="w")

        self.frame_tabla = None
        self.actualizar_tabla()

    def actualizar_tabla(self):
        if self.frame_tabla: self.frame_tabla.destroy()
        self.frame_tabla = ctk.CTkScrollableFrame(self)
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure((1,2,3), weight=1)

        headers = ["ID", "Empleado", "Login", "Rol", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.frame_tabla, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, pady=10)

        query = """
            SELECT u.id_usuario, e.nombre, u.usuario, r.nombre 
            FROM usuario u
            JOIN empleado e ON u.id_empleado = e.id_empleado
            JOIN rol r ON u.id_rol = r.id_rol
        """
        for row_idx, (uid, emp, log, rol) in enumerate(ejecutar_consulta(query), start=1):
            ctk.CTkLabel(self.frame_tabla, text=uid).grid(row=row_idx, column=0)
            ctk.CTkLabel(self.frame_tabla, text=emp).grid(row=row_idx, column=1)
            ctk.CTkLabel(self.frame_tabla, text=log, font=("Arial", 12, "bold")).grid(row=row_idx, column=2)
            ctk.CTkLabel(self.frame_tabla, text=rol).grid(row=row_idx, column=3)
            
            btn_f = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
            btn_f.grid(row=row_idx, column=4)
            ctk.CTkButton(btn_f, text="✏️", width=30, fg_color="#FFB300", text_color="black",
                          command=lambda i=uid: self.abrir_ventana_usuario(i)).pack(side="left", padx=2)
            ctk.CTkButton(btn_f, text="🗑️", width=30, fg_color="#E74C3C",
                          command=lambda i=uid: self.eliminar_acceso(i)).pack(side="left", padx=2)

    def abrir_ventana_usuario(self, usuario_id=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Configurar Credenciales")
        ventana.geometry("400x580")
        ventana.grab_set()

        # Cargar Roles
        roles_db = ejecutar_consulta("SELECT id_rol, nombre FROM rol")
        dict_roles = {r[1]: r[0] for r in roles_db}

        datos = ["", "", "", ""]
        if usuario_id:
            # Si editamos, cargamos los datos actuales del usuario
            res = ejecutar_consulta("SELECT id_empleado, usuario, contraseña, id_rol FROM usuario WHERE id_usuario = ?", (usuario_id,))
            if res: datos = res[0]
            # En edición, el empleado no se cambia fácilmente para mantener integridad
            empleado_nombre = ejecutar_consulta("SELECT nombre FROM empleado WHERE id_empleado = ?", (datos[0],))[0][0]
            ctk.CTkLabel(ventana, text=f"Empleado: {empleado_nombre}", font=("Arial", 12, "bold")).pack(pady=20)
        else:
            # En creación, mostramos empleados disponibles (sin cuenta)
            empleados_db = ejecutar_consulta("SELECT id_empleado, nombre FROM empleado WHERE id_empleado NOT IN (SELECT id_empleado FROM usuario)")
            if not empleados_db:
                messagebox.showinfo("Aviso", "No hay empleados disponibles para nuevas cuentas.")
                return ventana.destroy()
            dict_emp = {e[1]: e[0] for e in empleados_db}
            ctk.CTkLabel(ventana, text="Seleccionar Empleado:").pack(pady=(20,0))
            combo_emp = ctk.CTkComboBox(ventana, values=list(dict_emp.keys()), width=250); combo_emp.pack()

        ctk.CTkLabel(ventana, text="Nombre de Usuario (Login):").pack(pady=10)
        ent_log = ctk.CTkEntry(ventana, width=250); ent_log.pack(); ent_log.insert(0, datos[1])

        ctk.CTkLabel(ventana, text="Nueva Contraseña:").pack(pady=10)
        ent_pass = ctk.CTkEntry(ventana, width=250, show="●"); ent_pass.pack(); ent_pass.insert(0, datos[2])

        ctk.CTkLabel(ventana, text="Rol del Sistema:").pack(pady=10)
        combo_rol = ctk.CTkComboBox(ventana, values=list(dict_roles.keys()), width=250); combo_rol.pack()
        
        # Seleccionar rol actual si es edición
        if usuario_id:
            nombre_rol = [k for k, v in dict_roles.items() if v == datos[3]][0]
            combo_rol.set(nombre_rol)

        def guardar():
            u, p = ent_log.get(), ent_pass.get()
            r_id = dict_roles.get(combo_rol.get())
            
            if usuario_id:
                sql = "UPDATE usuario SET usuario=?, contraseña=?, id_rol=? WHERE id_usuario=?"
                params = (u, p, r_id, usuario_id)
            else:
                e_id = dict_emp.get(combo_emp.get())
                sql = "INSERT INTO usuario (id_empleado, usuario, contraseña, id_rol) VALUES (?,?,?,?)"
                params = (e_id, u, p, r_id)

            if ejecutar_accion(sql, params):
                messagebox.showinfo("Éxito", "Usuario actualizado")
                ventana.destroy()
                self.actualizar_tabla()

        ctk.CTkButton(ventana, text="✅ Guardar Credenciales", command=guardar).pack(pady=30)

    def eliminar_acceso(self, uid):
        if messagebox.askyesno("Confirmar", "¿Desea revocar el acceso a este usuario?"):
            if ejecutar_accion("DELETE FROM usuario WHERE id_usuario=?", (uid,)):
                self.actualizar_tabla()