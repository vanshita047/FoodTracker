CREATE DATABASE food_tracker;
USE food_tracker;

CREATE TABLE orders(
id INT AUTO_INCREMENT PRIMARY KEY,
orders_date DATE NOT NULL,
platform VARCHAR(50) NOT NULL,
restaurant VARCHAR(100),
item_name VARCHAR(100) NOT NULL,
quantity INT DEFAULT 1,
price DECIMAL(8,2) NOT NULL,
delivery_fee DECIMAL (8,2) DEFAULT 0,
discount DECIMAL(8,2) DEFAULT 0,
total DECIMAL(8,2) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE price_comparison(
id INT AUTO_INCREMENT PRIMARY KEY,
item_name VARCHAR(100) NOT NULL ,
platform VARCHAR(50) NOT NULL,
restaurant VARCHAR(100),
price DECIMAL(8,2) NOT NULL,
last_updated DATE NOT NULL
);
DROP TABLE budget;
CREATE TABLE budget(
	id INT AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(7) NOT NULL,   
    monthly_limit DECIMAL(10,2),
);
ALTER TABLE price_comparison
ADD UNIQUE KEY uq_item_platform (item_name, platform);
