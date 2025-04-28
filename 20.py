import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QStackedLayout
from PySide6.QtGui import QPalette, QColor
from _18_color import Color

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")
        layout = QStackedLayout()
        layout.addWidget(Color("red"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("blue"))
        layout.addWidget(Color("yellow"))

        layout.setCurrentIndex(1)

        dummy_widget = QWidget()
        dummy_widget.setLayout(layout)
        self.setCentralWidget(dummy_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()