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


def execute_sql(query, args=None, rows=None, many=False, test=False):
    """
    Ejecuta una petición SQL y devuelve su resultado.

    Argumentos:
    query (str) -- Petición a realizar
    args (tuple/list/dict) --  Parámetros de la petición (opc)
    rows (int or None) -- Número de filas de resultado (opc).
    many (bool) -- Si la petición se hará con varios conjuntos de datos.
    test (bool) -- Modo de prueba (solo muestra la petición)
    """
    result = None
    # Crea la conexión a la base de datos
    connection = connect()
    try:
        with connection.cursor() as cursor:
            if test and not many:
                # Modo de prueba: imprime la petición solamente.
                # No funciona con múltiples conjuntos de datos.
                print(cursor.mogrify(query, args))
            else:
                # Ejecuta la petición
                if many:
                    cursor.executemany(query, args)
                else:
                    cursor.execute(query, args)
                # Recoge el número de resultados que se piden
                if rows is None:
                    result = cursor.fetchall()
                elif rows == 1:
                    result = cursor.fetchone()
                elif rows > 1:
                    result = cursor.fetchmany(size=rows)
        # Confirma la transacción
        connection.commit()
    finally:
        # Cierra la conexión
        connection.close()
    return result
