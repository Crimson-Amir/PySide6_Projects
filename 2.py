import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.button_is_checkd = False

        self.setWindowTitle("My App")
        
        self.setFixedSize(300, 200)
        self.button = QPushButton("Click Me!")

        
        self.button.clicked.connect(self.change_title)
        
        
        self.button.setCheckable(True)
        self.button.setChecked(self.button_is_checkd)

        self.setCentralWidget(self.button)

    def change_title(self, clicked):
        self.count += 1
        print("Button clicked:", self.button.isChecked())
        self.setWindowTitle("New Title %s" % clicked)
        self.button_is_checkd = clicked 
        if self.count >= 3:
            self.button.setEnabled(False)
            self.button.setText("Button Disabled")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()