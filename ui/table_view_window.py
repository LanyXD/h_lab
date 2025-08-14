from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem


class TableViewWindow(QDialog):
    def __init__(self, data, columns, n, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Tabla #{n}")
        self.resize(500, 300)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)
