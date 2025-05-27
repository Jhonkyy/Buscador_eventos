import sqlite3
import os

# Ruta absoluta al archivo de base de datos
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "buscador_eventos.db")

# Asegura que la carpeta 'datos' exista
carpeta = os.path.dirname(db_path)
if carpeta and not os.path.exists(carpeta):
    os.makedirs(carpeta)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Crea las tablas si no existen
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT UNIQUE,
        contrasena TEXT,
        gustos TEXT
    )
''')
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
conn.commit()

print("Tablas:")
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print("-", row[0])

print("\nUsuarios:")
usuarios = list(c.execute("SELECT * FROM usuarios;"))
if usuarios:
    for row in usuarios:
        print(row)
else:
    print("No hay usuarios registrados.")

print("\nEventos:")
eventos = list(c.execute("SELECT * FROM eventos;"))
if eventos:
    for row in eventos:
        print(row)
else:
    print("No hay eventos registrados.")

conn.close()
