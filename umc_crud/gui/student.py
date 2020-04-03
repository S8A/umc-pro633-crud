# coding=utf-8
"""Módulo de estudiante.

Mediante este módulo los usuarios de la base de datos que sean
estudiantes pueden consultar su información personal, récord
académico e índices académicos.

La ejecución del módulo debe empezar con la ventana principal
del módulo (MainWindow), ya que esta provee acceso a los demás
componentes y funciones del módulo.
"""


import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
from .. import crud
from ..io import split_list, validate_period
from ..student import calculate_ia
from . import utils


class MainWindow(qtw.QMainWindow):
    """Ventana principal del módulo de estudiante."""

    def __init__(self, user_id, parent=None):
        """Inicializa el módulo de estudiante con el usuario dado."""
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
        self.options = [
            ['Consultar información personal', self._get_personal_info],
            ['Consultar récord académico', self._get_record],
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
        """Crea el componente de consulta de información personal."""
        self.setCentralWidget(StudentInfoWidget(student=self.estudiante))
        self.resize(400, 300)

    def _get_record(self):
        """Crea el componente de consulta del récord académico."""
        self.setCentralWidget(StudentRecordWidget(student=self.estudiante))
        self.resize(700, 600)


class StudentInfoWidget(qtw.QWidget):
    """Componente de consulta de información personal."""

    def __init__(self, student=None, parent=None):
        """Inicializa el componente de consulta de información personal."""
        super().__init__(parent)
        self.estudiante = student
        # Si no se provee un estudiante, significa que el
        # componente se usará en modo de administrador
        self.admin_mode = self.estudiante is None
        # Inicializa la interfaz gráfica
        self._create_ui()
        if not self.admin_mode:
            self._get_personal_info()

    def _create_ui(self):
        """Crea la interfaz gráfica del componente."""
        # Estructura
        layout = qtw.QVBoxLayout()
        # Cabecera
        layout.addWidget(utils.create_label_h1('Información personal'))
        # Formulario de consulta (modo de administrador solamente)
        if self.admin_mode:
            form_layout = qtw.QFormLayout()
            # Campo de cédula del estudiante
            self.estudiante_input = qtw.QLineEdit()
            form_layout.addRow('Estudiante (C.I.)', self.estudiante_input)
            layout.addLayout(form_layout)
            # Botón de consulta
            consultar_btn = qtw.QPushButton('Consultar')
            consultar_btn.clicked.connect(self._get_personal_info)
            layout.addWidget(consultar_btn)
        # Contenido
        self.output_text = qtw.QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text, stretch=1)
        self.setLayout(layout)

    def _get_personal_info(self):
        """Consulta la información personal del estudiante dado."""
        # Datos de salida
        output = []
        # Si se está en modo de administrador, se deben extraer los
        # datos del estudiante a partir del formulario de consulta
        if self.admin_mode:
            # Extraer la cédula ingresada
            ci = self.estudiante_input.text().strip()
            if not ci:
                # Si no se ingresó ninguna cédula, mostrar error
                utils.show_error_message('Ingrese un número de cédula.', self)
                return
            # Buscar el estudiante por su cédula
            self.estudiante = crud.find_student_by_ci(ci)
            if not self.estudiante:
                # Si no se encuentra el estudiante, mostrar error
                utils.show_error_message('Estudiante no encontrado.', self)
                return
        # Agregar información a los datos de salida
        output.append(
            f'<b>Nombre y apellido:</b> {self.estudiante["nombre"]} '
            f'{self.estudiante["apellido"]}')
        output.append(f'<b>C.I.:</b> {self.estudiante["ci"]}')
        output.append(f'<b>Teléfono:</b> {self.estudiante["telefono"]}')
        output.append(f'<b>Dirección:</b> {self.estudiante["direccion"]}')
        carrera = crud.read_career_info(self.estudiante['id_carrera'])
        output.append(f'<b>Carrera:</b> {carrera["nombre"]} ({carrera["id"]})')
        mencion = carrera["mencion"]
        if mencion is not None:
            output.append(f'<b>Mención:</b> {mencion}')
        # Mostrar información
        self.output_text.setHtml('<br>'.join(output))


class StudentRecordWidget(qtw.QWidget):
    """Componente de consulta de récord académico."""

    def __init__(self, student=None, parent=None):
        """Inicializa el componente de consulta de récord académico."""
        super().__init__(parent)
        self.estudiante = student
        # Si no se provee un estudiante, significa que el
        # componente se usará en modo de administrador
        self.admin_mode = self.estudiante is None
        # Inicializa la interfaz gráfica
        self._create_ui()
        if not self.admin_mode:
            self._get_record()

    def _create_ui(self):
        """Crea la interfaz gráfica del componente."""
        # Estructura
        main_layout = qtw.QVBoxLayout()
        # Cabecera
        main_layout.addWidget(utils.create_label_h1('Récord académico'))
        # Formulario de consulta
        form_layout = qtw.QFormLayout()
        if self.admin_mode:
            # Si se está en modo de administrador, se necesita
            # un campo para la cédula del estudiante
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
        consultar_btn.clicked.connect(self._get_record)
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
        self.record_tbl_model = RecordTableModel(self.record_headers)
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
        self.uc_cursadas = utils.create_label('Materias cursadas:')
        main_layout.addWidget(self.uc_cursadas)
        self.uc_aprobadas = utils.create_label('Materias aprobadas:')
        main_layout.addWidget(self.uc_aprobadas)
        self.indice_academico = utils.create_label('Índice Académico (IA):')
        main_layout.addWidget(self.indice_academico)
        self.setLayout(main_layout)

    def _get_record(self):
        """Consulta el récord académico con los datos ingresados."""
        # Si se está en modo de administrador, se deben extraer los
        # datos del estudiante a partir del formulario de consulta
        if self.admin_mode:
            # Extraer la cédula ingresada
            ci = self.estudiante_input.text().strip()
            if not ci:
                # Si no se ingresó ninguna cédula, mostrar error
                utils.show_error_message('Ingrese un número de cédula.', self)
                return
            # Buscar el estudiante por su cédula
            self.estudiante = crud.find_student_by_ci(ci)
            if not self.estudiante:
                # Si no se encuentra el estudiante, mostrar error
                utils.show_error_message('Estudiante no encontrado.', self)
                return
        # Extraer las materias ingresadas
        materia_ids = split_list(self.materias_input.text().strip())
        # Filtrar elementos vacíos
        materia_ids = [m for m in materia_ids if m]
        if not materia_ids:
            materia_ids = None
        # Extraer y comprobar el período ingresado
        periodo = self.periodo_input.text().upper().strip()
        if not periodo:
            periodo = None
        elif not validate_period(periodo):
            utils.show_error_message(
                ('Ingrese un período académico válido. '
                 'Ejemplos: 2018-02, 2019-IN, 2020-01'),
                self)
            return
        # Buscar el récord académico con los datos obtenidos
        record = crud.read_records(self.estudiante['ci'],
                                   materia_ids,
                                   periodo)
        # Realizar el reemplazo de los datos
        self.record_tbl_model.replace_record(record)
        # Actualizar la información adicional
        self._update_record_info()

    def _update_record_info(self):
        """Actualiza la información adicional del récord académico."""
        # Extraer las UC de las materias cursadas
        uc_cursadas = [r['uc'] for r in self.record_tbl_model.record]
        # Mostrar el número de materias cursadas y su total de UC
        self.uc_cursadas.setText(
            f'Materias cursadas: {len(uc_cursadas)} ({sum(uc_cursadas)} UC)')
        # Extraer las UC de las materias aprobadas
        uc_aprobadas = [r['uc'] for r in self.record_tbl_model.record
                        if r['nota'] >= 12]
        # Mostrar el número de materias aprobadas y su total de UC
        self.uc_aprobadas.setText(
            f'Materias aprobadas: {len(uc_aprobadas)} '
            f'({sum(uc_aprobadas)} UC)')
        # Mostrar el índice académico del registro dado
        ia = calculate_ia(self.record_tbl_model.record) or "N/A"
        self.indice_academico.setText(f'Índice Académico (IA): {ia}')


class RecordTableModel(qtc.QAbstractTableModel):
    """Modelo interno para tablas de récords académicos."""

    def __init__(self, header, record=None, editable=False, parent=None):
        """Inicializa el modelo de tabla con el récord y cabecera dados."""
        super().__init__(parent)
        self.record = record or []
        self.header = header
        self.editable = ['nota', 'periodo'] if editable else []

    def flags(self, index):
        """Provee las propiedades (flags) del índice dado."""
        col = self._header_column(index.column())
        flags = qtc.QAbstractTableModel.flags(self, index)
        if col in self.editable:
            # Indicar si la columna es editable
            return flags | qtc.Qt.ItemIsEditable
        else:
            # De lo contrario, devolver las flags predeterminadas
            return flags

    def data(self, index, role):
        """Provee los datos del récord en el índice y rol dado."""
        row = index.row()
        col = self._header_column(index.column())
        if role == qtc.Qt.DisplayRole:
            # Mostrar los datos del índice dado
            return self.record[row][col]
        if col in self.editable and role == qtc.Qt.EditRole:
            # Si la columna es editable, devolver el dato existente
            return self.record[row][col]

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
                col = self._header_column(section)
                return str(self.header[col])

    def setData(self, index, value, role):
        """Realiza la edición de datos de la tabla."""
        row = index.row()
        col = self._header_column(index.column())
        if col in self.editable and role == qtc.Qt.EditRole:
            # Si se permite editar en la columna actual
            if col == 'nota':
                # Si se edita en la columna de la nota
                try:
                    # Tratar de convertir el valor ingresado a entero
                    nota = int(value)
                    if nota in range(21):
                        # Si la nota ingresada está entre 0 y 20,
                        # registrar el nuevo valor
                        self.record[row][col] = value
                        self.dataChanged.emit(index, index)
                        # Cambio exitoso
                        return True
                except ValueError:
                    # Si no se puede convertir a entero,
                    # la entrada es inválida. Cambio fallido.
                    return False
            elif col == 'periodo':
                # Si se edita en la columna del período académico
                if validate_period(value):
                    # Si el valor ingresado es un período válido,
                    # registrar el nuevo valor
                    self.record[row][col] = value
                    self.dataChanged.emit(index, index)
                    # Cambio exitoso
                    return True
        # Si no se cumplen las condiciones, el cambio no fue exitoso
        return False

    def _header_column(self, i):
        """Obtiene el nombre de la columna a partir de su número."""
        return list(self.header.keys())[i]

    def replace_record(self, record):
        """Reemplaza los registros de la tabla."""
        self.beginResetModel()
        self.record = record
        self.endResetModel()
