import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("click")
        self.setMouseTracking(True)
        self.setCentralWidget(self.label)
        self.setFixedSize(300, 200)
        self.label.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        self.label.setText("Mouse moved to: (%d, %d)" % (event.x(), event.y()))

    def contextMenuEvent(self, event):
        context = QMenu(self)
        context.addAction(QAction("Copy", self))
        context.addAction(QAction("Paste", self))
        context.addAction(QAction("Remove", self))
        context.exec(event.globalPos())       

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()