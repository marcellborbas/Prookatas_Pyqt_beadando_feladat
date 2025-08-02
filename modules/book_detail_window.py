from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel
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

