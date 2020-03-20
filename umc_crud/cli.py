import re
import textwrap
from math import ceil

# Funciones auxiliares para la consola

def print_h1(s, newline=True):
    """Muestra el texto como encabezado de primer nivel."""
    print(f'..:: {s.upper()} ::..')
    if newline:
        print()


def print_h2(s, newline=True):
    """Muestra el texto como encabezado de segundo nivel."""
    print(f'{s} ::..')
    if newline:
        print()


def print_h3(s, newline=True):
    """Muestra el texto como encabezado de tercer nivel."""
    print(f'{s} ::')
    if newline:
        print()


def print_long(s, newline=True):
    """Muestra el texto dividido en varias líneas."""
    for line in textwrap.wrap(s):
        print(line)
    if newline:
        print()


def print_error(s, newline=True):
    """Muestra un mensaje de error con el texto dado."""
    print_long(f'ERROR: {s}', newline)


def print_table(data, cols=None, widths=None, newline=True):
    """Muestra una tabla con los datos dados."""
    if not data:
        # Si no hay datos, no hay nada que mostrar
        print_error('Tabla vacía')
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
        if newline:
            print()


def input_list(prompt, separator='[,\s]+', newline=True):
    """Pide al usuario que ingrese uno o varios ítems y extrae los datos."""
    result = re.split(separator, input(prompt))
    if newline:
        print()
    return result


def input_int(prompt, newline=True):
    """Pide al usuario que ingrese un número entero y verifica la entrada."""
    result = None
    while True:
        user_input = input(prompt)
        if newline:
            print()
        try:
            result = int(user_input)
        except ValueError:
            print_error('Entrada inválida. Ingrese un número.', newline)
            continue
        break
    return result


def input_yes_no(prompt, yes='^[Ss]$', no='^[Nn]$', newline=True):
    """Pide al usuario que ingrese sí o no a la pregunta que se le hace."""
    result = None
    while True:
        user_input = input(prompt)
        if newline:
            print()
        if re.match(yes, user_input):
            result = True
        elif re.match(no, user_input):
            result = False
        else:
            print_error('Entrada inválida. Ingrese sí o no como se indica.',
                        newline)
            continue
        break
    return result


def input_period(prompt, pattern='^\d{4}-(01|IN|02)$', newline=True):
    """Pide al usuario que ingrese un período académico válido."""
    result = None
    while True:
        user_input = input(prompt).upper()
        if newline:
            print()
        if re.match(pattern, user_input):
            result = user_input
        else:
            print_error('Período académico inválido.')
            continue
        break
    return result
