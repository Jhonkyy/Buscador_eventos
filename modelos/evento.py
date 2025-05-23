# modelos/evento.py
class Evento:
    def __init__(self, nombre, categoria, subcategoria, ubicacion, fecha, descripcion):
        self.nombre = nombre
        self.categoria = categoria  # música, comida, cultura
        self.subcategoria = subcategoria  # rock, italiana, teatro, etc.
        self.ubicacion = ubicacion
        self.fecha = fecha
        self.descripcion = descripcion

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"{self.nombre} | {self.categoria} - {self.subcategoria} | {self.ubicacion} | {self.fecha}\n{self.descripcion}\n"

