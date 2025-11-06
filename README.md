Hola 
uwu

script de la base de datos para el programa con algunnas inserciones

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

INSERT INTO Alumnos (Num_control, Nombre, Semestre, Carrera, Contraseña_hash, Foto)
VALUES ('23212001', 'Himiko Toga', 2, 'Ing. en Sistemas Computaciones', 'tshzeybste', 'img/toga.jpg');
