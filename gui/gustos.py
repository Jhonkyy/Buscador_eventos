import customtkinter as ctk
import tkinter.messagebox as mb
import sqlite3
import json

CATEGORIAS = {
    'musica': ['rock', 'pop', 'jazz', 'clasica', 'electrónica'],
    'comida': ['mexicana', 'italiana', 'colombiana', 'china', 'india'],
    'cultura': ['teatro', 'museo', 'zoológico', 'danza', 'cine'],
    'deporte': ['futbol', 'baloncesto', 'tenis', 'natacion', 'ciclismo']
}

class GustosFrame(ctk.CTkFrame):
    def __init__(self, master, usuario, sistema, on_volver):
        super().__init__(master)
        self.usuario = usuario
        self.sistema = sistema
        self.on_volver = on_volver
        self.pack(fill="both", expand=True)
        self.show_gustos()

    def show_gustos(self):
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
            conn = sqlite3.connect(self.sistema.db_path)
            c = conn.cursor()
            c.execute("UPDATE usuarios SET gustos=? WHERE correo=?", (json.dumps(self.usuario.gustos), self.usuario.correo))
            conn.commit()
            conn.close()
            mb.showinfo("Gustos", "¡Gustos actualizados!")
            self.on_volver()
        ctk.CTkButton(self, text="Guardar gustos", command=guardar_gustos).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=self.on_volver).pack()
