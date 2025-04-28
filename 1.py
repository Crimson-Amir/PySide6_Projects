import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

app = QApplication(sys.argv)    

window = QMainWindow()
button = QPushButton("Click Me!")
window.setCentralWidget(button)
window.showFullScreen()

app.exec()