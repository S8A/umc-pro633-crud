from . import crud
from .cli import print_h1, print_h2, print_long, print_error, print_table
import re

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
        index = int(input(f'Elegir opción (1-{len(menu)}): '))
        print()
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


def get_personal_info(student_data):
    """Consulta la información personal del estudiante."""
    print_h2(f'Información personal: {student_data["id_usuario"]}')
    print(f'Nombre y apellido: {student_data["nombre"]} '
          f'{student_data["apellido"]}')
    print(f'C.I.: {student_data["ci"]}')
    print(f'Teléfono: {student_data["telefono"]}')
    print(f'Dirección: {student_data["direccion"]}')
    carrera = crud.read_career_info(student_data['id_carrera'])
    print(f'Carrera: {carrera["nombre"]} ({carrera["id"]})')
    mencion = carrera["mencion"]
    if mencion is not None:
        print(f'Mención {mencion}')
    print()


def get_record(student_data):
    """Consulta el record académico completo del estudiante."""
    print_h2(f'Récord académico: {student_data["id_usuario"]}')
    record = crud.read_records(student_data['ci'])
    # Muestra la tabla
    print_record(record)
    # Muestra información adicional
    uc_cursadas = [r['uc'] for r in record]
    print(f'Materias cursadas: {len(uc_cursadas)} ({sum(uc_cursadas)} UC)')
    uc_aprobadas = [r['uc'] for r in record if r['nota'] >= 12]
    print(f'Materias aprobadas: {len(uc_aprobadas)} ({sum(uc_aprobadas)} UC)')
    print(f'Índice Académico Acumulado (IAA): {calculate_ia(record)}')
    print()


def find_grades(student_data):
    """Consulta las calificaciones por materia del estudiante."""
    print_h2(f'Consulta de calificaciones: {student_data["id_usuario"]}')
    print_long('Introduzca el código de una o varias materias para '
               'consultar sus calificaciones. El código de materia '
               'consiste de letras y números solamente, por ejemplo '
               'CAL114. Para buscar varias materias escriba '
               'sus códigos separados por espacios o comas.')
    # Pide al usuario los códigos de materia y los separa en una lista
    materia_ids = re.split('[,\s]+', input('Materia(s): ').upper())
    print()
    # Muestra la tabla
    print_record(crud.read_records(student_data['ci'], materia_ids))


def calculate_iaa(student_data):
    """Calcula el índice académico acumulado (IAA) del estudiante."""
    print_h2(f'Índice Académico Acumulado: {student_data["id_usuario"]}')
    record = crud.read_records(student_data['ci'])
    iaa = calculate_ia(record)
    print(f'Su IAA es de {iaa} según su récord académico completo.')
    print()


def calculate_iap(student_data):
    """Calcula el índice académico parcial (IAP) del estudiante por período."""
    print_h2(f'Índice Académico Parcial: {student_data["id_usuario"]}')
    print_long('El IAP es el índice académico calculado con las materias '
               'de un solo período académico. Introduzca el período '
               'académico para calcular su IAP (ejemplos: 2020-01, '
               '2018-IN, 2019-02).')
    # Pide al usuario el período académico límite
    period = input('Período académico: ').upper()
    print()
    if re.match('^\d{4}-(01|IN|02)$', period):
        # Si el usuario ingresó un período válido
        # Filtrar record de materias
        record = [r for r in crud.read_records(student_data['ci'])
                  if r['periodo'] == period]
        # Calcular índice académico parcial
        iap = calculate_ia(record)
        if iap is not None:
            print(f'Su IAP es de {iap} según su récord académico '
                  f'hasta el período {period}.')
        else:
            print(f'No tiene materias cursadas en el período {period}.')
    else:
        # Si no se ingresó un período válido, mostrar un error
        print_error('Período académico inválido.')
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
