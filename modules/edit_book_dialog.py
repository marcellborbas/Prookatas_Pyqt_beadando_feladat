import os
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QFileDialog

class EditBookDialog(QDialog):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Könyv módosítása")
        layout = QFormLayout()

        self.title_input = QLineEdit(book["title"])
        self.authors_input = QLineEdit(book["authors"])
        self.year_input = QLineEdit(str(book["year"]))
        self.pdf_path = book.get("pdf_path")

        layout.addRow("Cím:", self.title_input)
        layout.addRow("Szerző(k):", self.authors_input)
        layout.addRow("Megjelenés éve:", self.year_input)

        self.pdf_btn = QPushButton("PDF módosítása")
        self.pdf_btn.clicked.connect(self.attach_pdf)
        self.pdf_btn.setText(f"PDF: {os.path.basename(self.pdf_path) if self.pdf_path else 'Nincs csatolva, adj hozzá egyet'}")
        layout.addRow(self.pdf_btn)

        save_btn = QPushButton("Mentés")
        save_btn.clicked.connect(self.accept)
        layout.addRow(save_btn)
        self.setLayout(layout)

    # PDF fájl kiválasztása
    def attach_pdf(self):
        fname, _ = QFileDialog.getOpenFileName(self, "PDF kiválasztása", filter="PDF files (*.pdf)")
        if fname:
            self.pdf_path = fname
            self.pdf_btn.setText(f"PDF: {os.path.basename(fname)}")

    # A szerkesztett adatok visszaadása
    def get_data(self):
        return (
            self.title_input.text(),
            self.authors_input.text(),
            self.year_input.text(),
            self.pdf_path
        )