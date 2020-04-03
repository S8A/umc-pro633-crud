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
        """Crea la interfaz de registro de calificaciones."""
        self.setCentralWidget(RecordMakerWidget())
        self.resize(700, 600)

    def _load_csv_records(self):
        """Crea la interfaz de carga de archivo de calificaciones."""
        self.setCentralWidget(RecordMakerWidget())
        self.resize(700, 600)

    def _update_records(self):
        """Crea la interfaz de modificación de calificaciones."""
        print('TODO: _update_records')

    def _delete_records(self):
        """Crea la interfaz de eliminación de calificaciones."""
        print('TODO: _delete_records')


class RecordMakerWidget(qtw.QWidget):
    """Componente de registro de calificaciones."""

    def __init__(self, parent=None):
        """Inicializa el componente de registro de calificaciones."""
        super().__init__(parent)
        self.estudiante_ci = None
        # Inicializa la interfaz gráfica
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica del componente."""
        # Estructura
        main_layout = qtw.QVBoxLayout()
        # Cabecera
        main_layout.addWidget(utils.create_label_h1(
            'Registro de calificaciones'))
        # Formulario de búsqueda
        form_layout = qtw.QFormLayout()
        # Campo de cédula del estudiante
        self.estudiante_input = qtw.QLineEdit()
        form_layout.addRow('Estudiante (C.I.)', self.estudiante_input)
        # Campo de materias a registrar
        self.materias_input = qtw.QLineEdit()
        form_layout.addRow('Materias', self.materias_input)
        main_layout.addLayout(form_layout)
        # Botón de búsqueda
        buscar_btn = qtw.QPushButton('Buscar')
        buscar_btn.clicked.connect(self._prepare_records)
        main_layout.addWidget(buscar_btn)
        # Tabla de datos
        self.record_tbl = qtw.QTableView()
        # Encabezados de la tabla
        self.record_headers = {'id': 'Código',
                               'nombre': 'Materia',
                               'uc': 'UC',
                               'nota': 'Nota',
                               'periodo': 'Período'}
        # Modelo interno de la tabla
        self.record_tbl_model = student.RecordTableModel(
            self.record_headers, editable=True)
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
        # Botón de registro de calificaciones
        registrar_btn = qtw.QPushButton('Registrar')
        registrar_btn.clicked.connect(self._make_records)
        main_layout.addWidget(registrar_btn)
        self.setLayout(main_layout)

    def _prepare_records(self):
        """Prepara los datos de las calificaciones a registrar."""
        # Extraer la cédula ingresada
        ci = self.estudiante_input.text().strip()
        if not ci:
            # Si no se ingresó ninguna cédula, mostrar error
            utils.show_error_message('Ingrese un número de cédula.', self)
            return
        elif not crud.find_student_by_ci(ci):
            # Si no se encuentra el estudiante, mostrar error
            utils.show_error_message('Estudiante no encontrado.', self)
            return
        else:
            # Si se encuentra, almacenar su cédula en el componente
            self.estudiante_ci = ci
        # Verificar que se hayan ingresado materias para registrar
        materia_ids = self.materias_input.text().upper().strip()
        if not materia_ids:
            utils.show_error_message(
                'Ingrese materias para registrar sus calificaciones.', self)
            return
        # Buscar materias que no han sido cursadas por el estudiante
        por_cursar = [item['id_materia'] for item
                      in crud.find_subjects_not_taken_by_student(ci)]
        # Extraer las materias a registrar y conservar las que están en
        # la lista de materias por cursar del estudiante
        materia_ids = [m for m in split_list(materia_ids) if m in por_cursar]
        if materia_ids:
            # Si hay materias por registrar, extraer sus datos
            materias = crud.find_subjects(materia_ids)
            # Agregar campos de nota y período para crear registros parciales
            for m in materias:
                m.update({'nota': '', 'periodo': ''})
            # Guardar los registros parciales
            self.record_tbl_model.replace_record(materias)
        else:
            # Si no hay materias por registrar, mostrar error
            utils.show_error_message(
                'Ingrese materias que el estudiante '
                'no haya cursado anteriormente',
                self)
            return

    def _make_records(self):
        """Registra las nuevas calificaciones."""
        # Verifica que todos los campos estén llenos
        for r in self.record_tbl_model.record:
            if not r['nota'] or not r['periodo']:
                utils.show_error_message(
                    'Rellene todos los campos primero.', self)
                return
        # Crea los registros a almacenar
        record = []
        for r in self.record_tbl_model.record:
            record.append({'ci_estudiante': self.estudiante_ci,
                           'id_materia': r['id'],
                           'nota': r['nota'],
                           'periodo': r['periodo']})
        # Realiza el registro en la base de datos
        crud.create_records(record)
        # Vacía los campos y la tabla
        self.estudiante_ci = None
        self._clear_inputs()
        self.record_tbl_model.replace_record({})

    def _clear_inputs(self):
        self.estudiante_input.clear()
        self.materias_input.clear()
