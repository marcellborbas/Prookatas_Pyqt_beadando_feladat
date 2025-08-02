import csv

# Könyvek exportálása CSV fájlba
def export_books_to_csv(books, filename="books.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Cím", "Szerző(k)", "ISBN", "Év"])
        for book in books:
            writer.writerow([book["title"], book["authors"], book["isbn"], book["year"]])