CREATE DATABASE Productos;
USE Productos; 
CREATE TABLE Producto(
	codigo char(4) primary key,
	nombre varchar(20) not null,
	precio char(10) not null,
	stock char(3) not null,
	talle INT not null
	);
 CREATE TABLE Calzado(
	codigo char(4) primary key,
    tipo_calzado varchar(50),calzado
	color varchar(20),
	foreign key (codigo) references Producto(codigo)
	);
CREATE TABLE Bikini(
	codigo char(4) primary key,
    tipo_bikini varchar(50),
    estampa varchar(50),
    FOREIGN KEY (codigo) REFERENCES Producto(codigo)
    );

ALTER TABLE bikini DROP foreign key Bikini_ibfk_1;
ALTER TABLE calzado DROP foreign key Calzado_ibfk_1;

ALTER TABLE bikini MODIFY codigo char(6);
ALTER TABLE calzado MODIFY codigo char(6);
ALTER TABLE producto MODIFY codigo char(6);

alter table Calzado add constraint Calzado_ibfk_1 foreign key(codigo) references Producto(codigo);

alter table Bikini add constraint Bikini_ibfk_1 foreign key(codigo) references Producto(codigo);
ALTER TABLE producto MODIFY talle varchar(6);
