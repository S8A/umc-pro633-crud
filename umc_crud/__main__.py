# coding=utf-8
"""Módulo principal del programa.

La ejecución del programa debe comenzar en este módulo.

La función main() toma los argumentos ingresados, verifica la
configuración y ejecuta el módulo de configuración o el de inicio
de sesión según sea el caso.
"""


import argparse
from .config import config, is_configured
from .login import login


def main(args):
    """Función principal del programa."""
    if args['config'] or not is_configured():
        config()
    else:
        login()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sistema CRUD de campus UMC.')
    parser.add_argument('--config', action='store_true',
                        help='Configura la conexión a MySQL')
    args = parser.parse_args()
    main(vars(args))
