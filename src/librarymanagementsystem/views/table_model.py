from datetime import datetime

import pandas as pd
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

from librarymanagementsystem.entities.book import Book


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.__data = data
        self.__filtered_data = self.__data.copy()

    @property
    def raw_data(self) -> pd.DataFrame:
        return self.__data

    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.__filtered_data.iloc[index.row(), index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            # check if null
            if pd.isnull(value):
                return None

            if isinstance(value, list):
                # Render list to comma-separated string
                return ", ".join(value)

            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            # Default (anything not captured above: e.g. int)
            return str(value)

        return None

    def rowCount(self, index):
        return self.__filtered_data.shape[0]

    def columnCount(self, index):
        return self.__filtered_data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.__filtered_data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self.__filtered_data.index[section])

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if self.__filtered_data.empty:
            return

        # Sort data based on the column
        self.__filtered_data.sort_values(
            by=self.__filtered_data.columns[column],
            ascending=order == Qt.SortOrder.AscendingOrder,
            inplace=True,
            key=lambda x: x.str.lower() if x.dtype == "object" else x,
        )

        self.layoutChanged.emit()

    def filter_function(self, row):
        row_str = row.astype(str).str.lower().to_string()
        words = self.filter_text.split()
        contains_filter_text = any(word.lower() in row_str for word in words)
        return contains_filter_text

    def filterData(self, filter_text):
        self.filter_text = filter_text
        self.layoutAboutToBeChanged.emit()
        if filter_text:
            self.__filtered_data = self.__data[
                self.__data.apply(
                    self.filter_function,
                    axis=1,
                )
            ]
        else:
            self.__filtered_data = self.__data.copy()
        self.layoutChanged.emit()

    def update_data(self, data):
        self.__data = data
        self.__filtered_data = self.__data.copy()
        self.layoutChanged.emit()


class TableModelList(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.__filtered_data = self.__data.copy()

    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.__filtered_data[index.row()][index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, list):
                # Render list to comma-separated string
                return ", ".join(value)

            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            # Default (anything not captured above: e.g. int)
            return str(value)
        elif role == Qt.ToolTipRole:
            # Generate rich text tooltip
            line_value = self.__filtered_data[index.row()]
            book_info = Book.from_list(line_value)
            tooltip = f"""
            <div>{book_info.titre}</div>
            <div>Auteur: {book_info.auteur}</div>
            <div>Genre: {book_info.genre}</div>
            <div>Date: {book_info.date_publication}</div>
            """
            return tooltip
        elif role == Qt.ItemDataRole.CheckStateRole and index.column() == 5:
            return Qt.Checked if value == 1 else Qt.Unchecked

    def rowCount(self, index):
        # The length of the outer list.
        return len(self.__filtered_data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.__filtered_data) and len(self.__filtered_data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = Book.headers()
                return headers[section]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()

        # Sort data based on the column
        self.__filtered_data.sort(
            key=lambda x: x[column].lower()
            if isinstance(x[column], str)
            else x[column],
            reverse=order == Qt.DescendingOrder,
        )

        self.layoutChanged.emit()

    def filterData(self, filter_text):
        self.layoutAboutToBeChanged.emit()
        if filter_text:
            self.__filtered_data = [
                row for row in self.__data if filter_text.lower() in str(row).lower()
            ]
        else:
            self.__filtered_data = self.__data.copy()
        self.layoutChanged.emit()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        # Items should be selectable, enbled but not editable
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def update_data(self, data):
        self.__data = data
        self.__filtered_data = self.__data.copy()
        self.layoutChanged.emit()
        self.layoutChanged.emit()
