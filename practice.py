import sys
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

class ClickableLabel(QLabel):
    clicked = Signal(str)
    def __init__(self, text, color):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"background-color: {color}; padding: 10px;")

    def mousePressEvent(self, event):
        self.clicked.emit(self.text())
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout_main = QHBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        self.context = QMenu()
        layout_v = QVBoxLayout()

        label_1 = ClickableLabel("Label1", "red")
        label_2 = ClickableLabel("Label2", "blue")
        label_3 = ClickableLabel("Main Window", "black")
        label_1.clicked.connect(self.change_the_context_menu)
        label_2.clicked.connect(self.change_the_context_menu)
        label_3.clicked.connect(self.change_the_context_menu)


        layout_v.addWidget(label_1)
        layout_v.addWidget(label_2)
        layout_main.addLayout(layout_v)
        layout_main.addWidget(label_3)

        widget = QWidget() 
        widget.setLayout(layout_main)

        self.setCentralWidget(widget)

    def change_the_context_menu(self, text):
        self.context.clear()
        options = {
            'Label1': ["encript", "comprese", "increase"],
            "Label2": ["decript", "decomprese", "decrease"],
            "Main Window": ['copy', 'remove', 'paste', 'save', 'save as']
            }
        options_text = options[text]
        for option in options_text:
            self.context.addAction(QAction(option, self))
    
    def contextMenuEvent(self, event):
        self.context.exec(event.globalPos())
        super().contextMenuEvent(event)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()