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

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212005', 'Ryuko', 3, 'Ing. en Sistemas Computaciones', 'kill', 'img/Ryukio.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212006', 'Miku', 2, 'Ing. en Sistemas Computaciones', 'miku', 'img/miku.jpg');


INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212007', 'Doro', 3, 'Ing. en Sistemas Computaciones', 'doro123', 'img/doro.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212008', 'Ryou', 4, 'Ing. en Sistemas Computaciones', 'dinero', 'img/Ryou.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212009', 'Anko', 5, 'Ing. en Sistemas Computaciones', 'vampiro', 'img/Anko.jpg');

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212010', 'Kobeni', 6, 'Ing. en Sistemas Computaciones', 'miedo', 'img/kobeni.jpg');


DELETE FROM Alumnos
WHERE Num_control = 23212005;

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
('23212002', 'AED-1285', 50, 'REPROBADA'),  
('23212002', 'ACC-0906', 69, 'REPROBADA'),  
('23212002', 'SCH-1024', 99, 'APROBADA'),  
('23212002', 'ACA-0907', 89, 'APROBADA'),  
('23212002', 'AEF-1041', 93, 'APROBADA');  

SELECT * FROM Kardex

-- ryuko prueba
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212005', 'ACF-0901', 97, 'APROBADA'),  
('23212005', 'AED-1285', 91, 'APROBADA'),  
('23212005', 'ACC-0906', 79, 'APROBADA'),  
('23212005', 'SCH-1024', 78, 'APROBADA'),  
('23212005', 'ACA-0907', 98, 'APROBADA'),  
('23212005', 'AEF-1041', 93, 'APROBADA'),  

('23212005', 'ACF-0902', 97, 'APROBADA'),  
('23212005', 'AED-1286', 99, 'APROBADA'),  
('23212005', 'ACF-0903', 79, 'APROBADA'),  
('23212005', 'SCC-1005', 80, 'APROBADA'),  
('23212005', 'AEF-1052', 89, 'APROBADA'),  
('23212005', 'SCF-1006', 93, 'APROBADA'); 

-- materias de miku
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212006', 'ACF-0901', 67, 'REPROBADA'),  
('23212006', 'AED-1285', 90, 'APROBADA'),  
('23212006', 'ACC-0906', 70, 'APROBADA'),  
('23212006', 'SCH-1024', 99, 'APROBADA'),  
('23212006', 'ACA-0907', 89, 'APROBADA'),  
('23212006', 'AEF-1041', 93, 'APROBADA');  

-- Doro 
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212007','ACF-0901',85,'APROBADA'),
('23212007','AED-1285',90,'APROBADA'),
('23212007','ACC-0906',80,'APROBADA'),
('23212007','SCH-1024',88,'APROBADA'),
('23212007','ACA-0907',92,'APROBADA'),
('23212007','AEF-1041',87,'APROBADA'),

('23212007','ACF-0902',89,'APROBADA'),
('23212007','AED-1286',91,'APROBADA'),
('23212007','ACF-0903',85,'APROBADA'),
('23212007','SCC-1005',90,'APROBADA'),
('23212007','AEF-1052',88,'APROBADA'),
('23212007','SCF-1006',86,'APROBADA'),

('23212007','ACF-0904',55,'REPROBADA'), -- 1 reprobada
('23212007','AED-1026',80,'APROBADA'),
('23212007','AEC-1058',75,'APROBADA'),
('23212007','AEC-1008',82,'APROBADA'),
('23212007','SCC-1013',70,'APROBADA'),
('23212007','SCD-1018',85,'APROBADA');


-- Semestre 1
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212008','ACF-0901',85,'APROBADA'),          
('23212008','AED-1285',90,'APROBADA'),          
('23212008','ACC-0906',55,'REPROBADA'),         
('23212008','SCH-1024',60,'REPROBADA'),         
('23212008','ACA-0907',88,'APROBADA'),
('23212008','AEF-1041',87,'APROBADA');          

-- Semestre 2
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212008','ACF-0902',82,'APROBADA'),          
('23212008','AED-1286',85,'APROBADA'),         
('23212008','ACF-0903',80,'APROBADA'),          
('23212008','SCC-1005',78,'APROBADA'),          
('23212008','AEF-1052',81,'APROBADA'),          
('23212008','SCF-1006',79,'APROBADA');          

-- Semestre 3
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212008','ACF-0904',80,'APROBADA'),          
('23212008','AED-1026',84,'APROBADA'),          
('23212008','AEC-1058',76,'APROBADA'),         
('23212008','AEC-1008',73,'APROBADA'),         
('23212008','SCC-1013',75,'APROBADA'),         
('23212008','SCD-1018',72,'APROBADA');          


-- Semestre 1
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212009','ACF-0901',86,'APROBADA'),
('23212009','AED-1285',89,'APROBADA'),
('23212009','ACC-0906',58,'REPROBADA'),         
('23212009','SCH-1024',83,'APROBADA'),
('23212009','ACA-0907',55,'REPROBADA'),         
('23212009','AEF-1041',88,'APROBADA');

-- Semestre 2
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212009','ACF-0902',85,'APROBADA'),
('23212009','AED-1286',90,'APROBADA'),
('23212009','ACF-0903',82,'APROBADA'),
('23212009','SCC-1005',80,'APROBADA'),
('23212009','AEF-1052',84,'APROBADA'),
('23212009','SCF-1006',79,'APROBADA');

-- Semestre 3
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212009','ACF-0904',81,'APROBADA'),
('23212009','AED-1026',86,'APROBADA'),
('23212009','AEC-1058',58,'REPROBADA'),         
('23212009','AEC-1008',60,'REPROBADA'),        
('23212009','SCC-1013',76,'APROBADA'),         
('23212009','SCD-1018',74,'APROBADA');          

-- Semestre 4
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212009','ACF-0905',80,'APROBADA'),          
('23212009','SCD-1027',85,'APROBADA'),          
('23212009','SCC-1017',78,'APROBADA'),
('23212009','AEF-1031',82,'APROBADA'),          
('23212009','SCD-1022',79,'APROBADA'),          
('23212009','SCD-1003',81,'APROBADA');          


-- Semestre 1
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212010','ACF-0901',87,'APROBADA'),
('23212010','AED-1285',91,'APROBADA'),
('23212010','ACC-0906',52,'REPROBADA'),        
('23212010','SCH-1024',58,'REPROBADA'),         
('23212010','ACA-0907',86,'APROBADA'),
('23212010','AEF-1041',88,'APROBADA');

-- Semestre 2
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212010','ACF-0902',86,'APROBADA'),
('23212010','AED-1286',88,'APROBADA'),
('23212010','ACF-0903',83,'APROBADA'),
('23212010','SCC-1005',80,'APROBADA'),
('23212010','AEF-1052',82,'APROBADA'),
('23212010','SCF-1006',81,'APROBADA');

-- Semestre 3
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212010','ACF-0904',82,'APROBADA'),          
('23212010','AED-1026',85,'APROBADA'),          
('23212010','AEC-1058',54,'REPROBADA'),         
('23212010','AEC-1008',79,'APROBADA'),
('23212010','SCC-1013',77,'APROBADA'),          
('23212010','SCD-1018',76,'APROBADA');          

-- Semestre 4
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212010','ACF-0905',80,'APROBADA'),
('23212010','SCD-1027',84,'APROBADA'),
('23212010','SCC-1017',75,'APROBADA'),
('23212010','AEF-1031',81,'APROBADA'),          -
('23212010','SCD-1022',78,'APROBADA'),
('23212010','SCD-1003',79,'APROBADA');

-- Semestre 5
INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus) VALUES
('23212010','SCC-1010',50,'REPROBADA'),         
('23212010','AEC-1034',84,'APROBADA'),         
('23212010','AEC-1061',83,'APROBADA'),          
('23212010','SCA-1025',80,'APROBADA'),         
('23212010','SCC-1007',82,'APROBADA'),          
('23212010','ACD-0908',55,'REPROBADA');        


------------------------
-- Estructura para hacer la carga de materias muejeje

CREATE TABLE Periodos (
    Id_periodo INT IDENTITY(1,1) PRIMARY KEY,
    Periodo_texto VARCHAR(10) NOT NULL UNIQUE,   -- '2025-2'
    Nombre_periodo NVARCHAR(50),
    Activo BIT DEFAULT 0                         
);

CREATE TABLE Grupos (
    Id_grupo INT IDENTITY(1,1) PRIMARY KEY,
    Id_periodo INT NOT NULL,
    Serie_materia VARCHAR(20) NOT NULL,
    Grupo_letra CHAR(1) NOT NULL CHECK (Grupo_letra IN ('A','B','C','D')),
    Cupo_maximo INT DEFAULT 40,
    Cupo_actual INT DEFAULT 0,
    Aula NVARCHAR(20),
    FOREIGN KEY (Id_periodo) REFERENCES Periodos(Id_periodo),
    FOREIGN KEY (Serie_materia) REFERENCES Materias(Serie),
    UNIQUE (Id_periodo, Serie_materia, Grupo_letra)
);

CREATE TABLE Horario_Grupo (
    Id_horario INT IDENTITY(1,1) PRIMARY KEY,
    Id_grupo INT NOT NULL,
    Dia_semana VARCHAR(10) NOT NULL CHECK (Dia_semana IN ('Lunes','Martes','Miércoles','Jueves','Viernes')),
    Hora_inicio TIME NOT NULL,
    Hora_fin TIME NOT NULL,
    FOREIGN KEY (Id_grupo) REFERENCES Grupos(Id_grupo)
);

CREATE TABLE Inscripciones (
    Id_inscripcion INT IDENTITY(1,1) PRIMARY KEY,
    Num_control CHAR(8) NOT NULL,
    Id_grupo INT NOT NULL,
    Fecha_inscripcion DATETIME DEFAULT GETDATE(),
    Estado NVARCHAR(20) DEFAULT 'INSCRITO',
    FOREIGN KEY (Num_control) REFERENCES Alumnos(Num_control),
    FOREIGN KEY (Id_grupo) REFERENCES Grupos(Id_grupo),
    UNIQUE (Num_control, Id_grupo)
);


CREATE TRIGGER TR_Inscribir_Auto_Cursando
ON Inscripciones
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Kardex (Num_control, Serie, Calificacion, Estatus)
    SELECT 
        i.Num_control, 
        g.Serie_materia, 
        0.00, 
        'CURSANDO'
    FROM inserted i
    JOIN Grupos g ON i.Id_grupo = g.Id_grupo
    WHERE NOT EXISTS (   
        SELECT 1 
        FROM Kardex k 
        WHERE k.Num_control = i.Num_control 
          AND k.Serie = g.Serie_materia 
          AND k.Estatus = 'CURSANDO'
    );
END
GO

USE PruebaDB
GO

-- funcion para generar los paquetes de cada semestre 
-- tomando en cuenta que las materias de 5 creditos son 5 clases a la semana
-- y las materias de 4 creditos son 4 clases a la semana
-- tenemos la tabla de plantilla horario con la que se basa
IF NOT EXISTS (SELECT 1 FROM Periodos WHERE Periodo_texto = '2025-2')
BEGIN
    INSERT INTO Periodos (Periodo_texto, Nombre_periodo, Activo)
    VALUES ('2025-2', 'Agosto-Diciembre 2025', 1);
END
GO

DECLARE @id_periodo INT = (SELECT Id_periodo FROM Periodos WHERE Activo = 1);

DECLARE @serie VARCHAR(20), @creditos INT, @aula_base NVARCHAR(20);
DECLARE cur CURSOR FOR
SELECT Serie, Creditos FROM Materias ORDER BY Semestre;
OPEN cur;
FETCH NEXT FROM cur INTO @serie, @creditos;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- 4 grupos por materia
    INSERT INTO Grupos (Id_periodo, Serie_materia, Grupo_letra, Cupo_maximo, Aula)
    VALUES 
    (@id_periodo, @serie, 'A', 40, 'B-101'),
    (@id_periodo, @serie, 'B', 40, 'B-102'),
    (@id_periodo, @serie, 'C', 40, 'B-103'),
    (@id_periodo, @serie, 'D', 40, 'B-104');

    DECLARE @id_grupo_A INT = SCOPE_IDENTITY() - 3;
    DECLARE @id_grupo_B INT = SCOPE_IDENTITY() - 2;
    DECLARE @id_grupo_C INT = SCOPE_IDENTITY() - 1;
    DECLARE @id_grupo_D INT = SCOPE_IDENTITY();

    -- Horarios según créditos
    IF @creditos = 5 OR @creditos = 10
    BEGIN
        -- 5 créditos Lunes a Viernes
        INSERT INTO Horario_Grupo (Id_grupo, Dia_semana, Hora_inicio, Hora_fin) VALUES
        -- Grupo A
        (@id_grupo_A,'Lunes','07:00','08:50'),(@id_grupo_A,'Martes','07:00','08:50'),(@id_grupo_A,'Miércoles','07:00','08:50'),(@id_grupo_A,'Jueves','07:00','08:50'),(@id_grupo_A,'Viernes','07:00','08:50'),
        -- Grupo B
        (@id_grupo_B,'Lunes','09:00','10:50'),(@id_grupo_B,'Martes','09:00','10:50'),(@id_grupo_B,'Miércoles','09:00','10:50'),(@id_grupo_B,'Jueves','09:00','10:50'),(@id_grupo_B,'Viernes','09:00','10:50'),
        -- Grupo C
        (@id_grupo_C,'Lunes','11:00','12:50'),(@id_grupo_C,'Martes','11:00','12:50'),(@id_grupo_C,'Miércoles','11:00','12:50'),(@id_grupo_C,'Jueves','11:00','12:50'),(@id_grupo_C,'Viernes','11:00','12:50'),
        -- Grupo D
        (@id_grupo_D,'Lunes','15:00','16:50'),(@id_grupo_D,'Martes','15:00','16:50'),(@id_grupo_D,'Miércoles','15:00','16:50'),(@id_grupo_D,'Jueves','15:00','16:50'),(@id_grupo_D,'Viernes','15:00','16:50');
    END
    ELSE
    BEGIN
        -- 4 créditos Lunes a Jueves
        INSERT INTO Horario_Grupo (Id_grupo, Dia_semana, Hora_inicio, Hora_fin) VALUES
        -- Grupo A
        (@id_grupo_A,'Lunes','07:00','08:50'),(@id_grupo_A,'Martes','07:00','08:50'),(@id_grupo_A,'Miércoles','07:00','08:50'),(@id_grupo_A,'Jueves','07:00','08:50'),
        -- Grupo B
        (@id_grupo_B,'Lunes','09:00','10:50'),(@id_grupo_B,'Martes','09:00','10:50'),(@id_grupo_B,'Miércoles','09:00','10:50'),(@id_grupo_B,'Jueves','09:00','10:50'),
        -- Grupo C
        (@id_grupo_C,'Lunes','11:00','12:50'),(@id_grupo_C,'Martes','11:00','12:50'),(@id_grupo_C,'Miércoles','11:00','12:50'),(@id_grupo_C,'Jueves','11:00','12:50'),
        -- Grupo D
        (@id_grupo_D,'Lunes','15:00','16:50'),(@id_grupo_D,'Martes','15:00','16:50'),(@id_grupo_D,'Miércoles','15:00','16:50'),(@id_grupo_D,'Jueves','15:00','16:50');
    END

    FETCH NEXT FROM cur INTO @serie, @creditos;
END
CLOSE cur;
DEALLOCATE cur;
GO

-- SERVICIO SOCIAL 
UPDATE Grupos SET Aula = 'Lab-Red' WHERE Serie_materia = '4SC9';
UPDATE Horario_Grupo SET Hora_inicio = '07:00', Hora_fin = '11:00' WHERE Id_grupo IN (SELECT Id_grupo FROM Grupos WHERE Serie_materia = '4SC9');




SELECT * FROM Materias
SELECT *FROM Kardex
SELECT * FROM Alumnos
SELECT * FROM Periodos
SELECT * FROM Inscripciones
DELETE FROM Inscripciones
SELECT COUNT (*) AS Total_Grupos FROM Grupos
SELECT * FROM PlantillaHorarios

--DELETE FROM Alumnos
--WHERE Num_control = 23211907;
-- id materias
-- materia
-- serie
-- semestre
-- 

DELETE FROM Kardex
WHERE Num_control = 23212002

SELECT* FROM Kardex
WHERE Num_control = 23212002