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
