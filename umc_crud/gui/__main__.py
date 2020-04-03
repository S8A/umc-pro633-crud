# coding=utf-8
"""Módulo principal del programa.

La ejecución del programa debe comenzar en este módulo.

La función main() toma los argumentos ingresados, crea una
QApplication y ejecuta el controlador del flujo del programa.
"""


import argparse
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ..config import is_configured
from . import admin, config, login, student, utils


class MainController:
    """Controlador del flujo del programa."""

    def __init__(self, args):
        """Inicializa el controlador del flujo del programa."""
        # Buscar el ícono del programa
        script_dir = os.path.dirname(os.path.realpath(__file__))
        separator = os.path.sep
        icon_dir = separator.join([script_dir, 'resources', 'umc_logo.png'])
        self.icon = QIcon(icon_dir)
        # Seleccionar la ventana inicial
        if args['config'] or not is_configured():
            # Si el programa se inicia con --config o
            # no está configurado, inicia el diálogo de
            # configuración
            self.show_config_window()
        else:
            # De lo contrario, inicia el diálogo de inicio de sesión
            self.show_login_window()

    def show_config_window(self):
        """Muestra la ventana de configuración."""
        self.config = config.ConfigDialog()
        self.config.setWindowIcon(self.icon)
        utils.center_window(self.config)
        self.config.accepted.connect(self.show_login_window)
        self.config.show()

    def show_login_window(self):
        """Muestra la ventana de inicio de sesión."""
        if not is_configured():
            QApplication.instance().exit()
        self.login = login.LoginDialog()
        self.login.setWindowIcon(self.icon)
        utils.center_window(self.login)
        self.login.user_login.connect(self.show_main_window)
        self.login.show()

    def show_main_window(self, user_id, user_admin):
        """Muestra la ventana del módulo correspondiente al usuario."""
        if user_admin:
            self.show_admin_window(user_id)
        else:
            self.show_student_window(user_id)

    def show_student_window(self, user_id):
        """Muestra la ventana del módulo de estudiante."""
        self.student_window = student.MainWindow(user_id)
        self.student_window.setWindowIcon(self.icon)
        utils.center_window(self.student_window)
        self.student_window.show()

    def show_admin_window(self, user_id):
        """Muesta la ventana del módulo de administrador."""
        self.admin_window = admin.MainWindow(user_id)
        self.admin_window.setWindowIcon(self.icon)
        utils.center_window(self.admin_window)
        self.admin_window.show()


def main(args):
    """Función principal del programa."""
    app = QApplication(sys.argv)
    control = MainController(args)
    sys.exit(app.exec())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sistema CRUD de campus UMC con interfaz gráfica.')
    parser.add_argument('--config', action='store_true',
                        help='Configura la conexión a MySQL')
    args = parser.parse_args()
    main(vars(args))
