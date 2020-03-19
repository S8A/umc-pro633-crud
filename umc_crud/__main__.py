from .login import login
from .config import config, is_configured
import argparse

def main(args):
    """Función principal del programa."""
    if args['config'] or not is_configured():
        config()
    else:
        login()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sistema CRUD de campus UMC.')
    parser.add_argument('--config', action='store_true')
    args = parser.parse_args()
    main(vars(args))
