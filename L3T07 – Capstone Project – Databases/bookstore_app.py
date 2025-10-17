import sqlite3
import os
import shutil

def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect('bookstore.db')

def create_tables(conn):
    """Create the books and authors tables if they do not exist."""
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            UNIQUE(id, title),
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
        ''')

def get_author_id(conn, name, country):
    """Get the author_id for an existing author or add a new author."""
    cursor = conn.execute('SELECT id FROM authors WHERE name = ? AND '
                          'country = ?', (name, country))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return add_author(conn, name, country)

def add_author(conn, name, country):
    """Add a new author to the database and return the author_id."""
    with conn:
        cursor = conn.execute('INSERT INTO authors (name, country) VALUES '
                              '(?, ?)', (name, country))
        return cursor.lastrowid

def add_book(conn, book_id, title, author_name, country, qty):
    """Add a new book to the database."""
    try:
        author_id = get_author_id(conn, author_name, country)
        with conn:
            conn.execute('INSERT INTO books (id, title, author_id, qty) '
                         'VALUES (?, ?, ?, ?)', (book_id, title, author_id, 
                         qty))
        print(f'Book "{title}" added to the database.')
    except sqlite3.IntegrityError:
        print('Error: Book ID already exists.')

def update_book(conn, book_id, title=None, author_name=None, country=None, 
                qty=None):
    """Update book information in the database."""
    try:
        with conn:
            if title:
                conn.execute('UPDATE books SET title = ? WHERE id = ?', 
                             (title, book_id))
            if author_name and country:
                author_id = get_author_id(conn, author_name, country)
                conn.execute('UPDATE books SET author_id = ? WHERE id = ?', 
                             (author_id, book_id))
            if qty:
                conn.execute('UPDATE books SET qty = ? WHERE id = ?', 
                             (qty, book_id))
        print(f'Book with ID {book_id} updated.')
    except sqlite3.Error as e:
        print(f'Error: {e}')

def delete_book(conn, book_id):
    """Delete a book from the database."""
    try:
        with conn:
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        print(f'Book with ID {book_id} deleted from the database.')
    except sqlite3.Error as e:
        print(f'Error: {e}')

def search_book(conn, search_term):
    """Search for a book in the database."""
    try:
        cursor = conn.execute('SELECT * FROM books WHERE title LIKE ? OR '
                              'author_id IN (SELECT id FROM authors WHERE '
                              'name LIKE ?)', (f'%{search_term}%', 
                              f'%{search_term}%'))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f'ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, '
                      f'Quantity: {row[3]}')
        else:
            print('No books found.')
    except sqlite3.Error as e:
        print(f'Error: {e}')

def show_all_books(conn):
    """Display all books in the database."""
    try:
        cursor = conn.execute('SELECT books.id, books.title, authors.name, '
                              'authors.country, books.qty FROM books JOIN '
                              'authors ON books.author_id = authors.id')
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f'ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, '
                      f'Country: {row[3]}, Quantity: {row[4]}')
        else:
            print('No books found.')
    except sqlite3.Error as e:
        print(f'Error: {e}')

def backup_database():
    """Create a backup of the database."""
    try:
        shutil.copy('bookstore.db', 'bookstore_backup.db')
        print('Database backup created successfully.')
    except IOError as e:
        print(f'Error: {e}')

def restore_database():
    """Restore the database from a backup."""
    try:
        shutil.copy('bookstore_backup.db', 'bookstore.db')
        print('Database restored successfully.')
    except IOError as e:
        print(f'Error: {e}')

def populate_initial_data(conn):
    """Populate the books table with initial data."""
    initial_books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 'United Kingdom', 
         30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 
         'United Kingdom', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 
         'United Kingdom', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 'United Kingdom', 
         37),
        (3005, 'Alice\'s Adventures in Wonderland', 'Lewis Carroll', 
         'United Kingdom', 12)
    ]
    for book_id, title, author_name, country, qty in initial_books:
        cursor = conn.execute('SELECT 1 FROM books WHERE id = ?', (book_id,))
        if cursor.fetchone() is None:
            add_book(conn, book_id, title, author_name, country, qty)
        else:
            print(f'Book with ID {book_id} already exists. Skipping.')

def main():
    """Main function to run the bookstore management system."""
    conn = connect_db()
    create_tables(conn)
    populate_initial_data(conn)

    while True:
        print('\nBookstore Management System')
        print('1. Add a new book')
        print('2. Update book information')
        print('3. Delete a book')
        print('4. Search for a book')
        print('5. Show all books')
        print('6. Backup database')
        print('7. Restore database')
        print('8. Exit')
        choice = input('Enter your choice: ')

        if choice == '1':
            try:
                book_id = int(input('Enter book ID (4-digit integer): '))
                title = input('Enter book title: ')
                author_name = input('Enter author name: ')
                country = input('Enter author country: ')
                qty = int(input('Enter quantity: '))
                add_book(conn, book_id, title, author_name, country, qty)
            except ValueError:
                print('Invalid input. Please enter valid data.')
        elif choice == '2':
            try:
                book_id = int(input('Enter book ID to update (4-digit '
                                    'integer): '))
                title = input('Enter new title (leave blank to keep current): ')
                author_name = input('Enter new author name (leave blank to '
                                    'keep current): ')
                country = input('Enter new author country (leave blank to '
                                'keep current): ')
                qty = input('Enter new quantity (leave blank to keep current): ')
                update_book(conn, book_id, title if title else None, 
                            author_name if author_name else None, 
                            country if country else None,
                            int(qty) if qty else None)
            except ValueError:
                print('Invalid input. Please enter valid data.')
        elif choice == '3':
            try:
                book_id = int(input('Enter book ID to delete (4-digit '
                                    'integer): '))
                delete_book(conn, book_id)
            except ValueError:
                print('Invalid input. Please enter valid data.')
        elif choice == '4':
            search_term = input('Enter title or author to search: ')
            search_book(conn, search_term)
        elif choice == '5':
            show_all_books(conn)
        elif choice == '6':
            backup_database()
        elif choice == '7':
            restore_database()
        elif choice == '8':
            break
        else:
            print('Invalid choice. Please try again.')

    conn.close()

if __name__ == '__main__':
    main()
