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
    QTabWidget
)

from _18_color import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        tab = QTabWidget()
        tab.setTabPosition(QTabWidget.West)
        tab.setMovable(True)
        for color in ["red", "blue", "yellow"]:
            tab.addTab(Color(color), color)
        
        #dummy_tab = QWidget()
        #dummy_tab.setLayout(tab)

        self.setCentralWidget(tab)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()