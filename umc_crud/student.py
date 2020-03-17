from .cli import print_h1, print_h2, print_long, print_error
from .crud import get_career_info, get_student_info

# Módulo de estudiante

def main(user_id):
    """Función principal del módulo de estudiante."""
    print_h1(f'Módulo de Estudiante: {user_id}')

    estudiante = get_student_info(user_id)
    print(f'{estudiante["nombre"]} {estudiante["apellido"]} ('
          f'{estudiante["ci"]}')
    print()

    # Lista de opciones con sus funciones asociadas
    opciones = [('Consultar información personal', show_personal_info),
                ('Consultar récord académico completo', show_record),
                ('Consultar calificaciones por materia', find_grades),
                ('Calcular índice académico acumulado (IAA)', calculate_iaa),
                ('Calcular índice académico parcial (IAP)', calculate_iap),
                ('Salir', exit_module)]

    while True:
        # Mostrar las opciones del menú
        for n, opcion in enumerate(opciones):
            print(f'{n+1}. {opcion[0]}')
        print()
        # Pedir al usuario que elija alguna opción
        opcion_menu = int(input(f'Elegir opción (1-{len(opciones)})'))
        # Ejecutar la función correspondiente a la opción elegida
        funcion = opciones[opcion_menu][1]
        funcion(estudiante)


def show_personal_info(student_data):
    """Muestra la información personal del estudiante."""
    print_h2('Información personal')
    print(f'Nombre y apellido: {student_data["nombre"]} '
          f'{student_data["apellido"]}')
    print(f'C.I.: {student_data["ci"]}')
    print(f'Teléfono: {student_data["telefono"]}')
    print(f'Dirección: {student_data["direccion"]}')
    carrera = get_career_info(student_data['id_carrera'])
    print(f'Carrera: {carrera["nombre"]} Mención {carrera["mencion"]} ('
          f'{carrera["id"]}')
    print()


def show_record(student_data):
    """Muestra el record académico completo del estudiante."""
    records = read_records(student_data['ci'])
    for record in records:
        print(record)


def find_grades(student_data):
    """Consulta las calificaciones por materia del estudiante."""
    print('find_grades')


def calculate_iaa(student_data):
    """Calcula el índice académico acumulado (IAA) del estudiante."""
    print('calculate_iaa')


def calculate_iap(student_data):
    """Calcula el índice académico parcial (IAP) del estudiante por período."""
    print('calculate_iap')
