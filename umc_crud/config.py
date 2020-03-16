import configparser
from .cli import *

# Módulo de configuración

def config():
    """Crea un nuevo archivo de configuración."""
    print_h1('Configuración')
    print_h2('MySQL')
    print_long('Parámetros de la conexión a la base de datos donde se '
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


def read_config():
    """Lee el archivo de configuración."""
    conf = configparser.ConfigParser()
    conf.read('config/config.ini')
    return conf
