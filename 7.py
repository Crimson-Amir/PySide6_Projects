import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        print("Mouse moved to: (%d, %d)" % (event.x(), event.y()))      

class MyWidget(QLabel):
    def mousePressEvent(self, event):
        print("Label Failed")
        event.ignore()
class MyButton(QPushButton):
    def mousePressEvent(self, event):
        print("Button Failed")
        try:
            a = 1/0
        except Exception as e:
            event.ignore()
            raise e

app = QApplication(sys.argv)

window = MainWindow()
button = MyButton()
label = MyWidget("click")
layout = QVBoxLayout()

layout.addWidget(button)
label.setLayout(layout)
window.setCentralWidget(label)
window.show()

app.exec()