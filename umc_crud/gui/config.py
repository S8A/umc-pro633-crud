import PyQt5.QtWidgets as qtw
from ..config import create_config
from . import utils


class ConfigDialog(qtw.QDialog):
    """Diálogo de configuración del programa."""

    def __init__(self, parent=None):
        """Inicializa el diálogo de configuración y su interfaz gráfica."""
        super().__init__(parent)
        self.setWindowTitle('Configuración - UMC Campus CRUD')
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica del diálogo."""
        # Estructura principal
        vbox_layout = qtw.QVBoxLayout()
        # Título
        title_label = utils.create_label_h1('Configuración de MySQL')
        vbox_layout.addWidget(title_label)
        # Formulario
        form_layout = qtw.QFormLayout()
        self.form_inputs = {'host': ['Host'],
                            'user': ['Usuario'],
                            'password': ['Contraseña'],
                            'database': ['Base de datos']}
        for key, content in self.form_inputs.items():
            line_edit = qtw.QLineEdit()
            if key == 'password':
                line_edit.setEchoMode(qtw.QLineEdit.Password)
            self.form_inputs[key].append(line_edit)
        for label, text_input in self.form_inputs.values():
            form_layout.addRow(label, text_input)
        vbox_layout.addLayout(form_layout)
        # Botones
        buttons = qtw.QDialogButtonBox()
        buttons.setStandardButtons(
            qtw.QDialogButtonBox.Cancel | qtw.QDialogButtonBox.Save)
        buttons.accepted.connect(self._save_config)
        buttons.rejected.connect(self.reject)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
        self.setMinimumSize(400, 300)

    def _save_config(self):
        """Guarda la configuración ingresada."""
        # Extrae los datos ingresados
        mysql_data = {k: v[1].text() for k, v in self.form_inputs.items()}
        # Verifica que ningún dato esté vacío
        for item in mysql_data.values():
            if not item:
                utils.show_error_message(
                    'Complete todos los campos de configuración.', self)
                return
        # Crea el archivo de configuración
        create_config(mysql_data)
        # Emite la señal de aceptar
        self.accept()
