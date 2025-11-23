from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pyodbc
import os
from Logica_Interfaces.LogicaCargaMaterias import CargaMateriasLogic as CargaMaterias
from Diseño_Interfaces.Menu import Menu
from Diseño_Interfaces.Kardex import Kardex


class MenuLogic(Menu):
    def __init__(self, num_control):
        super().__init__()
        self.num_control = num_control
        self.semestre_alumn = None  

        # Cargar datos del alumno 
        self.cargar_datos_alumno()

        self.btn_kardex.clicked.connect(self.abrir_kardex)
        self.btn_materias.clicked.connect(self.abrir_carga_materias)

    # Navegación 
    def abrir_kardex(self):
        self.ventana_kardex = Kardex(self.num_control)
        self.ventana_kardex.show()
        self.close()

    def abrir_carga_materias(self):
        self.carga_window = CargaMaterias(self.num_control)  
        self.carga_window.show()
        self.close()

    # Conexión SQL
    def conectar_sql(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-33OLAEM\\SQLEXPRESS;'
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
                self.semestre_alumn = semestre

                # Etiquetas
                self.label_linea1.setText(f"<b>Nombre:</b> {nombre}")
                self.label_linea2.setText(f"<b>Número de Control:</b> {self.num_control}")
                self.label_linea3.setText(
                    f"<b>Carrera:</b> {carrera} &nbsp;&nbsp; "
                    f"<b>Semestre:</b> {semestre} &nbsp;&nbsp; "
                )
                self.label_linea4.setText("<b>Estatus:</b> VIGENTE")

                if foto:
                    ruta_base = os.path.dirname(os.path.abspath(__file__))
                    ruta_img = os.path.join(ruta_base, "..", foto) 
                    if os.path.exists(ruta_img):
                        pixmap = QPixmap(ruta_img).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.label_foto.setPixmap(pixmap)
                    else:
                        self.label_foto.setText("Foto perdida en la inmensidad del universo")
                else:
                    self.label_foto.setText("Sin foto")
            else:
                self.label_linea1.setText("Alumno no existente, fallo en la matrix?")
                self.label_linea2.clear()
                self.label_linea3.clear()
                self.label_linea4.clear()

            cursor.close()
            conn.close()

        except Exception as e:
            self.label_linea1.setText("Se tropezó la conexión, sorry vuelva mañana")
            self.label_linea2.setText(str(e))
            self.label_linea3.clear()
            self.label_linea4.clear()