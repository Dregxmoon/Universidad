from PyQt5.QtWidgets import QMessageBox
import pyodbc

from Diseño_Interfaces.login import LoginWindow

# Función para conectar a SQL Server
def conectar_sql():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-EMDLNML\\SQLEXPRESS;'
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
            'SERVER=DESKTOP-EMDLNML\\SQLEXPRESS;'
            'DATABASE=PruebaDB;'
            'Trusted_Connection=yes;'
        )

    def validar_login(self):
        numero_control = self.numero_control_input.text().strip()
        contraseña = self.contra_input.text().strip()


        if not numero_control or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, completa ambos campos.")
            return

        try:
            conn = self.conectar_sql()
            cursor = conn.cursor()
            query = "SELECT * FROM USUARIOS WHERE NUMERO_CONTROL = ? AND CONTRASEÑA = ?"
            cursor.execute(query, (numero_control, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                QMessageBox.information(self, "Acceso", f"Bienvenido,  {numero_control}")
            else:
                QMessageBox.critical(self, "Sujeto no identificado", "Invasor!!!!")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Se tropezo la conexion sorry vuelva mañana", str(e))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = LoginLogic()
    ventana.show()
    sys.exit(app.exec_())

