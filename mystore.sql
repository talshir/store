DROP DATABASE IF EXISTS mystore;
CREATE DATABASE mystore;
USE mystore;

DROP TABLE IF EXISTS products, categories;

CREATE TABLE categories(
    Id INT NOT NULL UNIQUE auto_increment(1001),
    Name VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(Id)
);

CREATE TABLE products(
    Id INT NOT NULL UNIQUE auto_increment,
    Title VARCHAR(50) NOT NULL,
    Description VARCHAR(200),
    Price double NOT NULL,
    Img_URL VARCHAR(100) NOT NULL,
    Category_Id INT NOT NULL,
    Favorite INT DEFAULT 0,
    PRIMARY KEY(Id),
    FOREIGN KEY(Category_Id) REFERENCES categories(Id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);