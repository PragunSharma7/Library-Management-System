DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customer_name ON customers(name);
CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_customer_phone ON customers(phone);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    genre TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_book_title ON books(title);
CREATE INDEX idx_book_author ON books(author);
CREATE INDEX idx_book_genre ON books(genre);
CREATE INDEX idx_book_isbn ON books(isbn);

CREATE TABLE borrowings (
    borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    borrow_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_on TIMESTAMP NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_borrowing_book ON borrowings(book_id);
CREATE INDEX idx_borrowing_customer ON borrowings(customer_id);
CREATE INDEX idx_borrowing_due ON borrowings(due_on);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    sale_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_sale_book ON sales(book_id);
CREATE INDEX idx_sale_customer ON sales(customer_id);
CREATE INDEX idx_sale_at ON sales(sale_at);

CREATE TABLE returns (
    return_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrowing_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    borrow_at TIMESTAMP NOT NULL,
    due_on TIMESTAMP NOT NULL,
    return_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_return_borrowing ON returns(borrowing_id);
CREATE INDEX idx_return_book ON returns(book_id);
CREATE INDEX idx_return_customer ON returns(customer_id);
CREATE INDEX idx_return_at ON returns(return_at);

INSERT INTO customers (customer_id, name, email, phone, created_at) VALUES
(1, 'Tom Harris', 'tom.harris@email.com', '555-0201', '2026-05-17 09:58:00'),
(2, 'Nancy Green', 'nancy.green@email.com', '555-0202', '2026-05-20 09:57:00'),
(3, 'Paul King', 'paul.king@email.com', '555-0203', '2026-05-24 09:58:00'),
(4, 'Rachel Scott', 'rachel.scott@email.com', '555-0204', '2026-05-31 09:57:00'),
(5, 'Steven Young', 'steven.young@email.com', '555-0205', '2026-05-06 09:58:00'),
(6, 'Amanda Walker', 'amanda.walker@email.com', '555-0206', '2026-06-11 09:57:00'),
(7, 'Brian Allen', 'brian.allen@email.com', '555-0207', '2026-06-15 09:58:00'),
(8, 'Michelle Lewis', 'michelle.lewis@email.com', '555-0208', '2026-06-19 09:57:00'),
(9, 'Jason Wright', 'jason.wright@email.com', '555-0209', '2026-06-21 09:58:00'),
(10, 'Karen Hall', 'karen.hall@email.com', '555-0210', '2026-06-25 09:57:00'),
(11, 'Alice Cooper', 'alice.cooper@email.com', '555-0211', '2026-05-11 09:58:00'),
(12, 'Bob Richardson', 'bob.richardson@email.com', '555-0212', '2026-05-15 09:57:00'),
(13, 'Carol White', 'carol.white@email.com', '555-0213', '2026-05-28 09:58:00'),
(14, 'Daniel Clark', 'daniel.clark@email.com', '555-0214', '2026-06-02 09:57:00'),
(15, 'Eva Garcia', 'eva.garcia@email.com', '555-0215', '2026-06-09 09:58:00'),
(16, 'Frank Miller', 'frank.miller@email.com', '555-0216', '2026-06-11 09:57:00'),
(17, 'Grace Lee', 'grace.lee@email.com', '555-0217', '2026-06-14 09:58:00'),
(18, 'Henry Adams', 'henry.adams@email.com', '555-0218', '2026-06-19 09:57:00'),
(19, 'Irene Scott', 'irene.scott@email.com', '555-0219', '2026-06-22 09:58:00'),
(20, 'Kevin Hall', 'kevin.hall@email.com', '555-0220', '2026-06-25 09:57:00'),
(21, 'John Smith', 'john.smith@email.com', '555-0101', '2026-05-15 09:58:00'),
(22, 'Sarah Johnson', 'sarah.j@email.com', '555-0102', '2026-05-23 09:57:00'),
(23, 'Mike Wilson', 'mike.wilson@email.com', '555-0103', '2026-05-28 09:58:00'),
(24, 'Emily Davis', 'emily.davis@email.com', '555-0104', '2026-06-03 09:57:00'),
(25, 'David Brown', 'david.b@email.com', '555-0105', '2026-06-10 09:58:00'),
(26, 'Lisa Anderson', 'lisa.a@email.com', '555-0106', '2026-06-16 09:57:00'),
(27, 'Robert Taylor', 'robert.t@email.com', '555-0107', '2026-06-22 09:58:00'),
(28, 'Jennifer Martinez', 'jennifer.m@email.com', '555-0108', '2026-06-25 09:57:00');

INSERT INTO books (book_id, title, author, isbn, price, quantity, genre, created_at) VALUES
(1, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1078.17, 15, 'Classic', '2026-05-10 09:00:00'),
(2, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 1203.50, 12, 'Fiction', '2026-05-10 09:05:00'),
(3, '1984', 'George Orwell', '9780451524935', 912.17, 20, 'Dystopian', '2026-05-10 09:10:00'),
(4, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 829.17, 18, 'Romance', '2026-05-10 09:15:00'),
(5, 'The Hobbit', 'J.R.R. Tolkien', '9780547928227', 1307.25, 10, 'Fantasy', '2026-05-10 09:20:00'),
(6, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769174', 933.75, 8, 'Fiction', '2026-05-10 09:25:00'),
(7, 'Harry Potter and the Sorcerers Stone', 'J.K. Rowling', '9780590353427', 1576.17, 25, 'Fantasy', '2026-05-10 09:30:00'),
(8, 'The Da Vinci Code', 'Dan Brown', '9780307474278', 1161.17, 14, 'Mystery', '2026-05-10 09:35:00'),
(9, 'The Alchemist', 'Paulo Coelho', '9780061122415', 1037.50, 22, 'Fiction', '2026-05-10 09:40:00'),
(10, 'The Hunger Games', 'Suzanne Collins', '9780439023481', 995.17, 16, 'Dystopian', '2026-05-10 09:45:00'),
(11, 'The Shining', 'Stephen King', '9780307743657', 1244.17, 9, 'Horror', '2026-05-10 09:50:00'),
(12, 'Dune', 'Frank Herbert', '9780441172719', 1369.50, 7, 'Science Fiction', '2026-05-10 09:55:00'),
(13, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 2074.17, 11, 'Fantasy', '2026-05-10 10:00:00'),
(14, 'Gone Girl', 'Gillian Flynn', '9780307588371', 1099.75, 13, 'Thriller', '2026-05-10 09:02:00'),
(15, 'The Book Thief', 'Markus Zusak', '9780375831003', 1058.25, 6, 'Historical Fiction', '2026-05-10 09:08:00');

INSERT INTO borrowings (borrowing_id, book_id, customer_id, borrow_at, due_on) VALUES
(1, 3, 21, '2026-05-15 10:00:00', '2026-05-22 10:00:00'),
(2, 7, 22, '2026-05-23 10:00:00', '2026-06-02 10:00:00'),
(3, 11, 23, '2026-05-28 10:00:00', '2026-06-04 10:00:00'),
(4, 5, 24, '2026-06-03 10:00:00', '2026-06-09 10:00:00'),
(5, 9, 25, '2026-06-10 10:00:00', '2026-06-20 10:00:00'),
(6, 2, 26, '2026-06-16 10:00:00', '2026-06-23 10:00:00'),
(7, 14, 27, '2026-06-22 10:00:00', '2026-06-29 10:00:00'),
(8, 8, 28, '2026-06-25 10:00:00', '2026-07-09 10:00:00');

INSERT INTO sales (sale_id, book_id, customer_id, quantity_sold, sale_at, unit_price, total_amount) VALUES
(1, 1, 11, 1, '2026-05-11 10:30:00', 1078.17, 1078.17),
(2, 4, 12, 2, '2026-05-15 10:45:00', 829.17, 1658.34),
(3, 6, 13, 1, '2026-05-28 11:00:00', 933.75, 933.75),
(4, 10, 14, 3, '2026-06-02 11:15:00', 995.17, 2985.51),
(5, 12, 15, 1, '2026-06-09 11:30:00', 1369.50, 1369.50),
(6, 13, 16, 2, '2026-06-11 10:30:00', 2074.17, 4148.34),
(7, 15, 17, 1, '2026-06-14 11:45:00', 1058.25, 1058.25),
(8, 1, 18, 1, '2026-06-19 10:30:00', 1078.17, 1078.17),
(9, 3, 19, 1, '2026-06-22 11:00:00', 912.17, 912.17),
(10, 7, 20, 2, '2026-06-25 10:45:00', 1576.17, 3152.34);

INSERT INTO returns (return_id, borrowing_id, book_id, customer_id, borrow_at, due_on, return_at, fine_amount, total_amount) VALUES
(1, 1, 3, 21, '2026-05-15 10:00:00', '2026-05-22 10:00:00', '2026-05-17 10:30:00', 0.00, 35.00),
(2, 2, 7, 22, '2026-05-23 10:00:00', '2026-06-02 10:00:00', '2026-05-31 10:45:00', 0.00, 70.00),
(3, 3, 11, 23, '2026-05-28 10:00:00', '2026-06-04 10:00:00', '2026-06-03 11:00:00', 0.00, 35.00),
(4, 4, 5, 24, '2026-06-03 10:00:00', '2026-06-09 10:00:00', '2026-06-09 10:30:00', 0.00, 30.00),
(5, 5, 9, 25, '2026-06-10 10:00:00', '2026-06-20 10:00:00', '2026-06-18 10:45:00', 0.00, 50.00),
(6, 6, 2, 26, '2026-06-16 10:00:00', '2026-06-23 10:00:00', '2026-06-23 11:00:00', 0.00, 35.00),
(7, 7, 14, 27, '2026-06-22 10:00:00', '2026-06-29 10:00:00', '2026-06-28 10:30:00', 0.00, 35.00),
(8, 8, 8, 28, '2026-06-25 10:00:00', '2026-07-09 10:00:00', '2026-07-08 10:45:00', 0.00, 70.00);