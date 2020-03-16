import configparser
from .cli import printh1, printh2, printlong

# Módulo de configuración

def config():
    """Crea un nuevo archivo de configuración."""
    printh1('Configuración')
    printh2('MySQL')
    printlong('Parámetros de la conexión a la base de datos donde se '
              'encuentran las tablas requeridas por el sistema CRUD. '
              'Leer README.md para instrucciones de cómo importar la '
              'estructura de la base de datos.')
    host = input('Host: ')
    user = input('Usuario: ')
    password = input('Contraseña: ')
    db = input('Base de datos: ')
    conf = configparser.ConfigParser()
    conf['mysql'] = {'host': host,
                     'user': user,
                     'password': password,
                     'db': db}
    with open('config/config.ini', 'w') as configfile:
        conf.write(configfile)


def read_config():
    """Lee el archivo de configuración."""
    conf = configparser.ConfigParser()
    conf.read('config/config.ini')
    return conf
