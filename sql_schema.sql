DROP SCHEMA IF EXISTS csi4142project CASCADE;
CREATE SCHEMA csi4142project;
		

DROP TABLE IF EXISTS csi4142project.Location;
CREATE TABLE IF NOT EXISTS  csi4142project.Location (
		location_skey	SERIAL		PRIMARY KEY,
		location_key	INTEGER		NOT NULL,
		location_type	VARCHAR(50)	NOT NULL,
		city	 		VARCHAR(30)	NOT NULL,
		country 		VARCHAR(30)	NOT NULL,
		gdp		 		FLOAT,
		population 		INTEGER,
		life_expectancy	FLOAT,
		anav_income		FLOAT,
		location_year 	INTEGER);
		
		
DROP TABLE IF EXISTS csi4142project.Date;
CREATE TABLE IF NOT EXISTS  csi4142project.Date (
		date_key		SERIAL		PRIMARY KEY,
		date			DATE		NOT NULL,
		day_of_week		INTEGER,
		week_in_year 	VARCHAR(30),
		month			INTEGER,
		year 			INTEGER,
		weekend			BOOLEAN);

		
DROP TABLE IF EXISTS csi4142project.Product;
CREATE TABLE IF NOT EXISTS  csi4142project.Product (
		product_skey	SERIAL		PRIMARY KEY,
		product_key		INTEGER		NOT NULL,
		product_name	VARCHAR(35)	NOT NULL,
		category		VARCHAR(30),
		energy 			INTEGER,
		carbohydrates	FLOAT,
		fat 			FLOAT,
		protein			FLOAT,
		product_year	INTEGER);

		
DROP TABLE IF EXISTS csi4142project.ProductPrice;
CREATE TABLE IF NOT EXISTS  csi4142project.ProductPrice (
		pp_key			INTEGER		NOT NULL,
		date_key		INTEGER		NOT NULL,
		product_key		INTEGER		NOT NULL,
		location_key	INTEGER		NOT NULL,
		price 			FLOAT		NOT NULL,
		PRIMARY KEY (pp_key), 
		FOREIGN KEY(date_key) REFERENCES csi4142project.Date(date_key) ON DELETE RESTRICT ON UPDATE CASCADE, 
		FOREIGN KEY(product_key) REFERENCES csi4142project.Product(product_key) ON DELETE RESTRICT ON UPDATE CASCADE, 
		FOREIGN KEY(location_key) REFERENCES csi4142project.Location(location_key) ON DELETE RESTRICT ON UPDATE CASCADE);