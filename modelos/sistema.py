import sqlite3
import json
import os
import smtplib
from email.mime.text import MIMEText
from modelos.usuario import Usuario
from modelos.evento import Evento

class Sistema:
    def __init__(self, db_path="datos/buscador_eventos.db"):
        carpeta = os.path.dirname(db_path)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.db_path = db_path
        self._crear_tablas()
        # self._reset_usuarios()  # Elimina o comenta esta línea para no borrar usuarios

    def _crear_tablas(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
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
        # Tabla de agendados: usuario_correo, evento_id
        c.execute('''
            CREATE TABLE IF NOT EXISTS agendados (
                usuario_correo TEXT,
                evento_id INTEGER,
                PRIMARY KEY (usuario_correo, evento_id),
                FOREIGN KEY (usuario_correo) REFERENCES usuarios(correo),
                FOREIGN KEY (evento_id) REFERENCES eventos(id)
            )
        ''')
        conn.commit()
        conn.close()

    def _reset_usuarios(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Borra todos los usuarios
        c.execute("DELETE FROM usuarios")
        # Inserta el usuario "a"
        gustos = json.dumps({'musica': [], 'comida': [], 'cultura': [], 'deporte': []})
        c.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, gustos) VALUES (?, ?, ?, ?)",
            ("a", "a", "a", gustos)
        )
        conn.commit()
        conn.close()

    def registrar_usuario(self, usuario):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, gustos) VALUES (?, ?, ?, ?)",
                (usuario.nombre, usuario.correo, usuario.contrasena, json.dumps(usuario.gustos))
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            print("Ya existe un usuario con ese correo.")
            return False

    def buscar_usuario(self, correo, contrasena):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT nombre, correo, contrasena, gustos FROM usuarios WHERE correo=? AND contrasena=?", (correo, contrasena))
        row = c.fetchone()
        conn.close()
        if row:
            nombre, correo, contrasena, gustos_json = row
            gustos = json.loads(gustos_json)
            return Usuario(nombre, correo, contrasena, gustos)
        return None

    def recomendar_eventos(self, usuario):
        eventos = self.cargar_eventos()
        recomendados = []
        for evento in eventos:
            if evento.categoria in usuario.gustos:
                if evento.subcategoria in usuario.gustos[evento.categoria]:
                    recomendados.append(evento)
        return recomendados

    def eventos_por_ciudad(self, ciudad):
        eventos = self.cargar_eventos()
        ciudad_lower = ciudad.lower()
        return [e for e in eventos if e.ubicacion.lower() == ciudad_lower]

    def cargar_eventos(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT nombre, categoria, subcategoria, ubicacion, fecha, descripcion FROM eventos")
        eventos = [Evento(*row) for row in c.fetchall()]
        conn.close()
        return eventos

    def agregar_evento(self, evento):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO eventos (nombre, categoria, subcategoria, ubicacion, fecha, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
            (evento.nombre, evento.categoria, evento.subcategoria, evento.ubicacion, evento.fecha, evento.descripcion)
        )
        conn.commit()
        conn.close()

    # --------- Búsqueda avanzada de eventos ---------
    def buscar_eventos_avanzado(self, nombre=None, categoria=None, subcategoria=None, ciudad=None, fecha=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT nombre, categoria, subcategoria, ubicacion, fecha, descripcion FROM eventos WHERE 1=1"
        params = []
        if nombre:
            query += " AND nombre LIKE ?"
            params.append(f"%{nombre}%")
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if subcategoria:
            query += " AND subcategoria = ?"
            params.append(subcategoria)
        if ciudad:
            query += " AND ubicacion = ?"
            params.append(ciudad)
        if fecha:
            query += " AND fecha = ?"
            params.append(fecha)
        c.execute(query, params)
        eventos = [Evento(*row) for row in c.fetchall()]
        conn.close()
        return eventos

    # --------- Sistema de agendados ---------
    def agendar_evento(self, usuario_correo, evento_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO agendados (usuario_correo, evento_id) VALUES (?, ?)", (usuario_correo, evento_id))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ya está agendado
        conn.close()

    def desagendar_evento(self, usuario_correo, evento_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM agendados WHERE usuario_correo=? AND evento_id=?", (usuario_correo, evento_id))
        conn.commit()
        conn.close()

    def obtener_agendados(self, usuario_correo):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT e.id, e.nombre, e.categoria, e.subcategoria, e.ubicacion, e.fecha, e.descripcion
            FROM eventos e
            JOIN agendados a ON e.id = a.evento_id
            WHERE a.usuario_correo = ?
        ''', (usuario_correo,))
        eventos = [Evento(row[1], row[2], row[3], row[4], row[5], row[6]) for row in c.fetchall()]
        conn.close()
        return eventos

    # --------- Notificaciones por correo ---------
    def enviar_recordatorio(self, usuario_correo, evento):
        # Configura aquí tus credenciales SMTP y el remitente
        remitente = "tucorreo@gmail.com"
        password = "tu_contraseña_de_aplicacion"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        asunto = f"Recordatorio: Evento agendado - {evento.nombre}"
        cuerpo = f"""Hola,

Este es un recordatorio de tu evento agendado:

Nombre: {evento.nombre}
Categoría: {evento.categoria}
Subcategoría: {evento.subcategoria}
Ubicación: {evento.ubicacion}
Fecha: {evento.fecha}
Descripción: {evento.descripcion}

¡No olvides asistir!

Buscador de Eventos
"""
        msg = MIMEText(cuerpo)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = usuario_correo

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(remitente, password)
                server.sendmail(remitente, usuario_correo, msg.as_string())
            return True
        except Exception as e:
            print(f"Error enviando correo: {e}")
            return False

    def obtener_id_evento(self, nombre, fecha):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM eventos WHERE nombre=? AND fecha=?", (nombre, fecha))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
