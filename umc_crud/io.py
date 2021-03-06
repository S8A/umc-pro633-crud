# coding=utf-8
"""Funciones auxiliares de entrada y salida.

Este módulo provee diversas funciones para la entrada y salida de
datos en la cónsola, así como la validación de datos ingresados y
el procesamiento de archivos CSV.
"""


import csv
import re
import textwrap as tw
from math import ceil


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
    for line in tw.wrap(s):
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
        print(' '.join([f'{tw.shorten(str(cols[col]), width=w) :<{w}}'
                        for col, w in widths.items()]))
        # Mostrar barra separadora decorativa
        print('+'.join(['-'*w for w in widths.values()]))
        # Mostrar datos de la tabla
        for row in data:
            print(' '.join([f'{tw.shorten(str(row[col]), width=w) :<{w}}'
                            for col, w in widths.items()]))
        if newline:
            print()


def print_hr(symbol='-', width=80, newline=True):
    """Muestra una línea horizontal."""
    print(symbol*width)
    if newline:
        print()


def input_list(prompt, separator='[,\s]+', newline=True):
    """Pide al usuario que ingrese uno o varios ítems y extrae los datos."""
    # Toma la entrada del usuario y la separa por el patrón dado
    items = split_list(input(prompt), separator)
    if newline:
        print()
    # Devuelve los ítems ingresados
    return items


def input_int(prompt, newline=True):
    """Pide al usuario que ingrese un número entero y verifica la entrada."""
    result = None
    # Mientras que no se haya obtenido el número
    while result is None:
        # Toma la entrada del usuario
        user_input = input(prompt)
        if newline:
            print()
        try:
            # Intenta convertir la entrada a entero
            result = int(user_input)
        except ValueError:
            # Si no se puede convertir, da error
            print_error('Entrada inválida. Ingrese un número entero.',
                        newline)
            # Continúa el bucle para que pida la entrada de nuevo
            continue
    # Devuelve el resultado
    return result


def input_int_range(prompt, min_value, max_value, newline=True):
    """Pide al usuario que ingrese un número entero en un rango dado."""
    result = None
    # Mientras que no se haya obtenido el número
    while result is None:
        # Toma la entrada del usuario
        user_input = input(prompt)
        if newline:
            print()
        try:
            # Intenta convertir la entrada a entero
            result = int(user_input)
        except ValueError:
            # Si no se puede convertir, da error
            print_error('Entrada inválida. Ingrese un número entero.',
                        newline)
            # Continúa el bucle para que pida la entrada de nuevo
            continue
        if result not in range(min_value, max_value + 1):
            # Si el número no se encuentra en el rango, da error
            print_error(f'El número ingresado no está en el intervalo '
                        f'[{min_value}, {max_value}]',
                        newline)
            # Eliminar el número para que pida la entrada de nuevo
            result = None
    # Devuelve el resultado
    return result


def input_yes_no(prompt, yes='^[Ss]$', no='^[Nn]$', newline=True):
    """Pide al usuario que ingrese sí o no a la pregunta que se le hace."""
    answer = None
    while answer is None:
        # Toma la entrada del usuario y quita espacios extra alrededor
        user_input = input(prompt).strip()
        if newline:
            print()
        if re.match(yes, user_input):
            # Respuesta afirmativa
            answer = True
        elif re.match(no, user_input):
            # Respuesta negativa
            answer = False
        else:
            # Si la entrada no cumple con ninguno de los patrones,
            # muestra mensaje de error
            print_error('Entrada inválida. Ingrese sí o no como se indica.',
                        newline)
    # Devuelve la respuesta
    return answer


def input_period(prompt, newline=True):
    """Pide al usuario que ingrese un período académico válido."""
    period = None
    while period is None:
        # Toma la entrada del usuario en mayúsculas y quita espacios alrededor
        user_input = input(prompt).upper().strip()
        if newline:
            print()
        if validate_period(user_input):
            # Si la entrada es un período académico válido, toma su valor
            period = user_input
        else:
            # De lo contrario, se muestra un error
            print_error('Período académico inválido.', newline)
    # Devuelve el período académico ingresado
    return period


def read_csv(filename, delim=',', quote='"'):
    """Extrae el contenido de un archivo CSV."""
    content = []
    # Abre el archivo de forma segura
    with open(filename, newline='') as csvfile:
        # Crea un objeto lector de CSV con el archivo dado
        csv_reader = csv.reader(csvfile, delimiter=delim, quotechar=quote)
        for row in csv_reader:
            # Agrega cada fila del archivo a la lista del contenido
            content.append(row)
    # Devuelve el contenido del CSV
    return content


def validate_period(user_input, pattern='^\d{4}-(01|IN|02)$'):
    """Verifica si la entrada corresponde con un período académico."""
    return re.match(pattern, user_input)


def split_list(s, separator='[,\s]+'):
    """Separa el texto según el patrón dado."""
    return re.split(separator, s)
