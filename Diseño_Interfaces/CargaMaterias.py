from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QRegion
from PyQt5.QtCore import Qt


class CargaMaterias(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carga de Materias")
        self.setFixedSize(1300, 750)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_position = None

        # Botón cerrar
        self.cerrar_btn = QPushButton("✕", self)
        self.cerrar_btn.setStyleSheet(
            "background: transparent; color: black; font-size: 18px; border: none;"
        )
        self.cerrar_btn.clicked.connect(self.close)

        self.init_ui()

    # ====================== DISEÑO GENERAL ======================
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#ffffff"))
        gradient.setColorAt(0.4, QColor("#a3d5ff"))
        gradient.setColorAt(1.0, QColor("#3399ff"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 25, 25)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))
        self.cerrar_btn.setGeometry(self.width() - 40, 10, 30, 30)
        super().resizeEvent(event)

    # Movimiento ventana
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Panel izquierdo
        panel_izq = QVBoxLayout()

        titulo_izq = QLabel("<b>MATERIAS DISPONIBLES</b>")
        titulo_izq.setStyleSheet("color: #003366; font-size: 16px; margin-bottom: 10px;")
        panel_izq.addWidget(titulo_izq)

        # materias
        self.tree_materias = QTreeWidget()
        self.tree_materias.setHeaderHidden(True)
        self.tree_materias.setStyleSheet("""
            QTreeWidget { background: white; border-radius: 10px; }
            QTreeWidget::item { padding: 6px; }
        """)
        panel_izq.addWidget(self.tree_materias)

        botones_layout = QHBoxLayout()

        # LIMPIAR SELECCIÓN
        self.btn_limpiar = QPushButton("Limpiar selección")
        self.btn_limpiar.setStyleSheet(
            "background:#03A9F4; color:white; padding:10px; border-radius:8px; font-weight:bold;"
        )

        # ELIMINAR CARGA REGISTRADA
        self.btn_eliminar_carga = QPushButton("Eliminar carga registrada")
        self.btn_eliminar_carga.setStyleSheet(
            "background:#F44336; color:white; padding:10px; border-radius:8px; font-weight:bold;"
        )

        # FINALIZAR CARGA
        self.btn_finalizar = QPushButton("FINALIZAR CARGA")
        self.btn_finalizar.setStyleSheet(
            "background:#4caf50; color:white; padding:12px; border-radius:10px; font-weight:bold;"
        )

        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addWidget(self.btn_eliminar_carga)
        botones_layout.addWidget(self.btn_finalizar)

        panel_izq.addLayout(botones_layout)

        # ================= PANEL DERECHO =================
        panel_der = QVBoxLayout()

        titulo_der = QLabel("<b>TU HORARIO</b>")
        titulo_der.setStyleSheet("color: #003366; font-size: 16px; margin-bottom: 10px;")
        panel_der.addWidget(titulo_der)

        # Tabla del horario
        self.tabla_horario = QTableWidget(15, 6)
        self.tabla_horario.setHorizontalHeaderLabels(
            ["HORA", "LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
        )
        self.tabla_horario.verticalHeader().setVisible(False)
        self.tabla_horario.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_horario.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_horario.setSelectionMode(QTableWidget.NoSelection)
        self.tabla_horario.setStyleSheet("background: white; gridline-color: #ddd;")

        horas = [f"{h:02d}:00 - {h+1:02d}:00" for h in range(7, 22)]
        for i, hora in enumerate(horas):
            item = QTableWidgetItem(hora)
            item.setBackground(QColor("#e3f2fd"))
            item.setFlags(Qt.ItemIsEnabled)
            self.tabla_horario.setItem(i, 0, item)

        panel_der.addWidget(self.tabla_horario)

        layout.addLayout(panel_izq, stretch=1)
        layout.addLayout(panel_der, stretch=2)

        self.setLayout(layout)
