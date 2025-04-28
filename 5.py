import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt


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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.label.setText("Left mouse button pressed at: (%d, %d)" % (event.x(), event.y()))
        elif event.button() == Qt.RightButton:
            self.label.setText("Right mouse button pressed at: (%d, %d)" % (event.x(), event.y()))
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        print(event.button())
        print(event.buttons())
        print(event.globalPos())
        print(event.globalX())
        print(event.globalY())
        print(event.pos())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()