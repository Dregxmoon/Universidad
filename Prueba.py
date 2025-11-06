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
    print("❌ La edad debe ser un número entero.")
    cursor.close()
    conn.close()
    exit()

# Insertar datos
query = "INSERT INTO PERSONAS (Nombre, Edad) VALUES (?, ?)"
cursor.execute(query, (nombre, edad))
conn.commit()
print("✅ Datos insertados correctamente.")

# Preguntar si desea ver todos los registros
ver_todo = input("¿Deseas ver todos los datos de la tabla PERSONAS? (s/n): ").strip().lower()

if ver_todo == 's':
    cursor.execute("SELECT * FROM PERSONAS")
    filas = cursor.fetchall()
    
    print("\n📋 Registros en la tabla PERSONAS:")
    for fila in filas:
        print(f"ID: {fila[0]} | NOMBRE: {fila[1]} | EDAD: {fila[2]}")

# Cierre
cursor.close()
conn.close()
