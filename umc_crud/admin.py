from . import crud
from . import student
from .cli import (print_h1, print_h2, print_h3, print_long, print_error,
    print_table, input_list, input_int, input_yes_no, input_period)


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
        for submenu, items in full_menu.items():
            print_h3(submenu, newline=False)
            for i, item in enumerate(items):
                menu.append(item)
                print(f'{len(menu)}. {item[0]}')
        print()
        # Pedir al usuario que elija alguna opción entre 1 y n
        index = input_int(f'Elegir opción (1-{len(menu)}): ')
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


def get_personal_info(title=True, intro=True):
    """Consulta la información personal de uno o varios estudiantes."""
    if title:
        print_h2('Consultar información personal')
    if intro:
        print_long('Ingrese uno o varios números de C.I. para buscar '
                   'la información personal de los estudiantes a los '
                   'que correspondan.')
    estudiantes = crud.find_students(input_list('Cédula(s): '))
    if not estudiantes:
        print_error('Las C.I. ingresadas no corresponden a ningún estudiante.')
    else:
        for estudiante in estudiantes:
            print_h3(estudiante['id_usuario'], newline=False)
            student.get_personal_info(estudiante, title=False)


def get_record(title=True, intro=True):
    """Consulta el registro académico completo de uno o varios estudiante."""
    if title:
        print_h2('Consultar récord académico completo')
    if intro:
        print_long('Ingrese uno o varios números de C.I. para buscar '
                   'los récords académicos de los estudiantes a los que '
                   'correspondan.')
    estudiantes = crud.find_students(input_list('Cédula(s): '))
    if not estudiantes:
        print_error('Las C.I. ingresadas no corresponden a ningún estudiante.')
    else:
        for estudiante in estudiantes:
            print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            student.get_record(estudiante, title=False)


def find_grades(title=True, intro=True):
    """Consulta las calificaciones de uno o varios estudiante."""
    if title:
        print_h2('Consultar calificaciones por materia')
    if intro:
        print_long('Ingrese uno o varios números de C.I. y uno o varios '
                   'códigos de materia para buscar las califaciones de '
                   'cada estudiante en cada una de esas materias que '
                   'haya cursado.')
    estudiantes = crud.find_students(input_list('Cédula(s): '))
    materia_ids = [materia.upper() for materia in input_list('Materia(s): ')]
    if not estudiantes:
        print_error('Las C.I. ingresadas no corresponden a ningún estudiante.')
    else:
        for estudiante in estudiantes:
            print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            student.print_record(crud.read_records(estudiante['ci'],
                                                   materia_ids))


def make_records(title=True, intro=True):
    """Registra calificaciones de un estudiante sin cambiar las anteriores."""
    if title:
        print_h2('Registrar calificaciones manualmente')
    if intro:
        print_long('Ingrese uno o varios números de C.I., las materias '
                   'que va a registrar para cada estudiante, y la '
                   'calificación obtenida en cada una de ellas.')
    estudiantes = crud.find_students(input_list('Cédula(s): '))
    if not estudiantes:
        print_error('Las C.I. ingresadas no corresponden a ningún estudiante.')
    else:
        for estudiante in estudiantes:
            print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            cursadas = [r['id'] for r in crud.read_records(estudiante['ci'])]
            periodo = input_period('Período académico: ')
            materias = crud.find_career_subjects(
                estudiante['id_carrera'],
                [materia.upper() for materia in input_list('Materia(s): ')])
            cols = {'ci_estudiante': 'Cédula',
                    'id_materia': 'Materia',
                    'nota': 'Nota',
                    'periodo': 'Período'}
            por_registrar = []
            print('Calificaciones:')
            for materia in materias:
                materia_id = materia['id_materia']
                if materia_id in cursadas:
                    print(f'- {materia_id} ya tiene calificación.')
                else:
                    nota = input_int(f'- {materia_id}: ', newline=False)
                    por_registrar.append({'ci_estudiante': estudiante['ci'],
                                          'id_materia': materia_id,
                                          'nota': nota,
                                          'periodo': periodo})
            print()
            if por_registrar:
                print('Se registrarán los siguientes datos:')
                print_table(por_registrar, cols)
                confirm = input_yes_no('¿Registrar datos? (s/n): ')
                if confirm:
                    crud.create_records(por_registrar)
                    print_long('Datos registrados exitosamente.')
                else:
                    print_long('Registro cancelado.')
            else:
                print_long('No se registrarán datos.')


def load_csv():
    """Registra calificaciones de varios estudiantes a partir de un CSV."""
    print('TODO: load_csv')


def update_record():
    """Modifica calificaciones de uno o varios estudiantes."""
    print('TODO: update_record')


def delete_record():
    """Elimina calificaciones de uno o varios estudiantes."""
    print('TODO: delete_record')
