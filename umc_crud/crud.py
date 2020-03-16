from .db import execute_sql

# Módulo de creación, consulta, modificación y eliminación de registros

def create_record(mysql_conf, ci, materia, nota):
	"""Registra la calificación de un estudiante en una asignatura."""
	query = 'INSERT INTO record VALUES (%s, %s, %s)'
	return execute_sql(mysql_conf, query, (ci, materia, nota))


def read_records(mysql_conf, ci, materias=None):
	"""Consulta las calificaciones de un estudiante."""
	query = 'SELECT * FROM record'
    if materias is not None and len(materias) > 0:
        query += (' WHERE '
                  ' AND '.join(['id_materia = ' + m for m in materias]))
    return execute_sql(mysql_conf, query)


def update_record(mysql_conf, ci, materia, nota):
	"""Modifica la calificación de un estudiante en una asignatura."""
    query = ('UPDATE record SET nota = %s WHERE ci_estudiante = %s '
             'AND id_materia = %s')
    return execute_sql(mysql_conf, query, (nota, ci, materia))


def delete_record(mysql_conf, ci, materia):
	"""Elimina la calificación de un estudiante en una asignatura."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    return execute_sql(mysql_conf, query, (ci, materia))
