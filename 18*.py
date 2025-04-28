import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPalette, QColor
from _18_color import Color
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # self.setWindowTitle("My App")
        # label = Color("red")
        # self.setCentralWidget(label)

        self.setWindowTitle("My App")
        layout_1 = QHBoxLayout()
        layout_2 = QVBoxLayout()
        layout_3 = QVBoxLayout()

        layout_2.addWidget(Color("red"))
        layout_2.addWidget(Color("green"))
        layout_2.addWidget(Color("blue"))

        layout_1.addLayout(layout_2)
        layout_1.addWidget(Color("yellow"))

        layout_3.addWidget(Color("cyan"))
        layout_3.addWidget(Color("magenta"))

        layout_1.addLayout(layout_3)
        

        layout_1.setSpacing(10)
        layout_2.setSpacing(0)
        layout_3.setSpacing(0)
        layout_3.setContentsMargins(10, 0, 0, 0)

        widget = QWidget()  # dummy widget
        widget.setLayout(layout_1)
        self.setCentralWidget(widget)  # label spacing

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
