from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from librarymanagementsystem.views.components.custom_table_view import CustomTableView


def get_selected_indexes(custom_table_view: CustomTableView):
    """Get the selected indexes from the table"""
    indexes = custom_table_view.selectedIndexes()
    if indexes is None or len(indexes) == 0:
        QMessageBox.information(None, "Pas de sélection", "Pas de lignes sélectionnées")
        return None

    return indexes


def get_column_index_by_name(model, column_name: str) -> int:
    """Get the column index by name"""
    for column in range(model.columnCount(0)):
        if (
            model.headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            == column_name
        ):
            return column
    return -1


def get_model_data(model, row, column_name: str):
    """Get the data from the model"""
    role = Qt.ItemDataRole.DisplayRole
    index = get_column_index_by_name(model, column_name)
    return model.data(model.index(row, index), role)


def get_integer_value(value: str | None) -> int | None:
    """Get the integer value from the string"""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return int(float(value))
        except ValueError:
            print(f"Invalid integer value: {value}")
            return None
