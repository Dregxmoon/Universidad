CREATE DATABASE PruebaDB
USE PruebaDB

CREATE TABLE Alumnos (
  Num_control CHAR(8) PRIMARY KEY,             
  Nombre NVARCHAR(100) NOT NULL,
  Semestre INT,         
  Carrera NVARCHAR(50) DEFAULT 'Ing. en Sistemas Computaciones',
  Contraseña_hash NVARCHAR(255) NOT NULL,
  Foto NVARCHAR(255)
);

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contrase�a_hash, Foto)
VALUES ('23212001', 'Himiko Toga', 2, 'Ing. en Sistemas Computaciones', 'tshzeybste', 'img/toga.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contrase�a_hash, Foto)
VALUES ('23212002', 'Urabe Mikoto', 2, 'Ing. en Sistemas Computaciones', 'panfilo', 'img/urabe.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contrase�a_hash, Foto)
VALUES ('23211907', 'Samuel "Galleta"', 5, 'Ing. en Sistemas Computaciones', 'galleta', 'img/galleta.jpeg');

CREATE TABLE Materias (
  Serie VARCHAR(20) PRIMARY KEY,
  Nombre NVARCHAR(100),
  Semestre INT,
  Creditos INT,
  Seriada VARCHAR(20) NULL,
  FOREIGN KEY (Seriada) REFERENCES Materias(Serie)
);

INSERT INTO Materias (Serie, Nombre, Semestre, Creditos, Seriada) VALUES
-- Materias
-- Semestre 1
('ACF-0901', 'Cálculo Diferencial', 1, 5, NULL),
('AED-1285', 'Fundamentos de Programación', 1, 5, NULL),
('ACC-0906', 'Fundamentos de Investigación', 1, 4, NULL),
('SCH-1024', 'Taller de Administración', 1, 4, NULL),
('ACA-0907', 'Taller de Ética', 1, 4, NULL),
('AEF-1041', 'Matemáticas Discretas', 1, 5, NULL),

-- Semestre 2
('ACF-0902', 'Cálculo Integral', 2, 5, 'ACF-0901'),
('AED-1286', 'Programación Orientada a Objetos', 2, 5, 'AED-1285'),
('ACF-0903', 'Álgebra Lineal', 2, 5, NULL),
('SCC-1005', 'Cultura Empresarial', 2, 4, NULL),
('AEF-1052', 'Probabilidad y Estadística', 2, 5, NULL),
('SCF-1006', 'Física General', 2, 5, NULL),

-- Semestre 3
('ACF-0904', 'Cálculo Vectorial', 3, 5, 'ACF-0902'),
('AED-1026', 'Estructura de Datos', 3, 5, NULL),
('AEC-1058', 'Química', 3, 4, NULL),
('AEC-1008', 'Contabilidad Financiera', 3, 4, NULL),
('SCC-1013', 'Investigación de Operaciones', 3, 4, 'AEF-1052'),
('SCD-1018', 'Principios Electricos y Aplicaciones Digitales', 3, 5, 'SCF-1006'),

-- Semestre 4
('ACF-0905', 'Ecuaciones Diferenciales', 4, 5, 'ACF-0904'),
('SCD-1027', 'Tópicos Avanzados de Programación', 4, 5, 'AED-1026'),
('SCC-1017', 'Métodos Numéricos', 4, 4, NULL),
('AEF-1031', 'Fundamentos de Bases de Datos', 4, 5, NULL),
('SCD-1022', 'Simulación', 4, 5, 'SCC-1013'),
('SCD-1003', 'Arquitectura de Computadoras', 4, 5, 'SCD-1018'),

--Semestre 5
('SCC-1010', 'Graficación', 5, 4, NULL),
('AEC-1034', 'Fundamentos de Telecomunicaciones', 5, 4, NULL),
('AEC-1061', 'Sistemas Operativos I', 5, 4, NULL),
('SCA-1025', 'Taller de Bases de Datos', 5, 4, 'AEF-1031'),
('SCC-1007', 'Fundamentos de Ingeniería de Software', 5, 4, NULL),
('ACD-0908', 'Desarrollo Sustentable', 5, 5, NULL),

--Semestre 6
('SCD-1015', 'Lenguajes y Autómatas I', 6, 5, NULL),
('SCD-1021', 'Redes de Computadoras', 6, 5, 'AEC-1034'),
('SCA-1026', 'Taller de Sistemas Operativos', 6, 4, 'AEC-1061'),
('SCB-1001', 'Administración de Bases de Datos', 6, 5, 'SCA-1025'),
('SCD-1011', 'Ingeniería de Software', 6, 5, 'SCC-1007'),
('SCC-1014', 'Lenguajes de Interfaz', 6, 4, NULL),
('4SC9', 'Servicio Social', 6, 10, NULL),

-- Semestre 7
('SCD-1016', 'Lenguajes y Autómatas II', 7, 5, 'SCD-1015'),
('SCD-1004', 'Conmutación y Enrutamiento en Redes', 7, 5, NULL),
('ACA-0909', 'Taller de Investigación I', 7, 4, NULL),
('SCC-1019', 'Programación Lógica y Funcional', 7, 4, NULL),
('SCG-1009', 'Gestión de Proyectos de Software', 7, 6, 'SCD-1011'),
('SCG-1023', 'Sistemas Programables', 7, 4, 'SCC-1014'),

-- Semestre 8
('AEB-1055', 'Programación Web', 8, 5, NULL),
('SCA-1002', 'Administración de Redes', 8, 4, 'SCD-1004'),
('ACA-0910', 'Taller de Investigación II', 8, 4, 'ACA-0909'),
('SCC-1002', 'Inteligencia Artificial', 8, 4, 'SCC-1019'),

-- Semestre 9
--('3SC9', 'Residencia Profesional', 8, 10, '4SC9'),
--('ACSC', 'Actividades Complementarias', 8, 5, NULL);


CREATE TABLE Kardex (
  Id_kardex INT IDENTITY PRIMARY KEY,   
  Num_control CHAR(8) NOT NULL,         
  Serie VARCHAR(20) NOT NULL,          
  Calificacion DECIMAL(4,2) NOT NULL,
  Estatus NVARCHAR(20) NOT NULL CHECK (Estatus IN ('APROBADA','REPROBADA','CURSANDO')),
  
  FOREIGN KEY (Num_control) REFERENCES Alumnos(Num_control),
  FOREIGN KEY (Serie) REFERENCES Materias(Serie)
);

-- Himiko Toga aprobó las 6 materias de 1er Semestre yey!
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212001', 'ACF-0901', 90, 'APROBADA'),  
('23212001', 'AED-1285', 95, 'APROBADA'),  
('23212001', 'ACC-0906', 88, 'APROBADA'),  
('23212001', 'SCH-1024', 92, 'APROBADA'),  
('23212001', 'ACA-0907', 85, 'APROBADA'),  
('23212001', 'AEF-1041', 93, 'APROBADA');  

-- Urabe prueba
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212002', 'ACF-0901', 67, 'REPROBADA'),  
('23212002', 'AED-1285', 90, 'APROBADA'),  
('23212002', 'ACC-0906', 70, 'APROBADA'),  
('23212002', 'SCH-1024', 99, 'APROBADA'),  
('23212002', 'ACA-0907', 89, 'APROBADA'),  
('23212002', 'AEF-1041', 93, 'APROBADA');  

SELECT * FROM Materias
SELECT *FROM Kardex
--DELETE FROM Alumnos
--WHERE Num_control = 23211907;
-- id materias
-- materia
-- serie
-- semestre
-- 


