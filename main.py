# main.py
from modelos.sistema import Sistema
from modelos.usuario import Usuario

sistema = Sistema()

def menu_usuario(usuario):
    while True:
        print(f"\nBienvenido {usuario.nombre}")
        print("1. Ver recomendaciones")
        print("2. Ver eventos cercanos")
        print("3. Modificar gustos")
        print("4. Ver eventos por categoría")
        print("5. Buscar eventos (búsqueda avanzada)")
        print("6. Agendar eventos")
        print("7. Cerrar sesión")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            recomendados = sistema.recomendar_eventos(usuario)
            if recomendados:
                print("\nEventos recomendados para ti:")
                for e in recomendados:
                    print(e)
            else:
                print("No se encontraron eventos que coincidan con tus gustos.")
        elif opcion == "2":
            ciudad = input("¿En qué ciudad estás? ")
            eventos = sistema.eventos_por_ciudad(ciudad)
            if eventos:
                print(f"\nEventos en {ciudad}:")
                for e in eventos:
                    print(e)
            else:
                print("No hay eventos en esa ciudad.")
        elif opcion == "3":
            modificar_gustos(usuario)
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def seleccionar_gustos(opciones_gustos):
    gustos = {}
    for categoria, opciones in opciones_gustos.items():
        print(f"\n¿Qué {categoria} te gustan? Elige los números separados por comas:")
        for i, opcion in enumerate(opciones, 1):
            print(f"{i}. {opcion}")

        seleccion = input("Tu elección: ")
        seleccion_indices = [int(x.strip()) for x in seleccion.split(",") if x.strip().isdigit() and 1 <= int(x.strip()) <= len(opciones)]

        gustos[categoria] = [opciones[i-1] for i in seleccion_indices] if seleccion_indices else []
    return gustos

# Usar en registrar:
def registrar():
    print("\n--- Registro ---")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    opciones_gustos = {
        'musica': ['rock', 'pop', 'jazz', 'clasica', 'electrónica'],
        'comida': ['mexicana', 'italiana', 'colombiana', 'china', 'india'],
        'cultura': ['teatro', 'museo', 'zoológico', 'danza', 'cine'],
        'deporte': ['futbol', 'baloncesto', 'tenis', 'natacion', 'ciclismo']
    }

    gustos = seleccionar_gustos(opciones_gustos)

    usuario = Usuario(nombre, correo, contrasena, gustos)
    sistema.registrar_usuario(usuario)
    print("¡Usuario registrado exitosamente!")

# Usar en modificar gustos:
def modificar_gustos(usuario):
    opciones_gustos = {
        'musica': ['rock', 'pop', 'jazz', 'clasica', 'electrónica'],
        'comida': ['mexicana', 'italiana', 'colombiana', 'china', 'india'],
        'cultura': ['teatro', 'museo', 'zoológico', 'danza', 'cine'],
        'deporte': ['futbol', 'baloncesto', 'tenis', 'natacion', 'ciclismo']
    }
    gustos = seleccionar_gustos(opciones_gustos)
    usuario.gustos = gustos
    # Actualiza gustos directamente en la base de datos
    import sqlite3, json
    conn = sqlite3.connect(sistema.db_path)
    c = conn.cursor()
    c.execute("UPDATE usuarios SET gustos=? WHERE correo=?", (json.dumps(usuario.gustos), usuario.correo))
    conn.commit()
    conn.close()
    print("¡Gustos actualizados!")

def ver_eventos_por_categoria():
    print("\nElige la categoría para ver eventos:")
    for i, cat in enumerate(CATEGORIAS_VALIDAS, 1):
        print(f"{i}. {cat.capitalize()}")

    while True:
        opcion = input("Selecciona una opción (número): ")
        if opcion.isdigit() and 1 <= int(opcion) <= len(CATEGORIAS_VALIDAS):
            categoria_seleccionada = CATEGORIAS_VALIDAS[int(opcion)-1]
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

    eventos_filtrados = [e for e in sistema.cargar_eventos() if e.categoria.lower() == categoria_seleccionada]

    if eventos_filtrados:
        print(f"\nEventos en la categoría '{categoria_seleccionada}':")
        for evento in eventos_filtrados:
            print(evento)
    else:
        print(f"No se encontraron eventos en la categoría '{categoria_seleccionada}'.")

def busqueda_avanzada_eventos(usuario):
    print("\n--- Búsqueda avanzada de eventos ---")
    nombre = input("Nombre del evento (dejar vacío para ignorar): ").strip() or None
    print("Categorías:", ", ".join(CATEGORIAS_VALIDAS))
    categoria = input("Categoría (dejar vacío para ignorar): ").strip() or None
    subcategoria = input("Subcategoría (dejar vacío para ignorar): ").strip() or None
    ciudad = input("Ciudad (dejar vacío para ignorar): ").strip() or None
    fecha = input("Fecha (YYYY-MM-DD, dejar vacío para ignorar): ").strip() or None

    eventos = sistema.buscar_eventos_avanzado(nombre, categoria, subcategoria, ciudad, fecha)
    if eventos:
        print("\nResultados de la búsqueda:")
        for idx, evento in enumerate(eventos, 1):
            print(f"{idx}. {evento}")
        # Opción para agendar eventos (permite varios)
        agendar = input("¿Deseas agendar alguno? (número(s) separados por coma o Enter para omitir): ").strip()
        if agendar:
            indices = [int(x.strip()) for x in agendar.split(",") if x.strip().isdigit() and 1 <= int(x.strip()) <= len(eventos)]
            for idx in indices:
                evento = eventos[idx-1]
                evento_id = sistema.obtener_id_evento(evento.nombre, evento.fecha)
                if evento_id:
                    sistema.agendar_evento(usuario.correo, evento_id)
            if indices:
                print("¡Evento(s) agendado(s)!")
    else:
        print("No se encontraron eventos con esos filtros.")

def menu_agendados(usuario):
    while True:
        print("\n--- Tus eventos agendados ---")
        agendados = sistema.obtener_agendados(usuario.correo)
        if agendados:
            for idx, evento in enumerate(agendados, 1):
                print(f"{idx}. {evento}")
        else:
            print("No tienes eventos agendados.")
        print("1. Desagendar un evento")
        print("2. Enviar recordatorio de un evento por correo")
        print("3. Volver")
        opcion = input("Elige una opción: ")
        if opcion == "1" and agendados:
            num = input("Número del evento a desagendar: ")
            if num.isdigit() and 1 <= int(num) <= len(agendados):
                evento = agendados[int(num)-1]
                evento_id = sistema.obtener_id_evento(evento.nombre, evento.fecha)
                if evento_id:
                    sistema.desagendar_evento(usuario.correo, evento_id)
                    print("Evento desagendado.")
            else:
                print("Opción inválida.")
        elif opcion == "2" and agendados:
            num = input("Número del evento para enviar recordatorio: ")
            if num.isdigit() and 1 <= int(num) <= len(agendados):
                evento = agendados[int(num)-1]
                exito = sistema.enviar_recordatorio(usuario.correo, evento)
                if exito:
                    print("¡Recordatorio enviado por correo!")
                else:
                    print("No se pudo enviar el correo.")
            else:
                print("Opción inválida.")
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")

def login():
    print("\n--- Iniciar sesión ---")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")
    usuario = sistema.buscar_usuario(correo, contrasena)
    if usuario:
        menu_usuario(usuario)
    else:
        print("Credenciales incorrectas.")

def main():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            registrar()
        elif opcion == "2":

            login()
        elif opcion == "3":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
