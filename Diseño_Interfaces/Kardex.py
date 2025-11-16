from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QDialog
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QRegion
from PyQt5.QtCore import Qt
from Logica_Interfaces.Kardex import obtener_materias_plan, obtener_estatus_materias, volver_inicio

class InfoMateriaPopup(QDialog):
    def __init__(self, serie, nombre, creditos, estado, calificacion):
        super().__init__()
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(240, 240, 240, 220);
            border: 2px solid #999;
            border-radius: 12px;
        """)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        texto = f"""
        <b>Materia:</b> {nombre}<br>
        <b>Serie:</b> {serie}<br>
        <b>Créditos:</b> {creditos}<br>
        <b>Estatus:</b> {estado}
        """
        if estado in ["APROBADA", "REPROBADA"] and calificacion is not None:
            texto += f"<br><b>Calificación:</b> {calificacion}"

        etiqueta = QLabel(texto)
        etiqueta.setTextFormat(Qt.RichText)
        etiqueta.setAlignment(Qt.AlignLeft)
        layout.addWidget(etiqueta)

class Kardex(QWidget):
    def __init__(self, num_control):
        super().__init__()
        self.num_control = num_control
        self.setWindowTitle("Kárdex")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1100, 700)
        self.drag_position = None

        self.cerrar_btn = QPushButton("✕", self)
        self.cerrar_btn.setGeometry(self.width() - 35, 10, 25, 25)
        self.cerrar_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                color: black;
            }
        """)
        self.cerrar_btn.clicked.connect(self.close)

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

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def mostrar_popup(self, event, serie, nombre, creditos, estado, calificacion):
        popup = InfoMateriaPopup(serie, nombre, creditos, estado, calificacion)
        popup.move(event.globalPos())
        popup.exec_()

    def init_ui(self):
        fuente_general = QFont("Segoe UI", 10)
        layout_principal = QHBoxLayout(self)

        panel_lateral = QVBoxLayout()
        panel_lateral.setSpacing(20)
        panel_lateral.addStretch()

        botones = {
            "Inicio": QPushButton("Inicio"),
            "Kárdex": QPushButton("Kárdex"),
            "Carga de Materias": QPushButton("Carga de Materias"),
            "Horario": QPushButton("Horario")
        }
        botones["Inicio"].clicked.connect(lambda: volver_inicio(self))

        for btn in botones.values():
            btn.setFont(fuente_general)
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
            panel_lateral.addWidget(btn, alignment=Qt.AlignHCenter)
        
        panel_lateral.addStretch()

        panel_central = QVBoxLayout()
        panel_central.setSpacing(20)
        panel_central.addSpacing(40)

        materias = obtener_materias_plan()
        estatus = obtener_estatus_materias(self.num_control)

        colores = {
            "APROBADA": "#a8e6cf",
            "CURSANDO": "#fff59d",
            "REPROBADA": "#ff8a80",
            "NO CURSADA": "#e0e0e0"
        }

        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)

        for sem in range(1, 9):
            titulo = QLabel(f"<b>Semestre {sem}</b>")
            titulo.setAlignment(Qt.AlignCenter)
            titulo.setFont(fuente_general)
            grid.addWidget(titulo, 0, sem - 1)

        contador_filas = {sem: 1 for sem in range(1, 9)}

        for serie, nombre_mat, semestre, creditos in materias:
            estado, calificacion = estatus.get(serie, ("NO CURSADA", None))
            estado = estado.upper()
            color = colores.get(estado, "#e0e0e0")

            cuadro = QFrame()
            cuadro.setStyleSheet(f"background-color: {color}; border-radius: 6px; padding: 6px;")
            cuadro_layout = QVBoxLayout()

            texto = f"<b>{serie}</b><br>{nombre_mat}<br><i>{creditos} créditos</i>"
            if estado in ["APROBADA", "REPROBADA"] and calificacion is not None:
                texto += f"<br><b>Calificación:</b> {calificacion}"

            etiqueta = QLabel(texto)
            etiqueta.setTextFormat(Qt.RichText)
            etiqueta.setAlignment(Qt.AlignCenter)
            etiqueta.setFont(fuente_general)
            cuadro_layout.addWidget(etiqueta)
            cuadro.setLayout(cuadro_layout)

            cuadro.mousePressEvent = lambda event, s=serie, n=nombre_mat, c=creditos, e=estado, cal=calificacion: self.mostrar_popup(event, s, n, c, e, cal)

            if semestre in contador_filas:
                fila = contador_filas[semestre]
                columna = semestre - 1
                grid.addWidget(cuadro, fila, columna)
                contador_filas[semestre] += 1

        panel_central.addLayout(grid)
        layout_principal.addLayout(panel_lateral)
        layout_principal.addLayout(panel_central)
        self.setLayout(layout_principal)
