# 🎓 Sistema de Gestión de Horarios Universitarios

> Aplicación de escritorio para la **carga y gestión de materias universitarias**, con soporte de **carga inteligente** basada en disponibilidad de maestros y horarios mediante SQL.

---

## 📋 Descripción

Este sistema permite a instituciones universitarias administrar de forma eficiente la asignación de materias, maestros y horarios. Su característica principal es la **carga inteligente de materias**, que genera automáticamente horarios válidos tomando en cuenta la disponibilidad docente, conflictos de horario y datos almacenados en una base de datos SQL.

---

## ✨ Características

- 📚 **Gestión de materias** — Alta, baja y modificación de materias del catálogo
- 👨‍🏫 **Gestión de maestros** — Registro de docentes y su disponibilidad de horario
- 🗓️ **Gestión de horarios** — Creación y administración de horarios por carrera y semestre
- 🤖 **Carga inteligente** — Asignación automática de materias basada en maestros disponibles y restricciones de horario
- 🗄️ **Base de datos SQL** — Persistencia de datos con consultas optimizadas
- 🖥️ **Interfaz gráfica** — GUI intuitiva para facilitar la administración

---

## 🗂️ Estructura del proyecto

```
Universidad/
├── BD/                   # Scripts y configuración de la base de datos SQL
├── Diseño_Interfaces/    # Archivos de diseño de la interfaz de usuario
├── Logica_Interfaces/    # Lógica de negocio y controladores
├── img/                  # Recursos gráficos e imágenes
├── Programa              # Punto de entrada principal
└── README.md
```

---

## ⚙️ Requisitos previos

- Python 3.8+
- pip
- SQLite / MySQL / PostgreSQL

---

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Dregxmoon/Universidad.git
cd Universidad

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar la base de datos
# Ejecutar los scripts dentro de la carpeta BD/ para crear las tablas
```

---

## ▶️ Uso

```bash
python Programa
```

---

## 🤖 Carga inteligente de materias

El módulo de carga inteligente utiliza el algoritmo de **Backtracking** para generar horarios válidos de forma automática.

### ¿Cómo funciona?

El algoritmo explora de manera recursiva todas las combinaciones posibles de materias, maestros y horarios. Cuando detecta un conflicto (choque de horario, maestro no disponible, etc.), **retrocede** y prueba otra combinación hasta encontrar una solución válida.

```
Inicio
  └── Asignar materia 1
        └── ¿Maestro disponible? ✅ → Asignar horario
              └── Asignar materia 2
                    └── ¿Conflicto de horario? ❌ → Backtrack
                          └── Probar siguiente combinación...
```

### El algoritmo toma en cuenta:

1. Disponibilidad de maestros por día y hora
2. Conflictos de materias ya asignadas al mismo grupo
3. Restricciones de horario definidas en la base de datos SQL
4. Generación del horario completo sin cruces con un solo clic

---

## 🗄️ Base de datos

Los scripts SQL para crear la estructura de tablas se encuentran en la carpeta `BD/`. Deben ejecutarse antes de correr el programa por primera vez.

---

## 👤 Autor

**Dregxmoon** — [github.com/Dregxmoon](https://github.com/Dregxmoon)

---

> Proyecto académico • 2025
