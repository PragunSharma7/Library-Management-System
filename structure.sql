CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS returns;



CREATE TABLE customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE COLLATE utf8mb4_0900_ai_ci,
    phone VARCHAR(20) UNIQUE COLLATE utf8mb4_0900_bin,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_customer_name (name),
    INDEX idx_customer_email (email),
    INDEX idx_customer_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;

CREATE TABLE books (
    book_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE COLLATE utf8mb4_0900_bin,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    genre VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_genre (genre),
    INDEX idx_isbn (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;

CREATE TABLE borrowings (
    borrowing_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    book_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    borrow_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_on DATETIME NOT NULL,

    INDEX idx_book_id (book_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_due_on (due_on),

    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;

CREATE TABLE sales (
    sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    book_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    quantity_sold INT NOT NULL,
    sale_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,

    INDEX idx_book_id (book_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_sale_at (sale_at),

    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;

CREATE TABLE returns (
return_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    borrowing_id BIGINT NOT NULL,
    book_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    borrow_at DATETIME NOT NULL,
    due_on DATETIME NOT NULL,
    return_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,

    INDEX idx_borrowing_id (borrowing_id),
    INDEX idx_book_id (book_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_return_at (return_at),

    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;