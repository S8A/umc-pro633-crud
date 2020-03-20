from .db import execute_sql

# Módulo de creación, consulta, modificación y eliminación de datos de la BDD

# Tabla record

def create_record(ci, materia_id, nota, periodo, test=False):
    """Registra la calificación de un estudiante en una asignatura."""
    query = 'INSERT INTO record VALUES (%s, %s, %s, %s)'
    return execute_sql(query, args=[ci, materia_id, nota, periodo], test=test)


def create_records(record):
    """Registra calificaciones de varias materias y estudiantes."""
    query = 'INSERT INTO record VALUES (%s, %s, %s, %s)'
    args = [tuple(r.values()) for r in record]
    return execute_sql(query, args, many=True)


def read_records(ci, materia_ids=None, test=False):
    """Consulta las calificaciones de un estudiante."""
    query = ('SELECT materia.id, materia.nombre, materia.uc, '
             'record.nota, record.periodo '
             'FROM materia INNER JOIN record '
             'ON materia.id = record.id_materia '
             'WHERE record.ci_estudiante = %s')
    args = [ci]
    if materia_ids is not None and len(materia_ids) > 0:
        # Utilizar la lista de materias si se provee
        query += (' AND materia.id IN ('
                  + ', '.join(['%s' for m in materia_ids])
                  + ')')
        args.extend(materia_ids)
    query += ' ORDER BY record.periodo'
    return execute_sql(query, args, test=test)


def update_record(ci, materia_id, nota, periodo, test=False):
    """Modifica la calificación de un estudiante en una asignatura."""
    query = ('UPDATE record SET nota = %s, periodo = %s, '
             'WHERE ci_estudiante = %s AND id_materia = %s')
    return execute_sql(query, args=[nota, periodo, ci, materia_id])


def delete_record(ci, materia_id, test=False):
    """Elimina la calificación de un estudiante en una asignatura."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    return execute_sql(query, args=[ci, materia_id], test=test)


# Tabla estudiante

def read_student_info(user_id, test=False):
    """Consulta toda la información del estudiante según su usuario."""
    query = 'SELECT * FROM estudiante WHERE id_usuario = %s'
    return execute_sql(query, args=[user_id], rows=1, test=test)


def find_students(ci_list, test=False):
    """Busca estudiantes por su número de cédula."""
    query = ('SELECT * FROM estudiante WHERE ci IN ('
             + ', '.join(['%s' for ci in ci_list]) + ')')
    return execute_sql(query, args=ci_list, test=test)


# Tabla carrera

def read_career_info(carrera_id, test=False):
    """Consulta la información de una carrera según su código."""
    query = 'SELECT * FROM carrera WHERE id = %s'
    return execute_sql(query, args=[carrera_id], rows=1, test=test)


# Tabla materia_carrera

def find_materias_carrera(carrera_id, materia_ids, test=False):
    """Busca materias de una carrera por su código."""
    query = ('SELECT id_materia FROM materia_carrera WHERE id_carrera = %s '
             + 'AND id_materia IN ('
             + ', '.join(['%s' for materia in materia_ids]) + ')')
    args = [carrera_id]
    args.extend(materia_ids)
    return execute_sql(query, args, test=test)
