
def filter_books(books, title=None, authors=None, isbn=None, year=None):

    # Szűri a könyvek listáját a megadott paraméterek szerint (részleges egyezés).
    filtered = []
    for book in books:
        # Cím szűrés
        if title and title.lower() not in str(book.get('title', '')).lower():
            continue
        # Szerző(k) szűrés
        if authors and authors.lower() not in str(book.get('authors', '')).lower():
            continue
        # ISBN szűrés
        if isbn and isbn.lower() not in str(book.get('isbn', '')).lower():
            continue
        # Év szűrés
        if year is not None:
            if str(year) != str(book.get('year', '')):
                continue
        filtered.append(book)
    return filtered

def filter_books_exact(books, title=None, authors=None, isbn=None, year=None):

    # Pontos egyezés alapján szűri a könyveket.
    filtered = []
    for book in books:
        if title and str(book.get('title', '')).lower() != title.lower():
            continue
        if authors and str(book.get('authors', '')).lower() != authors.lower():
            continue
        if isbn and str(book.get('isbn', '')).lower() != isbn.lower():
            continue
        if year is not None and str(book.get('year', '')) != str(year):
            continue
        filtered.append(book)
    return filtered

def search_books(books, query):

    # Egyszerű keresés: bárhol egyezik a query a címben, szerzőben vagy ISBN-ben.
    query = query.lower()
    return [
        book for book in books
        if query in str(book.get('title', '')).lower()
        or query in str(book.get('authors', '')).lower()
        or query in str(book.get('isbn', '')).lower()
    ]