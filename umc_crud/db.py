import pymysql

# Módulo de manejo de base datos

def connect_to_db(mysql_conf):
    """Crea una conexión a la base de datos indicada en la configuración."""
    return pymysql.connect(host=mysql_conf['host'],
                           user=mysql_conf['user'],
                           password=mysql_conf['password'],
                           database=mysql_conf['database'],
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
