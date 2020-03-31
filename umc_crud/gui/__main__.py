from ..config import is_configured
from . import config, login
from PyQt5.QtWidgets import QApplication
import argparse, sys


class MainController:
    """Controla el flujo del programa."""

    def __init__(self):
        """Inicialización."""
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
        self.login.admin_login.connect(self.show_admin_window)
        self.login.student_login.connect(self.show_student_window)
        self.login.show()

    def show_student_window(self):
        """Muestra la ventana del módulo de estudiante."""
        print('TODO: show_student_window')

    def show_admin_window(self):
        """Muesta la ventana del módulo de administrador."""
        print('TODO: show_admin_window')


def main(args):
    """Función principal del programa."""
    app = QApplication([])
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
