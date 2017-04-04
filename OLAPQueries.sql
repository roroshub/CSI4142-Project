##Explore the data in order to get “a feel of” the prices of the various products in a
##country. The user should be able to drill down from 6 months, to one month, to a
##specific day, and roll up again.

SELECT p.price
FROM csi4142project.ProductPrice p, csi4142project.Date d
WHERE d.date_key = p.date_key AND d.date >  CURRENT_DATE - INTERVAL '6 months'

SELECT p.price
FROM csi4142project.ProductPrice p, csi4142project.Date d
WHERE d.date_key = p.date_key AND d.date >  CURRENT_DATE - INTERVAL '1 months'

SELECT p.price
FROM csi4142project.ProductPrice p, csi4142project.Date d
WHERE d.date_key = p.date_key AND d.date =  CURRENT_DATE

##Explore the data in order to get “a feel of” the price differences of the products when
##considering more than one country. For example, one may want to contrast the price
##of tuna steaks in Kenya with that in India. The user should be able to drill down
##from 6 months, to one month, to a specific day, and roll up again.

SELECT p.price, l.country, t.product_name
FROM csi4142project.ProductPrice p, csi4142project.Date d, csi4142project.Location l, csi4142project.Product t 
WHERE t.product_key = p.product_key AND d.date_key = p.date_key AND l.location_key = p.location_key AND d.date >  CURRENT_DATE - INTERVAL '6 months'

SELECT p.price, l.country, t.product_name
FROM csi4142project.ProductPrice p, csi4142project.Date d, csi4142project.Location l, csi4142project.Product t 
WHERE t.product_key = p.product_key AND d.date_key = p.date_key AND l.location_key = p.location_key AND d.date >  CURRENT_DATE - INTERVAL '1 months'

SELECT p.price, l.country, t.product_name
FROM csi4142project.ProductPrice p, csi4142project.Date d, csi4142project.Location l, csi4142project.Product t 
WHERE t.product_key = p.product_key AND d.date_key = p.date_key AND l.location_key = p.location_key AND d.date =  CURRENT_DATE

##Explore the data by considering the prices of categories of products. That is, we wish
##to roll up from product to category. For example, the sales of apples, bananas and
##oranges are grouped into fruits while minced beef and chicken legs are grouped into
##fresh meat.

SELECT t.category, avg(p.price) 
FROM csi4142project.ProductPrice p, csi4142project.Product t 
WHERE t.product_key = p.product_key 
GROUP BY t.category

##Explore the data by considering the prices of categories of products, on a specific day
##of the week (e.g. the prices of fruits on Monday versus Saturday; weekend versus
##weekday, and so on).

##Laurence: not sure if we want to have the avg or not?

SELECT d.day_of_week, avg(p.price) 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Date d
WHERE t.product_key = p.product_key AND d.date_key = p.date_key
GROUP BY d.day_of_week

SELECT d.weekend, avg(p.price) 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Date d
WHERE t.product_key = p.product_key AND d.date_key = p.date_key
GROUP BY d.weekend

##Explore the fluctuations in individual product prices, per country, per city and per
##location.

SELECT p.price, t.product_name, l.country 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Location l
WHERE t.product_key = p.product_key AND l.location_key = p.location_key

SELECT p.price, t.product_name, l.city 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Location l
WHERE t.product_key = p.product_key AND l.location_key = p.location_key

SELECT p.price, t.product_name, l.location_key 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Location l
WHERE t.product_key = p.product_key AND l.location_key = p.location_key

##Explore the prices of a specific product (e.g. apples) in terms of socio-economic
##factors, such as the average income of a country.

SELECT p.price, t.product_name, l.anav_income 
FROM csi4142project.ProductPrice p, csi4142project.Product t , csi4142project.Location l
WHERE t.product_key = p.product_key AND l.location_key = p.location_key AND t.product_name = "Orange"

##Compare the prices of two complementary products (e.g. white rice and long-grain
##rice).

SELECT p.price, t.product_name
FROM csi4142project.ProductPrice p, csi4142project.Product t 
WHERE t.product_key = p.product_key AND (t.product_name = "Soybean oil" OR t.product_name = "Palm oil") 

##Compare the prices of two complementary products (e.g. white rice and long-grain
##rice), within a specific country. Next, drill down by city and location.

SELECT p.price, t.product_name, l.country
FROM csi4142project.ProductPrice p, csi4142project.Product t 
WHERE t.product_key = p.product_key AND l.location_key = p.location_key AND (t.product_name = "Soybean oil" OR t.product_name = "Palm oil") 

SELECT p.price, t.product_name, l.city
FROM csi4142project.ProductPrice p, csi4142project.Product t 
WHERE t.product_key = p.product_key AND l.location_key = p.location_key AND (t.product_name = "Soybean oil" OR t.product_name = "Palm oil") 

SELECT p.price, t.product_name, l.location_key
FROM csi4142project.ProductPrice p, csi4142project.Product t 
WHERE t.product_key = p.product_key AND l.location_key = p.location_key AND (t.product_name = "Soybean oil" OR t.product_name = "Palm oil") 
