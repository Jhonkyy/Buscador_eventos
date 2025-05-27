import customtkinter as ctk
import tkinter.messagebox as mb
from modelos.usuario import Usuario

CATEGORIAS = {
    'musica': ['rock', 'pop', 'jazz', 'clasica', 'electrónica'],
    'comida': ['mexicana', 'italiana', 'colombiana', 'china', 'india'],
    'cultura': ['teatro', 'museo', 'zoológico', 'danza', 'cine'],
    'deporte': ['futbol', 'baloncesto', 'tenis', 'natacion', 'ciclismo']
}

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, sistema, on_login):
        super().__init__(master)
        self.sistema = sistema
        self.on_login = on_login
        self.pack(fill="both", expand=True)
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
            user = self.sistema.buscar_usuario(correo.get(), contrasena.get())
            if user:
                self.on_login(user)
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
            if self.sistema.registrar_usuario(user):
                mb.showinfo("Éxito", "¡Usuario registrado!")
                self.show_login()
            else:
                mb.showerror("Error", "Correo ya registrado.")
        ctk.CTkButton(self, text="Registrar", command=registrar_action).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=self.show_login).pack()