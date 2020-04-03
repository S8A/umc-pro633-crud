# coding=utf-8
"""Módulo de administrador.

Mediante este módulo los usuarios de la base de datos que sean
administradores pueden realizar diversas actividades de consulta,
creación, modificación y eliminación de registros.

La ejecución del módulo debería empezar por la función main(), pues
esta provee el menú de opciones que es la interfaz principal para
el usuario.
"""


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
            ['Registrar calificaciones', make_records],
            ['Cargar archivo de calificaciones', load_csv_records]
        ],
        'Modificación': [
            ['Modificar calificaciones', update_records]
        ],
        'Eliminación': [
            ['Eliminar calificaciones', delete_records]
        ],
        'Sesión': [
            ['Salir']
        ]
    }
    while True:
        print()
        io.print_hr()
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
        n = len(menu)
        index = io.input_int_range(f'Elegir opción [1-{n}]: ', 1, n)
        if index in range(1, n):
            # Si la opción elegida está entre 1 y n-1,
            # ejecutar la función correspondiente
            io.print_hr()
            func = menu[index-1][1]
            func()
            cont = input('[Enter] para volver al menú principal... ')
        elif index == n:
            # Si se elige la última opción, salir
            print('Saliendo.')
            return


def get_personal_info(title=True, intro=True):
    """Consulta la información personal de uno o varios estudiantes."""
    if title:
        io.print_h2('Consultar información personal')
    if intro:
        io.print_long('Ingrese los números de cédula de los estudiantes '
                      'para consultar su información personal.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
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
        io.print_long('Ingrese los números de cédula de los estudiantes '
                      'para consultar su récord académico.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
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
        io.print_long('Ingrese los números de cédula de los estudiantes '
                      'y los códigos de las materias que quiere consultar '
                      'en el récord académico de cada uno.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    # Pedir las materias a consultar
    materia_ids = [m.upper() for m in io.input_list('Materia(s): ')]
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
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
        io.print_h2('Registrar calificaciones')
    if intro:
        io.print_long('Ingrese los números de cédula de los estudiantes, '
                      'las materias que quiere registrar para cada uno, '
                      'y la calificación obtenida y el período académico '
                      'en que se cursó cada una.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            ci = estudiante['ci']
            # Columnas de la tabla y sus cabeceras
            cols = {'ci_estudiante': 'Cédula',
                    'id_materia': 'Materia',
                    'nota': 'Nota',
                    'periodo': 'Período'}
            # Lista de datos a registrar
            por_registrar = []
            # Mostrar el usuario y cédula del estudiante
            print()
            io.print_h3(f'{estudiante["id_usuario"]} : {ci}')
            # Buscar materias que no han sido cursadas por el estudiante
            por_cursar = [item['id_materia'] for item
                          in crud.find_subjects_not_taken_by_student(ci)]
            # Pedir las materias a registrar y conservar las que están en
            # la lista de materias por cursar del estudiante
            materias = [m.upper() for m in io.input_list('Materia(s): ')
                        if m.upper() in por_cursar]
            if materias:
                # Si quedan materias por registrar
                print('Registro de calificaciones:')
                # Para cada materia
                for materia_id in materias:
                    # Pedir la calificación obtenida por el estudiante
                    nota = io.input_int(f'- {materia_id}: ', newline=False)
                    # Pedir el período académico en el que se cursó
                    periodo = io.input_period('  Período académico: ',
                                              newline=False)
                    # Agregar datos de la materia por registrar a la lista
                    por_registrar.append({'ci_estudiante': ci,
                                          'id_materia': materia_id,
                                          'nota': nota,
                                          'periodo': periodo})
            if por_registrar:
                # Si hay datos por registrar, mostrarlos en una tabla
                print()
                print(f'Se crearán {len(por_registrar)} nuevos registros:')
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
                print('No se registrarán nuevos datos.')
            print()


def load_csv_records(title=True, intro=True):
    """Registra calificaciones de varios estudiantes a partir de un CSV."""
    if title:
        io.print_h2('Cargar archivo de calificaciones')
    if intro:
        io.print_long('Ingrese la ruta del archivo CSV con las '
                      'califaciones que desea registrar. El archivo '
                      'debe consistir de cuatro columnas: número de '
                      'cédula del estudiante, código de materia, la '
                      'calificación obtenida, y el período en que se '
                      'cursó.')
    # Pedir la ruta del archivo CSV
    csv = input('Archivo: ')
    try:
        # Tratar de abrir el CSV y extraer su contenido
        csv = io.read_csv(csv)
    except FileNotFoundError:
        # Si el archivo no se encuentra, mostrar error y salir
        io.print_error('Archivo no encontrado.')
        return
    # Columnas de la tabla y sus cabeceras
    cols = {'ci_estudiante': 'Cédula',
            'id_materia': 'Materia',
            'nota': 'Nota',
            'periodo': 'Período'}
    # Filtrar las filas que no tengan el número correcto de campos
    csv = list(filter(lambda row: len(row) == 4, csv))
    # Convertir el contenido del CSV al formato requerido por print_table
    records = [dict(zip(cols.keys(), row)) for row in csv]
    # Diccionario de datos a registrar
    por_registrar = {}
    # Para cada registro
    for record in records:
        ci = record['ci_estudiante']
        materia_id = record['id_materia']
        # Verificar que la calificación sea un número entero
        try:
            # Trata de convertir la calificación a entero
            record['nota'] = int(record['nota'])
        except ValueError:
            # Si no se puede, el registro es inválido. Pasar al siguiente
            continue
        # Verificar que el período académico del registro sea válido
        if not io.validate_period(record['periodo']):
            # Si no es válido, pasar al siguiente registro
            continue
        # Buscar las materias que no han sido cursadas por el estudiante de
        # la cédula dada. Si no existe ningún estudiante con dicha cédula,
        # el resultado será un tuple vacío
        por_cursar = [item['id_materia'] for item
                      in crud.find_subjects_not_taken_by_student(ci)]
        if materia_id in por_cursar:
            # Si la materia no ha sido cursada por el estudiante,
            # se agregan los datos a la lista de registros por crear.
            # Si esta combinación de materia y estudiante ya estaba en
            # la lista, será reemplazada por este nuevo registro.
            por_registrar[(ci, materia_id)] = record
    # Convertir el diccionario de datos a lista
    por_registrar = list(por_registrar.values())
    print()
    if por_registrar:
        # Si hay datos por registrar, preguntar si quiere revisarlos
        print(f'Se crearán {len(por_registrar)} nuevos registros.')
        check = io.input_yes_no('¿Desea verlos antes de continuar? (s/n): ')
        if check:
            # Si la respuesta es afirmativa, mostrar la tabla
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
        print('No se registrarán nuevos datos.')
    print()


def update_records(title=True, intro=True):
    """Modifica calificaciones existentes de uno o varios estudiantes."""
    if title:
        io.print_h2('Modificar calificaciones')
    if intro:
        io.print_long('Ingrese los números de cédula de los estudiantes, '
                      'las materias que quiere modificar para cada uno, '
                      'y la calificación y período académico que se le '
                      'va a asignar a cada una.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            ci = estudiante['ci']
            # Columnas de la tabla y sus cabeceras
            cols = {'ci_estudiante': 'Cédula',
                    'id_materia': 'Materia',
                    'nota': 'Nota',
                    'periodo': 'Período'}
            # Lista de datos a modificar
            por_modificar = []
            # Mostrar el usuario y cédula del estudiante
            print()
            io.print_h3(f'{estudiante["id_usuario"]} : {ci}')
            # Extraer materias cursadas del récord académico del estudiante
            cursadas = [item['id'] for item in crud.read_records(ci)]
            # Pedir las materias a modificar y conservar las que están en
            # la lista de materias cursadas del estudiante
            materias = [m.upper() for m in io.input_list('Materia(s): ')
                        if m.upper() in cursadas]
            if materias:
                # Si quedan materias por modificar
                print('Modificación de calificaciones:')
                # Para cada materia
                for materia_id in materias:
                    # Pedir la calificación obtenida por el estudiante
                    nota = io.input_int(f'- {materia_id}: ', newline=False)
                    # Pedir el período académico en el que se cursó
                    periodo = io.input_period('  Período académico: ',
                                              newline=False)
                    # Agregar datos de la materia por modificar a la lista
                    por_modificar.append({'ci_estudiante': ci,
                                          'id_materia': materia_id,
                                          'nota': nota,
                                          'periodo': periodo})
            if por_modificar:
                # Si hay datos por modificar, mostrarlos en una tabla
                print()
                print(f'Se modificarán {len(por_modificar)} registros:')
                io.print_table(por_modificar, cols)
                # Pedir confirmación antes de modificar los datos
                confirm = io.input_yes_no('¿Modificar datos? (s/n): ')
                if confirm:
                    # Si la respuesta es afirmativa, modificar los registros
                    crud.update_records(por_modificar)
                    print('Datos modificados exitosamente.')
                else:
                    # De lo contrario, mostrar mensaje
                    print('Modificación cancelada.')
            else:
                # Si no hay datos por modificar, mostrar mensaje
                print('No se modificará ningún dato.')
            print()


def delete_records(title=True, intro=True):
    """Elimina calificaciones de uno o varios estudiantes."""
    if title:
        io.print_h2('Eliminar calificaciones')
    if intro:
        io.print_long('Ingrese los números de cédula de los estudiantes, '
                      'y las materias que quiera eliminar de sus registros.')
    # Pedir los números de cédula y buscar los estudiantes asociados
    estudiantes = crud.find_students(io.input_list('Cédula(s): '))
    if not estudiantes:
        # Si la lista de estudiantes está vacía, mostrar error
        io.print_error('Los números de cédula ingresados no corresponden '
                       'a ningún estudiante.')
    else:
        # De lo contrario, para cada estudiante
        for estudiante in estudiantes:
            ci = estudiante['ci']
            # Columnas de la tabla y sus cabeceras
            cols = {'ci_estudiante': 'Cédula',
                    'id_materia': 'Materia',
                    'nota': 'Nota',
                    'periodo': 'Período'}
            # Lista de datos a eliminar
            por_eliminar = []
            # Mostrar el usuario y cédula del estudiante
            print()
            io.print_h3(f'{estudiante["id_usuario"]} : {ci}')
            # Extraer materias cursadas del récord académico del estudiante
            cursadas = {item['id']: item for item in crud.read_records(ci)}
            # Pedir las materias a eliminar y conservar las que están en
            # la lista de materias cursadas del estudiante
            materias = [m.upper() for m in io.input_list('Materia(s): ')
                        if m.upper() in cursadas.keys()]
            if materias:
                # Si quedan materias por eliminar
                print('Eliminación de calificaciones:')
                # Para cada materia
                for materia_id in materias:
                    # Extraer datos del registro
                    nota = cursadas[materia_id]['nota']
                    periodo = cursadas[materia_id]['periodo']
                    # Agregar datos de la materia por eliminar a la lista
                    por_eliminar.append({'ci_estudiante': ci,
                                         'id_materia': materia_id,
                                         'nota': nota,
                                         'periodo': periodo})
            if por_eliminar:
                # Si hay datos por eliminar, mostrarlos en una tabla
                print()
                print(f'Se eliminarán {len(por_eliminar)} registros:')
                io.print_table(por_eliminar, cols)
                # Pedir confirmación antes de eliminar los datos
                confirm = io.input_yes_no('¿Eliminar datos? (s/n): ')
                if confirm:
                    # Si la respuesta es afirmativa, eliminar los registros
                    crud.delete_records(por_eliminar)
                    print('Datos eliminados exitosamente.')
                else:
                    # De lo contrario, mostrar mensaje
                    print('Eliminación cancelada.')
            else:
                # Si no hay datos por eliminar, mostrar mensaje
                print('No se eliminará ningún dato.')
            print()
