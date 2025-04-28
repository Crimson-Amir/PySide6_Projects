import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from _18_color import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My 21th App. LOL")

        pagelayout = QHBoxLayout()
        button_layout = QVBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("red")
        btn.pressed.connect(self.active_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn = QPushButton("blue")
        btn.pressed.connect(self.active_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("blue"))

        btn = QPushButton("green")
        btn.pressed.connect(self.active_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QPushButton("black")
        btn.pressed.connect(self.active_tab_4)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("black"))

        dummy_widget = QWidget()
        dummy_widget.setLayout(pagelayout)
        self.setCentralWidget(dummy_widget)

    def active_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def active_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def active_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

    def active_tab_4(self):
        self.stacklayout.setCurrentIndex(3)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()