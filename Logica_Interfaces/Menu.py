from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QComboBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import pyodbc
import os

from Diseño_Interfaces.Menu import Menu

class MenuLogic(Menu):
    def __init__(self, num_control):
        super().__init__()
        self.num_control = num_control
        self.cargar_datos_alumno()

    def conectar_sql(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-33OLAEM\SQLEXPRESS;'
            'DATABASE=PruebaDB;'
            'Trusted_Connection=yes;'
        )

    def cargar_datos_alumno(self):
        try:
            conn = self.conectar_sql()
            cursor = conn.cursor()
            query = "SELECT Nombre, Semestre, Carrera, Foto FROM Alumnos WHERE Num_control = ?"
            cursor.execute(query, (self.num_control,))
            resultado = cursor.fetchone()

            if resultado:
                nombre, semestre, carrera, foto = resultado

                # Formato visual solicitado
                self.label_linea1.setText(f"<b>Nombre:</b> {nombre}")
                self.label_linea2.setText(f"<b>Número de Control:</b> {self.num_control}")
                self.label_linea3.setText(
                    f"<b>Carrera:</b> {carrera} &nbsp;&nbsp; "
                    f"<b>Semestre:</b> {semestre} &nbsp;&nbsp; "
                )
                self.label_linea4.setText("<b>Estatus:</b> VIGENTE")

                # Foto
                if foto:
                    ruta_base = os.path.dirname(os.path.abspath(__file__))
                    ruta_img = os.path.join(ruta_base, "..", foto)
                    if os.path.exists(ruta_img):
                        pixmap = QPixmap(ruta_img).scaled(120, 120)
                        self.label_foto.setPixmap(pixmap)
                    else:
                        self.label_foto.setText("Foto perdida en la inmensidad del universo")
            else:
                self.label_linea1.setText("Alumno no existente, fallo en la matrix?")
                self.label_linea2.clear()
                self.label_linea3.clear()

            cursor.close()
            conn.close()

        except Exception as e:
            self.label_linea1.setText("Error al cargar datos")
            self.label_linea2.setText(str(e))
            self.label_linea3.clear()
