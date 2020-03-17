import textwrap
from math import ceil

# Funciones auxiliares para la consola

def print_h1(s):
    """Muestra el texto como encabezado de primer nivel."""
    print(f'..:: {s.upper()} ::..')
    print()

def print_h2(s):
    """Muestra el texto como encabezado de segundo nivel."""
    print(f'{s} ::..')
    print()

def print_long(s):
    """Muestra el texto dividido en varias líneas."""
    for line in textwrap.wrap(s):
        print(line)

def print_error(s):
    """Muestra un mensaje de error con el texto dado."""
    print_long(f'ERROR: {s}')
    print()

def print_table(data, cols=None, widths=None):
    """Muestra una tabla con los datos dados."""
    if len(data) == 0:
        # Si no hay datos, no hay nada que mostrar
        print('Tabla vacía')
    else:
        if cols is None:
            # Si no se proveen nombres de columna manualmente,
            # usar los de los datos
            cols = {c: c for c in data[0].keys()}
        if widths is None:
            # Si no se proveen anchos de columna manualmente,
            # calcularlos a partir de los nombres de columna
            widths = {c: (4*ceil(len(cols[c])/4) + 4) for c in cols.keys()}
        # Mostrar cabecera de la tabla
        print(' '.join([f'{cols[col] :<{w}}' for col, w in widths.items()]))
        # Mostrar barra separadora decorativa
        print('+'.join(['-'*w for w in widths.values()]))
        # Mostrar datos de la tabla
        for row in data:
            print(' '.join([f'{row[col] :<{w}}' for col, w in widths.items()]))
        print()
