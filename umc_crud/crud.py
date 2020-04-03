# coding=utf-8
"""Módulo de creación, consulta, modificación y eliminación de datos.

Este módulo provee funciones para realizar diversas operaciones
de alto nivel en la base de datos MySQL. Estas operaciones son la
base del funcionamiento de los módulos de estudiante y administrador.

Incluye funciones para crear, consultar, modificar y eliminar
récords académicos, así como funciones de consulta de usuarios,
estudiantes, carreras y materias.
"""


from .db import execute_sql


# Tabla record

def create_record(ci, materia_id, nota, periodo, test=False):
    """Registra la calificación de un estudiante en una materia."""
    query = 'INSERT INTO record VALUES (%s, %s, %s, %s)'
    return execute_sql(query, args=[ci, materia_id, nota, periodo], test=test)


def create_records(record):
    """Registra calificaciones de varias materias y estudiantes."""
    query = 'INSERT INTO record VALUES (%s, %s, %s, %s)'
    args = [tuple(r.values()) for r in record]
    return execute_sql(query, args, many=True)


def read_records(ci, materia_ids=None, periodo=None, test=False):
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
    if periodo is not None:
        # Toma en cuenta solo el período indicado, si se provee
        query += ' AND record.periodo = %s'
        args.append(periodo)
    query += ' ORDER BY record.periodo'
    return execute_sql(query, args, test=test)


def update_record(ci, materia_id, nota, periodo, test=False):
    """Modifica la calificación de un estudiante en una materia."""
    query = ('UPDATE record SET nota = %s, periodo = %s '
             'WHERE ci_estudiante = %s AND id_materia = %s')
    return execute_sql(query, args=[nota, periodo, ci, materia_id])


def update_records(record):
    """Modifica las calificaciones de varias materias y estudiantes."""
    query = ('UPDATE record SET nota = %s, periodo = %s '
             'WHERE ci_estudiante = %s AND id_materia = %s')
    args = [(r['nota'], r['periodo'], r['ci_estudiante'], r['id_materia'])
            for r in record]
    return execute_sql(query, args, many=True)


def delete_record(ci, materia_id, test=False):
    """Elimina la calificación de un estudiante en una materia."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    return execute_sql(query, args=[ci, materia_id], test=test)


def delete_records(record):
    """Elimina las calificaciones de varias materias y estudiantes."""
    query = 'DELETE FROM record WHERE ci_estudiante = %s AND id_materia = %s'
    args = [(r['ci_estudiante'], r['id_materia']) for r in record]
    return execute_sql(query, args, many=True)


# Tabla usuario

def authenticate_user(usuario_id, usuario_pw, test=False):
    """Trata de encontrar la combinación dada de usuario y contraseña."""
    query = 'SELECT * FROM usuario WHERE id = %s AND password = %s'
    return execute_sql(query, args=[usuario_id, usuario_pw], rows=1)


# Tabla estudiante

def find_student_by_username(usuario_id, test=False):
    """Consulta toda la información de un estudiante según su usuario."""
    query = 'SELECT * FROM estudiante WHERE id_usuario = %s'
    return execute_sql(query, args=[usuario_id], rows=1, test=test)


def find_student_by_ci(ci, test=False):
    """Consulta toda la información de un estudiante según su cédula."""
    query = 'SELECT * FROM estudiante  WHERE ci = %s'
    return execute_sql(query, args=[ci], rows=1, test=test)


def find_students(ci_list, test=False):
    """Consulta estudiantes por su número de cédula."""
    query = ('SELECT * FROM estudiante WHERE ci IN ('
             + ', '.join(['%s' for ci in ci_list]) + ')')
    return execute_sql(query, args=ci_list, test=test)


# Tabla carrera

def read_career_info(carrera_id, test=False):
    """Consulta la información de una carrera según su código."""
    query = 'SELECT * FROM carrera WHERE id = %s'
    return execute_sql(query, args=[carrera_id], rows=1, test=test)


# Tabla materia

def find_subject(materia_id, test=False):
    """Consulta la información de una materia por su código."""
    query = 'SELECT * FROM materia WHERE id = %s'
    return execute_sql(query, args=[materia_id], rows=1, test=test)


def find_subjects(materia_ids, test=False):
    """Consulta la información de varias materias."""
    query = ('SELECT * FROM materia WHERE id IN ('
             + ', '.join(['%s' for m in materia_ids]) + ')')
    return execute_sql(query, args=materia_ids, test=test)


# Tabla materia_carrera

def find_career_subject(carrera_id, materia_id, test=False):
    """Consulta una materia en una carrera por su código"""
    query = ('SELECT id_materia FROM materia_carrera '
             'WHERE id_carrera = %s AND id_materia = %s')
    args = [carrera_id, materia_id]
    return execute_sql(query, args, rows=1, test=test)


def find_career_subjects(carrera_id, materia_ids, test=False):
    """Consulta materias en una carrera por su código."""
    query = ('SELECT id_materia FROM materia_carrera WHERE id_carrera = %s '
             + 'AND id_materia IN ('
             + ', '.join(['%s' for materia in materia_ids]) + ')')
    args = [carrera_id]
    args.extend(materia_ids)
    return execute_sql(query, args, test=test)


# Múltiples tablas

def find_subjects_not_taken_by_student(ci_estudiante, test=False):
    """Consulta materias que no han sido cursadas por el estudiante."""
    query = ('SELECT id_materia FROM materia_carrera WHERE id_carrera = '
             '(SELECT id_carrera FROM estudiante WHERE ci = %(ci)s) AND '
             'id_materia NOT IN (SELECT id_materia FROM record '
             'WHERE ci_estudiante = %(ci)s)')
    return execute_sql(query, args={'ci': ci_estudiante}, test=test)
