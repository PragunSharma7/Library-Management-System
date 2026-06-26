import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import get_style

load_dotenv()

MENU_STYLE = get_style({
    "questionmark": "#e5c07b", 
    "question": "#ffffff bold",     
    "pointer": "#61afef bold",    
    "answer": "#61afef",
    }, style_override=True)

def isFloatP(x):
    try: 
        return float(x)>0
    except ValueError:
        return False

def configureSetting():

    dbHost = inquirer.text(
        message = "DB_HOST: ",
        default = os.getenv('DB_HOST') or '',
        style = MENU_STYLE
    ).execute()
    dbUser = inquirer.text(
        message = "DB_USER: ",
        default = os.getenv('DB_USER') or '',
        style = MENU_STYLE
    ).execute()
    dbPassword = inquirer.text(
        message = "DB_PASSWORD: ",
        default = os.getenv('DB_PASSWORD') or '',
        style = MENU_STYLE
    ).execute()
    dbName = inquirer.text(
        message = "DB_NAME: ",
        default = os.getenv('DB_NAME') or '',
        style = MENU_STYLE
    ).execute()
    lowStock = inquirer.text(
        message = "LOW_STOCK: ",
        default = os.getenv('LOW_STOCK') or '',
        validate =lambda x: x.isdigit() and int(x)>0,
        invalid_message = "Must be positive integer",
        style = MENU_STYLE
    ).execute()
    finePerDay = inquirer.text(
        message = "FINE_PER_DAY: ",
        default = os.getenv('FINE_PER_DAY') or '',
        validate = isFloatP,
        invalid_message = "Must be positive number",
        style = MENU_STYLE
    ).execute()
    borrowFeePerDay = inquirer.text(
        message = "BOWWOW_FEE_PER_DAY: ",
        default = os.getenv('BORROW_FEE_PER_DAY') or '',
        validate = isFloatP,
        invalid_message = "Must be positive number",
        style = MENU_STYLE
    ).execute()

    setting = {
        'DB_HOST': dbHost,
        'DB_USER': dbUser,
        'DB_PASSWORD': dbPassword,
        'DB_NAME': dbName,
        'LOW_STOCK': lowStock,
        'FINE_PER_DAY': finePerDay,
        'BORROW_FEE_PER_DAY': borrowFeePerDay
    }

    with open('.env','w',encoding='utf-8') as env:
        for key in setting:
            env.write(f"{key}={setting[key]}\n")

    load_dotenv(override=True)
    
    print("Settings Updated")

def validateSettings():

    required = [
        'DB_HOST',
        'DB_USER',
        'DB_PASSWORD',
        'DB_NAME',
        'LOW_STOCK',
        'FINE_PER_DAY',
        'BORROW_FEE_PER_DAY'
    ]

    for key in required:
        value = os.getenv(key)
        if value is None or value.strip() == '':
            configureSetting()
            return

class BookStore() :
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv('DB_HOST'),
                user = os.getenv('DB_USER'),
                database = os.getenv("DB_NAME"),
                password = os.getenv("DB_PASSWORD")
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def executeQuery(self, query, params = None, fetch = False):
        try:
            self.cursor.execute(query, params or tuple())

            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        
        except Error as e:
            print(f"Database error {e}")
            return None
        
    def addCustomer(self):
        print("\n=== ADD NEW CUSTOMER ===")

        name = inquirer.text("Enter Customer Name: ", style = MENU_STYLE).execute()
        email = inquirer.text("Enter Customer Email: ", style = MENU_STYLE).execute()
        phone = inquirer.text("Enter Customer Phone: ", style = MENU_STYLE).execute()

        existing = self.executeQuery("""SELECT customer_id FROM customers WHERE  email = %s""",
                                     (email,), fetch = True)
        
        if existing and len(existing) > 0: 
            print(f"Error: The Given already exists with Customer ID {existing[0]['customer_id']}")
            return
        
        if self.executeQuery("""INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)""",
                             (name, email, phone)):
            print("Customer added sucessfully")
        else:
            print("Failed to add Customer")
        
    def viewCustomers(self):
        print("\n=== VIEW CUSTOMERS ===")

        customers = self.executeQuery("SELECT * FROM customers ORDER BY name",
                                  fetch = True)
        if not customers:
            print("No customer found")
            return
        
        print(f"\n{'ID':<4} {'Name':<30} {'Email':<30} {'Phone':<10} {'Created At':<12}")
        print("-" * 86)

        for customer in customers:
            print(f"{customer['customer_id']:<4} {customer['name'][:29]:<30} {customer['email'][:29]:<30} {customer['phone']:<10} {customer['created_at'].strftime('%Y-%m-%d'):<12}")

    def searchCustomer(self):
        print("\n=== SEARCH CUSTOMER ===")

        search_options = {
            'Name': {
                'prompt': "Enter Name to search: ",
                'query': "SELECT * FROM customers WHERE name LIKE %s ORDER BY name",
                'transform': lambda x : f"%{x}%"
            },
            'Email': {
                'prompt': "Enter Email to search: ",
                'query': "SELECT * FROM customers WHERE email LIKE %s ORDER BY name",
                'transform': lambda x : f"%{x}%"
            },
            'Phone': {
                'prompt': "Enter Phone to search: ",
                'query': "SELECT * FROM customers WHERE phone LIKE %s ORDER BY name",
                'transform': lambda x : f"%{x}%"
            },
            'Customer ID': {
                'prompt': "Enter Customer ID to search: ",
                'query': "SELECT * FROM customers WHERE customer_id = %s ORDER BY name",
                'transform': lambda x : f"{x}"
            },
        }


        choice = inquirer.select(
            message="Search customer by:",
            choices=list(search_options.keys()),
            default=0,
            pointer=" ➤",
            qmark="🔍",
            style = MENU_STYLE
        ).execute()

        config = search_options[choice]

        term = inquirer.text(
            message=config["prompt"]
        ).execute()

        customers = self.executeQuery(
            config["query"],
            (config["transform"](term),),
            fetch = True
        )

        if not customers:
            print("No books found")
            return
        
        print(f"\n{'ID':<4} {'Name':<30} {'Email':<30} {'Phone':<10} {'Created At':<12}")
        print("-" * 86)

        for customer in customers:
            print(f"{customer['customer_id']:<4} {customer['name'][:29]:<30} {customer['email'][:29]:<30} {customer['phone']:<10} {customer['created_at'].strftime('%Y-%m-%d'):<12}")
        
    def updateCustomers(self):
        print("\n=== UPDATE CUSTOMERS ===")


        customerId = int(inquirer.text("Enter Customer ID to update: ",
                                    validate = lambda x: x.isdigit() and int(x)>0,
                                    invalid_message = "Please enter a valid number",
                                    style = MENU_STYLE).execute())

        customer = self.executeQuery("SELECT * FROM customers WHERE customer_id = %s",(customerId,), fetch = True)
        if not customer:
            print("Book not found")
            return
        
        customer = customer[0]

        print("\nEnter new details (press Enter to keep current value)")

        name = inquirer.text("Name: ",
                              default = str(customer['name']),
                              style = MENU_STYLE).execute()
        email = inquirer.text("Email: ",
                               default = str(customer['email']),
                               style = MENU_STYLE).execute()
        phone = inquirer.text("Phone: ",
                              default = str(customer['phone']),
                              style = MENU_STYLE).execute() 

        if self.executeQuery("""UPDATE customers
                             SET name = %s, email = %s, phone = %s
                             WHERE customer_id = %s""",
                             (name, email, phone, customerId)):
            print("Customer updated successfully")
        else:
            print("Failed to update customer")

    def deleteCustomer(self):
        print("\n=== DELETE CUSTOMER ===")

        customerId = int(inquirer.text("Enter Customer ID to update: ",
                                    validate = lambda x: x.isdigit() and int(x)>0,
                                    invalid_message = "Please enter a valid number",
                                    style = MENU_STYLE).execute())
    
        customer = self.executeQuery("""SELECT name FROM customers 
                                 WHERE customer_id = %s""",
                                 (customerId,), fetch = True)
        if not customer:
            print("Customer not found")
            return
        
        print(f"Customer to delete: {customer[0]['name']}")

        if inquirer.text("Are you sure you want to delete customer? (y/n): ", style = MENU_STYLE).execute().lower() != 'y':
            print("Deletion cancelled")
            return

        if self.executeQuery("DELETE FROM customers WHERE customer_id = %s",
                             (customerId,)):
            print("Customer deleted Successfully")
        else:
            print("Failed to delete customer")

        
    def addBook(self):
        print("\n=== ADD NEW BOOK ===")

        title = inquirer.text("Enter book title: ", style = MENU_STYLE).execute()
        author = inquirer.text("Enter author: ", style = MENU_STYLE).execute()
        isbn = inquirer.text("Enter ISBN: ", style = MENU_STYLE).execute()

        existing = self.executeQuery("""SELECT book_id FROM books 
                                     WHERE isbn = %s""",(isbn,), fetch = True)
        
        if existing:
            print("Error: A book with this ISBN already exists")
            return
        
        try:
            price = float(inquirer.text("Enter price (₹): ",
                                        validate = isFloatP,
                                        invalid_message = "Please enter valid number",
                                        style = MENU_STYLE).execute())
            quantity = int(inquirer.text("Enter quantity: ", 
                                         validate= lambda x: x.isdigit() and int(x)>0,
                                         invalid_message = "Please enter valid number",
                                         style = MENU_STYLE).execute())
            genre = inquirer.text("Enter genre: ", style = MENU_STYLE).execute()
        except ValueError:
            print("Error: Please enter Valid numeric quantities for Pries and Quantity")
            return
        
        if self.executeQuery("""INSERT INTO books
                             (title, author, isbn, price, quantity, genre)
                             VALUES (%s, %s, %s, %s, %s, %s)""",
                             (title, author, isbn, price, quantity, genre)):
            print("Book added sucessfully")
        else:
            print("Failed to add book")
        
    def viewAvaliable(self):
        print("\n=== AVAILAVLE BOOK INVENTORY ===")

        books = self.executeQuery("SELECT * FROM books ORDER BY title",
                                  fetch = True)
        if not books:
            print("No books found in inventory")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Price':<10} {'Qty':<15} {'ISBN':<15} {'Genre':<15} {'From':<12}")
        print("-" * 117)

        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} ₹{book['price']:<9.2f} {book['quantity']:<4} {book['isbn']:<15} {book['genre'] or 'N/A':<15} {book['created_at'].strftime('%Y-%m-%d'):12}")

    def searchBook(self):
        print("\n=== SEARCH BOOKS ===")

        search_options = {
            'Title': {
                'prompt': "Enter title to search: ",
                'query': "SELECT * FROM books WHERE title LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%",
                'validate': lambda x: True,
                'invalid_message': ""
            },
            'Author': {
                'prompt': "Enter author to search: ",
                'query': "SELECT * FROM books WHERE author LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%",
                'validate': lambda x: True,
                'invalid_message': ""
            },
            'Genre': {
                'prompt': "Enter genre to search: ",
                'query': "SELECT * FROM books WHERE genre LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%",
                'validate': lambda x: True,
                'invalid_message': ""
            },
            'ISBN': {
                'prompt': "Enter isbn to search: ",
                'query': "SELECT * FROM books WHERE isbn = %s ORDER BY title",
                'transform': lambda x : f"{x}",
                'validate': lambda x: len(str(x)) > 0,
                'invalid_message': "Please enter valid ISBN"
            },
        }


        choice = inquirer.select(
            message="Search books by:",
            choices=list(search_options.keys()),
            default=0,
            pointer=" ➤",
            qmark="🔍",
            style = MENU_STYLE
        ).execute()

        config = search_options[choice]

        term = inquirer.text(
            message=config["prompt"],
            validate=config["validate"],
            invalid_message=config['invalid_message']
        ).execute()

        books = self.executeQuery(
            config["query"],
            (config["transform"](term),),
            fetch = True
        )

        if not books:
            print("No books found")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Price':<10} {'Qty':<4} {'ISBN':<15} {'Genre':<15} {'From':<12}")
        print("-" * 107)
        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['price']:<9} {book['quantity']:<4} {book['isbn']:<15} {book['genre'] or 'N/A':<15} {book['created_at'].strftime('%Y-%m-%d'):12}")
        
    def updateBook(self):
        print("\n=== UPDATE BOOKS ===")

        try:
            bookId = int(inquirer.text("Enter book ID to update: ", style = MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return
        book = self.executeQuery("SELECT * FROM books WHERE book_id = %s",(bookId,), fetch = True)
        if not book:
            print("Book not found")
            return
        
        book = book[0]

        print("\nEnter new details (press Enter to keep current value)")

        title = inquirer.text("Title: ",
                              default = str(book['title']),
                              style = MENU_STYLE).execute()
        author = inquirer.text("Author: ",
                               default = str(book['author']),
                               style = MENU_STYLE).execute()
        price = inquirer.text("Price: ₹",
                              default = str(book['price']),
                              style = MENU_STYLE).execute() 
        quantity = inquirer.text("Quantity: ",
                                 default = str(book['quantity']),
                                 style = MENU_STYLE).execute() 
        genre = inquirer.text("Genre: ",
                              default = str(book['genre'] or ""),
                              style = MENU_STYLE).execute() 

        if self.executeQuery("""UPDATE books 
                             SET title = %s, author = %s, price = %s, quantity = %s, genre = %s
                             WHERE book_id = %s""",
                             (title, author, price, quantity, genre, int(bookId))):
            print("Book updated successfully")
        else:
            print("Failed to update book")

    def deleteBook(self):
        print("\n=== DELETE BOOK ===")
        try:
            bookId = int(inquirer.text("Enter book ID to delete: ", style = MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return
    
        book = self.executeQuery("""SELECT title FROM books WHERE book_id = %s""",
                                 (bookId,), fetch = True)
        if not book:
            print("Book not found")
            return
        
        print(f"Book to delete: {book[0]['title']}")

        if inquirer.text("Are you sure you want to delete book? (y/n): ", style = MENU_STYLE).execute().lower() != 'y':
            print("Deletion cancelled")
            return

        if self.executeQuery("DELETE FROM books WHERE book_id = %s",
                             (bookId,)):
            print("Book deleted Successfully")
        else:
            print("Failed to delete book")

    def sellBook(self):
        print("\n=== SELL BOOK ===")
        bookId = int(inquirer.text("Enter book ID to sell: ",
                                   validate = lambda x: x.isdigit() and int(x)>0,
                                   invalid_message = "Please enter a valid number",
                                   style = MENU_STYLE).execute())

        try:
            book = self.executeQuery("SELECT * FROM books WHERE book_id = %s",
                                    (bookId,), fetch = True)
        except Error as e:
            print(f"Error in finding book: {e}")
            return
        
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        print(f"Book: {book['title']} by {book['author']}")
        print(f"Available quantity: {book['quantity']}")
        print(f"Price: ₹{book['price']:.2f}")

        
        quantitySold = int(inquirer.text("Enter quantity to sell: ",
                                            validate = lambda x: x.isdigit() and int(x)>0,
                                            invalid_message = "Please enter a valid number",
                                            style = MENU_STYLE).execute())

        if quantitySold > int(book['quantity']):
            print("Insufficient quantity in stock")
            return
        
        customerId = int(inquirer.text("Enter Customer ID: ",
                                    validate = lambda x: x.isdigit() and int(x)>0,
                                    invalid_message = "Please enter a valid number",
                                    style = MENU_STYLE).execute())
        
        customer = self.executeQuery("SELECT * FROM customers WHERE customer_id = %s", (customerId,), fetch=True)
        if not customer:
            print("Customer not found. Please add the customer first.")
            return


        totalAmount = quantitySold  * float(book['price'])
        saleDate = datetime.now()

        try: 
            self.cursor.execute("UPDATE books SET quantity = quantity - %s WHERE book_id = %s",
                                (quantitySold, bookId))
            self.cursor.execute("""INSERT INTO sales 
                                (book_id, customer_id, quantity_sold, unit_price, total_amount)
                                VALUES (%s, %s, %s, %s, %s)""",
                                (bookId, customerId, quantitySold, book['price'], totalAmount))
            self.connection.commit()

            print(f"Sale completed successfully")
            print(f"Total amount: ₹{totalAmount:.2f}")
        except Error as e:
            self.connection.rollback()
            print(f"Error processing sale: {e}")
        
    def viewRevenueReport(self):
        print("\n=== COMPRENSIVE SALES REPORT ===")

        bookSales = self.executeQuery("""SELECT s.sale_at as sale_date, b.title, b.author, c.name as customer_name, s.quantity_sold, 
                                      s.unit_price, s.total_amount, 'Book Sale' as transaction_type
                                      FROM sales s
                                      JOIN books b ON s.book_id = b.book_id
                                      JOIN customers c ON s.customer_id = c.customer_id
                                      WHERE DATE(s.sale_at) >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                      ORDER BY s.sale_at DESC""", fetch = True)
        borrowingRevenue = self.executeQuery("""SELECT r.return_at as sale_date, b.title, b.author, 
                                             c.name as customer_name, 1 as quantity_sold,
                                             r.fine_amount as unit_price, r.total_amount,
                                             'Borrowing Fine' as transaction_type
                                             FROM returns r
                                             JOIN books b ON r.book_id = b.book_id
                                             JOIN customers c ON r.customer_id = c.customer_id
                                             WHERE DATE(r.return_at) >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                             ORDER BY r.return_at DESC""", fetch = True)
        
        allTransactions = (bookSales or []) + (borrowingRevenue or [])
        allTransactions.sort(key = lambda x: x['sale_date'], reverse = True)

        print(f"\n{'Date':<12} {'Type':<20} {'Customer':<15} {'Qty':<4} {'Amount':<10}")
        print("-" * 85)
        totalSalesRevenue, totalBorrowingRevenue = 0, 0

        for transaction in allTransactions:
            print(f"{transaction['sale_date'].strftime('%Y-%m-%d'):<12} {transaction['transaction_type']:<15} {transaction['title'][:19]:<20} {transaction['customer_name'][:14]:<15} {transaction['quantity_sold']:<4} ₹{transaction['total_amount']:<9.2f}")
            if transaction['transaction_type'] == 'Book Sale': 
                totalSalesRevenue += int(transaction['total_amount'])
            else:
                totalBorrowingRevenue += int(transaction['total_amount'])
        
        print("-"*85)
        print("\nREVENEUE SUMMARY")
        print(f"Book Sales Revenue: ₹{totalSalesRevenue:.2f}")
        print(f"Borrowing Revenue: ₹{totalBorrowingRevenue:.2f}")
        print(f"Grand Total Revenue: ₹{totalSalesRevenue + totalBorrowingRevenue:.2f}")

    def viewRevenueReportSeperate(self):
        print("\n=== DETAILED SALES REPORT ===")

        print("--- BOOK SALES ---")
        bookSales = self.executeQuery("""SELECT s.book_id, b.title, b.author, c.name,
                                      s.quantity_sold, s.unit_price, s.total_amount, s.sale_at
                                      FROM sales s 
                                      JOIN books b ON s.book_id = b.book_id
                                      JOIN customers c ON s.customer_id = c.customer_id
                                      WHERE DATE(s.sale_at) >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                      ORDER BY s.sale_at DESC""", fetch = True)
        print(f"\n{'Date':<12} {'Title':<20} {'Customer':<15} {'Qty':<4} {'Price':<8} {'Total':<10}")
        print("-" * 75)
        totalSalesRevenue, totalBorrowingRevenue = 0, 0
        for sale in (bookSales or []):
            print(f"{sale['sale_at'].strftime('%Y-%m-%d') or 'N/A':<12} {sale['title'][:19]<20} {sale['name'][:14]:<15} {sale['quantity_sold']:<4} ₹{sale['unit_price']:<7.2f} ₹{sale['total_amount']:<9.2f}")
            totalSalesRevenue += sale['total_amount']
        print(f"\nTotal Book Sales Revenue: ₹{totalSalesRevenue:.2f}")


        print("\n--- BORROWING FINES ---")
        borrowingRevenue = self.executeQuery("""SELECT r.return_at, b.title, b.author, 
                                             c.name, r.fine_amount, r.total_amount,
                                             DATEDIFF(DATE(r.return_at), DATE(r.due_on)) as days_overdue
                                             FROM returns r
                                             JOIN books b ON r.book_id = b.book_id
                                             JOIN customers c ON r.customer_id = c.customer_id
                                             WHERE DATE(r.return_at) >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                             ORDER BY r.return_at DESC""", fetch = True)
        print(f"\n{'Date':<12} {'Title':<20} {'Borrower':<15} {'Days':<4} {'Fine':<10}")
        print('-'*70)
        for item in (borrowingRevenue or []):
            print(f"{item['return_at'].strftime('%Y-%m-%d'):<12} {item['title'][:19]:<20} {item['name'][:14]:<15} {item['days_overdue'] or 0:<4} ₹{item['total_amount']:<9.2f}")
            totalBorrowingRevenue += item['total_amount']
        print(f"\nTotal Borrowing Revenue: ₹{totalBorrowingRevenue:.2f}")

        print("\n" + "="*50)
        print("REVENUE SUMMARY")
        print(f"Book Sales: ₹{totalSalesRevenue:.2f}")
        print(f"Borrowing Revenue: ₹{totalBorrowingRevenue:.2f}")
        print(f"Grand total: ₹{totalSalesRevenue+totalBorrowingRevenue:.2f}")
        print("="*50)

    def borrowBook(self):
        print("\n=== BORROW BOOK ===")
        bookId= int(inquirer.text("Enter book ID to borrow: ",
                                  validate = lambda x: x.isdigit() and int(x)>0,
                                  invalid_message = "Please enter a valid number",
                                  style = MENU_STYLE).execute())

        book = self.executeQuery("SELECT * FROM books WHERE book_id = %s",
                                 (bookId,), fetch = True)
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        if int(book['quantity']) == 0:
            print("Book is out of stock")
            return
        
        print(f"Book: {book['title']} by {book['author']}")

        customerId = int(inquirer.text("Enter Customer ID: ",
                                    validate = lambda x: x.isdigit() and int(x)>0,
                                    invalid_message = "Please enter a valid number",
                                    style = MENU_STYLE).execute())
        
        customer = self.executeQuery("SELECT * FROM customers WHERE customer_id = %s", (customerId,), fetch=True)
        if not customer:
            print("Customer not found. Please add the customer first.")
            return


        borrowDays = int(inquirer.text("Enter number of days to borrow: ",
                                        validate = lambda x: x.isdigit() and int(x)>0,
                                        invalid_message = "Please enter a valid number",
                                        style = MENU_STYLE).execute())


        borrowDate = datetime.now()
        dueDate = borrowDate + timedelta(days = borrowDays)

        try:
            self.cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s",
                                (bookId,))
            self.cursor.execute("""INSERT INTO borrowings (book_id, customer_id, borrow_at, due_on)
                                VALUES (%s, %s, %s, %s)""",
                                (bookId, customerId, borrowDate, dueDate))
            self.connection.commit()
            print("Borrowed Book Sucessfully")
            print(f"Due date: {dueDate}")

        except Error as e:
            self.connection.rollback()
            print(f"Error processsing borrowing: {e}")

    def returnBook(self):
        print("\n=== RETURN BORROWED BOOK ===")

        borrowId = int(inquirer.text("Enter borrow ID to return: ",
                                        validate = lambda x: x.isdigit() and int(x)>0,
                                        invalid_message = "Please enter a valid number",
                                        style = MENU_STYLE).execute())


        borrowRecord = self.executeQuery("""SELECT bb.*, b.title, b.author, c.name
                                         FROM borrowings bb 
                                         JOIN books b ON bb.book_id = b.book_id 
                                         JOIN customers c ON bb.customer_id = c.customer_id
                                         WHERE bb.borrowing_id = %s""",
                                         (borrowId,), fetch = True)
        if not borrowRecord:
            print("Borrow record not found")
            return

        borrowRecord = borrowRecord[0]
        print(f"Book: {borrowRecord['title']} by {borrowRecord['author']}")
        print(f"Borrower: {borrowRecord['name']}")
        print(f"Due Date: {borrowRecord['due_on']}")

        returnDate = datetime.now()
        dueDate = borrowRecord['due_on']
        borrowDate = borrowRecord['borrow_at']

        if returnDate > dueDate:
            daysOverdue = (returnDate - dueDate).days
            fineAmount = daysOverdue * float(os.getenv("FINE_PER_DAY"))
            print(f"Book is {daysOverdue} days overdue. Fine: ₹{fineAmount:.2f}")
        else:
            fineAmount = 0

        totalAmount = (dueDate - borrowDate).days * float(os.getenv("BORROW_FEE_PER_DAY"))
        try:
            self.cursor.execute("""INSERT INTO returns (borrowing_id, book_id, customer_id, borrow_at, due_on, 
                                fine_amount, total_amount)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                (borrowId, borrowRecord['book_id'], borrowRecord['customer_id'], borrowRecord['borrow_at'], borrowRecord['due_on'],
                                 fineAmount, totalAmount))
            self.cursor.execute("DELETE FROM borrowings WHERE borrowing_id = %s",
                                (borrowId,))
            self.cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s",
                                (borrowRecord['book_id'],))
            self.connection.commit()
            print("Book returned successfully")
        except Error as e:
            self.connection.rollback()
            print(f"Error processing return: {e}")

    def viewBorrowedBook(self):
        print("\n=== CURRENTLY BORROWED BOOKS ===")

        borrowedBooks = self.executeQuery("""SELECT bb.borrowing_id, c.name, bb.borrow_at, bb.due_on, 
                                          b.title, b.author, b.isbn, DATEDIFF(CURDATE(), DATE(bb.due_on)) as days_overdue
                                          FROM borrowings bb JOIN books b ON bb.book_id = b.book_id
                                          JOIN customers c ON bb.customer_id = c.customer_id
                                          ORDER BY bb.due_on ASC""",
                                          fetch = True)
        if not borrowedBooks:
            print("No currently borrowed books")
            return
        
        print(f"\n{'BorrowID':<8} {'Borrower':<15} {'Title':<20} {'Borrow Date':<12} {'Due Date':<12} {'Overdue':<8}")
        print("-" * 80)

        for book in borrowedBooks:
            # to many this time
            borrowDate = book['borrow_at'].strftime('%Y-%m-%d') if book['borrow_at'] else 'N/A'
            dueDate = book['due_on'].strftime('%Y-%m-%d') if book['due_on'] else 'N/A'
            overdue = book['days_overdue'] if book['days_overdue'] and book['days_overdue'] > 0 else 0
            status = f"{overdue} days" if overdue > 0 else "On time"
            print(f"{book['borrowing_id']:<8} {book['name'][:14]:<15} {book['title'][:19]:<20} {borrowDate:<12} {dueDate:<12} {status:<8}")

    def viewBorrowingHistory(self):
        print("\n=== BORROWING HISTORY ===")

        history = self.executeQuery("""SELECT r.borrowing_id, c.name, b.title,
                                    r.borrow_at, r.due_on, r.return_at, r.fine_amount, r.total_amount
                                    FROM returns r JOIN books b ON r.book_id = b.book_id
                                    JOIN customers c ON r.customer_id = c.customer_id
                                    ORDER BY r.return_at DESC
                                    LIMIT 30""", fetch = True)
        if not history:
            print("No borrowing history found")
            return
        
        print(f"\n{'BorrowID':<8} {'Borrower':<15} {'Title':<20} {'Borrow Date':<12} {'Return Date':<12} {'Fine':<10}")
        print("-" * 80)
        
        for record in history:
            borrowDate = record['borrow_at'].strftime('%Y-%m-%d') if record['borrow_at'] else 'N/A'
            returnDate = record['return_at'].strftime('%Y-%m-%d') if record['return_at'] else 'N/A'
            totalAmt = f"₹{record['fine_amount']:.2f}" if record['total_amount'] and record['total_amount'] > 0 else "None"
            print(f"{record['borrowing_id']:<8} {record['name'][:14]:<15} {record['title'][:19]:<20} {borrowDate:<12} {returnDate:<12} {totalAmt:<10}")

    def viewSalesHistory(self): 
        print("\n=== SALES HISTORY ===")

        history = self.executeQuery("""SELECT s.sale_id, c.name, b.title, s.sale_at,
                                    s.quantity_sold, s.unit_price, s.total_amount
                                    FROM sales s JOIN books b ON s.book_id = b.book_id
                                    JOIN customers c ON s.customer_id = c.customer_id
                                    ORDER BY s.sale_at DESC LIMIT 30 """, fetch = True)

        if not history:
            print("No sales history found")
            return

        print(f"\n{'SaleID':<8} {'Customer':<15} {'Title':<20} {'Date':<12} {'Qty':<5} {'Amount':<10}")
        print("-" * 80)

        for record in history:
            saleDate = record['sale_at'].strftime('%Y-%m-%d') if record['sale_at'] else 'N/A'
            print(f"{record['sale_id']:<8} {record['name'][:14]:<15} {record['title'][:19]:<20} {saleDate:<12} {record['quantity_sold']:<5} ₹{record['total_amount']:<9.2f}")

    def viewLowStock(self):
        print("\n=== LOW STOCK ALERT ===")

        books = self.executeQuery("SELECT * FROM books WHERE quantity < %s ORDER BY quantity ASC",
                                  (int(os.getenv("LOW_STOCK")),), fetch = True)
        
        if not books:
            print("No books with low stock!")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Qty':<4} {'Price':<10}")
        print("-" * 75)
        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['quantity']:<4} ₹{book['price']:<9}")

def main():
    validateSettings()

    bookstore = BookStore()

    menu = {
        "Add Customer": bookstore.addCustomer,
        "View Customers": bookstore.viewCustomers,
        "Search Customers": bookstore.searchCustomer,
        "Update Customers": bookstore.updateCustomers,
        "Delete Customer": bookstore.deleteCustomer,
        "Add Book": bookstore.addBook,
        "View Books": bookstore.viewAvaliable,
        "Search Books": bookstore.searchBook,
        "Update Books": bookstore.updateBook,
        "Delete Book": bookstore.deleteBook,
        "Sell Book": bookstore.sellBook,
        "View Revenue Report": bookstore.viewRevenueReport,
        "View Revenue Report Seperate": bookstore.viewRevenueReportSeperate,
        "Borrow Book": bookstore.borrowBook,
        "Return Book": bookstore.returnBook,
        "View Currently Borrowed Books": bookstore.viewBorrowedBook,
        "View Borrowing History": bookstore.viewBorrowingHistory,
        "View Sales History": bookstore.viewSalesHistory,
        "View Low Stock": bookstore.viewLowStock,
        "Setting": configureSetting,
        "Exit": lambda: (None),
        }

    if not bookstore.connection.is_connected():
        print("Failed to connect. Please check the MySQL configurations")
        return
    
    print("Welcome to Book Store Mannagement System")

    while True:
        choice = inquirer.select(
            message = "BOOK STORE MANAGEMENT SYSTEM",
            choices = list(menu.keys()),
            default = 0,
            pointer = " ➤",
            qmark = "📚",
            style = MENU_STYLE,
        ).execute()

        if choice == "Exit":
            bookstore.disconnect()
            break

        menu[choice]()


if __name__ == "__main__":
    main()


