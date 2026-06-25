CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

DROP TABLE IF EXISTS borrowedbooksales;
DROP TABLE IF EXISTS soldbooksales;
DROP TABLE IF EXISTS borrowedbooks;
DROP TABLE IF EXISTS availablebooks;

CREATE TABLE availablebooks (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    genre VARCHAR(100)
);

CREATE TABLE borrowedbooks (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    borrower_name VARCHAR(255) NOT NULL,
    borrower_email VARCHAR(255),
    borrower_phone VARCHAR(20),
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL
);

CREATE TABLE soldbooksales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    quantity_sold INT NOT NULL,
    sale_date DATE DATE NOT NULL DEFAULT (CURRENT_DATE),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL
);

CREATE TABLE borrowedbooksales (
    borrow_sale_id INT AUTO_INCREMENT PRIMARY KEY,
    borrow_id INT NOT NULL,
    book_id INT NOT NULL,
    borrower_name VARCHAR(255) NOT NULL,
    borrower_email VARCHAR(255),
    borrower_phone VARCHAR(20),
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NOT NULL,
    fine_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) DEFAULT 0,
    transaction_date DATE
);