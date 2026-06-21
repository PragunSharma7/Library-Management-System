import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

load_dotenv()

class BookStore() :
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
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
            self.cursor(query, params or ())

            if fetch:
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return True
        
        except Error as e:
            print(f"Database error {e}")
            return None
        
        
    def addBook(self):
        print("\n=== ADD NEW BOOK ===")

        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()

        existing = self.executeQuery("""SELECT book_id FROM avilablebooks 
                                     WHERE isbn = %s""",(isbn,), fetch=True)
        
        if existing:
            print("Error: A book with this ISBN already exists")
            return
        
        try:
            price = float(input("Enter price (₹): "))
            quantity = int(input("Enter quantity: "))
            genre = input("Enter genre: ")
        except ValueError:
            print("Error: Please enter Valid numeric quantities for Pries and Quantity")
            return
        
        if self.executeQuery("""INSERT INTO availavlebooks
                             (title, author, isbn, price, quantity, genre)
                             VALUE (%s, %s, %s, %s, %s, %s)""",
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
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} ₹{book['price']:<9} {book['quantity']:<4} {book['isbn']:<15} {book['genre'] or 'N/A':<15}")

    def searchBook(self):
        print("\n=== SEARCH BOOKS ===")
        print("Search by: 1.Title  2.Author 3.Genre  4.ISBN")

        choice = int(input("Enter your choice (1-4):"))

        if choice == 1:
            term = input("Enter title to search")
            query = "SELECT * FROM availablebooks WHERE title LIKE %s ORDER BY title"
            params = (f"%{term}%",)
        elif choice == 2:
            term = input("Enter author to search")
            query = "SELECT * FROM availablebooks WHERE author LIKE %s ORDER BY title"
            params = (f"%{term}%",)
        elif choice == 3:
            term = input("Enter genre to search")
            query = "SELECT * FROM availablebooks WHERE genre LIKE %s ORDER BY title"
            params = (f"%{term}%",)
        elif choice == 4:
            term = input("Enter ISBN to search")
            query = "SELECT * FROM availablebooks WHERE isbn LIKE %s ORDER BY title"
            params = (term,)
        else:
            print("Invalid choice")
            return
        
        books =  self.executeQuery(query, params, fetch=True)

        if not books:
            print("No books found")
            return
        
        print(f"\n{'ID':<4} {'Title':<30} {'Author':<20} {'Price':<10} {'Qty':<4} {'ISBN':<15}")
        print("-" * 90)
        for book in books:
            print(f"{book['book_id']:<4} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['price']:<9} {book['quantity']:<4} {book['isbn']:<15}")
        
    def updateBook(self):
        print("\n=== UPDATE BOOKS ===")

        bookId = int(input("Enter book ID to update: "))
        book = self.executeQuery("SELECT * FROM availablebooks WHERE book_id = %s",(bookId,),fetch=True)
        if not book:
            print("Book not found")
            return
        
        book = book[0]
        print("\nCurrent Details:")
        print(f"Title:   {book['title']}")
        print(f"Author:  {book['author']}")
        print(f"Price:   ₹{book['price']}")
        print(f"Quality: {book['quality']}")
        print(f"Genre:   {book['genre']}")

        print("\nEnter new details (press Enter to keep current value)")

        title = input(f"Title [{book['title']}]: ").strip() or book['title']
        author = input(f"Author [{book['author']}]: ").strip() or book['author']
        price = input(f"Price [{book['price']}]: ").strip() or book['price']
        quantity = input(f"Quantity [{book['quantity']}]: ").strip() or book['quantity']
        genre = input(f"Genre [{book['genre']}]: ").strip() or book['genre']

        if self.executeQuery("""UPDATE available 
                             SET title = %s, author = %s, price = %s, quantity = %s, genre = %s
                             WHERE book_id = %s""",
                             (title, author, price, quantity, genre, int(bookId))):
            print("Book updated successfully")
        else:
            print("Failed to update book")

    def deleteBook(self):
        print("\n=== DELETE BOOK ===")
    def sellBook(self):
        pass
    def viewSalesReport(self):
        pass
    def viewDetailedSalesRepoart(self):
        pass
    def borrowBook(self):
        pass
    def returnBook(self):
        pass
    def viewBorrowedBook(self):
        pass
    def viewBorrowingHistory(self):
        pass
    def viewLowStock(self):
        pass
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
        print("7.  View Sales Report (Combined)")
        print("8.  View Detailed Sales Report")
        print("9.  Borrow Books")
        print("10. Return Books")
        print("11. View Currently Borrowed Books")
        print("12. View Borrowing History")
        print("13. View Low Stock")
        print("14. Exit")
        print("-"*60)


def main():
    bookstore = BookStore()

    if not bookstore.connect:
        print("Failed to connect. Please check the MySQL configurations")
        return
    
    print("Welcome to Book Store Mannagement System")

    while True:
        bookstore.displayMenu()
        choice = int(input("Enter your choice (1-14): "))
        if choice == 1:
            bookstore.addBook()
        elif choice == 2:
            bookstore.viewAvaliable()
        elif choice == 2:
            bookstore.searchBook()
        elif choice == 2:
            bookstore.updateBook()
        elif choice == 2:
            bookstore.deleteBook()
        elif choice == 2:
            bookstore.sellBook()
        elif choice == 2:
            bookstore.viewSalesReport()
        elif choice == 2:
            bookstore.viewDetailedSalesRepoart()
        elif choice == 2:
            bookstore.borrowBook()
        elif choice == 2:
            bookstore.returnBook()
        elif choice == 2:
            bookstore.viewBorrowedBook()
        elif choice == 2:
            bookstore.viewBorrowingHistory()
        elif choice == 2:
            bookstore.viewLowStock()
        elif choice == 14:
            print("Thank you for using Book Store Management Syatem")
            bookstore.disconnect()
            break
        else:
            print("Invalid Choice! Please try again.")
        
        input("\nPress any key to Continue")


if __name__ == "__main__":
    main()


