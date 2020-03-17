from .db import execute_sql

# Módulo de creación, consulta, modificación y eliminación de registros

def create_record(ci, materia, nota):
	"""Registra la calificación de un estudiante en una asignatura."""
	query = 'INSERT INTO record VALUES (%s, %s, %s)'
	return execute_sql(query, args=(ci, materia, nota))


def read_records(ci, materias=None):
	"""Consulta las calificaciones de un estudiante."""
	query = 'SELECT * FROM record'
    if materias is not None and len(materias) > 0:
        query += (' WHERE '
                  ' AND '.join(['id_materia = ' + m for m in materias]))
    return execute_sql(query)


def update_record(ci, materia, nota):
	"""Modifica la calificación de un estudiante en una asignatura."""
    query = ('UPDATE record SET nota = %s WHERE ci_estudiante = %s '
             'AND id_materia = %s')
    return execute_sql(query, args=(nota, ci, materia))


def delete_record(ci, materia):
	"""Elimina la calificación de un estudiante en una asignatura."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    return execute_sql(query, args=(ci, materia))
