# umc-pro633-crud

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

Sistema CRUD de campus UMC hecho como proyecto de Programación 3 (PRO633).

## Requerimientos

- [Python 3](https://www.python.org/)
- Librería [PyMySQL](https://pypi.org/project/PyMySQL/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)

## Instalación y uso

Para utilizar este programa, primero clone este repositorio:

```bash
git clone https://github.com/S8A/umc-pro633-crud.git
cd umc-pro633-crud
```

Luego, importe uno de los archivos del directorio `db` a su servidor MySQL para 
crear la base de datos. En dicho directorio se encuentran dos archivos: 
`umc_db_structure.sql` y `umc_db.sql`.

Para crear la base de datos con las tablas vacías, ejecute el siguiente comando reemplazando `user` y `database` por los valores apropiados:

```bash
mysql -u user -p database < db/umc_db_structure.sql
```

Para crear la base de datos con los datos iniciales de ejemplo:

```bash
mysql -u user -p database < db/umc_db.sql
```

Finalmente, para utilizar el programa solo tiene que ejecutar el módulo 
`umc_crud`:

```bash
python3 -m umc_crud
```

Al iniciar, el programa verifica si el archivo de configuración 
`config/config.ini` existe y está completo. En caso negativo, solicita al 
usuario los datos de conexión al servidor MySQL y los almacena en un nuevo 
archivo de configuración. Si luego desea modificar la configuración, puede 
editar el archivo manualmente o ejecutar el programa con la opción `--config`:

```bash
python3 -m umc_crud --config
```

## Licencia

Este proyecto está licenciado bajo los términos de la 
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/). 
