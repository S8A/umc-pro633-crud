from . import crud
from .cli import print_h1, print_h2, print_long, print_error, print_table

# Módulo de estudiante

def main(user_id):
    """Función principal del módulo de estudiante."""
    # Lista de opciones con sus funciones asociadas
    opciones = [['Consultar información personal', show_personal_info],
                ['Consultar récord académico completo', show_record],
                ['Consultar calificaciones por materia', find_grades],
                ['Calcular índice académico acumulado (IAA)', calculate_iaa],
                ['Calcular índice académico parcial (IAP)', calculate_iap],
                ['Salir']]
    while True:
        print()
        print_h1(f'Módulo de Estudiante')
        print_h2(user_id)
        # Mostrar las opciones del menú
        for i, opcion in enumerate(opciones):
            print(f'{i+1}. {opcion[0]}')
        print()
        # Pedir al usuario que elija alguna opción entre 1 y n
        opc = int(input(f'Elegir opción (1-{len(opciones)}): '))
        print()
        if opc in range(1, len(opciones)):
            # Si la opción elegida está entre 1 y n-1,
            # ejecutar la función correspondiente
            funcion = opciones[opc-1][1]
            funcion(crud.get_student_info(user_id))
            cont = input('[Enter] para volver al menu principal... ')
        else:
            # De lo contrario, salir
            print('Saliendo.')
            break


def show_personal_info(student_data):
    """Muestra la información personal del estudiante."""
    print_h2(f'Información personal: {student_data["id_usuario"]}')
    print(f'Nombre y apellido: {student_data["nombre"]} '
          f'{student_data["apellido"]}')
    print(f'C.I.: {student_data["ci"]}')
    print(f'Teléfono: {student_data["telefono"]}')
    print(f'Dirección: {student_data["direccion"]}')
    carrera = crud.get_career_info(student_data['id_carrera'])
    print(f'Carrera: {carrera["nombre"]} ({carrera["id"]})')
    print(f'Mención {carrera["mencion"]}')
    print()


def show_record(student_data):
    """Muestra el record académico completo del estudiante."""
    print_h2(f'Récord académico: {student_data["id_usuario"]}')
    records = crud.read_records(student_data['ci'])
    columnas = {'id_materia': 'Materia',
                'nota': 'Nota',
                'periodo': 'Período'}
    anchuras = dict(zip(columnas.keys(), [10, 4, 10]))
    print_table(records, cols=columnas, widths=anchuras)


def find_grades(student_data):
    """Consulta las calificaciones por materia del estudiante."""
    print('find_grades')


def calculate_iaa(student_data):
    """Calcula el índice académico acumulado (IAA) del estudiante."""
    print('calculate_iaa')


def calculate_iap(student_data):
    """Calcula el índice académico parcial (IAP) del estudiante por período."""
    print('calculate_iap')
