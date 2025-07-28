from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit, QStatusBar
)
import data.db as db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.id_le: QLineEdit | None = None
        self.name_le: QLineEdit | None = None
        self.start_btn: QPushButton | None = None
        self.commit_btn: QPushButton | None = None
        self.insert_btn: QPushButton | None = None
        self.rollback_btn: QPushButton | None = None
        self.conn = None

        self.setup_ui()
        self.setup_connection_db()

    def setup_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.setup_status_bar()
        self.setup_connections()

    def setup_window(self):
        self.setWindowTitle("Formulario")
        self.resize(320, 400)

    def setup_central_widget(self):
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(self)

        # Componentes
        id_lb = QLabel(self)
        id_lb.setText("Id")
        id_lb.setFixedSize(200, 20)

        self.id_le = QLineEdit(self)

        name_lb = QLabel(self)
        name_lb.setText("Nombre")
        name_lb.setFixedSize(200, 20)

        self.name_le = QLineEdit(self)

        bottom_layout = QVBoxLayout(self)
        bottom_widget = QWidget(self)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        bottom_layout.setSpacing(30)

        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.insert_btn = QPushButton(self)
        self.insert_btn.setText("Insert")
        self.commit_btn = QPushButton(self)
        self.commit_btn.setText("Commit")
        self.rollback_btn = QPushButton(self)
        self.rollback_btn.setText("Rollback")

        # Estructura
        main_layout.addWidget(id_lb)
        main_layout.addWidget(self.id_le)
        main_layout.addWidget(name_lb)
        main_layout.addWidget(self.name_le)

        bottom_layout.addWidget(self.start_btn)
        bottom_layout.addWidget(self.insert_btn)
        bottom_layout.addWidget(self.commit_btn)
        bottom_layout.addWidget(self.rollback_btn)

        bottom_widget.setLayout(bottom_layout)
        main_layout.addWidget(bottom_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def setup_connections(self):
        self.start_btn.clicked.connect(self.start)
        self.insert_btn.clicked.connect(self.insert)
        self.commit_btn.clicked.connect(self.commit)
        self.rollback_btn.clicked.connect(self.rollback)

    def setup_connection_db(self):
        self.conn = db.get_connection()
        print(self.conn)

    def start(self):
        self.conn.start_transaction()
        self.statusBar().showMessage("Iniciando transaccion", 1000)

    def insert(self):
        id_val = self.id_le.text()
        name_val = self.name_le.text()

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO datos(nombre) VALUES (%s)", (name_val,))
            self.statusBar().showMessage("Insertando...", 1000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 1000)

    def commit(self):
        self.conn.commit()
        self.id_le.setText("")
        self.name_le.setText("")
        self.statusBar().showMessage("Transacción confirmada.", 1500)

    def rollback(self):
        self.conn.rollback()
        self.id_le.setText("")
        self.name_le.setText("")
        self.statusBar().showMessage("Transacción cancelada.", 1000)

