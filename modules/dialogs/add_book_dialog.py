
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QFileDialog


class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Könyv hozzáadása")
        layout = QFormLayout()

        # Könyv adatainak bevitelére szolgáló input mezők
        self.title_input = QLineEdit()
        self.authors_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.year_input = QLineEdit()
        self.pdf_path = None

        # Form mezők hozzáadása
        layout.addRow("Cím:", self.title_input)
        layout.addRow("Szerző(k):", self.authors_input)
        layout.addRow("ISBN:", self.isbn_input)
        layout.addRow("Megjelenés éve:", self.year_input)

        # PDF csatolás gomb létrehozása
        self.pdf_btn = QPushButton("PDF csatolása")
        self.pdf_btn.clicked.connect(self.attach_pdf)
        layout.addRow(self.pdf_btn)

        submit_btn = QPushButton("Hozzáadás")
        submit_btn.clicked.connect(self.accept)
        layout.addRow(submit_btn)
        self.setLayout(layout)

   # PDF fájl csatolása
    def attach_pdf(self):
        fname, _ = QFileDialog.getOpenFileName(self, "PDF kiválasztása", filter="PDF files (*.pdf)")
        if fname:
            self.pdf_path = fname
            self.pdf_btn.setText(f"PDF csatolva: {os.path.basename(fname)}")