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


--DELETE FROM Alumnos
--WHERE Num_control = 23211907;
-- id materias
-- materia
-- serie
-- semestre
-- 