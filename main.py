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
    sistema.guardar_usuarios()
    print("¡Gustos actualizados!")

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
