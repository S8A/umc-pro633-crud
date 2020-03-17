from . import admin, student
from .cli import print_h1, print_h2, print_long, print_error
from .config import read_config
from .db import execute_sql

# Módulo de inicio de sesión

def login():
    """Permite iniciar sesión como un usuario del campus UMC."""
    conf = read_config()
    if 'mysql' not in conf.sections():
        # Muestra un error si no se encuentra la configuración de MySQL
        print_error('Archivo de configuración no encontrado o incompleto. '
                    'Ejecutar de nuevo usando la opción --config para '
                    'crear un nuevo archivo de configuración.')
    else:
        # Petición de búsqueda en la tabla usuario
        query = 'SELECT * FROM usuario WHERE id = %s AND password = %s'

        print_h1('Inicio de Sesión')
        # Pregunta los datos de inicio de sesión de forma repetitiva
        while True:
            user_id = input('Usuario: ')
            user_pw = input('Contraseña: ')
            print()
            # Ejecuta la búsqueda por usuario y contraseña
            result = execute_sql(query,
                                 args=[user_id, user_pw],
                                 rows=1)
            if result is not None:
                # Si los datos coinciden con un usuario, se verifica si es 
                # un administrador o un estudiante y se ejecuta el módulo 
                # apropiado.
                if result['admin'] == 0:
                    student.main(result['id'])
                else:
                    admin.main(result['id'])

                # Se rompe el bucle
                break
            else:
                # Si los datos no coinciden con ningún usuario, se muestra
                # un mensaje de error.
                print_error('Usuario o contraseña incorrecta. '
                            'Intente de nuevo.')
