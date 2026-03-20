from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QFont, QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QRegion
from PyQt5.QtCore import Qt

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(700, 400)
        self.drag_position = None

        # Botón cerrar
        self.cerrar_btn = QPushButton("✕", self)
        self.cerrar_btn.setGeometry(self.width() - 35, 10, 25, 25)
        self.cerrar_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 18px;
                border: none;
            }
        """)
        self.cerrar_btn.clicked.connect(self.close)

        # Fuentes
        self.fuente_general = QFont("Segoe UI", 10)
        self.fuente_titulo = QFont("Segoe UI", 14, QFont.Bold)

        # Etiquetas de datos
        self.label_linea1 = QLabel()  # Nombre
        self.label_linea2 = QLabel()  # Número de control
        self.label_linea3 = QLabel()  # Carrera y semestre
        self.label_linea4 = QLabel()  # Estatus

        for lbl in [self.label_linea1, self.label_linea2, self.label_linea3, self.label_linea4]:
            lbl.setFont(self.fuente_general)
            lbl.setTextFormat(Qt.RichText)
            lbl.setStyleSheet("color: #003366; font-size: 13px;")

        # Layout de datos
        self.datos_layout = QVBoxLayout()
        self.datos_layout.setSpacing(2)
        self.datos_layout.addWidget(self.label_linea1)
        self.datos_layout.addWidget(self.label_linea2)
        self.datos_layout.addSpacing(5)
        self.datos_layout.addWidget(self.label_linea4)
        self.datos_layout.addWidget(self.label_linea3)

        # Tarjeta de identificación
        self.tarjeta = QFrame()
        self.tarjeta.setStyleSheet("background-color: white; border-radius: 12px;")
        self.tarjeta.setFixedHeight(250)
        self.tarjeta_layout = QHBoxLayout()
        self.tarjeta.setLayout(self.tarjeta_layout)

        # Foto
        self.label_foto = QLabel()
        self.label_foto.setFixedSize(120, 120)
        self.label_foto.setStyleSheet("border: 1px solid #ccc; border-radius: 8px;")
        self.label_foto.setAlignment(Qt.AlignCenter)

        self.tarjeta_layout.addWidget(self.label_foto)
        self.tarjeta_layout.addLayout(self.datos_layout)

        self.init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#ffffff"))
        gradient.setColorAt(0.4, QColor("#a3d5ff"))
        gradient.setColorAt(1.0, QColor("#3399ff"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = path.toFillPolygon().toPolygon()
        self.setMask(QRegion(region))
        self.cerrar_btn.setGeometry(self.width() - 35, 10, 25, 25)
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        super().mouseReleaseEvent(event)

    def init_ui(self):
        layout_principal = QHBoxLayout(self)

        # Panel lateral
        panel_lateral = QVBoxLayout()
        panel_lateral.setSpacing(20)

        # Botones del menú lateral
        self.btn_inicio = QPushButton("Inicio")
        self.btn_kardex = QPushButton("Kárdex")
        self.btn_materias = QPushButton("Carga de Materias")  # ← Este es el botón que usarás en MenuLogic
        self.btn_horario = QPushButton("Horario")

        for btn in [self.btn_inicio, self.btn_kardex, self.btn_materias, self.btn_horario]:
            btn.setFont(self.fuente_general)
            btn.setFixedWidth(180)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #003366;
                    font-weight: bold;
                    border: 1px solid #99ccff;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #cce6ff;
                }
            """)

        panel_lateral.addStretch()
        panel_lateral.addWidget(self.btn_inicio)
        panel_lateral.addWidget(self.btn_kardex)
        panel_lateral.addWidget(self.btn_materias)
        panel_lateral.addWidget(self.btn_horario)
        panel_lateral.addStretch()

        # Panel central
        panel_central = QVBoxLayout()
        panel_central.addSpacing(20)

        titulo_identificacion = QLabel("<b>Identificación</b>")
        titulo_identificacion.setFont(self.fuente_titulo)
        titulo_identificacion.setStyleSheet("color: #003366;")
        panel_central.addWidget(titulo_identificacion, alignment=Qt.AlignLeft)
        panel_central.addWidget(self.tarjeta)
        panel_central.addStretch()

        layout_principal.addLayout(panel_lateral)
        layout_principal.addLayout(panel_central)
