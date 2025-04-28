import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("click")
        self.setMouseTracking(True)
        self.button = QPushButton("Click me")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # self.setFixedSize(300, 200)
        self.widget.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        self.label.setText("Mouse moved to: (%d, %d)" % (event.x(), event.y()))

    def mousePressEvent(self, event):
        self.label.setText("Mouse pressed at: (%d, %d) (%s)" % (event.x(), event.y(), str(event.button())))
        # super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.label.setText("Mouse released at: (%d, %d)" % (event.x(), event.y()))

    def mouseDoubleClickEvent(self, event):
        self.label.setText("Mouse double clicked at: (%d, %d)" % (event.x(), event.y()))


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()