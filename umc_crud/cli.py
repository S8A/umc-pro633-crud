import textwrap

# Funciones auxiliares para la consola

def print_h1(s):
    """Muestra el texto como encabezado de primer nivel."""
    print(f'..:: {s.upper()} ::..')
    print()

def print_h2(s):
    """Muestra el texto como encabezado de segundo nivel."""
    print(f'{s} ::..')

def print_long(s):
    """Muestra el texto dividido en varias líneas."""
    for line in textwrap.wrap(s):
        print(line)

def print_error(s):
    """Muestra un mensaje de error con el texto dado."""
    print_long(f'ERROR: {s}')
    print()
