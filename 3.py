import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Enter text here")
        self.label = QLabel()
        self.label.setText("Label")
        button = QPushButton("Click Me!")

        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        button.clicked.connect(self.change_label_text)

    def change_label_text(self):
        self.label.setText(self.text_box.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()