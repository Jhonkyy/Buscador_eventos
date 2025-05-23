# modelos/usuario.py
class Usuario:
    def __init__(self, nombre, correo, contrasena, gustos=None):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.gustos = gustos if gustos else {
            'musica': [],
            'comida': [],
            'cultura': []
        }

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'correo': self.correo,
            'contrasena': self.contrasena,
            'gustos': self.gustos
        }

    @staticmethod
    def from_dict(data):
        return Usuario(data['nombre'], data['correo'], data['contrasena'], data['gustos'])
