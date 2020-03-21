from . import io
import configparser

# Módulo de configuración

def config():
    """Crea un nuevo archivo de configuración."""
    io.print_h1('Configuración')
    io.print_h2('MySQL')
    io.print_long('Parámetros de la conexión a la base de datos donde se '
                  'encuentran las tablas requeridas por el sistema CRUD. '
                  'Leer README.md para instrucciones de cómo importar la '
                  'estructura de la base de datos.')
    host = input('Host: ')
    user = input('Usuario: ')
    password = input('Contraseña: ')
    database = input('Base de datos: ')
    conf = configparser.ConfigParser()
    conf['mysql'] = {'host': host,
                     'user': user,
                     'password': password,
                     'database': database}
    with open('config/config.ini', 'w') as configfile:
        conf.write(configfile)
    print()
    print('Configuración completada. Ejecute el programa de nuevo.')
    print()


def read_config():
    """Lee el archivo de configuración."""
    conf = configparser.ConfigParser()
    conf.read('config/config.ini')
    return conf


def is_configured():
    """Verifica si el archivo de configuración existe y está completo."""
    # Trata de cargar la configuración
    conf = read_config()
    # Lista de atributos de la configuración MySQL
    options = ['host', 'user', 'password', 'database']
    # Comprobar que todos los atributos existen y tienen valor
    for option in options:
        if not conf.get('mysql', option):
            return False
    return True
