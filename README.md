<div align="center">

# 🎓 Sistema de Gestión de Horarios Universitarios

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL_Server-Database-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>
  <img src="https://img.shields.io/badge/Algorithm-Backtracking-6A0DAD?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/Dregxmoon/Universidad?style=flat-square&color=orange"/>
  <img src="https://img.shields.io/github/repo-size/Dregxmoon/Universidad?style=flat-square&color=blue"/>
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square"/>
</p>

> Aplicación de escritorio para la **gestión de horarios universitarios** y **carga de materias**, con un motor de **carga inteligente** basado en el algoritmo de Backtracking que asigna maestros y horarios sin conflictos, respaldado por **SQL Server**.

</div>

---

## 📋 Descripción

El **Sistema de Gestión de Horarios Universitarios** es una aplicación de escritorio desarrollada en Python con interfaz gráfica en PyQt5. Permite administrar de forma centralizada la asignación de materias, maestros y horarios de una institución universitaria.

Su módulo estrella es la **carga inteligente de materias**, que mediante el algoritmo de **Backtracking** genera automáticamente un horario completo, válido y sin conflictos, consultando la disponibilidad de maestros y restricciones almacenadas en SQL Server.

---

## ✨ Características

| Módulo | Descripción |
|---|---|
| 📚 Gestión de materias | Alta, baja y modificación de materias del catálogo |
| 👨‍🏫 Gestión de maestros | Registro de docentes con disponibilidad por día y hora |
| 🗓️ Gestión de horarios | Creación y administración de horarios por carrera y semestre |
| 🤖 Carga inteligente | Asignación automática con Backtracking sin cruces de horario |
| 🗄️ SQL Server | Persistencia robusta con consultas optimizadas |
| 🖥️ Interfaz PyQt5 | GUI moderna e intuitiva para el administrador |

---

## 🛠️ Tecnologías

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL_Server-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white"/>
  <img src="https://img.shields.io/badge/pyodbc-lightgrey?style=flat-square"/>
</p>

- **Python 3.8+** — Lenguaje principal
- **PyQt5** — Interfaz gráfica de escritorio
- **SQL Server** — Base de datos relacional
- **pyodbc** — Conexión Python ↔ SQL Server
- **Backtracking** — Algoritmo de carga inteligente de materias

---

## 🗂️ Estructura del proyecto

```
Universidad/
├── BD/                        # Scripts SQL (creación de tablas, procedimientos)
├── Diseño_Interfaces/         # Archivos .ui de PyQt5 (vistas)
├── Logica_Interfaces/         # Controladores y lógica de negocio
├── img/                       # Recursos gráficos e íconos
├── Programa.py                # Punto de entrada de la aplicación
└── README.md
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- SQL Server instalado y corriendo
- ODBC Driver 17 for SQL Server

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Dregxmoon/Universidad.git
cd Universidad

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install PyQt5 pyodbc
```

### Configurar la base de datos

1. Abre SQL Server Management Studio
2. Ejecuta los scripts dentro de la carpeta `BD/` en orden
3. Actualiza la cadena de conexión en el archivo de configuración con tu servidor y credenciales

---

## ▶️ Uso

```bash
python Programa.py
```

---

## 🤖 Carga inteligente con Backtracking

El módulo de carga inteligente utiliza el algoritmo de **Backtracking** para generar horarios completos y válidos de forma automática.

### ¿Cómo funciona?

```
Inicio → Tomar materia sin asignar
           └─ Buscar maestro disponible
                 ├─ ✅ Sin conflicto → Asignar y avanzar a la siguiente materia
                 └─ ❌ Conflicto    → Backtrack → Probar otra combinación
```

### Restricciones que evalúa

- ✔️ Disponibilidad del maestro por día y franja horaria
- ✔️ Materias ya asignadas al mismo grupo (sin cruces)
- ✔️ Capacidad y disponibilidad de aulas
- ✔️ Restricciones definidas en SQL Server

El resultado es un **horario completo, sin conflictos**, generado automáticamente con un solo clic.

---

## 🗄️ Base de datos

Los scripts de creación de tablas y datos iniciales se encuentran en la carpeta `BD/`. Deben ejecutarse en SQL Server antes de iniciar la aplicación por primera vez.

**Tablas principales:**

| Tabla | Descripción |
|---|---|
| `Maestros` | Registro de docentes y disponibilidad |
| `Materias` | Catálogo de materias por carrera |
| `Horarios` | Asignaciones generadas |
| `Grupos` | Grupos y semestres activos |

---

<div align="center">
  <img width="693" height="488" alt="image" src="https://github.com/user-attachments/assets/44063976-3c64-4565-8456-829f30ad747c" />
</div>

---

<div align="center">
  <sub>Proyecto académico universitario • 2025</sub>
</div>
