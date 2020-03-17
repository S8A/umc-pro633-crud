from .config import read_config
import pymysql

# Módulo de manejo de base datos

def connect():
    """Crea una conexión a la base de datos indicada en la configuración."""
    mysql_conf = read_config()['mysql']
    return pymysql.connect(host=mysql_conf['host'],
                           user=mysql_conf['user'],
                           password=mysql_conf['password'],
                           database=mysql_conf['database'],
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def execute_sql(query, args=None, rows=None):
    """
    Ejecuta una petición SQL y devuelve su resultado.

    Argumentos:
    query (str) -- Petición a realizar
    args (tuple/list/dict) --  Parámetros de la petición (opc)
    rows (int or None) -- Número de filas de resultado (opc).
    """
    connection = connect()
    result = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            if rows is None:
                result = cursor.fetchall()
            elif rows == 1:
                result = cursor.fetchone()
            elif rows > 1:
                result = cursor.fetchmany(size=rows)
        connection.commit()
    finally:
        connection.close()
    return result
