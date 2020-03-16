import textwrap

# Funciones auxiliares para la consola

def printh1(s):
	print(f'..:: {s.upper()} ::..')
	print()

def printh2(s):
	print(f'{s} ::..')

def printlong(s):
	for line in textwrap.wrap(s):
		print(line)
	print()
