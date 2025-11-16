from PyQt5.QtWidgets import QMessageBox
import pyodbc

from Diseño_Interfaces.login import LoginWindow
from Logica_Interfaces.Menu import MenuLogic

# conexión con SQL Server
def conectar_sql():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-33OLAEM\SQLEXPRESS;'
        'DATABASE=PruebaDB;'
        'Trusted_Connection=yes;'
    )

class LoginLogic(LoginWindow):
    def __init__(self):
        super().__init__()
        self.login_btn.clicked.connect(self.validar_login)

    def conectar_sql(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-33OLAEM\SQLEXPRESS;'
            'DATABASE=PruebaDB;'
            'Trusted_Connection=yes;'
        )
 
    def validar_login(self):
        numero_control = self.numero_control_input.text().strip()
        contraseña = self.contra_input.text().strip()

        if not numero_control or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Coloca algo no seas huevón")
            return

        try:
            conn = self.conectar_sql()
            cursor = conn.cursor()
            query = "SELECT * FROM Alumnos WHERE Num_control = ? AND Contraseña_hash = ?"
            cursor.execute(query, (numero_control, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                QMessageBox.information(self, "Acceso", f"Bienvenido, {resultado.Nombre}")
                self.close()
                self.dashboard = MenuLogic(numero_control)
                self.dashboard.show()
                
            else:
                QMessageBox.critical(self, "Sujeto no identificado", "Invasor!!!!")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Se tropezó la conexión, sorry vuelva mañana", str(e))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = LoginLogic()
    ventana.show()
    sys.exit(app.exec_())
