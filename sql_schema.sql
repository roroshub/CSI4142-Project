DROP SCHEMA IF EXISTS csi4142project CASCADE;
CREATE SCHEMA csi4142project;
		

DROP TABLE IF EXISTS csi4142project.Location;
CREATE TABLE IF NOT EXISTS  csi4142project.Location (
		location_key	INTEGER		PRIMARY KEY,
		location_type	VARCHAR(50)	NOT NULL,
		city	 		VARCHAR(30)	NOT NULL,
		country 		VARCHAR(30)	NOT NULL,
		gdp		 		INTEGER		NOT NULL,
		population 		INTEGER		NOT NULL,
		life-expectancy	INTEGER		NOT NULL,
		anav_income		FLOAT		NOT NULL);
		
		
DROP TABLE IF EXISTS csi4142project.Date;
CREATE TABLE IF NOT EXISTS  csi4142project.Date (
		date_key		SERIAL		PRIMARY KEY,
		date			DATE		NOT NULL,
		day_of_week		INTEGER		NOT NULL,
		week_in_year 	VARCHAR(30)	NOT NULL,
		month			INTEGER		NOT NULL,
		year 			INTEGER		NOT NULL,
		weekend			BOOLEAN		NOT NULL);

		
DROP TABLE IF EXISTS csi4142project.Product;
CREATE TABLE IF NOT EXISTS  csi4142project.Product (
		product_key		INTEGER		PRIMARY KEY,
		product_name	VARCHAR(30)	NOT NULL,
		category		VARCHAR(30)	NOT NULL,
		energy 			INTEGER		NOT NULL,
		carbohydrates	INTEGER		NOT NULL,
		fat 			INTEGER		NOT NULL,
		protein			INTEGER		NOT NULL);

		
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