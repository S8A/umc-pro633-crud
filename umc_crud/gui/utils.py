import PyQt5.QtWidgets as qtw


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
