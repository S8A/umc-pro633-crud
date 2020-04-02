import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
from .. import crud
from ..io import split_list, validate_period
from ..student import calculate_ia
from . import student, utils


class MainWindow(qtw.QMainWindow):
    """Ventana principal del módulo de administrador."""

    def __init__(self, user_id, parent=None):
        """Inicializa el módulo de administrador con el usuario dado."""
        super().__init__(parent)
        self.setWindowTitle(
            f'Módulo de Administrador - {user_id} - UMC Campus CRUD')
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica de la ventana."""
        # Crea la barra de herramientas
        self._create_main_toolbar()
        # Inicia en el módulo de consulta de información personal
        self._get_personal_info()
        self.setMinimumSize(400, 300)

    def _create_main_toolbar(self):
        """Crea la barra de herramientas principal de la ventana."""
        # Barra de herramientas
        main_toolbar = self.addToolBar('')
        main_toolbar.setMovable(False)
        main_toolbar.setFloatable(False)
        # Lista de opciones con sus funciones asociadas
        self.options = [
            ['Consultar información personal', self._get_personal_info],
            ['Consultar récord académico', self._get_record],
            ['Registrar calificaciones', self._make_records],
            ['Cargar archivo de calificaciones', self._load_csv_records],
            ['Modificar calificaciones', self._update_records],
            ['Eliminar calificaciones', self._delete_records],
        ]
        # Selector de opciones
        combo = qtw.QComboBox()
        combo.setSizeAdjustPolicy(qtw.QComboBox.AdjustToContents)
        for item in self.options:
            combo.addItem(item[0])
        combo.activated[int].connect(self._option_activated)
        main_toolbar.addWidget(combo)

    def _option_activated(self, index):
        """Ejecuta la función apropiada según la opción seleccionada."""
        self.options[index][1]()

    def _get_personal_info(self):
        """Crea la interfaz de consulta de información personal."""
        self.setCentralWidget(student.StudentInfoWidget())
        self.resize(400, 300)

    def _get_record(self):
        """Crea la interfaz de consulta del récord académico."""
        self.setCentralWidget(student.StudentRecordWidget())
        self.resize(700, 600)

    def _make_records(self):
        """Crea la interfaz de Registrar calificaciones."""
        print('TODO: _make_records')

    def _load_csv_records(self):
        """Crea la interfaz de Cargar archivo de calificaciones."""
        print('TODO: _load_csv_records')

    def _update_records(self):
        """Crea la interfaz de Modificar calificaciones."""
        print('TODO: _update_records')

    def _delete_records(self):
        """Crea la interfaz de Eliminar calificaciones."""
        print('TODO: _delete_records')
