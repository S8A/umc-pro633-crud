from .. import crud
from ..student import calculate_ia, print_record
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
        # Inicia mostrando la información del estudiante
        self._get_personal_info()
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
        self.resize(400, 300)

    def _get_record(self):
        """Consulta el récord académico del estudiante."""
        # Crea una interfaz de consulta de récord académico para
        # un solo estudiante
        self.setCentralWidget(StudentRecordWidget(student=self.estudiante))
        self.resize(500, 500)


class StudentRecordWidget(qtw.QWidget):
    """Interfaz de consulta de récord académico."""

    def __init__(self, student=None):
        """Inicialización."""
        super().__init__()
        self.record = {}
        if student is not None:
            self.single = True
            self.estudiante = student
        self._create_ui()
        self._find_record()

    def _create_ui(self):
        """Crea la interfaz gráfica de consulta de récord académico."""
        # Estructura
        main_widget = qtw.QWidget()
        main_layout = qtw.QVBoxLayout()
        # Cabecera
        main_layout.addWidget(utils.create_label_h1('Récord académico'))
        # Formulario de búsqueda
        form_layout = qtw.QFormLayout()
        if not self.single:
            self.estudiante_input = qtw.QLineEdit()
            form_layout.addRow('Estudiante', self.estudiante_input)
        self.materias_input = qtw.QLineEdit()
        form_layout.addRow('Materias', self.materias_input)
        self.periodo_input = qtw.QLineEdit()
        form_layout.addRow('Período', self.periodo_input)
        main_layout.addLayout(form_layout)
        consultar_btn = qtw.QPushButton('Consultar')
        consultar_btn.clicked.connect(self._find_record)
        main_layout.addWidget(consultar_btn)
        # Tabla de datos
        # TODO: Convertir la tabla a QTableView
        self.record_tbl = qtw.QTextEdit()
        self.record_tbl.setReadOnly(True)
        main_layout.addWidget(self.record_tbl, stretch=2)
        # Información adicional
        uc_cursadas = [r['uc'] for r in self.record]
        main_layout.addWidget(utils.create_label(
            f'Materias cursadas: {len(uc_cursadas)} ({sum(uc_cursadas)} UC)'))
        uc_aprobadas = [r['uc'] for r in self.record if r['nota'] >= 12]
        main_layout.addWidget(utils.create_label(
            f'Materias aprobadas: {len(uc_aprobadas)} '
            f'({sum(uc_aprobadas)} UC)'))
        main_layout.addWidget(utils.create_label(
            f'Índice Académico Acumulado (IAA): {calculate_ia(self.record)}'))
        self.setLayout(main_layout)

    def _find_record(self):
        """Consulta el récord académico con los datos ingresados."""
        print('TODO: _find_record')
