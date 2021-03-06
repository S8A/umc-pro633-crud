# coding=utf-8
"""Módulo de inicio de sesión.

Provee el diálogo de inicio de sesión (LoginDialog), el cual
permite al usuario ingresar sus credenciales del sistema campus
UMC y lo dirige al módulo de estudiante o administrador según
sea el caso.
"""


import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
from .. import crud
from . import utils


class LoginDialog(qtw.QDialog):
    """Diálogo de inicio de sesión."""
    user_login = qtc.pyqtSignal(str, bool)

    def __init__(self, parent=None):
        """Inicializa el diálogo de inicio de sesión y su interfaz gráfica."""
        super().__init__(parent)
        self.setWindowTitle('Inicio de Sesión - UMC Campus CRUD')
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica del diálogo."""
        # Estructura principal
        vbox_layout = qtw.QVBoxLayout()
        # Título
        title_label = utils.create_label_h1('Inicio de Sesión')
        vbox_layout.addWidget(title_label)
        # Formulario
        form_layout = qtw.QFormLayout()
        self.user_id = qtw.QLineEdit()
        form_layout.addRow('Usuario', self.user_id)
        self.user_pw = qtw.QLineEdit()
        self.user_pw.setEchoMode(qtw.QLineEdit.Password)
        form_layout.addRow('Contraseña', self.user_pw)
        vbox_layout.addLayout(form_layout)
        # Botones
        buttons = qtw.QDialogButtonBox()
        buttons.setStandardButtons(
            qtw.QDialogButtonBox.Cancel | qtw.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._login)
        buttons.rejected.connect(self.reject)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
        self.setMinimumSize(400, 300)

    def _login(self):
        """Intenta iniciar sesión con los datos ingresados."""
        # Ejecuta la búsqueda por usuario y contraseña
        result = crud.authenticate_user(
            self.user_id.text(), self.user_pw.text())
        if result is not None:
            # Si los datos coinciden con un usuario, se verifica si es
            # un administrador o un estudiante y se emite la señal apropiada
            if result['admin'] in [0, 1]:
                self.user_login.emit(result['id'], result['admin'])
                self.accept()
            else:
                utils.show_error_message(
                    'Valor inesperado en el registro de usuario.', self)
        else:
            # Si los datos no coinciden con ningún usuario, se muestra
            # un mensaje de error.
            utils.show_error_message(
                'Usuario o contraseña incorrecta. Intente de nuevo.', self)
