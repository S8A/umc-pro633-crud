# umc-pro633-crud

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

Sistema CRUD de campus UMC hecho como proyecto de Programación 3 (PRO633).

## Requerimientos

- [Python 3](https://www.python.org/)
- [Librería PyMySQL](https://pypi.org/project/PyMySQL/)
- [Librería PyQt5](https://pypi.org/project/PyQt5/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)

## Instalación y preparación de la base de datos

Primero, clone este repositorio:

```bash
git clone https://github.com/S8A/umc-pro633-crud.git
cd umc-pro633-crud
```

Luego, importe uno de los archivos del directorio `db` a su servidor MySQL para 
crear la base de datos. En dicho directorio se encuentran dos archivos: 
`umc_db_structure.sql` y `umc_db.sql`.

Para crear la base de datos con los datos iniciales de ejemplo, ejecute el
siguiente comando reemplazando `user` y `database` por los valores apropiados:

```bash
mysql -u user -p database < db/umc_db.sql
```

En cambio, para crear la base de datos con las tablas vacías, ejecute el
comando con el otro archivo:

```bash
mysql -u user -p database < db/umc_db_structure.sql
```

## Uso: modo de línea de comandos (CLI)

Desde la carpeta donde clonó el repositorio, ejecute el módulo `umc_crud`:

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

## Uso: modo gráfico (GUI)

Desde la carpeta donde clonó el repositorio, ejecute el módulo `umc_crud.gui`:

```bash
python3 -m umc_crud.gui
```

Al iniciar, el programa verifica si el archivo de configuración 
`config/config.ini` existe y está completo. En caso negativo, solicita al 
usuario los datos de conexión al servidor MySQL y los almacena en un nuevo 
archivo de configuración. Si luego desea modificar la configuración, puede 
editar el archivo manualmente o ejecutar el programa con la opción `--config`:

```bash
python3 -m umc_crud.gui --config
```

## Capturas de pantalla: CLI

### Configuración inicial

![Ventana mostrando la configuración inicial del programa](https://s8a.github.io/assets/img/umc-pro633-crud-first-config.png)

### Módulo de estudiante

![Ventana mostrando el módulo de estudiante con el usuario janedoe](https://s8a.github.io/assets/img/umc-pro633-crud-student-janedoe.png)
![Ventana mostrando el módulo de estudiante con el usuario s8a](https://s8a.github.io/assets/img/umc-pro633-crud-student-s8a.png)

### Módulo de administrador

![Ventana mostrando el módulo de administrador con el usuario superman](https://s8a.github.io/assets/img/umc-pro633-crud-admin-superman.png)

## Capturas de pantalla: GUI

### Configuración inicial

![Ventana de configuración inicial del programa en modo GUI](https://s8a.github.io/assets/img/umc-pro633-crud-gui-config.png)

### Módulo de estudiante

![Ventana de inicio de sesión como usuario janedoe](https://s8a.github.io/assets/img/umc-pro633-crud-gui-student-janedoe-login.png)
![Ventana de información personal del estudiante (usuario janedoe)](https://s8a.github.io/assets/img/umc-pro633-crud-gui-student-janedoe-info.png)
![Ventana de consulta de calificaciones del estudiante (usuario janedoe)](https://s8a.github.io/assets/img/umc-pro633-crud-gui-student-janedoe-record.png)

### Módulo de administrador

![Ventana de inicio de sesión como usuario superman](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-login.png)
![Ventana de consulta de información personal de estudiantes](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-info.png)
![Ventana de consulta de calificaciones de estudiantes](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-find.png)
![Ventana de registro manual de calificaciones](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-make.png)
![Ventana de carga de calificaciones a partir de archivo CSV](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-load.png)
![Ventana de modificación de calificaciones](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-update.png)
![Ventana de eliminación de calificaciones](https://s8a.github.io/assets/img/umc-pro633-crud-gui-admin-superman-delete.png)

## Licencia

Este proyecto está licenciado bajo los términos de la 
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/).

La librería PyMySQL está distribuida bajo los términos de la
[MIT License](https://github.com/PyMySQL/PyMySQL/blob/master/LICENSE)

La librería PyQt5 está distribuida bajo los términos de la licencia [GNU GPLv3](https://pypi.org/project/PyQt5/#License)
