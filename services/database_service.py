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


