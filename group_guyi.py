from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QHeaderView, QAbstractItemView
)
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from datetime import datetime

# Dummy data
dummy_data = {
    "Group A": {
        "code": "GA01",
        "designation": "Alpha",
        "last_update": "2024-04-01",
        "endpoints": [
            {"code": "1242", "designation": "Second", "last_update": "2024/02/19"},
            {"code": "4281", "designation": "nine", "last_update": "2024/05/20"},
        ]
    },
    "Group B": {
        "code": "GB01",
        "designation": "Beta",
        "last_update": "2024-04-15",
        "endpoints": [
            {"code": "6231", "designation": "ten", "last_update": "2024/05/21"},
            {"code": "9231", "designation": "thousand", "last_update": "2024/05/25"},
        ]
    }
}

endpoint_pool = {
    "1242": {"code": "1242", "designation": "Second", "last_update": "2024/02/19"},
    "4281": {"code": "4281", "designation": "Nine", "last_update": "2024/05/20"},
    "6231": {"code": "6231", "designation": "Ten", "last_update": "2024/05/21"},
    "9231": {"code": "9231", "designation": "New Endpoint", "last_update": "2024/06/01"},
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pending_deletes = set()
        self.pending_additions = set()

        self.setWindowTitle("Group Manager")
        self.resize(700, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Top control layout
        save_and_header = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.group_combo = QComboBox()
        self.group_combo.setCurrentIndex(0)
        
        self.group_combo.addItems(dummy_data.keys())
        self.group_combo.currentTextChanged.connect(self.load_group_data)

        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("Code")
        self.designation_edit = QLineEdit()
        self.designation_edit.setPlaceholderText("Designation")
        self.last_update_label = QLabel("")

        self.save_button = QPushButton("Save")

        top_layout.addWidget(self.group_combo)
        top_layout.addWidget(self.code_edit)
        top_layout.addWidget(self.designation_edit)
        top_layout.addWidget(QLabel("Last Update:"))
        top_layout.addWidget(self.last_update_label)
        
        save_and_header.addWidget(self.save_button)
        save_and_header.addLayout(top_layout)

        self.layout.addLayout(save_and_header)
        self.save_button.clicked.connect(self.save_new_data)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Code", "Designation", "Last Update", "Remove"])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(-1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionsMovable(True)
        self.table.horizontalHeader().setSectionsClickable(True)

        self.load_group_data(self.group_combo.currentText())

    def load_group_data(self, group_name):
        self.pending_deletes.clear()
        self.pending_additions.clear()
        group = dummy_data[group_name]
        self.code_edit.setText(group["code"])
        self.designation_edit.setText(group["designation"])
        self.last_update_label.setText(group["last_update"])

        endpoints = group["endpoints"]
        self.table.setRowCount(len(endpoints))
        available_code = set()
        print(endpoints)

        self.table.clearContents()
        for row, ep in enumerate(endpoints):
            self.table.setItem(row, 0, QTableWidgetItem(ep["code"]))
            self.table.setItem(row, 1, QTableWidgetItem(ep["designation"]))
            self.table.setItem(row, 2, QTableWidgetItem(ep["last_update"]))
            chk = QCheckBox()
            chk.checkStateChanged.connect(lambda _, r=row: self.toggle_row_removal(r))
            chk.setStyleSheet("""
                QCheckBox::indicator {
                    border: 2px solid white;
                    width: 15px;
                    height: 15px;
                }
                QCheckBox::indicator:checked {
                background-color: red;
                }
            """)
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(chk)
            layout.setAlignment(chk, Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            self.table.setCellWidget(row, 3, container)
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)  # editable
            self.table.item(row, 1).setFlags(self.table.item(row, 1).flags() & ~Qt.ItemIsEditable)  # editable
            self.table.item(row, 2).setFlags(self.table.item(row, 2).flags() & ~Qt.ItemIsEditable)  # NOT editable
            available_code.add(ep["code"])
        self.add_new_endpoint_row()

    def add_new_endpoint_row(self):
        row = self.table.rowCount()

        used_codes = set(e["code"] for e in dummy_data[self.group_combo.currentText()]["endpoints"])
        used_codes.update(e for e in self.pending_additions)

        available = [ep for ep in endpoint_pool.values() if ep["code"] not in used_codes]
        if not available:
            return  # No endpoints left to add

        self.table.insertRow(row)

        combo = QComboBox()
        combo.addItem("")
        for ep in available:
            combo.addItem(ep['code'])

        combo.currentIndexChanged.connect(self.fill_new_endpoint_row)
        self.table.setCellWidget(row, 0, combo)
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem(""))
        self.table.setItem(row, 3, QTableWidgetItem(""))

        self.table.item(row, 1).setFlags(self.table.item(row, 1).flags() & ~Qt.ItemIsEditable)  # editable
        self.table.item(row, 2).setFlags(self.table.item(row, 2).flags() & ~Qt.ItemIsEditable)  # editable
        self.table.item(row, 3).setFlags(self.table.item(row, 3).flags() & ~Qt.ItemIsEditable) 


    def toggle_row_removal(self, row):
        code = self.table.item(row, 0).text()

        if code not in self.pending_deletes:
            self.pending_deletes.add(code)
            self.set_row_red(row, True)
        else:
            self.pending_deletes.remove(code)
            self.set_row_red(row, False)

    def set_row_red(self, row, red=True):
        color = QColor(255, 80, 80) if red else QColor(255, 255, 255)
        for col in range(3):
            item = self.table.item(row, col)
            if item:
                item.setForeground(color)

    def fill_new_endpoint_row(self):
        combo = self.sender()
        if not isinstance(combo, QComboBox):
            return

        # Dynamically find the row of this combo
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 0) == combo:
                break
        else:
            return  # Combo not found

        text = combo.currentText().strip()
        if not text:
            return

        ep = endpoint_pool.get(text)
        if not ep:
            return

        # Replace combo with static text
        combo.setEnabled(False)
        combo.setStyleSheet("background-color: blue;")
        self.table.removeCellWidget(row, 0)
        item_code = QTableWidgetItem(ep["code"])
        item_code.setForeground(QColor("green"))
        item_code.setFlags(item_code.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, 0, item_code)

        item_designation = QTableWidgetItem(ep["designation"])
        item_designation.setForeground(QColor("green"))
        item_designation.setFlags(item_designation.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, 1, item_designation)

        item_update = QTableWidgetItem(ep["last_update"])
        item_update.setForeground(QColor("green"))
        item_update.setFlags(item_update.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, 2, item_update)

        btn = QPushButton("Revert")
        btn.clicked.connect(self.clear_pending_row)
        self.table.setCellWidget(row, 3, btn)

        if ep["code"] not in self.pending_additions:
            self.pending_additions.add(ep["code"])

        # Check for empty rows; only add new if none are empty
        if not self.has_empty_endpoint_row():
            self.add_new_endpoint_row()

    def has_empty_endpoint_row(self):
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, 0)

            if isinstance(widget, QComboBox) and widget.currentText().strip() == "":
                return True
        return False


    def clear_pending_row(self):
        btn = self.sender()
        if not isinstance(btn, QPushButton):
            return

        # Find which row this button is in
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 3) == btn:
                break
        else:
            return  # Button not found in any row

        # Get the code from the row
        item = self.table.item(row, 0)
        if item:
            code = item.text().strip()
            self.pending_additions.remove(code)

        # Remove the row from the table
        self.table.removeRow(row)
        if not self.has_empty_endpoint_row():
            self.add_new_endpoint_row()
        


    def save_new_data(self):
        group_name = self.group_combo.currentText()
        code = self.code_edit.text()
        designation = self.designation_edit.text()
        last_update = datetime.now().strftime("%Y-%m-%d")

        # Update the dummy data
        dummy_data[group_name]["code"] = code
        dummy_data[group_name]["designation"] = designation
        dummy_data[group_name]["last_update"] = last_update

        # Reload the data to reflect changes

        for code in self.pending_deletes:
            for endpoint in dummy_data[group_name]["endpoints"]:
                if endpoint["code"] == code:
                    dummy_data[group_name]["endpoints"].remove(endpoint)
                    break
                
        for code in self.pending_additions:
            dummy_data[group_name]["endpoints"].append(endpoint_pool[code])
        
        self.pending_additions.clear()
        self.pending_deletes.clear()
        self.load_group_data(group_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
