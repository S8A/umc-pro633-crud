import PyQt5.QtWidgets as qtw
import textwrap as tw


def create_label(s, wrap=True):
    """Crea un QLabel con el texto dado."""
    l = qtw.QLabel(s)
    l.setWordWrap(wrap)
    return l

def create_label_h1(s, wrap=True):
    """Crea un encabezado de primer nivel."""
    return create_label(f'<h1 style="text-align: center;">{s}</h1>', wrap)

def create_label_h2(s, wrap=True):
    """Crea un encabezado de segundo nivel."""
    return create_label(f'<h2>{s}</h2>', wrap)

def create_label_h3(s, wrap=True):
    """Crea un encabezado de tercer nivel."""
    return create_label(f'<h3>{s}</h3>', wrap)

# TEMPORAL: Código duplicado y adaptado de umc_crud
def create_text_table(data, cols=None, widths=None):
    """Crea una tabla con los datos dados."""
    result = ''
    if not data:
        # Si no hay datos, no hay nada que mostrar
        result = 'ERROR: Tabla vacía'
    else:
        if cols is None:
            # Si no se proveen nombres de columna manualmente,
            # usar los de los datos
            cols = {c: c for c in data[0].keys()}
        if widths is None:
            # Si no se proveen anchos de columna manualmente,
            # calcularlos a partir de los nombres de columna
            widths = {c: (4*ceil(len(cols[c])/4) + 4) for c in cols.keys()}
        # Mostrar cabecera de la tabla
        result += ' '.join([f'{tw.shorten(str(cols[col]), width=w) :<{w}}'
                            for col, w in widths.items()])
        # Mostrar barra separadora decorativa
        result += '+'.join(['-'*w for w in widths.values()])
        # Mostrar datos de la tabla
        for row in data:
            result += ' '.join([f'{tw.shorten(str(row[col]), width=w) :<{w}}'
                                for col, w in widths.items()])
    return result

def create_text_record(record):
    """Crea una tabla de récords académicos a partir de los datos dados."""
    cols = {'id': 'Código',
            'nombre': 'Materia',
            'uc': 'UC',
            'nota': 'Nota',
            'periodo': 'Período'}
    widths = dict(zip(cols.keys(), [10, 45, 5, 5, 10]))
    return create_text_table(record, cols, widths)
