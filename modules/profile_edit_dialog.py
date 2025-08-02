from PyQt6.QtWidgets import (QDialog )
from services.database_service import DatabaseService



# Profil szerkesztése adblak
class ProfileEditDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.db = DatabaseService()
        self.user_id = user_id
        self.setWindowTitle("Profil szerkesztése")
        self.setMinimumWidth(400)
        self.init_ui()
        self.setSizeGripEnabled(True)
        self.adjustSize()

