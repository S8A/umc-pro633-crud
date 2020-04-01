from .. import db
from . import utils
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class LoginDialog(qtw.QDialog):
    """Diálogo de inicio de sesión."""
    user_login = qtc.pyqtSignal(str, bool)

    def __init__(self, parent=None):
        """Inicialización."""
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
        # Petición de búsqueda en la tabla usuario
        query = 'SELECT * FROM usuario WHERE id = %s AND password = %s'
        # Ejecuta la búsqueda por usuario y contraseña
        result = db.execute_sql(query,
                                args=[self.user_id.text(),
                                      self.user_pw.text()],
                                rows=1)
        if result is not None:
            # Si los datos coinciden con un usuario, se verifica si es
            # un administrador o un estudiante y se emite la señal apropiada
            if result['admin'] in [0, 1]:
                self.user_login.emit(result['id'], result['admin'])
                self.accept()
            else:
                error_msg = qtw.QErrorMessage(self)
                error_msg.setModal(True)
                error_msg.showMessage(
                    'Valor inesperado en el registro de usuario.')
        else:
            # Si los datos no coinciden con ningún usuario, se muestra
            # un mensaje de error.
            error_msg = qtw.QErrorMessage(self)
            error_msg.setModal(True)
            error_msg.showMessage(
                'Usuario o contraseña incorrecta. Intente de nuevo.')
