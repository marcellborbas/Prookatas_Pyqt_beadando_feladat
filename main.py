import sys
from PyQt6.QtWidgets import QApplication
from modules.auth_module import LoginWindow
from style import APP_STYLE


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()