from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView


def update_viewport(table_view, model):
    # Get the current sort column and order
    sort_column = table_view.horizontalHeader().sortIndicatorSection()
    sort_order = table_view.horizontalHeader().sortIndicatorOrder()

    # Set the model to the table view
    table_view.setModel(model)
    table_view.resizeColumnsToContents()
    table_view.viewport().update()

    # Reapply the sort order
    table_view.sortByColumn(sort_column, sort_order)


def setup_table(table_view, model):
    table_view.setModel(model)
    table_view.resizeColumnsToContents()
    table_view.setSortingEnabled(True)
    table_view.sortByColumn(1, Qt.SortOrder.AscendingOrder)
    table_view.setColumnHidden(0, True)
    table_view.verticalHeader().setVisible(False)
    table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
