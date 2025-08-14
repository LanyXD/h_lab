from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit, QStatusBar, QMainWindow, QComboBox, QHBoxLayout
)


class FormWindow(QMainWindow):
    def __init__(self, conn):
        super().__init__()
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

        self.setup_ui()

    def setup_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.setup_status_bar()
        self.setup_connections()

    def setup_window(self):
        self.setWindowTitle("Form")
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
        pass

    def change(self):
        pass

    def start(self):
        self.conn.start_transaction()
        self.statusBar().showMessage("Transacción iniciada", 1000)

    def view(self):
        pass

    def insert(self):
        id_val = self.id_le.text()
        name_val = self.name_le.text()

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute("INSERT INTO datos(nombre) VALUES (%s)", (name_val,))
            self.statusBar().showMessage("Insertando...", 1000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 1000)

    def commit(self):
        self.conn.commit()
        self.id_le.setText("")
        self.name_le.setText("")
        self.statusBar().showMessage("Transacción confirmada.", 1500)
        self.cursor.close()

    def rollback(self):
        self.conn.rollback()
        self.id_le.setText("")
        self.name_le.setText("")
        self.statusBar().showMessage("Transacción cancelada.", 1000)
        self.cursor.close()
