import pyodbc

# Conexión con autenticación de Windows
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-EMDLNML\\SQLEXPRESS;'
    'DATABASE=PruebaDB;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Solicitar datos al usuario
nombre = input("Ingresa el nombre de la persona: ")
edad = input("Ingresa la edad: ")

# Validar que edad sea número
try:
    edad = int(edad)
except ValueError:
    print("Esa no es una edad valida :v")
    cursor.close()
    conn.close()
    exit()

# Insertar datos
query = "INSERT INTO PERSONAS (Nombre, Edad) VALUES (?, ?)"
cursor.execute(query, (nombre, edad))
conn.commit()
print("Datos insertados yey!")

# Preguntar si desea ver todos los registros
ver_todo = input("¿Quieres consultar los demas datos? (s/n): ").strip().lower()

if ver_todo == 's':
    cursor.execute("SELECT * FROM PERSONAS")
    filas = cursor.fetchall()
    
    print("\nRegistros en la tabla PERSONAS:")
    for fila in filas:
        print(f"ID: {fila[0]} | NOMBRE: {fila[1]} | EDAD: {fila[2]}")

# Cierre
cursor.close()
conn.close()
