APP_STYLE = """
QWidget {
    background-color: #f9f9fb;
    color: #222;
    font-size: 15px;
}
QMainWindow {
    background-color: #f9f9fb;
}
QLabel {
    font-size: 15px;
}
QTableWidget, QTableView {
    background: #fff;
    border-radius: 8px;
    font-size: 14px;
    gridline-color: #e6ecf7;
}
QHeaderView::section {
    background-color: #e6ecf7;
    color: #222;
    font-weight: bold;
    border: none;
    padding: 8px;
}
QLineEdit, QSpinBox, QTextEdit {
    background: #fafafa;
    color: #222;
    border: 1px solid #e6ecf7;
    border-radius: 5px;
    padding: 6px;
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
QMenuBar, QMenu {
    background: #e6ecf7;
    color: #222;
    border-radius: 0px;
}
QMenu::item:selected {
    background: #b7d2fc;
}
QDialog {
    background-color: #f9f9fb;
}
QListWidget {
    background: #fff;
    border-radius: 8px;
    font-size: 14px;
}

/* --- QCheckBox hozzáadva --- */
QCheckBox {
    spacing: 8px;
    font-size: 15px;
    color: #222;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #2d7efb;
    background: #fff;
}
QCheckBox::indicator:checked {
    background: #2d7efb;
    border: 2px solid #165dc8;
}
"""