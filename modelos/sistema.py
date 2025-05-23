# modelos/sistema.py
import json
from modelos.usuario import Usuario
from modelos.evento import Evento


class Sistema:
    def __init__(self, archivo_usuarios="datos/usuarios.json", archivo_eventos="datos/eventos.json"):
        self.archivo_usuarios = archivo_usuarios
        self.archivo_eventos = archivo_eventos
        self.usuarios = self.cargar_usuarios()
        self.eventos = self.cargar_eventos()

    def cargar_usuarios(self):
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                return [Usuario.from_dict(u) for u in json.load(f)]
        except:
            return []

    def guardar_usuarios(self):
        with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4)

    def cargar_eventos(self):
        try:
            with open(self.archivo_eventos, 'r', encoding='utf-8') as f:
                return [Evento(**e) for e in json.load(f)]
        except:
            return []

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.guardar_usuarios()

    def buscar_usuario(self, correo, contrasena):
        for u in self.usuarios:
            if u.correo == correo and u.contrasena == contrasena:
                return u
        return None

    def recomendar_eventos(self, usuario):
        recomendados = []
        for evento in self.eventos:
            if evento.categoria in usuario.gustos:
                if evento.subcategoria in usuario.gustos[evento.categoria]:
                    recomendados.append(evento)
        return recomendados

    def eventos_por_ciudad(self, ciudad):
        ciudad_lower = ciudad.lower()
        return [e for e in self.eventos if e.ubicacion.lower() == ciudad_lower]
