from .. import crud
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class MainWindow(qtw.QMainWindow):
    """Ventana principal del módulo de estudiante."""

    def __init__(self, user_id):
        """Inicialización."""
        super().__init__()
        self.usuario_id = user_id
        self.setWindowTitle(
            f'Módulo de Estudiante - {self.usuario_id} - UMC Campus CRUD')
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica de la ventana."""
        # Crea la barra de herramientas
        self._create_main_toolbar()
        # Crea un widget vacío para llenar el área central
        self.setCentralWidget(qtw.QWidget())

    def _create_main_toolbar(self):
        """Crea la barra de herramientas principal de la ventana."""
        # Barra de herramientas
        main_toolbar = self.addToolBar('')
        main_toolbar.setMovable(False)
        main_toolbar.setFloatable(False)
        # Lista de opciones con sus funciones asociadas
        self.options = [['Consultar información personal',
                         self._get_personal_info],
                        ['Consultar récord académico',
                         self._get_record]]
        # Selector de opciones
        combo = qtw.QComboBox()
        combo.setSizeAdjustPolicy(qtw.QComboBox.AdjustToContents)
        for item in self.options:
            combo.addItem(item[0])
        combo.activated[int].connect(self._option_activated)
        main_toolbar.addWidget(combo)

    def _option_activated(self, index):
        """Ejecuta la función apropiada según la opción seleccionada."""
        self.options[index][1]

    def _get_personal_info(self):
        print('TODO: _get_personal_info')

    def _get_record(self):
        print('TODO: _get_record')
