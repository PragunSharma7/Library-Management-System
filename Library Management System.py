import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import get_style

load_dotenv()

MENU_STYLE = get_style({"questionmark": "#e5c07b", 
                        "question": "#ffffff bold",     
                        "pointer": "#61afef bold",    
                        "answer": "#61afef",},
                        style_override=True)

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

    def executeQuery(self, query, params=None,fetch=False):
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
        
        
    def addBook(self):
        print("\n=== ADD NEW BOOK ===")

        title = inquirer.text("Enter book title: ",style=MENU_STYLE).execute()
        author = inquirer.text("Enter author: ",style=MENU_STYLE).execute()
        isbn = inquirer.text("Enter ISBN: ",style=MENU_STYLE).execute()

        existing = self.executeQuery("""SELECT book_id FROM availablebooks 
                                     WHERE isbn = %s""",(isbn,), fetch=True)
        
        if existing:
            print("Error: A book with this ISBN already exists")
            return
        
        try:
            price = float(inquirer.text("Enter price (₹): ",style=MENU_STYLE).execute())
            quantity = int(inquirer.text("Enter quantity: ",style=MENU_STYLE).execute())
            genre = inquirer.text("Enter genre: ",style=MENU_STYLE).execute()
        except ValueError:
            print("Error: Please enter Valid numeric quantities for Pries and Quantity")
            return
        
        if self.executeQuery("""INSERT INTO availablebooks
                             (title, author, isbn, price, quantity, genre)
                             VALUES (%s, %s, %s, %s, %s, %s)""",
                             (title, author, isbn, price, quantity, genre)):
            print("Book added sucessfully")
        else:
            print("Failed to add book")
        
    def viewAvaliable(self):
        print("\n=== AVAILAVLE BOOK INVENTORY ===")

        books = self.executeQuery("SELECT * FROM availablebooks ORDER BY title",
                                  fetch=True)
        if not books:
            print("No books found in inventory")
            return
        
        print(f"/n{'ID':<4} {'Title':<30} {'Author':<20} {'Price':<10} {'Qty':<15} {'ISBN':<15} {'Genre':<15}")
        print("-" * 105)

        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} ₹{book['price']:<9.2f} {book['quantity']:<4} {book['isbn']:<15} {book['genre'] or 'N/A':<15}")

    def searchBook(self):
        print("\n=== SEARCH BOOKS ===")

        search_options = {
            'Title': {
                'prompt': "Enter title to search: ",
                'query': "SELECT * FROM availablebooks WHERE title LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%"
            },
            'Author': {
                'prompt': "Enter author to search: ",
                'query': "SELECT * FROM availablebooks WHERE author LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%"
            },
            'Genre': {
                'prompt': "Enter genre to search: ",
                'query': "SELECT * FROM availablebooks WHERE genre LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%"
            },
            'ISBN': {
                'prompt': "Enter isbn to search: ",
                'query': "SELECT * FROM availablebooks WHERE isbn LIKE %s ORDER BY title",
                'transform': lambda x : f"%{x}%"
            },
        }
        print("Search by: 1.Title  2.Author 3.Genre  4.ISBN")

        choice = inquirer.select(
            message="Search books by:",
            choices=list(search_options.keys()),
            default=0,
            pointer=" ➤",
            qmark="🔍",
            style=MENU_STYLE
        ).execute()

        config = search_options[choice]

        term = inquirer.text(
            message=config["prompt"]
        ).execute()

        books = self.executeQuery(
            config["query"],
            (config["transform"](term),),
            fetch=True
        )

        if not books:
            print("No books found")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Price':<10} {'Qty':<4} {'ISBN':<15}")
        print("-" * 90)
        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['price']:<9} {book['quantity']:<4} {book['isbn']:<15}")
        
    def updateBook(self):
        print("\n=== UPDATE BOOKS ===")

        try:
            bookId = int(inquirer.text("Enter book ID to update: ",style=MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return
        book = self.executeQuery("SELECT * FROM availablebooks WHERE book_id = %s",(bookId,),fetch=True)
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        print("\nCurrent Details:")
        print(f"Title:   {book['title']}")
        print(f"Author:  {book['author']}")
        print(f"Price:   ₹{book['price']:.2f}")
        print(f"Quality: {book['qantity']}")
        print(f"Genre:   {book['genre']}")

        print("\nEnter new details (press Enter to keep current value)")

        title = inquirer.text("Title: ",
                              default=str(book['title']),
                              style=MENU_STYLE).execute()
        author = inquirer.text("Author: ",
                               default=str(book['author']),
                               style=MENU_STYLE).execute()
        price = inquirer.text("Price: ₹",
                              default=str(book['price']),
                              style=MENU_STYLE).execute() 
        quantity = inquirer.text("Quantity: ",
                                 default=str(book['quantity']),
                                 style=MENU_STYLE).execute() 
        genre = inquirer.text("Genre: ",
                              default=str(book['genre'] or ""),
                              style=MENU_STYLE).execute() 

        if self.executeQuery("""UPDATE availablebooks 
                             SET title = %s, author = %s, price = %s, quantity = %s, genre = %s
                             WHERE book_id = %s""",
                             (title, author, price, quantity, genre, int(bookId))):
            print("Book updated successfully")
        else:
            print("Failed to update book")

    def deleteBook(self):
        print("\n=== DELETE BOOK ===")
        try:
            bookId = int(inquirer.text("Enter book ID to delete: ",style=MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return
    
        book = self.executeQuery("""SELECT title FROM availablebooks 
                                 WHERE book_id = %s""",
                                 (bookId,), fetch=True)
        if not book:
            print("Book not found")
            return
        
        print(f"Book to delete: {book[0]['title']}")

        if inquirer.text("Are you sure you want to delete book? (y/n): ",style=MENU_STYLE).execute().lower() != 'y':
            print("Deletion cancelled")
            return

        if self.executeQuery("DELETE FROM availablebooks WHERE book_id = %s",
                             (bookId,)):
            print("Book deleted Successfully")
        else:
            print("Failed to delete book")

    def sellBook(self):
        print("\n=== SELL BOOK ===")
        bookId = int(inquirer.text("Enter book ID to sell: ",style=MENU_STYLE).execute())

        try:
            book = self.executeQuery("SELECT * FROM availablebooks WHERE book_id = %s",
                                    (bookId,),fetch=True)
        except Error as e:
            print(f"Error in finding book: {e}")
            return
        
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        print(f"Books: {book['title']} by {book['author']}")
        print(f"Available quantity: {book['quantity']}")
        print(f"Price: ₹{book['price']:.2f}")

        
        try:
            quantitySold = int(inquirer.text("Enter quantity to sell: ",style=MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return

        if quantitySold > int(book['quantity']):
            print("Insufficient quantity in stock")
            return
        if quantitySold < 0:
            print("Quantity can't be nagative")
            return
        
        customerName = inquirer.text("Enter customer name: ",style=MENU_STYLE).execute()
        customerEmail = inquirer.text("Enter customer email (optional): ",style=MENU_STYLE).execute()

        totalAmount = quantitySold  * float(book['price'])
        saleDate = datetime.now().date()

        try: 
            self.cursor.execute("UPDATE availablebooks SET quantity = quantity - %s WHERE book_id = %s",
                                (quantitySold, bookId))
            self.cursor.execute("""INSERT INTO soldbooksales 
                                (book_id, customer_name, customer_email, quantity_sold, unit_price, total_ammount)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (bookId, customerName, customerEmail, quantitySold, book['price'], totalAmount))
            self.connection.commit()

            print(f"Sale completed successfully")
            print(f"Total amount: ₹{totalAmount:.2f}")
        except Error as e:
            self.connection.rollback()
            print(f"Error processing sale: {e}")
        
    def viewRevenueReport(self):
        print("\n=== COMPRENSIVE SALES REPORT ===")

        bookSales = self.executeQuery("""SELECT s.sale_date, b.title, b.author, s.customer_name, s.quantity_sold, 
                                      s.unit_price, s.total_amount, 'Book Sale' as transaction_type
                                      FROM soldbooksales s
                                      JOIN availablebooks b ON s.book_id = b.book_id
                                      WHERE s.sale_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                      ORDER BY s.sale_date DESC""",fetch=True)
        borrowingRevenue = self.executeQuery("""SELECT bs.transaction_date as sale_date, ab.title, ab.author, 
                                             bs.borrower_name as customer_name, 1 as quantity_sold,
                                             bs.fine_amount as unit_price, bs.total_amount,
                                             'Borrowing Fine' as transaction_type
                                             FROM borrowedbooksales bs
                                             JOIN availablebooks ab ON bs.book_id = ab.book_id
                                             WHERE bs.total_amount > 0 AND bs.transaction_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                             ORDER BY bs.transaction_date DESC""", fetch=True)
        
        allTransactions = (bookSales or []) + (borrowingRevenue or [])
        allTransactions.sort(key = lambda x: x['sale_date'], reversed=True)

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

    def viewRevenueRepoartSeperate(self):
        print("\n=== DETAILED SALES REPORT ===")

        print("--- BOOK SALES ---")
        bookSales = self.executeQuery("""SELECT s.book_id, b.title, b.author, s.customer_name,
                                      s.quantity_sold, s.unit_price, s.total_amount, s.sale_date
                                      FROM soldbooksales s JOIN availablebooks b ON s.book_id = b.book_id
                                      WHERE s.sale_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                      ORDER BY s.sale_date DESC""", fetch=True)
        print(f"\n{'Date':<12} {'Title':<20} {'Customer':<15} {'Qty':<4} {'Price':<8} {'Total':<10}")
        print("-" * 75)
        totalSalesRevenue, totalBorrowingRevenue = 0, 0
        for sale in (bookSales or []):
            print(f"{sale['sale_date'].strftime('%Y-%m-%d') or 'N/A':<12} {sale['customer_name'][:14]:<15} {sale['quantity_sold']:<4} ₹{sale['unit_price']:<7.2f} ₹{sale['total_amount']:<9.2f}")
            totalSalesRevenue += sale['total_amount']
        print(f"\nTotal Book Sales Revenue: ₹{totalSalesRevenue:.2f}")


        print("\n--- BORROWING FINES ---")
        borrowingRevenue = self.executeQuery("""SELECT bs.transaction_date, ab.title, ab.author, 
                                             bs.borrower_name, bs.fine_amount, bs.total_amount,
                                             DATEDIFF(bs.return_date, bs.due_date) as days_overdue
                                             FROM borrowedbooksales bs
                                             JOIN availablebooks ab ON bs.book_id = ab.book_id
                                             WHERE bs.total_amount > 0 and bs.transaction_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
                                             ORDER BY bs.transaction_date DESC""", fetch=True)
        print(f"\n{'Date':<12} {'Title':<20} {'Borrower':<15} {'Days':<4} {'Fine':<10}")
        print('-'*70)
        for item in (borrowingRevenue or []):
            print(f"{item['transaction_date'].strftime('%Y-%m-%d'):<12} {item['title'][:19]:<20} {item['borrower_name'][:14]:<15} {item['days_overdue'] or 0:<4} ₹{item['total_amount']:<9.2f}")
            totalBorrowingRevenue += item['total_amount']
        print(f"\nTotal Borrowing Revenue")

        print("\n" + "="*50)
        print("REVENUE SUMMARY")
        print(f"Book Sales: ₹{totalSalesRevenue:.2f}")
        print(f"Borrowing Revenue: ₹{totalBorrowingRevenue:.2f}")
        print(f"Grand total: ₹{totalSalesRevenue+totalBorrowingRevenue:.2f}")
        print("="*50)

    def borrowBook(self):
        print("\n=== BORROW BOOK ===")
        bookId= int(inquirer.text("Enter book ID to borrow: ",style=MENU_STYLE).execute())

        book = self.executeQuery("SELECT * FROM availablebooks WHERE book_id = %s",
                                 (bookId,), fetch = True)
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        if int(book['quantity']) == 0:
            print("book is out of stock")
            return
        
        print(f"Book: {book['title']} by {book['author']}")

        borroweName = inquirer.text("Enter borrower name: ",style=MENU_STYLE).execute()
        borroweEmail = inquirer.text("Enter borrower email: ",style=MENU_STYLE).execute()
        borrowePhone = inquirer.text("Enter borrower phone: ",style=MENU_STYLE).execute()

        try:
            borrowDays = int(inquirer.text("Enter number of days to borrow: ",style=MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return

        borrowDate = datetime.now().date()
        dueDate = borrowDate + timedelta(days=borrowDays)

        try:
            self.cursor.execute("UPDATE availablebooks SET quantity = quantity - 1 WHERE book_id = %s",
                                (bookId,))
            self.cursor.execute("""INSERT INTO borrowedbooks (book_id, borrower_name, borrower_email, borrower_phone, borrow_date, due_date)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (bookId, borroweName, borroweEmail, borrowePhone, borrowDate, dueDate))
            self.connection.commit()
            print("Borrowed Book Sucessfully")
            print(f"Due date: {dueDate}")

        except Error as e:
            self.connection.rollback()
            print(f"Error processsing borrowing: {e}")

    def returnBook(self):
        print("\n=== RETURN BORROWED BOOK ===")
        try:
            borrowId = int(inquirer.text("Enter borrow ID to return",style=MENU_STYLE).execute())
        except ValueError:
            print("Please enter a valid number")
            return

        borrowRecord = self.executeQuery("""SELECT bb.*, ab.title, ab.author 
                                         FROM borrowedbooks bb 
                                         JOIN availablebooks ab ON bb.book_id = ab.book_id 
                                         WHERE bb.borrow_id = %s""",
                                         (borrowId,),fetch=True)
        if not borrowRecord:
            print("Borrow record not found")
            return

        borrowRecord = borrowRecord[0]
        print(f"Book: {borrowRecord['title']} by {borrowRecord['author']}")
        print(f"Borrower: {borrowRecord['borrower_name']}")
        print(f"Due Date: {borrowRecord['due_date']}")

        returnDate = datetime.now().date()
        transactionDate = datetime.now().date()
        dueDate = borrowRecord['due_date']
        borrowDate = borrowRecord['borrow_date']

        if returnDate > dueDate:
            daysOverdue = (returnDate - dueDate).days
            fineAmount = daysOverdue * float(os.getenv("FINE_PER_DAY"))
            print(f"Book is {daysOverdue} days overdue. Fine: ₹{fineAmount:.2f}")
        else:
            fineAmount = 0

        totalAmount = (dueDate - borrowDate).days * float(os.getenv("BORROW_FEE_PER_DAY"))
        try:
            self.cursor.execute("""INSERT INTO borrowedbooksales (borrow_id, book_id, borrower_name, borrower_email, 
                                borrower_phone, borrow_date, due_date, return_date, 
                                fine_amount, total_amount, transaction_date)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (borrowId, borrowRecord['book_id'], borrowRecord['borrower_name'], borrowRecord['borrower_email'],
                                 borrowRecord['borrower_phone'], borrowRecord['borrow_date'], borrowRecord['due_date'], returnDate,
                                 fineAmount, totalAmount, transactionDate))
            self.cursor.execute("DELETE FROM borrowedbooks WHERE borrow_id = %s",
                                (borrowId,))
            self.cursor.execute("UPDATE availablebooks WHERE borrow_id = %s SET quantity = quantity + 1",
                                (borrowId,))
            self.connection.commit()
            print("Book returned successfully")
        except Error as e:
            self.connection.rollback()
            print(f"Error processing return: {e}")

    def viewBorrowedBook(self):
        print("\n=== CURRENTLY BORROWED BOOKS ===")

        borrowedBooks = self.executeQuery("""SELECT bb.borrow_id, bb.borrower_name, bb.borrow_date, bb.due_date, 
                                          ab.title, ab.author, ab.isbn, DATEDIFF(CURDATE(), bb.due_date) as days_overdue
                                          FROM borrowedbooks bb JOIN availablebooks ab ON bb.book_id = ab.book_id
                                          ORDER BY bb.due_date ASC""",
                                          fetch=True)
        if not borrowedBooks:
            print("No currently borrowed books")
            return
        
        print(f"\n{'BorrowID':<8} {'Borrower':<15} {'Title':<20} {'Borrow Date':<12} {'Due Date':<12} {'Overdue':<8}")
        print("-" * 80)

        for book in borrowedBooks:
            # to many this time
            borrow_date = book['borrow_date'].strftime('%Y-%m-%d') if book['borrow_date'] else 'N/A'
            due_date = book['due_date'].strftime('%Y-%m-%d') if book['due_date'] else 'N/A'
            overdue = book['days_overdue'] if book['days_overdue'] and book['days_overdue'] > 0 else 0
            status = f"{overdue} days" if overdue > 0 else "On time"
            print(f"{book['borrow_id']:<8} {book['borrower_name'][:14]:<15} {book['title'][:19]:<20} {borrow_date:<12} {due_date:<12} {status:<8}")

    def viewBorrowingHistory(self):
        print("\n=== BORROWING HISTORY ===")

        history = self.executeQuery("""SELECT bs.borrow_id, bs.borrower_name, ab.title,
                                    bs.borrow_date, bs.due_date, bs.return_date, bs.fine_amount, bs.total_amount
                                    FROM borrowedbooksales bs JOIN availablebooks ab ON bs.book_id = ab.book_id
                                    ORDER BY bs.return_date DESC
                                    LIMIT 30""",fetch=True)
        if not history:
            print("No borrowing history found")
            return
        
        print(f"\n{'BorrowID':<8} {'Borrower':<15} {'Title':<20} {'Borrow Date':<12} {'Return Date':<12} {'Fine':<10}")

        for record in history:
            borrow_date = record['borrow_date'].strftime('%Y-%m-%d') if record['borrow_date'] else 'N/A'
            return_date = record['return_date'].strftime('%Y-%m-%d') if record['return_date'] else 'N/A'
            fine = f"₹{record['fine_amount']:.2f}" if record['fine_amount'] and record['fine_amount'] > 0 else "None"
            print(f"{record['borrow_id']:<8} {record['borrower_name'][:14]:<15} {record['title'][:19]:<20} {borrow_date:<12} {return_date:<12} {fine:<10}")

    def viewSalesHistory(self): 
        print("\n=== SALES HISTORY ===")

        history = self.executeQuery("""SELECT s.sale_id, s.customer_name, ab.title, s.sale_date,
                                    s.quantity_sold, s.unit_price, s.total_amount
                                    FROM soldbooksales s JOIN availablebooks ab ON s.book_id = ab.book_id
                                    ORDER BY s.sale_date DESC LIMIT 30 """, fetch=True)

        if not history:
            print("No sales history found")
            return

        print(f"\n{'SaleID':<8} {'Customer':<15} {'Title':<20} {'Date':<12} {'Qty':<5} {'Amount':<10}")
        print("-" * 80)

        for record in history:
            saleDate = record['sale_date'].strftime('%Y-%m-%d') if record['sale_date'] else 'N/A'
            print(f"{record['sale_id']:<8} {record['customer_name'][:14]:<15} {record['title'][:19]:<20} {saleDate:<12} {record['quantity_sold']:<5} ₹{record['total_amount']:<9.2f}")

    def viewLowStock(self):
        print("\n=== LOW STOCK ALERT ===")

        books = self.executeQuery("SELECT * FROM availablebooks WHERE quantity < %s ORDER BY quantity ASC",
                                  (int(os.getenv("LOW_STOCK")),),fetch=True)
        
        if not books:
            print("No books with low stock!")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Qty':<4} {'Price':<10}")
        print("-" * 75)
        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} "
                  f"{book['quantity']:<4} ₹{book['price']:<9}")

    def displayMenu(self):
        print("\n" + "="*60)
        print("         BOOK STORE MANNAGEMENT SYSTEM")
        print("="*60)
        print("1.  Add New Book")
        print("2.  View All Available Books")
        print("3.  Search Books")
        print("4.  Update Books")
        print("5.  Delete Book")
        print("6.  Sell Book")
        print("7.  View Revenue Report")
        print("8.  View Revenue Report (Seperate)")
        print("9.  Borrow Books")
        print("10. Return Books")
        print("11. View Currently Borrowed Books")
        print("12. View Borrowing History")
        print("13. View Sales History")
        print("14. View Low Stock")
        print("15. Exit")
        print("-"*60)


def main():
    bookstore = BookStore()

    menu = {"Add Book": bookstore.addBook,
            "View Books": bookstore.viewAvaliable,
            "Search Books": bookstore.searchBook,
            "Update Books": bookstore.updateBook,
            "Delete Book": bookstore.deleteBook,
            "Sell Book": bookstore.sellBook,
            "View Revenue Report": bookstore.viewRevenueReport,
            "View Revenue Report Seperate": bookstore.viewRevenueRepoartSeperate,
            "Borrow Book": bookstore.borrowBook,
            "Return Book": bookstore.returnBook,
            "View Currently Borrowed Books": bookstore.viewBorrowedBook,
            "View Borrowing History": bookstore.viewBorrowingHistory,
            "View Sales History": bookstore.viewSalesHistory,
            "View Low Stock": bookstore.viewLowStock,
            "Exit": lambda: (None),}

    if not bookstore.connection.is_connected():
        print("Failed to connect. Please check the MySQL configurations")
        return
    
    print("Welcome to Book Store Mannagement System")

    while True:
        choice = inquirer.select(
            message="BOOK STORE MANAGEMENT SYSTEM",
            choices=list(menu.keys()),
            default=0,
            pointer=" ➤",
            qmark="📚",
            style=MENU_STYLE,
        ).execute()

        if choice == "Exit":
            bookstore.disconnect()
            break

        menu[choice]()


if __name__ == "__main__":
    main()


