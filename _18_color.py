from PySide6.QtGui import QPalette, QColor 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)  # Hey, fill your background with your palette's background color automatically.
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

