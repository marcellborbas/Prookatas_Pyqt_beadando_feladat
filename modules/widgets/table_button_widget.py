from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class TableButtonWidget(QWidget):
    def __init__(self, borrow_callback=None, return_callback=None):
        super().__init__()
        layout = QHBoxLayout(self)
        if borrow_callback:
            borrow_btn = QPushButton("Kikölcsönzés")
            borrow_btn.clicked.connect(borrow_callback)
            layout.addWidget(borrow_btn)
        if return_callback:
            return_btn = QPushButton("Visszaadás")
            return_btn.clicked.connect(return_callback)
            layout.addWidget(return_btn)