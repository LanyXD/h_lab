from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar
)
from ui.form_window import FormWindow
import data.db as db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn_list = []
        self.setup_ui()

    def setup_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.setup_status_bar()

    def setup_window(self):
        self.setWindowTitle("Crear conexión")
        self.resize(300, 200)

    def setup_central_widget(self):
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_1 = QLabel(self)
        label_1.setText("Nueva conexión")
        label_1.setFixedSize(QSize(100, 20))
        label_1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_1 = QPushButton(self)
        button_1.setText("Crear")
        button_1.setFixedSize(QSize(150, 25))
        button_1.clicked.connect(self.clicked_create)

        main_layout.addWidget(label_1)
        main_layout.addWidget(button_1)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def clicked_create(self):
        new_conn = db.get_connection()
        if new_conn is not None:
            new_form = FormWindow(new_conn)
            self.conn_list.append(new_form)
            new_form.show()
            self.statusBar().showMessage("Conexion creada.")
            print(self.conn_list)
        else:
            self.statusBar().showMessage("No se ha podido conectar.")
