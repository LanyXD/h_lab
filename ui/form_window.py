from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QMainWindow,
    QLabel, QPushButton, QLineEdit,
    QStatusBar, QComboBox, QHBoxLayout
)
from ui.table_view_window import TableViewWindow


class FormWindow(QMainWindow):
    def __init__(self, conn, n):
        super().__init__()
        self.flag: bool = True
        self.n: int = n
        self.conn = conn
        self.cursor = conn.cursor()
        self.id_le: QLineEdit | None = None
        self.name_le: QLineEdit | None = None

        self.start_btn: QPushButton | None = None
        self.commit_btn: QPushButton | None = None
        self.insert_btn: QPushButton | None = None
        self.rollback_btn: QPushButton | None = None
        self.view_btn: QPushButton | None = None

        self.combo_isolation: QComboBox | None = None
        self.view_isolation_btn: QPushButton | None = None
        self.change_btn: QPushButton | None = None
        self.table_window: TableViewWindow | None = None

        self.setup_ui()

    def setup_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.setup_status_bar()
        self.setup_connections()

    def setup_window(self):
        self.setWindowTitle(f"Form #{self.n}")
        self.resize(320, 400)

    def setup_central_widget(self):
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(self)

        header_layout = QVBoxLayout()
        isolation_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        header_widget = QWidget(self)
        isolation_widget = QWidget(self)
        button_widget = QWidget(self)

        # header layout
        id_lb = QLabel(self)
        id_lb.setText("Id")
        self.id_le = QLineEdit(self)
        name_lb = QLabel(self)
        name_lb.setText("Name")
        self.name_le = QLineEdit(self)

        header_layout.addWidget(id_lb)
        header_layout.addWidget(self.id_le)
        header_layout.addWidget(name_lb)
        header_layout.addWidget(self.name_le)

        # isolation layout
        h_layout = QHBoxLayout()
        h_widget = QWidget(self)
        self.combo_isolation = QComboBox(self)
        self.view_isolation_btn = QPushButton(self)
        self.view_isolation_btn.setText("Isolation level")

        self.combo_isolation.addItems(["READ UNCOMMITTED",
                                       "READ COMMITTED",
                                       "REPEATABLE READ",
                                       "SERIALIZABLE", ])

        h_layout.addWidget(self.combo_isolation)
        h_layout.addWidget(self.view_isolation_btn)

        self.change_btn = QPushButton(self)
        self.change_btn.setText("Change")

        h_widget.setLayout(h_layout)
        isolation_layout.addWidget(h_widget)
        isolation_layout.addWidget(self.change_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # btn layout
        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.view_btn = QPushButton(self)
        self.view_btn.setText("View")
        self.insert_btn = QPushButton(self)
        self.insert_btn.setText("Insert")
        self.commit_btn = QPushButton(self)
        self.commit_btn.setText("Commit")
        self.rollback_btn = QPushButton(self)
        self.rollback_btn.setText("Rollback")

        self.view_btn.setEnabled(False)
        self.insert_btn.setEnabled(False)
        self.commit_btn.setEnabled(False)
        self.rollback_btn.setEnabled(False)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.view_btn)
        button_layout.addWidget(self.insert_btn)
        button_layout.addWidget(self.commit_btn)
        button_layout.addWidget(self.rollback_btn)

        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Assemble
        header_widget.setLayout(header_layout)
        isolation_widget.setLayout(isolation_layout)
        button_widget.setLayout(button_layout)

        main_layout.addWidget(header_widget)
        main_layout.addWidget(isolation_widget)
        main_layout.addWidget(button_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def setup_connections(self):
        self.view_isolation_btn.clicked.connect(self.view_isolation)
        self.change_btn.clicked.connect(self.change)

        self.start_btn.clicked.connect(self.start)
        self.view_btn.clicked.connect(self.view)
        self.insert_btn.clicked.connect(self.insert)
        self.commit_btn.clicked.connect(self.commit)
        self.rollback_btn.clicked.connect(self.rollback)

    # Botones
    def view_isolation(self):
        self.cursor.execute("SELECT @@transaction_isolation")
        isolation_level = self.cursor.fetchone()[0]
        self.statusBar().showMessage(f"El nivel de aislamiento es {isolation_level}", 1000)

    def change(self):
        isolation_level = self.combo_isolation.currentText()
        self.cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level}")
        self.statusBar().showMessage(f"Cambiado a {isolation_level}", 1000)

    def start(self):
        self.state()
        self.conn.start_transaction()
        self.statusBar().showMessage("Transacción iniciada", 1000)

    def view(self):
        try:
            self.cursor.execute("SELECT * FROM datos")
            rows = self.cursor.fetchall()
            columns = self.cursor.column_names

            self.table_window = TableViewWindow(rows, columns, self.n, self)
            self.table_window.exec()

        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 2000)

    def insert(self):
        id_val = self.id_le.text().strip()
        name_val = self.name_le.text()

        try:
            if id_val == "":
                self.cursor.execute(
                    "INSERT INTO datos (nombre) VALUES (%s)",
                    (name_val,)
                )
                self.statusBar().showMessage("Registro insertado", 1000)
            else:
                self.cursor.execute("""
                    INSERT INTO datos (id, nombre)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
                    """, (id_val, name_val))
                self.statusBar().showMessage("Registro insertado/actualizado", 1000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 1000)

    def commit(self):
        self.conn.commit()
        self.id_le.setText("")
        self.name_le.setText("")
        self.state()
        self.statusBar().showMessage("Transacción confirmada.", 1500)

    def rollback(self):
        self.conn.rollback()
        self.id_le.setText("")
        self.name_le.setText("")
        self.state()
        self.statusBar().showMessage("Transacción cancelada.", 1000)

    def state(self):
        if self.flag:
            self.start_btn.setEnabled(False)
            self.change_btn.setEnabled(False)
            self.view_btn.setEnabled(True)
            self.insert_btn.setEnabled(True)
            self.commit_btn.setEnabled(True)
            self.rollback_btn.setEnabled(True)
            self.flag = False
        else:
            self.start_btn.setEnabled(True)
            self.change_btn.setEnabled(True)
            self.view_btn.setEnabled(False)
            self.insert_btn.setEnabled(False)
            self.commit_btn.setEnabled(False)
            self.rollback_btn.setEnabled(False)
            self.flag = True
