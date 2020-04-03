import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
from .. import crud
from ..io import read_csv, split_list, validate_period
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
        self.setCentralWidget(RecordLoaderWidget())
        self.resize(700, 700)

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
                m.update({'nota': 0, 'periodo': ''})
            # Guardar los registros parciales
            self.record_tbl_model.replace_record(materias)
        else:
            # Si no hay materias por registrar, mostrar error
            error = ('Ingrese materias que el estudiante '
                     'no haya cursado anteriormente')
            utils.show_error_message(error, self)
            return

    def _make_records(self):
        """Registra las nuevas calificaciones."""
        # Verificar que todos los campos estén llenos
        for r in self.record_tbl_model.record:
            if not r['nota'] or not r['periodo']:
                utils.show_error_message('No puede haber campos vacíos.', self)
                return
        # Crear los registros a almacenar
        record = []
        for r in self.record_tbl_model.record:
            record.append({'ci_estudiante': self.estudiante_ci,
                           'id_materia': r['id'],
                           'nota': r['nota'],
                           'periodo': r['periodo']})
        # Realizar el registro en la base de datos
        crud.create_records(record)
        # Vaciar los campos y la tabla
        self.estudiante_ci = None
        self.estudiante_input.clear()
        self.materias_input.clear()
        self.record_tbl_model.replace_record([])


class RecordLoaderWidget(qtw.QWidget):
    """Componente de carga de calificaciones a partir de archivos CSV."""

    def __init__(self, parent=None):
        """Inicializa el componente de carga de calificaciones."""
        super().__init__(parent)
        # Inicializa la interfaz gráfica
        self._create_ui()

    def _create_ui(self):
        """Crea la interfaz gráfica del componente."""
        # Estructura
        main_layout = qtw.QVBoxLayout()
        # Cabecera
        main_layout.addWidget(utils.create_label_h1('Carga de calificaciones'))
        # Formulario
        form_layout = qtw.QFormLayout()
        # Campo de nombre de archivo
        self.archivo = qtw.QLineEdit()
        self.archivo.setReadOnly(True)
        form_layout.addRow('Archivo CSV', self.archivo)
        main_layout.addLayout(form_layout)
        # Botón de cargar archivo
        cargar_btn = qtw.QPushButton('Cargar archivo')
        cargar_btn.clicked.connect(self._load_csv_records)
        main_layout.addWidget(cargar_btn)
        # Tabla de datos
        self.record_tbl = qtw.QTableView()
        # Encabezados de la tabla
        self.record_headers = {'ci': 'Cédula',
                               'estudiante': 'Nombre del estudiante',
                               'id': 'Código',
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
            if header in ['estudiante', 'nombre']:
                # Excepto las columnas de nombres, que se expanden
                resize_mode = qtw.QHeaderView.Stretch
            self.record_tbl_header.setSectionResizeMode(i, resize_mode)
        main_layout.addWidget(self.record_tbl, stretch=2)
        # Botón de registro de calificaciones
        registrar_btn = qtw.QPushButton('Registrar')
        registrar_btn.clicked.connect(self._make_records)
        main_layout.addWidget(registrar_btn)
        self.setLayout(main_layout)

    def _load_csv_records(self):
        """Carga los datos de las calificaciones a registrar."""
        # Diálogo de apertura de archivo
        dialogo_archivo = qtw.QFileDialog()
        # Solicitar archivo CSV al usuario
        archivo = dialogo_archivo.getOpenFileName(
            self, caption='Abrir archivo de registros', filter='*.csv')[0]
        self.archivo.setText(archivo)
        # Extraer contenido del CSV
        csv = read_csv(archivo)
        # Filtrar las filas que no tengan el número correcto de campos
        csv = list(filter(lambda row: len(row) == 4, read_csv(archivo)))
        if not csv:
            # Si no quedan filas, mostrar error
            error = ('El archivo CSV seleccionado no posee contenido o '
                     'no tiene el número adecuado de filas. Los archivos '
                     'de registro de calificaciones deben consistir de '
                     'cuatro columnas: número de cédula del estudiante, '
                     'código de materia, la calificación obtenida, y el '
                     'período en que se cursó.')
            utils.show_error_message(error, self)
            return
        # Diccionario de datos a registrar
        por_registrar = {}
        # Diccionario de materias por cursar de cada estudiante en el CSV
        por_cursar = {}
        # Para cada fila
        for fila in csv:
            # Crear un registro
            record = {'ci': fila[0],
                 'estudiante': '',
                 'id': fila[1],
                 'nombre': '',
                 'uc': '',
                 'nota': fila[2],
                 'periodo': fila[3]}
            # Identificadores
            ci = record['ci']
            materia_id = record['id']
            # Verificar que la calificación sea un número entero
            try:
                # Trata de convertir la calificación a entero
                record['nota'] = int(record['nota'])
            except ValueError:
                # Si no se puede, el registro es inválido. Pasar al siguiente
                continue
            # Verificar que el período académico del registro sea válido
            if not validate_period(record['periodo']):
                # Si no es válido, pasar al siguiente registro
                continue
            # Buscar las materias que no han sido cursadas por el estudiante de
            # la cédula dada. Si no existe ningún estudiante con dicha cédula,
            # el resultado será un tuple vacío
            if ci not in por_cursar.keys():
                mpc = crud.find_subjects_not_taken_by_student(ci)
                por_cursar[ci] = [item['id_materia'] for item in mpc]
            # Verificar que la materia esté en la lista de materias por
            # cursar del estudiante
            if materia_id in por_cursar[ci]:
                # Si la materia no ha sido cursada por el estudiante,
                # se busca la información faltante
                estudiante = crud.find_student_by_ci(ci)
                record['estudiante'] = ' '.join([estudiante["nombre"],
                                            estudiante["apellido"]])
                materia = crud.find_subject(materia_id)
                record['nombre'] = materia['nombre']
                record['uc'] = materia['uc']
                # Se agregan los datos a la lista de registros por crear.
                # Si esta combinación de materia y estudiante ya estaba en
                # la lista, será reemplazada por este nuevo registro.
                por_registrar[(ci, materia_id)] = record
        # Convertir el diccionario de datos a lista
        por_registrar = list(por_registrar.values())
        if por_registrar:
            # Si hay datos por registrar, mostrarlos en la tabla
            self.record_tbl_model.replace_record(por_registrar)
        else:
            # Si no hay datos por registrar, mostrar error
            utils.show_error_message(
                'No se registrarán nuevos datos.', self)
            return

    def _make_records(self):
        """Registra las nuevas calificaciones."""
        # Verificar que todos los campos estén llenos
        for r in self.record_tbl_model.record:
            if not r['nota'] or not r['periodo']:
                utils.show_error_message('No puede haber campos vacíos.', self)
                return
        # Crear los registros a almacenar
        record = []
        for r in self.record_tbl_model.record:
            record.append({'ci_estudiante': r['ci'],
                           'id_materia': r['id'],
                           'nota': r['nota'],
                           'periodo': r['periodo']})
        # Realizar el registro en la base de datos
        crud.create_records(record)
        # Vacía los campos y la tabla
        self.archivo.clear()
        self.record_tbl_model.replace_record({})
