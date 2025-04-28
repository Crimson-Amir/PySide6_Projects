from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(800, 600))

        label = QLabel("Hello, World!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("Main Toolbar")
        button_action = QAction("first one", self)
        # button_action.setStatusTip("This is a button")
        button_action.setToolTip("This is a button")  # in ubuntu
        button_action.triggered.connect(self.toolbar_button_clicked)
        button_action.setCheckable(True)
        toolbar.setMovable(False)
        toolbar.addAction(button_action)
        self.addToolBar(toolbar)

        self.setStatusBar(QStatusBar(self))  # does not work in ubuntu
        
    def toolbar_button_clicked(self, s):
        print("Button clicked", s)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()