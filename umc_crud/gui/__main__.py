# coding=utf-8
"""Módulo principal del programa.

La ejecución del programa debe comenzar en este módulo.

La función main() toma los argumentos ingresados, verifica la
configuración y ejecuta el controlador del flujo del programa.
"""


import argparse
import sys
from PyQt5.QtWidgets import QApplication
from ..config import is_configured
from . import admin, config, login, student


class MainController:
    """Controlador del flujo del programa."""

    def __init__(self):
        pass

    def show_config_window(self):
        """Muestra la ventana de configuración."""
        self.config = config.ConfigDialog()
        self.config.accepted.connect(self.show_login_window)
        self.config.show()

    def show_login_window(self):
        """Muestra la ventana de inicio de sesión."""
        if not is_configured():
            QApplication.instance().exit()
        self.login = login.LoginDialog()
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
        self.student_window.show()

    def show_admin_window(self, user_id):
        """Muesta la ventana del módulo de administrador."""
        self.admin_window = admin.MainWindow(user_id)
        self.admin_window.show()


def main(args):
    """Función principal del programa."""
    app = QApplication(sys.argv)
    control = MainController()
    if args['config'] or not is_configured():
        control.show_config_window()
    else:
        control.show_login_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sistema CRUD de campus UMC con interfaz gráfica.')
    parser.add_argument('--config', action='store_true',
                        help='Configura la conexión a MySQL')
    args = parser.parse_args()
    main(vars(args))
