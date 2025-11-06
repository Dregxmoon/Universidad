from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QFrame
)

from PyQt5.QtGui import (
    QFont, QIcon, QPainter, QLinearGradient, QColor, QBrush,
    QPainterPath, QRegion
)
from PyQt5.QtCore import Qt
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(400, 500)
        self.drag_position = None
        self.init_ui()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#ffffff"))     # Blanco arriba
        gradient.setColorAt(0.4, QColor("#a3d5ff"))      # Azul claro centro
        gradient.setColorAt(1.0, QColor("#3399ff"))      # Azul intenso abajo
        painter.fillRect(self.rect(), QBrush(gradient))


    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = path.toFillPolygon().toPolygon()
        self.setMask(QRegion(region))
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
        fuente_titulo = QFont("Segoe UI", 20, QFont.Bold)
        fuente_texto = QFont("Segoe UI", 10)
        

        # Botón "X" 
        cerrar_btn = QPushButton("✕", self)
        cerrar_btn.setGeometry(self.width() - 35, 10, 25, 25)
        cerrar_btn.setStyleSheet("background-color: transparent; color: black; font-size: 16px; border: none;")
        cerrar_btn.clicked.connect(self.close)

        # Caja de login
        login_box = QFrame(self)
        login_box.setGeometry(50, 80, 300, 360)
        login_box.setStyleSheet("""
            QFrame {
                background-color: #cce 6ff;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(login_box)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        titulo = QLabel("UWU")
        titulo.setFont(fuente_titulo)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)
        layout.addWidget(linea)

        # Campo NUMRO DE CONTROL
        numero_control_label = QLabel("NUMERO DE CONTROL")
        numero_control_label.setFont(fuente_texto)
        layout.addWidget(numero_control_label)

        numero_control_input = QLineEdit()
        numero_control_input.setPlaceholderText("COLOCA TU NUMERO DE CONTROL")
        numero_control_input.setFont(fuente_texto)
        numero_control_input.setFixedHeight(40)
        numero_control_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 10px;
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(numero_control_input)

        # Campo CONTRASEÑA
        contra_label = QLabel("CONTRASEÑA")
        contra_label.setFont(fuente_texto)
        layout.addWidget(contra_label)

        contra_input = QLineEdit()
        contra_input.setPlaceholderText("COLOCA TU CONTRASEÑA")
        contra_input.setEchoMode(QLineEdit.Password)
        contra_input.setFont(fuente_texto)
        contra_input.setFixedHeight(40)
        contra_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 10px;
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(contra_input)

        # Botón Login
        login_btn = QPushButton("LOGIN")
        login_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        login_btn.setFixedHeight(45)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #00bcd4;
                color: white;
                border-radius: 10px;
                                
            }
            QPushButton:hover {
                background-color: #0097a7;
            }
        """)
        layout.addWidget(login_btn)
        self.numero_control_input = numero_control_input
        self.contra_input = contra_input
        self.login_btn = login_btn
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec_())
