from .db import execute_sql

# Módulo de creación, consulta, modificación y eliminación de registros

def create_record(ci, materia_id, nota):
    """Registra la calificación de un estudiante en una asignatura."""
    query = 'INSERT INTO record VALUES (%s, %s, %s)'
    return execute_sql(query, args=(ci, materia_id, nota))


def read_records(ci, materia_ids=None):
    """Consulta las calificaciones de un estudiante."""
    query = 'SELECT * FROM record'
    if materia_ids is not None and len(materia_ids) > 0:
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


def get_student_info(user_id):
    """Obtiene toda la información del estudiante según su usuario."""
    query = 'SELECT * FROM estudiante WHERE id_usuario = %s'
    return execute_sql(query, args=(user_id), rows=1)


def get_career_info(carrera_id):
    """Obtiene la información de una carrera según su código."""
    query = 'SELECT * FROM carrera WHERE id = %s'
    return execute_sql(query, args=(carrera_id), rows=1)
