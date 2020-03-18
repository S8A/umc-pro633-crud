from . import crud
from .cli import (print_h1, print_h2, print_h3, print_long, print_error,
    print_table)

def main(user_id):
    """Función principal del módulo de administrador."""
    # Opciones categorizadas con sus funciones asociadas
    full_menu = {
        'Consulta': [
            ['Consultar información personal', get_personal_info],
            ['Consultar récord académico completo', get_record],
            ['Consultar calificaciones por materia', find_grades]
        ],
        'Registro': [
            ['Registrar calificaciones manualmente', make_records],
            ['Cargar archivo de calificaciones', load_csv]
        ],
        'Modificación': [
            ['Modificar calificaciones', update_record]
        ],
        'Eliminación': [
            ['Eliminar calificaciones', delete_record]
        ],
        'Sesión': [
            ['Salir']
        ]
    }
    while True:
        print()
        print_h1(f'Módulo de Administrador')
        print_h2(user_id)
        # Mostrar las opciones del menú
        menu = []
        for category, items in full_menu.items():
            print_h3(category, newline=False)
            for i, item in enumerate(items):
                menu.append(item)
                print(f'{len(menu)}. {item[0]}')
        print()
        # Pedir al usuario que elija alguna opción entre 1 y n
        index = int(input(f'Elegir opción (1-{len(menu)}): '))
        print()
        if index in range(1, len(menu)):
            # Si la opción elegida está entre 1 y n-1,
            # ejecutar la función correspondiente
            func = menu[index-1][1]
            func()
            cont = input('[Enter] para volver al menu principal... ')
        elif index == len(menu):
            # Si se elige la última opción, salir
            print('Saliendo.')
            break
        else:
            print_error('Opción inválida. Intente de nuevo.')


def get_personal_info():
    """Consulta la información personal de uno o varios estudiantes."""
    print('TODO: get_personal_info')

def get_record():
    """Consulta el registro académico completo de uno o varios estudiante."""
    print('TODO: get_record')

def find_grades():
    """Consulta las calificaciones de uno o varios estudiante."""
    print('TODO: find_grades')

def make_records():
    """Registra calificaciones de un estudiante sin cambiar las anteriores."""
    print('TODO: make_records')

def load_csv():
    """Registra calificaciones de varios estudiantes a partir de un CSV."""
    print('TODO: load_csv')

def update_record():
    """Modifica calificaciones de uno o varios estudiantes."""
    print('TODO: update_record')

def delete_record():
    """Elimina calificaciones de uno o varios estudiantes."""
    print('TODO: delete_record')
