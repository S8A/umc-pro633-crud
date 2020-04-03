from . import admin, crud, io, student

# Módulo de inicio de sesión

def login():
    """Permite iniciar sesión como un usuario del campus UMC."""
    io.print_h1('Inicio de Sesión')
    # Pregunta los datos de inicio de sesión de forma repetitiva
    while True:
        user_id = input('Usuario: ')
        user_pw = input('Contraseña: ')
        print()
        # Ejecuta la búsqueda por usuario y contraseña
        result = crud.authenticate_user(user_id, user_pw)
        if result is not None:
            # Si los datos coinciden con un usuario, se verifica si es
            # un administrador o un estudiante y se ejecuta el módulo
            # apropiado.
            if result['admin'] == 0:
                student.main(result['id'])
            elif result['admin'] == 1:
                admin.main(result['id'])
            else:
                io.print_error('Valor inesperado en el registro de usuario.')

            # Se rompe el bucle
            break
        else:
            # Si los datos no coinciden con ningún usuario, se muestra
            # un mensaje de error.
            io.print_error('Usuario o contraseña incorrecta. '
                           'Intente de nuevo.')
