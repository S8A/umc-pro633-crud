from .db import execute_sql

# Módulo de creación, consulta, modificación y eliminación de registros

def create_record(ci, materia_id, nota):
	"""Registra la calificación de un estudiante en una asignatura."""
	query = 'INSERT INTO record VALUES (%s, %s, %s)'
	return execute_sql(query, args=(ci, materia_id, nota))


def read_records(ci, materia_ids=None):
	"""Consulta las calificaciones de un estudiante."""
	query = 'SELECT * FROM record'
    if materias is not None and len(materias) > 0:
        # Utilizar la lista de materias si se provee
        query += (' WHERE '
                  ' AND '.join(['id_materia = ' + m for m in materia_ids]))
    return execute_sql(query)


def update_record(ci, materia_id, nota):
	"""Modifica la calificación de un estudiante en una asignatura."""
    query = ('UPDATE record SET nota = %s WHERE ci_estudiante = %s '
             'AND id_materia = %s')
    return execute_sql(query, args=(nota, ci, materia_id))


def delete_record(ci, materia_id):
	"""Elimina la calificación de un estudiante en una asignatura."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    return execute_sql(query, args=(ci, materia_id))
