import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "buscador_eventos.db")

eventos_demo = [
    # Medellín
    {
        "nombre": "Rock al Parque Medellín",
        "categoria": "musica",
        "subcategoria": "rock",
        "ubicacion": "Medellin",
        "fecha": "2024-07-15",
        "descripcion": "Festival de rock con bandas nacionales e internacionales en Medellín."
    },
    {
        "nombre": "Jazz Nights Medellín",
        "categoria": "musica",
        "subcategoria": "jazz",
        "ubicacion": "Medellin",
        "fecha": "2024-11-20",
        "descripcion": "Noches de jazz con artistas locales e internacionales."
    },
    {
        "nombre": "Feria Gastronómica Paisa",
        "categoria": "comida",
        "subcategoria": "colombiana",
        "ubicacion": "Medellin",
        "fecha": "2024-08-10",
        "descripcion": "Disfruta de la mejor comida típica antioqueña en la feria gastronómica."
    },
    # Bogotá
    {
        "nombre": "Pop Fest Bogotá",
        "categoria": "musica",
        "subcategoria": "pop",
        "ubicacion": "Bogotá",
        "fecha": "2024-08-22",
        "descripcion": "Festival de música pop con artistas reconocidos en Bogotá."
    },
    {
        "nombre": "Cine al Parque Bogotá",
        "categoria": "cultura",
        "subcategoria": "cine",
        "ubicacion": "Bogotá",
        "fecha": "2024-09-05",
        "descripcion": "Proyección de películas al aire libre en diferentes parques de Bogotá."
    },
    {
        "nombre": "Festival de Pizza Italiana",
        "categoria": "comida",
        "subcategoria": "italiana",
        "ubicacion": "Bogotá",
        "fecha": "2024-09-18",
        "descripcion": "Las mejores pizzerías de Bogotá en un solo lugar."
    },
    # Cali
    {
        "nombre": "Clásicos en Concierto",
        "categoria": "musica",
        "subcategoria": "clasica",
        "ubicacion": "Cali",
        "fecha": "2024-09-10",
        "descripcion": "Orquesta sinfónica interpretando piezas clásicas en Cali."
    },
    {
        "nombre": "Sabores de México",
        "categoria": "comida",
        "subcategoria": "mexicana",
        "ubicacion": "Cali",
        "fecha": "2024-10-12",
        "descripcion": "Festival de comida mexicana con tacos, burritos y más en Cali."
    },
    {
        "nombre": "Danza Folclórica Colombiana",
        "categoria": "cultura",
        "subcategoria": "danza",
        "ubicacion": "Cali",
        "fecha": "2024-11-11",
        "descripcion": "Presentación de grupos de danza tradicional en Cali."
    },
    # Barranquilla
    {
        "nombre": "Electro Barranquilla",
        "categoria": "musica",
        "subcategoria": "electrónica",
        "ubicacion": "Barranquilla",
        "fecha": "2024-12-05",
        "descripcion": "Fiesta de música electrónica con DJs internacionales en Barranquilla."
    },
    {
        "nombre": "China Food Fest",
        "categoria": "comida",
        "subcategoria": "china",
        "ubicacion": "Barranquilla",
        "fecha": "2024-11-02",
        "descripcion": "Descubre la auténtica comida china en Barranquilla."
    },
    {
        "nombre": "Obra de Teatro: La Casa de Bernarda Alba",
        "categoria": "cultura",
        "subcategoria": "teatro",
        "ubicacion": "Barranquilla",
        "fecha": "2024-08-30",
        "descripcion": "Clásico del teatro español en el Teatro Amira de la Rosa."
    },
    # Cartagena
    {
        "nombre": "Curry y Sabor",
        "categoria": "comida",
        "subcategoria": "india",
        "ubicacion": "Cartagena",
        "fecha": "2024-12-15",
        "descripcion": "Festival de comida india con chefs invitados en Cartagena."
    },
    {
        "nombre": "Exposición de Arte Moderno",
        "categoria": "cultura",
        "subcategoria": "museo",
        "ubicacion": "Cartagena",
        "fecha": "2024-10-20",
        "descripcion": "Obras de artistas contemporáneos en el Museo de Arte Moderno de Cartagena."
    },
    # Bucaramanga
    {
        "nombre": "Maratón de Bucaramanga",
        "categoria": "deporte",
        "subcategoria": "ciclismo",
        "ubicacion": "Bucaramanga",
        "fecha": "2024-10-01",
        "descripcion": "Participa en la maratón anual de ciclismo por las calles de Bucaramanga."
    },
    {
        "nombre": "Torneo de Fútbol Infantil",
        "categoria": "deporte",
        "subcategoria": "futbol",
        "ubicacion": "Bucaramanga",
        "fecha": "2024-08-05",
        "descripcion": "Torneo para niños y jóvenes en diferentes comunas de Bucaramanga."
    },
    # Pereira
    {
        "nombre": "Copa de Baloncesto Pereira",
        "categoria": "deporte",
        "subcategoria": "baloncesto",
        "ubicacion": "Pereira",
        "fecha": "2024-09-12",
        "descripcion": "Equipos locales compiten por la copa de la ciudad de Pereira."
    },
    # Manizales
    {
        "nombre": "Torneo de Tenis Abierto",
        "categoria": "deporte",
        "subcategoria": "tenis",
        "ubicacion": "Manizales",
        "fecha": "2024-11-18",
        "descripcion": "Competencia abierta de tenis para todas las edades en Manizales."
    },
    # Armenia
    {
        "nombre": "Festival de Natación Armenia",
        "categoria": "deporte",
        "subcategoria": "natacion",
        "ubicacion": "Armenia",
        "fecha": "2024-12-08",
        "descripcion": "Competencias y exhibiciones de natación en la unidad deportiva de Armenia."
    },
    # Cúcuta
    {
        "nombre": "Festival Internacional de Poesía",
        "categoria": "cultura",
        "subcategoria": "teatro",
        "ubicacion": "Cúcuta",
        "fecha": "2024-07-28",
        "descripcion": "Lecturas y talleres con poetas de todo el mundo en Cúcuta."
    },
    # Santa Marta
    {
        "nombre": "Encuentro de Food Trucks",
        "categoria": "comida",
        "subcategoria": "mexicana",
        "ubicacion": "Santa Marta",
        "fecha": "2024-09-25",
        "descripcion": "Variedad de food trucks con opciones mexicanas y más en Santa Marta."
    },
    # Pasto
    {
        "nombre": "Noche de Salsa Pasto",
        "categoria": "musica",
        "subcategoria": "pop",
        "ubicacion": "Pasto",
        "fecha": "2024-10-14",
        "descripcion": "Baile y música salsa en vivo en Pasto."
    },
    # Villavicencio
    {
        "nombre": "Ciclo de Cine Francés",
        "categoria": "cultura",
        "subcategoria": "cine",
        "ubicacion": "Villavicencio",
        "fecha": "2024-11-03",
        "descripcion": "Proyección de películas francesas clásicas y contemporáneas en Villavicencio."
    },
    # Montería
    {
        "nombre": "Expo Café Montería",
        "categoria": "comida",
        "subcategoria": "colombiana",
        "ubicacion": "Montería",
        "fecha": "2024-10-28",
        "descripcion": "Muestra de cafés especiales y charlas con baristas en Montería."
    },
    # Quibdó
    {
        "nombre": "Festival de Música del Pacífico",
        "categoria": "musica",
        "subcategoria": "jazz",
        "ubicacion": "Quibdó",
        "fecha": "2024-09-20",
        "descripcion": "Festival con agrupaciones musicales del Pacífico colombiano en Quibdó."
    },
    {
        "nombre": "Feria Gastronómica Chocoana",
        "categoria": "comida",
        "subcategoria": "colombiana",
        "ubicacion": "Quibdó",
        "fecha": "2024-11-10",
        "descripcion": "Muestra de la gastronomía típica del Chocó en Quibdó."
    },
    {
        "nombre": "Carnaval de Quibdó",
        "categoria": "cultura",
        "subcategoria": "danza",
        "ubicacion": "Quibdó",
        "fecha": "2024-12-01",
        "descripcion": "Desfile de comparsas y danzas tradicionales en el Carnaval de Quibdó."
    },
    {
        "nombre": "Copa de Baloncesto Quibdó",
        "categoria": "deporte",
        "subcategoria": "baloncesto",
        "ubicacion": "Quibdó",
        "fecha": "2024-08-18",
        "descripcion": "Torneo de baloncesto con equipos locales en Quibdó."
    }
]

# Asegura que la carpeta 'datos' exista
carpeta = os.path.dirname(db_path)
if carpeta and not os.path.exists(carpeta):
    os.makedirs(carpeta)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Crea la tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        subcategoria TEXT,
        ubicacion TEXT,
        fecha TEXT,
        descripcion TEXT
    )
''')

# Inserta los eventos demo
for evento in eventos_demo:
    c.execute(
        "INSERT INTO eventos (nombre, categoria, subcategoria, ubicacion, fecha, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
        (
            evento["nombre"],
            evento["categoria"],
            evento["subcategoria"],
            evento["ubicacion"],
            evento["fecha"],
            evento["descripcion"]
        )
    )

conn.commit()
conn.close()
print("Eventos de prueba insertados correctamente.")