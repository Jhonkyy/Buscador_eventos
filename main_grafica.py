#main_grafica.py

import customtkinter as ctk
import tkinter.messagebox as mb
from modelos.sistema import Sistema
from modelos.usuario import Usuario
from datetime import datetime

sistema = Sistema()
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

CATEGORIAS = {
    'musica': ['rock', 'pop', 'jazz', 'clasica', 'electrónica'],
    'comida': ['mexicana', 'italiana', 'colombiana', 'china', 'india'],
    'cultura': ['teatro', 'museo', 'zoológico', 'danza', 'cine'],
    'deporte': ['futbol', 'baloncesto', 'tenis', 'natacion', 'ciclismo']
}

def obtener_ciudades():
    eventos = sistema.cargar_eventos()
    # Normaliza las ciudades para evitar duplicados por mayúsculas/minúsculas
    ciudades = sorted(set(e.ubicacion.strip().title() for e in eventos if e.ubicacion))
    return ciudades if ciudades else ["Medellin"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Buscador de Eventos")
        self.geometry("700x600")
        self.usuario = None
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        ctk.CTkLabel(self, text="Iniciar sesión", font=("Arial", 20)).pack(pady=10)
        correo = ctk.CTkEntry(self, placeholder_text="Correo")
        correo.pack(pady=5)
        contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        contrasena.pack(pady=5)
        def login_action():
            user = sistema.buscar_usuario(correo.get(), contrasena.get())
            if user:
                self.usuario = user
                self.show_menu_usuario()
            else:
                mb.showerror("Error", "Credenciales incorrectas.")
        ctk.CTkButton(self, text="Iniciar sesión", command=login_action).pack(pady=5)
        ctk.CTkButton(self, text="Registrarse", command=self.show_registro).pack(pady=5)

    def show_registro(self):
        self.clear()
        ctk.CTkLabel(self, text="Registro", font=("Arial", 20)).pack(pady=10)
        nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        nombre.pack(pady=5)
        correo = ctk.CTkEntry(self, placeholder_text="Correo")
        correo.pack(pady=5)
        contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        contrasena.pack(pady=5)
        gustos = {}
        checks = {}
        for cat, ops in CATEGORIAS.items():
            frame = ctk.CTkFrame(self)
            frame.pack(pady=2)
            ctk.CTkLabel(frame, text=cat.capitalize()).pack(side="left")
            checks[cat] = []
            for op in ops:
                var = ctk.StringVar()
                chk = ctk.CTkCheckBox(frame, text=op, variable=var, onvalue=op, offvalue="")
                chk.pack(side="left")
                checks[cat].append(var)
        def registrar_action():
            for cat in CATEGORIAS:
                gustos[cat] = [v.get() for v in checks[cat] if v.get()]
            user = Usuario(nombre.get(), correo.get(), contrasena.get(), gustos)
            if sistema.registrar_usuario(user):
                mb.showinfo("Éxito", "¡Usuario registrado!")
                self.show_login()
            else:
                mb.showerror("Error", "Correo ya registrado.")
        ctk.CTkButton(self, text="Registrar", command=registrar_action).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=self.show_login).pack()

    def show_menu_usuario(self):
        self.clear()
        ctk.CTkLabel(self, text=f"Bienvenido {self.usuario.nombre}", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(self, text="Ver recomendaciones", command=self.show_recomendaciones).pack(pady=5)
        ctk.CTkButton(self, text="Buscar eventos (avanzado)", command=self.show_busqueda_avanzada).pack(pady=5)
        ctk.CTkButton(self, text="Agendados", command=self.show_agendados).pack(pady=5)
        ctk.CTkButton(self, text="Recordatorios", command=self.show_recordatorios).pack(pady=5)
        ctk.CTkButton(self, text="Ver/Editar gustos", command=self.show_gustos).pack(pady=5)
        ctk.CTkButton(self, text="Cerrar sesión", command=self.show_login).pack(pady=5)

    def show_recomendaciones(self):
        self.clear()
        ctk.CTkLabel(self, text="Eventos recomendados", font=("Arial", 16)).pack(pady=10)
        eventos = sistema.recomendar_eventos(self.usuario)
        if eventos:
            resultados_frame = ctk.CTkScrollableFrame(self, width=650, height=350)
            resultados_frame.pack(pady=5, fill="both", expand=True)
            for e in eventos:
                frame = ctk.CTkFrame(resultados_frame)
                frame.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(frame, text=str(e)).pack(side="left")
                evento_id = sistema.obtener_id_evento(e.nombre, e.fecha)
                ctk.CTkButton(frame, text="Agendar", width=80, command=lambda eid=evento_id: self.agendar_evento(eid)).pack(side="right")
        else:
            ctk.CTkLabel(self, text="No hay recomendaciones según tus gustos.").pack()
        ctk.CTkButton(self, text="Volver", command=self.show_menu_usuario).pack(pady=10)

    def show_gustos(self):
        self.clear()
        ctk.CTkLabel(self, text="Tus gustos", font=("Arial", 16)).pack(pady=10)
        gustos_actuales = self.usuario.gustos
        checks = {}
        for cat, ops in CATEGORIAS.items():
            frame = ctk.CTkFrame(self)
            frame.pack(pady=2)
            ctk.CTkLabel(frame, text=cat.capitalize()).pack(side="left")
            checks[cat] = []
            for op in ops:
                var = ctk.StringVar(value=op if op in gustos_actuales.get(cat, []) else "")
                chk = ctk.CTkCheckBox(frame, text=op, variable=var, onvalue=op, offvalue="")
                chk.pack(side="left")
                checks[cat].append(var)
        def guardar_gustos():
            nuevos_gustos = {}
            for cat in CATEGORIAS:
                nuevos_gustos[cat] = [v.get() for v in checks[cat] if v.get()]
            self.usuario.gustos = nuevos_gustos
            # Actualiza en la base de datos
            import sqlite3, json
            conn = sqlite3.connect(sistema.db_path)
            c = conn.cursor()
            c.execute("UPDATE usuarios SET gustos=? WHERE correo=?", (json.dumps(self.usuario.gustos), self.usuario.correo))
            conn.commit()
            conn.close()
            mb.showinfo("Gustos", "¡Gustos actualizados!")
            self.show_menu_usuario()
        ctk.CTkButton(self, text="Guardar gustos", command=guardar_gustos).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=self.show_menu_usuario).pack()

    def show_agendados(self):
        self.clear()
        ctk.CTkLabel(self, text="Tus eventos agendados", font=("Arial", 16)).pack(pady=10)
        agendados = sistema.obtener_agendados(self.usuario.correo)
        if agendados:
            for idx, e in enumerate(agendados, 1):
                frame = ctk.CTkFrame(self)
                frame.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(frame, text=f"{idx}. {e.nombre} | {e.categoria} - {e.subcategoria} | {e.fecha}").pack(side="left")
                evento_id = sistema.obtener_id_evento(e.nombre, e.fecha)
                ctk.CTkButton(frame, text="Desagendar", width=80, command=lambda eid=evento_id: self.desagendar_evento(eid)).pack(side="right")
                ctk.CTkButton(frame, text="Recordatorio", width=80, command=lambda eid=evento_id, ev=e: self.enviar_recordatorio(eid, ev)).pack(side="right")
        else:
            ctk.CTkLabel(self, text="No tienes eventos agendados.").pack()
        ctk.CTkButton(self, text="Volver", command=self.show_menu_usuario).pack(pady=10)

    def show_recordatorios(self):
        self.clear()
        ctk.CTkLabel(self, text="Tus recordatorios de eventos agendados", font=("Arial", 16)).pack(pady=10)
        agendados = sistema.obtener_agendados(self.usuario.correo)
        ahora = datetime.now()
        if agendados:
            resultados_frame = ctk.CTkScrollableFrame(self, width=650, height=350)
            resultados_frame.pack(pady=5, fill="both", expand=True)
            for idx, e in enumerate(agendados, 1):
                try:
                    fecha_evento = datetime.strptime(e.fecha, "%Y-%m-%d")
                    delta = fecha_evento - ahora
                    if delta.total_seconds() > 0:
                        dias = delta.days
                        horas, rem = divmod(delta.seconds, 3600)
                        minutos = rem // 60
                        tiempo_falta = f"Faltan {dias}d {horas}h {minutos}m"
                    else:
                        tiempo_falta = "¡Ya ocurrió!"
                except Exception:
                    tiempo_falta = "Fecha inválida"
                frame = ctk.CTkFrame(resultados_frame)
                frame.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(frame, text=f"{idx}. {e.nombre} | {e.categoria} - {e.subcategoria} | {e.fecha}").pack(side="left")
                ctk.CTkLabel(frame, text=tiempo_falta, fg_color="transparent", text_color="#007acc").pack(side="right")
        else:
            ctk.CTkLabel(self, text="No tienes eventos agendados.").pack()
        ctk.CTkButton(self, text="Volver", command=self.show_menu_usuario).pack(pady=10)

    def agendar_evento(self, evento_id):
        sistema.agendar_evento(self.usuario.correo, evento_id)
        mb.showinfo("Agendados", "¡Evento agendado!")

    def desagendar_evento(self, evento_id):
        sistema.desagendar_evento(self.usuario.correo, evento_id)
        mb.showinfo("Agendados", "Evento desagendado.")
        self.show_agendados()

    def enviar_recordatorio(self, evento_id, evento):
        exito = sistema.enviar_recordatorio(self.usuario.correo, evento)
        if exito:
            mb.showinfo("Recordatorio", "¡Recordatorio enviado por correo!")
        else:
            mb.showerror("Recordatorio", "No se pudo enviar el correo.")

    def show_busqueda_avanzada(self):
        self.clear()
        ctk.CTkLabel(self, text="Búsqueda avanzada", font=("Arial", 16)).pack(pady=10)
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=5)
        nombre = ctk.CTkEntry(frame_filtros, placeholder_text="Nombre del evento")
        nombre.grid(row=0, column=0, padx=5, pady=2)
        categorias = list(CATEGORIAS.keys())
        categoria_var = ctk.StringVar(value="")
        subcategoria_var = ctk.StringVar(value="")
        ciudad_var = ctk.StringVar(value="")
        ctk.CTkLabel(frame_filtros, text="Categoría:").grid(row=0, column=1)
        categoria_menu = ctk.CTkOptionMenu(frame_filtros, values=[""] + categorias, variable=categoria_var)
        categoria_menu.grid(row=0, column=2, padx=5)
        ctk.CTkLabel(frame_filtros, text="Subcategoría:").grid(row=1, column=1)
        subcategoria_menu = ctk.CTkOptionMenu(frame_filtros, values=[""], variable=subcategoria_var)
        subcategoria_menu.grid(row=1, column=2, padx=5)
        ctk.CTkLabel(frame_filtros, text="Ciudad:").grid(row=2, column=1)
        ciudades = obtener_ciudades()
        ciudad_menu = ctk.CTkOptionMenu(frame_filtros, values=[""] + ciudades, variable=ciudad_var)
        ciudad_menu.grid(row=2, column=2, padx=5)
        # Fecha por rango
        fecha_desde = ctk.CTkEntry(frame_filtros, placeholder_text="Fecha desde (YYYY-MM-DD)")
        fecha_desde.grid(row=3, column=1, padx=5)
        fecha_hasta = ctk.CTkEntry(frame_filtros, placeholder_text="Fecha hasta (YYYY-MM-DD)")
        fecha_hasta.grid(row=3, column=2, padx=5)
        resultados_frame = ctk.CTkScrollableFrame(self, width=600, height=250)
        resultados_frame.pack(pady=5)
        eventos = []
        def actualizar_subcategorias(*_):
            cat = categoria_var.get()
            if cat in CATEGORIAS:
                subcategoria_menu.configure(values=[""] + CATEGORIAS[cat])
            else:
                subcategoria_menu.configure(values=[""])
            subcategoria_var.set("")
        categoria_var.trace_add("write", actualizar_subcategorias)

        def buscar():
            for widget in resultados_frame.winfo_children():
                widget.destroy()
            eventos.clear()
            desde = fecha_desde.get().strip() or None
            hasta = fecha_hasta.get().strip() or None
            ciudad_filtro = ciudad_var.get().strip() or None
            eventos_bd = sistema.buscar_eventos_avanzado(
                nombre=nombre.get() or None,
                categoria=categoria_var.get() or None,
                subcategoria=subcategoria_var.get() or None,
                ciudad=ciudad_filtro,
                fecha=None
            )
            from datetime import datetime
            def en_rango(e):
                try:
                    f = datetime.strptime(e.fecha, "%Y-%m-%d")
                    if desde:
                        f_desde = datetime.strptime(desde, "%Y-%m-%d")
                        if f < f_desde:
                            return False
                    if hasta:
                        f_hasta = datetime.strptime(hasta, "%Y-%m-%d")
                        if f > f_hasta:
                            return False
                    return True
                except Exception:
                    return False
            eventos_filtrados = [e for e in eventos_bd if en_rango(e)]
            if eventos_filtrados:
                for idx, e in enumerate(eventos_filtrados, 1):
                    eventos.append(e)
                    frame = ctk.CTkFrame(resultados_frame)
                    frame.pack(fill="x", padx=5, pady=2)
                    ctk.CTkLabel(frame, text=f"{idx}. {e.nombre} | {e.categoria} - {e.subcategoria} | {e.fecha}").pack(side="left")
                    evento_id = sistema.obtener_id_evento(e.nombre, e.fecha)
                    ctk.CTkButton(frame, text="Agendar", width=80, command=lambda eid=evento_id: self.agendar_evento(eid)).pack(side="right")
            else:
                ctk.CTkLabel(resultados_frame, text="No se encontraron eventos.").pack()
        ctk.CTkButton(self, text="Buscar", command=buscar).pack(pady=5)
        ctk.CTkButton(self, text="Volver", command=self.show_menu_usuario).pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()
