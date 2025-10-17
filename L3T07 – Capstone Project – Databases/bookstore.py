# This is a bookkeeping program.
# Import sqlite3.
import sqlite3

# Define a function that will create a database and connect to it.
def connect():
    return sqlite3.connect('ebookstore.db')


# Define a function that will ceate the tables to use.
def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        authorID INTEGER NOT NULL,
        qty INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Define a function that will fill in the needed details in the tables.
def populate_tables():
    conn = connect()
    cursor = conn.cursor()
    books = [
        (3001, 'A Tale of Two Cities', 1290, 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 8937, 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
        (3004, 'The Lord of the Rings', 6380, 37),
        (3005, 'Alice’s Adventures in Wonderland', 5620, 12)
    ]
    authors = [
        (1290, 'Charles Dickens', 'England'),
        (8937, 'J.K. Rowling', 'England'),
        (2356, 'C.S. Lewis', 'Ireland'),
        (6380, 'J.R.R. Tolkien', 'South Africa'),
        (5620, 'Lewis Carroll', 'England')
    ]
    cursor.executemany('INSERT INTO book (id, title, authorID, qty) VALUES \
                        (?, ?, ?, ?)', books)
    cursor.executemany('INSERT INTO author (id, name, country) VALUES \
                       (?, ?, ?)', authors)
    conn.commit()
    conn.close()

# Define a function that adds a book to the table.
def add_book(id, title, authorID, qty):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO book (id, title, authorID, qty) VALUES \
                   (?, ?, ?, ?)', (id, title, authorID, qty))
    conn.commit()
    conn.close()

# Define a function that updates the detials of a book.
def update_book(id, title, authorID, qty):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE book SET title = ?, authorID = ?, qty = ? \
                    WHERE id = ?', (title, authorID, qty, id))
    conn.commit()
    conn.close()

# Define a function that deletes a book entry.
def delete_book(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM book WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Define a function that allows the user to search for a book.
def search_books(title=None, authorID=None, qty=None):
    conn = connect()
    cursor = conn.cursor()
    query = 'SELECT * FROM book WHERE 1=1'
    params = []
    if title:
        query += ' AND title = ?'
        params.append(title)
    if authorID:
        query += ' AND authorID = ?'
        params.append(authorID)
    if qty:
        query += ' AND qty = ?'
        params.append(qty)
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Define a function that views all books.
def view_all_books():
    conn = connect()
    cursor = conn.cursor()
    query = '''
    SELECT book.title, author.name, author.country
    FROM book
    INNER JOIN author ON book.authorID = author.id
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Define a function that presents the main menu and calls the functions.
def main():
    create_tables()
    populate_tables()
    while True:
        print("\nBookstore Management System")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            id = input("Enter book ID: ")
            title = input("Enter book title: ")
            authorID = input("Enter book author ID: ")
            qty = input("Enter book quantity: ")
            add_book(id, title, authorID, qty)
            print("Book added successfully!")
        elif choice == '2':
            id = input("Enter book ID to update: ")
            title = input("Enter new book title: ")
            authorID = input("Enter new book author ID: ")
            qty = input("Enter new book quantity: ")
            update_book(id, title, authorID, qty)
            print("Book updated successfully!")
        elif choice == '3':
            id = input("Enter book ID to delete: ")
            delete_book(id)
            print("Book deleted successfully!")
        elif choice == '4':
            title = input("Enter book title to search \
                          (leave blank if not searching by title): ")
            authorID = input("Enter book author ID to search \
                             (leave blank if not searching by author ID): ")
            qty = input("Enter book quantity to search \
                        (leave blank if not searching by quantity): ")
            results = search_books(title, authorID, qty)
            for book in results:
                print(book)
        elif choice == '5':
            results = view_all_books()
            print("\nDetails")
            print("-------------------------------------------------")
            for book in results:
                print(f"Title: {book[0]}")
                print(f"Author's Name: {book[1]}")
                print(f"Author's Country: {book[2]}")
                print("-------------------------------------------------")
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

# Call the main menu.
if __name__ == '__main__':
    main()
