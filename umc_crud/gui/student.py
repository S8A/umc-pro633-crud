from .. import crud
from . import utils
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class MainWindow(qtw.QMainWindow):
    """Ventana principal del módulo de estudiante."""

    def __init__(self, user_id):
        """Inicialización."""
        super().__init__()
        self.estudiante = crud.find_student_by_username(user_id)
        self.setWindowTitle(
            f'Módulo de Estudiante - {user_id} - UMC Campus CRUD')
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica de la ventana."""
        # Crea la barra de herramientas
        self._create_main_toolbar()
        # Crea un widget vacío para llenar el área central
        self.setCentralWidget(qtw.QWidget())
        self.setMinimumSize(400, 300)

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
        self.options[index][1]()

    def _get_personal_info(self):
        """Consulta la información personal del estudiante."""
        # Estructura
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        # Cabecera
        layout.addWidget(utils.create_label_h1('Información personal'))
        # Contenido
        layout.addWidget(utils.create_label(
            f'<b>Nombre y apellido:</b> {self.estudiante["nombre"]} '
            f'{self.estudiante["apellido"]}'))
        layout.addWidget(utils.create_label(
            f'<b>C.I.:</b> {self.estudiante["ci"]}'))
        layout.addWidget(utils.create_label(
            f'<b>Teléfono:</b> {self.estudiante["telefono"]}'))
        layout.addWidget(utils.create_label(
            f'<b>Dirección:</b> {self.estudiante["direccion"]}'))
        carrera = crud.read_career_info(self.estudiante['id_carrera'])
        layout.addWidget(utils.create_label(
            f'<b>Carrera:</b> {carrera["nombre"]} ({carrera["id"]})'))
        mencion = carrera["mencion"]
        if mencion is not None:
            layout.addWidget(qtw.QLabel(f'<b>Mención:</b> {mencion}'))
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _get_record(self):
        print('TODO: _get_record')
