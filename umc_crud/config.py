# coding=utf-8
"""Módulo de configuración.

Provee funciones para leer y crear el archivo de configuración,
verificar si el programa ya está configurado, y permitir al usuario
ingresar los datos de configuración interactivamente mediante la
función principal config().
"""


import configparser
from . import io


def config(title=True, intro=True):
    """Configura el programa a partir de la entrada del usuario."""
    if title:
        io.print_h1('Configuración')
    if intro:
        io.print_h2('MySQL')
        io.print_long('Parámetros de la conexión a la base de datos donde se '
                      'encuentran las tablas requeridas por el sistema CRUD. '
                      'Leer README.md para instrucciones de cómo importar la '
                      'estructura de la base de datos.')
    host = input('Host: ').strip()
    user = input('Usuario: ').strip()
    password = input('Contraseña: ').strip()
    database = input('Base de datos: ').strip()
    create_config({'host': host,
                   'user': user,
                   'password': password,
                   'database': database})
    print()
    print('Configuración completada. Ejecute el programa de nuevo.')
    print()


def create_config(mysql_data):
    """Crea un nuevo archivo de configuración."""
    conf = configparser.ConfigParser()
    conf['mysql'] = mysql_data
    with open('config/config.ini', 'w') as configfile:
        conf.write(configfile)


def read_config():
    """Lee el archivo de configuración."""
    conf = configparser.ConfigParser()
    conf.read('config/config.ini')
    return conf


def is_configured():
    """Verifica si el archivo de configuración existe y está completo."""
    # Trata de cargar la configuración
    conf = read_config()
    # Comprobar que la sección 'mysql' existe
    if not conf.has_section('mysql'):
        return False
    # Lista de atributos de la configuración MySQL
    options = ['host', 'user', 'password', 'database']
    # Comprobar que todos los atributos existen y tienen valor
    for option in options:
        if not conf.get('mysql', option):
            return False
    return True
