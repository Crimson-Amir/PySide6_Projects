import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PySide6.QtGui import QPalette, QColor
from _18_color import Color

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")
        layout = QGridLayout()
        layout.addWidget(Color("red"), 0, 0)
        layout.addWidget(Color("green"), 0, 4)
        layout.addWidget(Color("blue"), 0, 2)
        layout.addWidget(Color("yellow"), 1, 0)
        layout.addWidget(Color("cyan"), 1, 3)

        dummy_widget = QWidget()
        dummy_widget.setLayout(layout)
        self.setCentralWidget(dummy_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()