from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt
from services.database_service import DatabaseService


# Funkció, ami állapotot (badge) hoz létre a könyv státuszához
def status_badge(text, color):
    lbl = QLabel(text)
    lbl.setStyleSheet(f"""
        background-color: {color};
        color: white;
        padding: 4px 10px;
        border-radius: 10px;
        font-weight: bold;
        min-width: 100px;
        text-align: center;
    """)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return lbl


class BookDetailWindow(QDialog):
    def __init__(self, book, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Könyv részletei")
        self.setMinimumWidth(500)
        self.db = DatabaseService()
        self.book = book
        self.user_id = user_id
        self.setSizeGripEnabled(True)
        self.adjustSize()
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9fb;
                color: #222;
                font-size: 15px;
            }
            QLabel {
                font-size: 15px;
            }
            QListWidget {
                background: #fff;
                border-radius: 8px;
                font-size: 14px;
            }
            QSpinBox, QTextEdit {
                background: #fafafa;
                color: #222;
            }
            QPushButton {
                background: #2d7efb;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #165dc8;
            }
        """)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.update_content()

    # Az ablakban lévő összes widget törlése
    def clear_content(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            widget = child.widget()
            if widget is not None:
                widget.deleteLater()

    # Könyv részletes adatai és státuszok frissítése
    def update_content(self):
        self.clear_content()

        # Kártya fejléc + könyv info
        header = QFrame()
        header.setFrameShape(QFrame.Shape.StyledPanel)
        header.setStyleSheet("""
                background: #e6ecf7;
                border-radius: 12px;
                border: 2px solid #2d7efb;
                padding: 18px;
            """)
        header_layout = QVBoxLayout(header)
        title_lbl = QLabel(self.book['title'])
        title_lbl.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header_layout.addWidget(title_lbl)

        author_lbl = QLabel(f"Szerző(k): {self.book['authors']}")
        author_lbl.setFont(QFont("Segoe UI", 14))
        header_layout.addWidget(author_lbl)

        info_lbl = QLabel(f"ISBN: {self.book['isbn']}   |   Év: {self.book['year']}")
        info_lbl.setFont(QFont("Segoe UI", 12))
        header_layout.addWidget(info_lbl)

        self.main_layout.addWidget(header)

        # Könyv státusz és foglalás kezelése (elérhető, kikölcsönözve)
        loan = self.db.conn.execute(
            'SELECT borrowed_at, due_date, returned_at FROM loans WHERE book_isbn=? ORDER BY borrowed_at DESC LIMIT 1',
            (self.book['isbn'],)
        ).fetchone()

        already_reserved = self.db.get_reservation(self.user_id, self.book['isbn'])

        self.reservation_btn = None
        self.cancel_reservation_btn = None

        if loan and not loan[2]:
            badge = status_badge("Kikölcsönözve", "#f5b041")
            self.main_layout.addWidget(badge)
            self.main_layout.addWidget(QLabel(
                f"Kikölcsönzés dátuma: <b>{loan[0][:10]}</b>   |   Lejárat: <b>{loan[1][:10]}</b>"
            ))
            # Foglalás gomb: csak ha nincs saját foglalás
            if not already_reserved:
                self.reservation_btn = QPushButton("Foglalás erre a könyvre")
                self.reservation_btn.clicked.connect(self.reserve_book)
                self.main_layout.addWidget(self.reservation_btn)
            else:
                self.cancel_reservation_btn = QPushButton("Foglalás lemondása")
                self.cancel_reservation_btn.clicked.connect(self.cancel_reservation)
                self.main_layout.addWidget(QLabel("Van érvényes foglalásod!"))
                self.main_layout.addWidget(self.cancel_reservation_btn)
        else:
            badge = status_badge("Elérhető", "#27ae60")
            self.main_layout.addWidget(badge)

        # PDF megnyitása, ha van csatolva
        book_row = self.db.conn.execute(
            'SELECT pdf_path FROM books WHERE isbn=?', (self.book['isbn'],)
        ).fetchone()
        pdf_path = book_row[0] if book_row and book_row[0] else None
        if pdf_path:
            self.pdf_btn = QPushButton("PDF megnyitása böngészőben")
            self.pdf_btn.clicked.connect(lambda: self.open_pdf(pdf_path))
            self.main_layout.addWidget(self.pdf_btn)

        # Átlagos értékelés (csillag ikon)
        reviews = self.db.get_reviews_for_book(self.book['isbn'])
        if reviews:
            avg = sum(r[0] for r in reviews) / len(reviews)
            avg_lbl = QLabel(f"★ {avg:.1f} / 5   ({len(reviews)} értékelés)")
            avg_lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            avg_lbl.setStyleSheet("color: #f1c40f; margin-top:12px;")
            self.main_layout.addWidget(avg_lbl)
        else:
            self.main_layout.addWidget(QLabel("Még nincs értékelés."))

        # Vélemények megjelenítése
        self.main_layout.addWidget(QLabel("Vélemények:"))
        self.reviews_list = QListWidget()
        for r in reviews:
            item = QListWidgetItem(f"★ {r[0]}   {r[2]} ({r[3][:10]})\n{r[1]}")
            item.setBackground(QColor("#f6f7fa"))
            item.setForeground(QColor("#222"))
            self.reviews_list.addItem(item)
        self.reviews_list.setStyleSheet("margin-bottom:18px;")
        self.main_layout.addWidget(self.reviews_list)

        # Új értékelés form
        rate_lbl = QLabel("Új értékelés:")
        rate_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.main_layout.addWidget(rate_lbl)

        form_layout = QHBoxLayout()
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        self.rating_input.setValue(5)
        self.rating_input.setFont(QFont("Segoe UI", 14))
        self.rating_input.setStyleSheet("min-width: 50px;")
        form_layout.addWidget(QLabel("Csillagok:"))
        form_layout.addWidget(self.rating_input)
        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Írj véleményt...")
        self.comment_input.setMaximumHeight(50)
        form_layout.addWidget(self.comment_input)
        self.main_layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Értékelés beküldése")
        self.submit_btn.clicked.connect(self.submit_review)
        self.main_layout.addWidget(self.submit_btn)
