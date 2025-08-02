import datetime
import os
import sqlite3


# Adatbáziskezelő a DB kapcsolódásért és műveletekért
class DatabaseService:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    # Adatbázis sémák létrehozása
    def create_tables(self):
        cursor = self.conn.cursor()

        # Felhasználók tábla
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                birthdate TEXT NOT NULL,
                phone TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                profile_pic TEXT,
                suspended INTEGER DEFAULT 0
            )
        ''')

        # Könyvek tábla
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                borrowed INTEGER DEFAULT 0,
                pdf_path TEXT
            )
        ''')

        # Foglalások tábla
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_isbn TEXT NOT NULL,
                    reserved_at TEXT NOT NULL,
                    expires_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_isbn) REFERENCES books(isbn)
                )
            ''')

        # Vélemények tábla
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_isbn TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    comment TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_isbn) REFERENCES books(isbn)
                )
            ''')

        # Kölcsönzések tábla
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_isbn TEXT NOT NULL,
                borrowed_at TEXT NOT NULL,
                due_date TEXT NOT NULL,
                returned_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_isbn) REFERENCES books(isbn)
            )
        ''')

        # Kategóriák tábla
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

        # Könyv-kategória kapcsolatok
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS book_categories (
                    book_isbn TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    FOREIGN KEY (book_isbn) REFERENCES books(isbn),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            ''')

        # Címkék tábla
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

        # Könyv-címke kapcsolatok
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS book_tags (
                    book_isbn TEXT NOT NULL,
                    tag_id INTEGER NOT NULL,
                    FOREIGN KEY (book_isbn) REFERENCES books(isbn),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                )
            ''')

        self.conn.commit()

    # Új felhasználó hozzáadása
    def add_user(self, name, username, email, birthdate, phone, password, role):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, username, email, birthdate, phone, password, role, suspended)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        ''', (name, username, email, birthdate, phone, password, role))
        self.conn.commit()

    # Felhasználó lekérése felhasználónév alapján
    def get_user_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None

    # Felhasználó lekérése ID alapján
    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, name, username, email, birthdate, phone, password, role, profile_pic FROM users WHERE id=?',
            (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "username": row[2],
                "email": row[3],
                "birthdate": row[4],
                "phone": row[5],
                "password": row[6],
                "role": row[7],
                "profile_pic": row[8]
            }
        return None

    # Felhasználói profiladatok frissítése
    def update_user_profile(self, user_id, name, username, email, birthdate, phone):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users
            SET name=?, username=?, email=?, birthdate=?, phone=?
            WHERE id=?
        ''', (name, username, email, birthdate, phone, user_id))
        self.conn.commit()

    # Jelszó frissítése
    def update_user_password(self, user_id, new_password):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET password=? WHERE id=?', (new_password, user_id))
        self.conn.commit()

    # Profilkép útvonal frissítése
    def update_profile_pic(self, user_id, pic_path):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET profile_pic=? WHERE id=?', (pic_path, user_id))
        self.conn.commit()

    # Jelszó ellenőrzése
    def check_user_password(self, user_id, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT password FROM users WHERE id=?', (user_id,))
        row = cursor.fetchone()
        if row and row[0] == password:
            return True
        return False

    # Profilkép fájl mentése/tárolása
    def save_profile_picture(self, user_id, file_path):
        save_dir = "profile_pics"
        os.makedirs(save_dir, exist_ok=True)
        ext = os.path.splitext(file_path)[1]
        dest = os.path.join(save_dir, f"user_{user_id}{ext}")
        with open(file_path, "rb") as f_in, open(dest, "wb") as f_out:
            f_out.write(f_in.read())
        self.update_profile_pic(user_id, dest)
        return dest

    # Új könyv hozzáadása
    def add_book(self, title, authors, isbn, year, pdf_path=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, authors, isbn, year, borrowed, pdf_path)
            VALUES (?, ?, ?, ?, 0, ?)
        ''', (title, authors, isbn, int(year), pdf_path))
        self.conn.commit()

    # Minden könyv lekérésw
    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT title, authors, isbn, year, borrowed FROM books')
        rows = cursor.fetchall()
        books = []
        for r in rows:
            books.append({
                "title": r[0],
                "authors": r[1],
                "isbn": r[2],
                "year": r[3],
                "borrowed": bool(r[4])
            })
        return books

    # Könyv kikölcsönzése
    def borrow_book(self, isbn, user_id, loan_days=14):
        cursor = self.conn.cursor()

        # Ellenőrzések
        cursor.execute('SELECT borrowed FROM books WHERE isbn=?', (isbn,))
        book_row = cursor.fetchone()
        if not book_row or book_row[0]:
            raise Exception("A könyv már ki van kölcsönözve!")
        cursor.execute('SELECT id FROM loans WHERE book_isbn=? AND returned_at IS NULL', (isbn,))
        if cursor.fetchone():
            raise Exception("A könyv már ki van kölcsönözve!")
        cursor.execute('UPDATE books SET borrowed=1 WHERE isbn=?', (isbn,))
        borrowed_at = datetime.datetime.now()
        due_date = borrowed_at + datetime.timedelta(days=loan_days)
        cursor.execute('''
            INSERT INTO loans (user_id, book_isbn, borrowed_at, due_date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, isbn, borrowed_at.isoformat(), due_date.date().isoformat()))
        self.conn.commit()

    # Könyv visszahozása
    def return_book(self, isbn, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id, due_date, borrowed_at FROM loans
            WHERE book_isbn=? AND returned_at IS NULL
        ''', (isbn,))
        loan = cursor.fetchone()
        if not loan:
            raise Exception("A könyv jelenleg nincs kikölcsönözve.")
        actual_user_id, due_date, borrowed_at = loan
        if actual_user_id != user_id:
            cursor.execute('SELECT username FROM users WHERE id=?', (actual_user_id,))
            username = cursor.fetchone()[0]
            raise Exception(f"A könyvet {username} user kölcsönözte ki, próbáld meg később!")
        returned_at = datetime.datetime.now()
        cursor.execute('UPDATE books SET borrowed=0 WHERE isbn=?', (isbn,))
        cursor.execute('''
            UPDATE loans SET returned_at=?
            WHERE book_isbn=? AND user_id=? AND returned_at IS NULL
        ''', (returned_at.isoformat(), isbn, user_id))
        self.conn.commit()

        # Késés ellenőrzése
        if returned_at.date() > datetime.date.fromisoformat(due_date):
            days_late = (returned_at.date() - datetime.date.fromisoformat(due_date)).days
            return days_late
        return 0

    # Kikölcsönzött könyvek listázása
    def get_borrowed_books(self):
        cursor = self.conn.cursor()
        cursor.execute('''
               SELECT b.title, b.authors, b.isbn, l.user_id, u.username, l.borrowed_at, l.returned_at
               FROM loans l
               JOIN books b ON l.book_isbn = b.isbn
               JOIN users u ON l.user_id = u.id
               WHERE l.returned_at IS NULL
           ''')
        return cursor.fetchall()

    # Könyv törlése adatbázisból (és kölcsönzések)
    def delete_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM loans WHERE book_isbn=?', (isbn,))
        cursor.execute('DELETE FROM books WHERE isbn=?', (isbn,))
        self.conn.commit()

    # Könyv lefoglalása, ha már ki van kölcsönözve
    def reserve_book(self, isbn, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT borrowed FROM books WHERE isbn=?', (isbn,))
        book_row = cursor.fetchone()
        if not book_row or not book_row[0]:
            raise Exception("A könyv szabadon kikölcsönözhető, foglalás nem szükséges!")
        cursor.execute('''
            SELECT id FROM reservations
            WHERE book_isbn=? AND user_id=? AND (expires_at IS NULL OR expires_at = '')
        ''', (isbn, user_id))
        if cursor.fetchone():
            raise Exception("Már van foglalásod erre a könyvre!")
        cursor.execute('''
            INSERT INTO reservations (user_id, book_isbn, reserved_at)
            VALUES (?, ?, ?)
        ''', (user_id, isbn, datetime.datetime.now().isoformat()))
        self.conn.commit()


    # Vélemény hozzáadása egy könyvhöz
    def add_review(self, user_id, isbn, rating, comment):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (user_id, book_isbn, rating, comment, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, isbn, rating, comment, datetime.datetime.now().isoformat()))
        self.conn.commit()

    # Könyvhöz tartozó vélemények lekérdezése
    def get_reviews_for_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT r.rating, r.comment, u.username, r.created_at
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.book_isbn=?
            ORDER BY r.created_at DESC
        ''', (isbn,))
        return cursor.fetchall()

    # Könyv kölcsönzési statisztikák
    def get_book_borrow_stats(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT b.title, b.isbn, COUNT(DISTINCT l.user_id) AS user_count, COUNT(l.id) AS borrow_count
            FROM books b
            LEFT JOIN loans l ON b.isbn = l.book_isbn
            GROUP BY b.isbn
            ORDER BY borrow_count DESC
        ''')
        return cursor.fetchall()

    # Legtöbb kölcsönzést végző felhasználók (top lista)
    def get_top_readers(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT u.username, u.name, COUNT(l.id) AS borrow_count
            FROM users u
            JOIN loans l ON u.id = l.user_id
            GROUP BY u.id
            ORDER BY borrow_count DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    # Felhasználó adott könyvre vonatkozó aktív foglalásának lekérdezése
    def get_reservation(self, user_id, isbn):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM reservations
            WHERE user_id=? 
              AND book_isbn=? 
              AND (expires_at IS NULL OR expires_at = '')
            ORDER BY reserved_at DESC
            LIMIT 1
        ''', (user_id, isbn))
        return cursor.fetchone()

    # Felhasználó aktív foglalásainak lekérdezése
    def get_reservations_for_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT r.id, r.book_isbn, r.reserved_at, b.title, b.authors
            FROM reservations r
            JOIN books b ON r.book_isbn = b.isbn
            WHERE r.user_id=? AND r.expires_at IS NULL
            ORDER BY r.reserved_at DESC
        ''', (user_id,))
        return cursor.fetchall()


    # Foglalás lemondása (lejárttá tétele)
    def cancel_reservation(self, reservation_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE reservations SET expires_at=?
            WHERE id=?
        ''', (datetime.datetime.now().isoformat(), reservation_id))
        self.conn.commit()

    # Felhasználó felfüggesztése/aktiválása
    def suspend_user(self, user_id, suspend=True):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET suspended=? WHERE id=?', (1 if suspend else 0, user_id))
        self.conn.commit()

    # Felhasználó jogosultságának módosítása
    def change_user_role(self, user_id, new_role):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET role=? WHERE id=?', (new_role, user_id))
        self.conn.commit()

    # Új kategória hozzáadása
    def add_category(self, name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        self.conn.commit()

