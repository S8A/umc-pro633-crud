from . import crud
from .cli import (print_h1, print_h2, print_long, print_error, print_table,
    input_list, input_int, input_period)

# Módulo de estudiante

def main(user_id):
    """Función principal del módulo de estudiante."""
    # Lista de opciones con sus funciones asociadas
    menu = [['Consultar información personal', get_personal_info],
            ['Consultar récord académico completo', get_record],
            ['Consultar calificaciones por materia', find_grades],
            ['Calcular índice académico acumulado (IAA)', calculate_iaa],
            ['Calcular índice académico parcial (IAP)', calculate_iap],
            ['Salir']]
    while True:
        print()
        print_h1(f'Módulo de Estudiante')
        print_h2(user_id)
        # Mostrar las opciones del menú
        for i, item in enumerate(menu):
            print(f'{i+1}. {item[0]}')
        print()
        # Pedir al usuario que elija alguna opción entre 1 y n
        index = input_int(f'Elegir opción (1-{len(menu)}): ')
        if index in range(1, len(menu)):
            # Si la opción elegida está entre 1 y n-1,
            # ejecutar la función correspondiente
            func = menu[index-1][1]
            func(crud.read_student_info(user_id))
            cont = input('[Enter] para volver al menú principal... ')
        elif index == len(menu):
            # Si se elige la última opción, salir
            print('Saliendo.')
            break
        else:
            print_error('Opción inválida. Intente de nuevo.')


def get_personal_info(estudiante, title=True):
    """Consulta la información personal del estudiante."""
    if title:
        print_h2(f'Información personal: {estudiante["id_usuario"]}')
    print(f'Nombre y apellido: {estudiante["nombre"]} '
          f'{estudiante["apellido"]}')
    print(f'C.I.: {estudiante["ci"]}')
    print(f'Teléfono: {estudiante["telefono"]}')
    print(f'Dirección: {estudiante["direccion"]}')
    carrera = crud.read_career_info(estudiante['id_carrera'])
    print(f'Carrera: {carrera["nombre"]} ({carrera["id"]})')
    mencion = carrera["mencion"]
    if mencion is not None:
        print(f'Mención: {mencion}')
    print()


def get_record(estudiante, title=True):
    """Consulta el record académico completo del estudiante."""
    if title:
        print_h2(f'Récord académico: {estudiante["id_usuario"]}')
    record = crud.read_records(estudiante['ci'])
    # Muestra la tabla
    print_record(record)
    # Muestra información adicional
    uc_cursadas = [r['uc'] for r in record]
    print(f'Materias cursadas: {len(uc_cursadas)} ({sum(uc_cursadas)} UC)')
    uc_aprobadas = [r['uc'] for r in record if r['nota'] >= 12]
    print(f'Materias aprobadas: {len(uc_aprobadas)} ({sum(uc_aprobadas)} UC)')
    print(f'Índice Académico Acumulado (IAA): {calculate_ia(record)}')
    print()


def find_grades(estudiante, title=True, intro=True):
    """Consulta las calificaciones por materia del estudiante."""
    if title:
        print_h2(f'Consulta de calificaciones: {estudiante["id_usuario"]}')
    if intro:
        print_long('Introduzca el código de una o varias materias para '
                   'consultar sus calificaciones. El código de materia '
                   'consiste de letras y números solamente, por ejemplo '
                   'CAL114. Para buscar varias materias escriba '
                   'sus códigos separados por espacios o comas.')
    # Pide al usuario los códigos de materia y los separa en una lista
    materia_ids = [materia.upper() for materia in input_list('Materia(s): ')]
    # Muestra la tabla
    print_record(crud.read_records(estudiante['ci'], materia_ids))


def calculate_iaa(estudiante, title=True):
    """Calcula el índice académico acumulado (IAA) del estudiante."""
    if title:
        print_h2(f'Índice Académico Acumulado: {estudiante["id_usuario"]}')
    record = crud.read_records(estudiante['ci'])
    iaa = calculate_ia(record)
    print(f'Su IAA es de {iaa} según su récord académico completo.')
    print()


def calculate_iap(estudiante, title=True, intro=True):
    """Calcula el índice académico parcial (IAP) del estudiante por período."""
    if title:
        print_h2(f'Índice Académico Parcial: {estudiante["id_usuario"]}')
    if intro:
        print_long('El IAP es el índice académico calculado con las materias '
                   'cursadas en un solo período académico. Introduzca el '
                   'período académico para calcular su IAP (ejemplos: '
                   '2020-01, 2018-IN, 2019-02).')
    # Pide al usuario el período académico límite
    periodo = input_period('Período académico: ')
    # Filtrar record de materias
    record = [r for r in crud.read_records(estudiante['ci'])
              if r['periodo'] == periodo]
    # Calcular índice académico parcial
    iap = calculate_ia(record)
    if iap is not None:
        print(f'Su IAP para el período {periodo} es de {iap}.')
    else:
        print(f'No tiene materias cursadas en el período {periodo}.')
    print()


def calculate_ia(record):
    """Calcula el índice académico acumulado a partir del récord dado."""
    suma_uc = sum([r['uc'] for r in record])
    if suma_uc == 0: return None
    suma_ponderada = sum([r['uc']*r['nota'] for r in record])
    return round(suma_ponderada/suma_uc, 2)


def print_record(record):
    """Muestra una tabla de récords académicos a partir de los datos dados."""
    cols = {'id': 'Código',
            'nombre': 'Materia',
            'uc': 'UC',
            'nota': 'Nota',
            'periodo': 'Período'}
    widths = dict(zip(cols.keys(), [10, 45, 5, 5, 10]))
    print_table(record, cols, widths)
