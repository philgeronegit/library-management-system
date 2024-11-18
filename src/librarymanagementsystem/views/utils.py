from PyQt6.QtWidgets import QLabel

from librarymanagementsystem.views.components.styled_qlinedit import StyledLineEdit


def input_factory(label, placeholder=""):
    # Factory method to create a label and input field
    label = QLabel(label)
    input_field = StyledLineEdit()
    input_field.setPlaceholderText(placeholder)
    return label, input_field
