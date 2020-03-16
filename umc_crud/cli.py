import textwrap

# Funciones auxiliares para la consola

def print_h1(s):
    print(f'..:: {s.upper()} ::..')
    print()

def print_h2(s):
    print(f'{s} ::..')

def print_long(s):
    for line in textwrap.wrap(s):
        print(line)

def print_error(s):
    print_long(f'ERROR: {s}')
    print()
