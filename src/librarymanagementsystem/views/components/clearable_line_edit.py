import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QStyle

from librarymanagementsystem.views.components.styled_qlinedit import StyledLineEdit
from librarymanagementsystem.views.constants import LIGHT_GREEN_COLOR


class ClearableLineEdit(StyledLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clear_button = QPushButton(self)
        self.clear_button.setIcon(qta.icon("fa.times", color=LIGHT_GREEN_COLOR))
        self.clear_button.setCursor(Qt.CursorShape.ArrowCursor)
        self.clear_button.setStyleSheet("border: none; padding: 0px;")
        self.clear_button.setFixedSize(16, 16)
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.hide()

        self.textChanged.connect(self.update_clear_button)
        self.update_clear_button()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        frame_width = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        button_size = self.clear_button.size()
        self.clear_button.move(
            self.rect().right() - frame_width - button_size.width(),
            (self.rect().bottom() + 1 - button_size.height()) // 2,
        )

    def update_clear_button(self):
        if self.text():
            self.clear_button.show()
        else:
            self.clear_button.hide()
