from . import crud, io, student


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
            ['Cargar archivo de calificaciones', load_csv_records]
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
        io.print_h1(f'Módulo de Administrador')
        io.print_h2(user_id)
        # Mostrar las opciones del menú
        menu = []
        for submenu, items in full_menu.items():
            io.print_h3(submenu, newline=False)
            for i, item in enumerate(items):
                menu.append(item)
                print(f'{len(menu)}. {item[0]}')
        print()
        # Pedir al usuario que elija alguna opción entre 1 y n
        index = io.input_int(f'Elegir opción (1-{len(menu)}): ')
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
            io.print_error('Opción inválida. Intente de nuevo.')


def get_personal_info(title=True, intro=True):
    """Consulta la información personal de uno o varios estudiantes."""
    if title:
        io.print_h2('Consultar información personal')
    if intro:
        io.print_long('Ingrese uno o varios números de C.I. para buscar '
                      'la información personal de los estudiantes a los '
                      'que correspondan.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Las C.I. ingresadas no corresponden a ningún '
                       'estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            # Mostrar la información personal del estudiante
            io.print_h3(estudiante['id_usuario'], newline=False)
            student.get_personal_info(estudiante, title=False)


def get_record(title=True, intro=True):
    """Consulta el registro académico completo de uno o varios estudiante."""
    if title:
        io.print_h2('Consultar récord académico completo')
    if intro:
        io.print_long('Ingrese uno o varios números de C.I. para buscar '
                      'los récords académicos de los estudiantes a los que '
                      'correspondan.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Las C.I. ingresadas no corresponden a ningún '
                       'estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            # Mostrar el récord académico del estudiante
            io.print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            student.get_record(estudiante, title=False)


def find_grades(title=True, intro=True):
    """Consulta las calificaciones de uno o varios estudiante."""
    if title:
        io.print_h2('Consultar calificaciones por materia')
    if intro:
        io.print_long('Ingrese uno o varios números de C.I. y uno o varios '
                      'códigos de materia para buscar las califaciones de '
                      'cada estudiante en cada una de esas materias que '
                      'haya cursado.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    # Pedir las materias a consultar
    materia_ids = [m.upper() for m in io.input_list('Materia(s): ')]
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Las C.I. ingresadas no corresponden a ningún '
                       'estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            # Mostrar el récord académico del estudiante en las materias dadas
            io.print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            student.print_record(crud.read_records(estudiante['ci'],
                                                   materia_ids))


def make_records(title=True, intro=True):
    """Registra calificaciones de un estudiante sin cambiar las anteriores."""
    if title:
        io.print_h2('Registrar calificaciones manualmente')
    if intro:
        io.print_long('Ingrese uno o varios números de C.I., las materias '
                      'que va a registrar para cada estudiante, y la '
                      'calificación obtenida en cada una de ellas.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Las C.I. ingresadas no corresponden a ningún '
                       'estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            # Mostrar el usuario y cédula del estudiante
            io.print_h3(f'{estudiante["id_usuario"]} : {estudiante["ci"]}')
            # Buscar las materias cursadas por el estudiante
            cursadas = [r['id'] for r in crud.read_records(estudiante['ci'])]
            # Pedir el período académico en el que se registrarán los datos
            periodo = io.input_period('Período académico: ')
            # Pedir las materias que se registrarán y buscarlas en la
            # base de datos
            materias = crud.find_career_subjects(
                estudiante['id_carrera'],
                [m.upper() for m in io.input_list('Materia(s): ')])
            # Columnas de la tabla y sus cabeceras
            cols = {'ci_estudiante': 'Cédula',
                    'id_materia': 'Materia',
                    'nota': 'Nota',
                    'periodo': 'Período'}
            # Lista de datos a registrar
            por_registrar = []
            print('Calificaciones:')
            # Para cada materia válida a registrar
            for materia in materias:
                # Código de la materia
                materia_id = materia['id_materia']
                if materia_id in cursadas:
                    # Si la materia ya fue cursada, mostrar mensaje
                    print(f'- {materia_id} ya tiene calificación.')
                else:
                    # Si no ha sido cursada, pedir su calificación
                    nota = io.input_int(f'- {materia_id}: ', newline=False)
                    # Agregar datos de la materia a registrar a la lista
                    por_registrar.append({'ci_estudiante': estudiante['ci'],
                                          'id_materia': materia_id,
                                          'nota': nota,
                                          'periodo': periodo})
            print()
            if por_registrar:
                # Si hay datos por registrar, mostrarlos en una tabla
                print('Se registrarán los siguientes datos:')
                io.print_table(por_registrar, cols)
                # Pedir confirmación antes de registrar los datos
                confirm = io.input_yes_no('¿Registrar datos? (s/n): ')
                if confirm:
                    # Si la respuesta es afirmativa, crear los registros
                    crud.create_records(por_registrar)
                    print('Datos registrados exitosamente.')
                else:
                    # De lo contrario, mostrar mensaje
                    print('Registro cancelado.')
            else:
                # Si no hay datos por registrar, mostrar mensaje
                print('No se registrarán datos.')
            print()


def load_csv_records():
    """Registra calificaciones de varios estudiantes a partir de un CSV."""
    print('TODO: load_csv_records')


def update_record():
    """Modifica calificaciones de uno o varios estudiantes."""
    print('TODO: update_record')


def delete_record():
    """Elimina calificaciones de uno o varios estudiantes."""
    print('TODO: delete_record')
