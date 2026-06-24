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

INSERT INTO availablebooks (book_id, title, author, isbn, price, quantity, genre) VALUES
(1,'The Great Gatsby','F. Scott Fitzgerald','9780743273565',1078.17,15,'Classic'),
(2,'To Kill a Mockingbird','Harper Lee','9780061120084',1203.50,12,'Fiction'),
(3,'1984','George Orwell','9780451524935',912.17,20,'Dystopian'),
(4,'Pride and Prejudice','Jane Austen','9780141439518',829.17,18,'Romance'),
(5,'The Hobbit','J.R.R. Tolkien','9780547928227',1307.25,10,'Fantasy'),
(6,'The Catcher in the Rye','J.D. Salinger','9780316769174',933.75,8,'Fiction'),
(7,'Harry Potter and the Sorcerer\'s Stone','J.K. Rowling','9780590353427',1576.17,25,'Fantasy'),
(8,'The Da Vinci Code','Dan Brown','9780307474278',1161.17,14,'Mystery'),
(9,'The Alchemist','Paulo Coelho','9780061122415',1037.50,22,'Fiction'),
(10,'The Hunger Games','Suzanne Collins','9780439023481',995.17,16,'Dystopian'),
(11,'The Shining','Stephen King','9780307743657',1244.17,9,'Horror'),
(12,'Dune','Frank Herbert','9780441172719',1369.50,7,'Science Fiction'),
(13,'The Lord of the Rings','J.R.R. Tolkien','9780544003415',2074.17,11,'Fantasy'),
(14,'Gone Girl','Gillian Flynn','9780307588371',1099.75,13,'Thriller'),
(15,'The Book Thief','Markus Zusak','9780375831003',1058.25,6,'Historical Fiction');

INSERT INTO borrowedbooks (borrow_id, book_id, borrower_name, borrower_email, borrower_phone, borrow_date, due_date) VALUES
(1,3,'John Smith','john.smith@email.com','555-0101','2025-01-15','2025-02-15'),
(2,7,'Sarah Johnson','sarah.j@email.com','555-0102','2025-01-18','2025-02-18'),
(3,11,'Mike Wilson','mike.wilson@email.com','555-0103','2025-01-20','2025-02-20'),
(4,5,'Emily Davis','emily.davis@email.com','555-0104','2025-01-22','2025-02-22'),
(5,9,'David Brown','david.b@email.com','555-0105','2025-01-25','2025-02-25'),
(6,2,'Lisa Anderson','lisa.a@email.com','555-0106','2025-01-28','2025-02-28'),
(7,14,'Robert Taylor','robert.t@email.com','555-0107','2025-01-30','2025-03-01'),
(8,8,'Jennifer Martinez','jennifer.m@email.com','555-0108','2025-02-01','2025-03-03');

INSERT INTO borrowedbooksales (borrow_sale_id, borrow_id, book_id, borrower_name, borrower_email, borrower_phone, borrow_date, due_date, return_date, fine_amount, total_amount, transaction_date) VALUES
(11,101,1,'Tom Harris','tom.harris@email.com','555-0201','2024-12-01','2024-12-15','2024-12-14',0.00,0.00,'2024-12-14'),
(12,102,4,'Nancy Green','nancy.green@email.com','555-0202','2024-12-05','2024-12-19','2024-12-20',50.00,50.00,'2024-12-20'),
(13,103,6,'Paul King','paul.king@email.com','555-0203','2024-12-10','2024-12-24','2024-12-23',0.00,0.00,'2024-12-23'),
(14,104,10,'Rachel Scott','rachel.scott@email.com','555-0204','2024-12-15','2024-12-29','2025-01-02',200.00,200.00,'2025-01-02'),
(15,105,12,'Steven Young','steven.young@email.com','555-0205','2024-12-20','2025-01-03','2025-01-03',0.00,0.00,'2025-01-03'),
(16,106,13,'Amanda Walker','amanda.walker@email.com','555-0206','2024-12-25','2025-01-08','2025-01-10',100.00,100.00,'2025-01-10'),
(17,107,15,'Brian Allen','brian.allen@email.com','555-0207','2024-12-28','2025-01-11','2025-01-11',0.00,0.00,'2025-01-11'),
(18,108,2,'Michelle Lewis','michelle.lewis@email.com','555-0208','2025-01-02','2025-01-16','2025-01-15',0.00,0.00,'2025-01-15'),
(19,109,5,'Jason Wright','jason.wright@email.com','555-0209','2025-01-05','2025-01-19','2025-01-22',150.00,150.00,'2025-01-22'),
(20,110,8,'Karen Hall','karen.hall@email.com','555-0210','2025-01-08','2025-01-22','2025-01-21',0.00,0.00,'2025-01-21');

INSERT INTO soldbooksales (sale_id, book_id, customer_name, customer_email, quantity_sold, sale_date, unit_price, total_amount) VALUES
(1,1,'Alice Cooper','alice.cooper@email.com',1,'2025-01-10',1078.17,1078.17),
(2,4,'Bob Richardson','bob.richardson@email.com',2,'2025-01-12',829.17,1658.34),
(3,6,'Carol White','carol.white@email.com',1,'2025-01-14',933.75,933.75),
(4,10,'Daniel Clark','daniel.clark@email.com',3,'2025-01-16',995.17,2985.51),
(5,12,'Eva Garcia','eva.garcia@email.com',1,'2025-01-18',1369.50,1369.50),
(6,13,'Frank Miller','frank.miller@email.com',2,'2025-01-20',2074.17,4148.34),
(7,15,'Grace Lee','grace.lee@email.com',1,'2025-01-22',1058.25,1058.25),
(8,1,'Henry Adams','henry.adams@email.com',1,'2025-01-25',1078.17,1078.17),
(9,3,'Irene Scott','irene.scott@email.com',1,'2025-01-28',912.17,912.17),
(10,7,'Kevin Hall','kevin.hall@email.com',2,'2025-02-01',1576.17,3152.34);
