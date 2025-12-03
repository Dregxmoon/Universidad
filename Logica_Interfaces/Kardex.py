import pyodbc

# Conexión a SQL Server
def conectar_sql():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=tcp:localhost,1433;'   
        'DATABASE=PruebaDB;'
        'Trusted_Connection=yes;'
    )

def volver_inicio(self):
    from Logica_Interfaces.Menu import MenuLogic  
    self.ventana_menu = MenuLogic(self.num_control)
    self.ventana_menu.show()
    self.close()

def obtener_datos_alumno(num_control):
    conn = conectar_sql()
    cursor = conn.cursor()
    query = "SELECT Nombre, Carrera, Semestre, Foto FROM Alumnos WHERE Num_control = ?"
    cursor.execute(query, (num_control,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        return resultado
    else:
        return ("Desconocido", "Sin carrera", 0, None)

# Obtener materias del plan
def obtener_materias_plan():
    conn = conectar_sql()
    cursor = conn.cursor()
    query = "SELECT Serie, Nombre, Semestre, Creditos FROM Materias ORDER BY Semestre, Serie"
    cursor.execute(query)
    materias = cursor.fetchall()
    cursor.close()
    conn.close()
    return materias

# Obtener estatus de materias del alumno
def obtener_estatus_materias(num_control):
    conn = conectar_sql()
    cursor = conn.cursor()
    query = "SELECT Serie, Estatus, Calificacion FROM Kardex WHERE Num_control = ?"
    cursor.execute(query, (num_control,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    return {serie: (estatus.upper(), calificacion) for serie, estatus, calificacion in resultados}
