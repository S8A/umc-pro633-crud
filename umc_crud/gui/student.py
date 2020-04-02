from .. import crud
from ..io import split_list, validate_period
from ..student import calculate_ia
from . import utils
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class MainWindow(qtw.QMainWindow):
    """Ventana principal del módulo de estudiante."""

    def __init__(self, user_id, parent=None):
        """Inicialización."""
        super().__init__(parent)
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
        self.resize(700, 600)


class StudentRecordWidget(qtw.QWidget):
    """Interfaz de consulta de récord académico."""

    def __init__(self, student=None, parent=None):
        """Inicialización."""
        super().__init__(parent)
        self.record = {}
        if student is not None:
            # Si se inicializa con un estudiante, se establece el modo
            # de estudiante único para desactivar la búsqueda por cédula
            self.single_mode = True
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
        if not self.single_mode:
            # Campo de cédula del estudiante, si el modo de estudiante
            # único no aplica
            self.estudiante_input = qtw.QLineEdit()
            form_layout.addRow('Estudiante (C.I.)', self.estudiante_input)
        # Campo de materias a consultar
        self.materias_input = qtw.QLineEdit()
        form_layout.addRow('Materias', self.materias_input)
        # Campo de período académico a consultar
        self.periodo_input = qtw.QLineEdit()
        form_layout.addRow('Período', self.periodo_input)
        main_layout.addLayout(form_layout)
        # Botón de consulta
        consultar_btn = qtw.QPushButton('Consultar')
        consultar_btn.clicked.connect(self._find_record)
        main_layout.addWidget(consultar_btn)
        # Tabla de datos
        self.record_tbl = qtw.QTableView()
        # Encabezados de la tabla
        self.record_headers = {'id': 'Código',
                               'nombre': 'Materia',
                               'uc': 'UC',
                               'nota': 'Nota',
                               'periodo': 'Período'}
        # Modelo interno de la tabla
        self.record_tbl_model = RecordTableModel(
            self.record, self.record_headers)
        self.record_tbl.setModel(self.record_tbl_model)
        # Configura el encabezado de la tabla
        self.record_tbl_header = self.record_tbl.horizontalHeader()
        for i, header in enumerate(self.record_headers.keys()):
            # Todas las columnas se ajustan a su contenido
            resize_mode = qtw.QHeaderView.ResizeToContents
            if header == 'nombre':
                # Excepto la columna del nombre de materia, que se expande
                resize_mode = qtw.QHeaderView.Stretch
            self.record_tbl_header.setSectionResizeMode(i, resize_mode)
        main_layout.addWidget(self.record_tbl, stretch=2)
        # Información adicional
        self.uc_cursadas = utils.create_label('')
        main_layout.addWidget(self.uc_cursadas)
        self.uc_aprobadas = utils.create_label('')
        main_layout.addWidget(self.uc_aprobadas)
        self.indice_academico = utils.create_label('')
        main_layout.addWidget(self.indice_academico)
        self.setLayout(main_layout)

    def _find_record(self):
        """Consulta el récord académico con los datos ingresados."""
        if not self.single_mode:
            # Si no está activado el modo de estudiante único,
            # extraer la cédula ingresada
            ci = self.estudiante_input.text().strip()
            # Buscar el estudiante por su cédula
            self.estudiante = crud.find_student_by_ci(ci)
            # Si no se encuentra el estudiante, mostrar error
            if not self.estudiante:
                error_msg = qtw.QErrorMessage(self)
                error_msg.setModal(True)
                error_msg.showMessage('Estudiante no encontrado.')
                return
        # Extraer las materias ingresadas
        materia_ids = split_list(self.materias_input.text().strip())
        # Filtrar elementos vacíos
        materia_ids = [m for m in materia_ids if m]
        if not materia_ids:
            materia_ids = None
        # Extraer y comprobar el período ingresado
        periodo = self.periodo_input.text().upper().strip()
        if not validate_period(periodo):
            periodo = None
        # Buscar el récord académico con los datos obtenidos
        self.record = crud.read_records(self.estudiante['ci'],
                                        materia_ids,
                                        periodo)
        # Realiza el reemplazo de los datos
        self.record_tbl_model.replace_record(self.record)
        # Actualiza la información adicional
        self._update_record_info()

    def _update_record_info(self):
        """Actualiza la información adicional del récord académico."""
        # Extrae las UC de las materias cursadas
        uc_cursadas = [r['uc'] for r in self.record]
        # Muestra el número de materias cursadas y su total de UC
        self.uc_cursadas.setText(
            f'Materias cursadas: {len(uc_cursadas)} ({sum(uc_cursadas)} UC)')
        # Extrae las UC de las materias aprobadas
        uc_aprobadas = [r['uc'] for r in self.record if r['nota'] >= 12]
        # Muestra el número de materias aprobadas y su total de UC
        self.uc_aprobadas.setText(
            f'Materias aprobadas: {len(uc_aprobadas)} '
            f'({sum(uc_aprobadas)} UC)')
        # Muestra el índice académico del registro dado
        self.indice_academico.setText(
            f'Índice Académico (IA): {calculate_ia(self.record) or "N/A"}')


class RecordTableModel(qtc.QAbstractTableModel):
    """Modelo interno para tablas de récords académicos."""

    def __init__(self, record, header, parent=None):
        """Inicialización"""
        super().__init__(parent)
        self.record = record
        self.header = header

    def data(self, index, role):
        """Obtiene los datos del récord en el índice y rol dado."""
        if role == qtc.Qt.DisplayRole:
            # Muestra los datos del índice dado
            column_name = self._header_column(index.column())
            return self.record[index.row()][column_name]

    def _header_column(self, i):
        """Obtiene el nombre de la columna a partir de su número."""
        return list(self.header.keys())[i]

    def rowCount(self, parent):
        """Obtiene el número de registros."""
        return len(self.record)

    def columnCount(self, parent):
        """Obtiene el número de columnas de la tabla."""
        return len(self.header)

    def headerData(self, section, orientation, role):
        """Obtiene los datos de la cabecera de la tabla."""
        if role == qtc.Qt.DisplayRole:
            if orientation == qtc.Qt.Horizontal:
                column_name = self._header_column(section)
                return str(self.header[column_name])

    def replace_record(self, record):
        """Reemplaza los registros de la tabla."""
        # Notifica el cambio
        self.beginResetModel()
        # Realiza el reemplazo
        self.record = record
        # Notifica el fin de la operación
        self.endResetModel()
