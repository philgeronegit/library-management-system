from PyQt6.QtWidgets import QLineEdit


class StyledLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                color: #D3D3D3;
            }
        """)
