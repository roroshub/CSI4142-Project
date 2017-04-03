DROP TABLE IF EXISTS csi4142project.temptable;
CREATE TABLE IF NOT EXISTS  csi4142project.temptable (
		line	INTEGER	PRIMARY KEY,
		country	VARCHAR(60)	NOT NULL,
		locationcode	 		INTEGER	NOT NULL,
		locationname 		VARCHAR(60)	NOT NULL,
		outletcode		 		INTEGER		NOT NULL,
		outlettype 		VARCHAR(60)		NOT NULL,
		obsdate	DATE		NOT NULL,
		productcode		INTEGER		NOT NULL,
		productname VARCHAR(60) NOT NULL,
    	prefqty FLOAT NOT NULL,
    	obsqty FLOAT NOT NULL,
    	quantity VARCHAR(30) NOT NULL,
   	 	obsuomcode INTEGER NOT NULL,
    	obsprice FLOAT NOT NULL,
    	convprice FLOAT NOT NULL,
    	pricetype VARCHAR(30) NOT NULL,
   	 	rejected INTEGER NOT NULL,
    	currency VARCHAR(30) NOT NULL);
        
INSERT INTO csi4142project.location (location_key, city, location_type)
SELECT locationcode, locationname, outlettype
FROM csi4142project.temptable

ALTER TABLE csi4142project.location ALTER COLUMN anav_income DROP NOT NULL

"C:\Users\roro\Desktop\data science\project\Crowd-Sourced_Price_Collection_CSV.csv"
        