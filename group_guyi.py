from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QHeaderView, QMenu, QMessageBox 
)
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from datetime import datetime
import json
import os

class AppConfig:
    def __init__(self, filename="setting.json"):
        self.file_path = os.path.join(os.path.dirname(__file__), filename)
        self.data = self.load_config()

    def load_config(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)

    def save_config(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print("Failed to save config:", e)


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

class CustomTable(QTableWidget):
    def __init__(
            self, dummy_data, endpoint_pool, group_combo
            ):
        super().__init__()
        self.group_combo = group_combo
        self.config = AppConfig("group_config.json")
        self.dummy_data = dummy_data
        self.endpoint = endpoint_pool

        self.pending_deletes = set()
        self.pending_additions = set()
        self.skip_revert_confirmation = False

        self.setColumnCount(4)
        header = self.get_header()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_context_menu)

        # header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(-1, QHeaderView.ResizeToContents)
        header.setSectionsMovable(True)
        header.setSectionsClickable(True)
        header.sectionResized.connect(self.column_width_resized)
        header.sectionMoved.connect(self.column_moved)

        self.menu_button = QPushButton("☰")
        self.menu_button.setFixedWidth(30)
        self.menu_button.mousePressEvent = self.handle_menu_button_click

    def return_hidden_menu(self):
        return self.menu_button

    def get_header(self):
        return self.horizontalHeader()
    
    def header_context_menu(self, pos):
        header = self.get_header()
        logical_index = header.logicalIndexAt(pos)
        if logical_index < 1:
            return
        menu = QMenu(self)
        hide_action = menu.addAction("Hide Column")
        action = menu.exec(header.mapToGlobal(pos))

        if action == hide_action:
            self.setColumnHidden(logical_index, True)
            hidden = self.config.data.setdefault("table_settings", {}).setdefault("hidden_columns", [])
            
            if logical_index not in hidden:
                hidden.append(logical_index)

            self.config.save_config()


    def column_width_resized(self, logical_index, _, new_size):
        hidden = self.config.data.setdefault("table_settings", {}).setdefault("hidden_columns", []) 
        if logical_index not in hidden:
            self.config.data["table_settings"]["column_widths"][str(logical_index)] = new_size
    

    def column_moved(self, logical_index, old_visual_index, new_visual_index):
        header = self.get_header()
        if logical_index == 0:
            header.moveSection(new_visual_index, old_visual_index)
            return
        order = [header.logicalIndex(i) for i in range(header.count())]
        print(order)
        self.config.data["table_settings"]["column_order"] = order 
        self.config.save_config()


    def restore_column_order(self):
        order = self.config.data["table_settings"].get("column_order")
        if not order:
            return

        header = self.horizontalHeader()
        for visual_index, logical_index in enumerate(order):
            current_visual = header.visualIndex(logical_index)
            if current_visual != visual_index:
                header.moveSection(current_visual, visual_index)
        
        hidden = self.config.data.get("table_settings", {}).get("hidden_columns", [])
        for index in hidden:
            self.setColumnHidden(index, True)

    def change_row_color(self, row, color: QColor = QColor(255, 255, 255)):
        for col in range(3):
            item = self.item(row, col)
            if item:
                item.setForeground(color)

    def toggle_row_removal(self, row):
        code = self.item(row, 0).text()

        if code not in self.pending_deletes:
            self.pending_deletes.add(code)
            self.change_row_color(row, QColor(255, 80, 80))
        else:
            self.pending_deletes.remove(code)
            self.change_row_color(row)


    def has_empty_endpoint_row(self):
        for row in range(self.rowCount()):
            widget = self.cellWidget(row, 0)

            if isinstance(widget, QComboBox) and widget.currentText().strip() == "":
                return True
        return False
    

    def save_new_data(self, code, designation):
        group_name = self.group_combo.currentText()
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


    def clear_pending_row(self):
        if self.config.data.get("dialog_settings").get("show_revert_warning"):
            confirm_dialog = QMessageBox(self)
            confirm_dialog.setWindowTitle("Confirm Revert")
            confirm_dialog.setText("Are you sure you want to revert?")
            confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_dialog.setIcon(QMessageBox.Question)

            dont_ask_again = QCheckBox("Don't show this message again")
            confirm_dialog.setCheckBox(dont_ask_again)

            result = confirm_dialog.exec()

            if result == QMessageBox.No:
                return

            if dont_ask_again.isChecked():
                self.config.data["dialog_settings"]["show_revert_warning"] = False
                print(self.config.data)
                self.config.save_config()


        btn = self.sender()
        if not isinstance(btn, QPushButton):
            return

        for row in range(self.rowCount()):
            if self.cellWidget(row, 3) == btn:  # column_indexes.get("3")
                break
        else:
            return

        # Get the code from the row
        item = self.item(row, 0)  # column_indexes.get("0")
        if item:
            code = item.text().strip()
            self.pending_additions.remove(code)

        self.removeRow(row)
        if not self.has_empty_endpoint_row():
            self.add_new_endpoint_row()


    def fill_new_endpoint_row(self):
        combo = self.sender()

        if not isinstance(combo, QComboBox):
            return
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0) == combo:  # column_indexes.get("0")
                break
        else:
            return

        text = combo.currentText().strip()
        if not text:
            return

        ep = endpoint_pool.get(text)
        if not ep:
            return

        combo.setEnabled(False)
        combo.setStyleSheet("background-color: blue;")
        self.removeCellWidget(row, 0)  # column_indexes.get("0")
        item_code = QTableWidgetItem(ep["code"])
        item_code.setForeground(QColor("green"))
        item_code.setFlags(item_code.flags() & ~Qt.ItemIsEditable)
        self.setItem(row, 0, item_code)  # column_indexes.get("0")

        item_designation = QTableWidgetItem(ep["designation"])
        item_designation.setForeground(QColor("green"))
        item_designation.setFlags(item_designation.flags() & ~Qt.ItemIsEditable)
        self.setItem(row, 1, item_designation)

        item_update = QTableWidgetItem(ep["last_update"])
        item_update.setForeground(QColor("green"))
        item_update.setFlags(item_update.flags() & ~Qt.ItemIsEditable)
        self.setItem(row, 2, item_update)

        btn = QPushButton("Revert")
        btn.clicked.connect(self.clear_pending_row)
        self.setCellWidget(row, 3, btn)

        if ep["code"] not in self.pending_additions:
            self.pending_additions.add(ep["code"])

        if not self.has_empty_endpoint_row():
            self.add_new_endpoint_row()


    def add_new_endpoint_row(self):
        row = self.rowCount()

        used_codes = set(e["code"] for e in dummy_data[self.group_combo.currentText()]["endpoints"])
        used_codes.update(e for e in self.pending_additions)
        available = [ep for ep in endpoint_pool.values() if ep["code"] not in used_codes]
        
        if not available:
            return

        self.insertRow(row)

        combo = QComboBox()
        combo.addItem("")
        for ep in available:
            combo.addItem(ep['code'])

        self.restore_column_order()

        combo.currentIndexChanged.connect(self.fill_new_endpoint_row)
        self.setCellWidget(row, 0, combo)
        self.setItem(row, 1, QTableWidgetItem(""))
        self.setItem(row, 2, QTableWidgetItem(""))
        self.setItem(row, 3, QTableWidgetItem(""))

        self.item(row, 1).setFlags(self.item(row, 1).flags() & ~Qt.ItemIsEditable)
        self.item(row, 2).setFlags(self.item(row, 2).flags() & ~Qt.ItemIsEditable)
        self.item(row, 3).setFlags(self.item(row, 3).flags() & ~Qt.ItemIsEditable) 


    def load_group_data(self, group_name):
        self.config.save_config()
        self.pending_deletes.clear()
        self.pending_additions.clear()

        group = dummy_data[group_name]

        endpoints = group["endpoints"]
        self.setRowCount(len(endpoints))
        available_code = set()

        table_setting = self.config.data.get("table_settings", {}) 
        column_widths = table_setting.get("column_widths", {"0": 100, "1": 100, "2": 100, "3": 100})

        headers = ["Code", "Designation", "Last Update", "Remove"]
        self.setHorizontalHeaderLabels(headers)
        self.restore_column_order()  
        
        self.clearContents()
        for row, ep in enumerate(endpoints):
            self.setItem(row, 0, QTableWidgetItem(ep["code"]))
            self.setItem(row, 1, QTableWidgetItem(ep["designation"]))
            self.setItem(row, 2, QTableWidgetItem(ep["last_update"]))
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

            self.setCellWidget(row, 3, container)

            available_code.add(ep["code"])

            self.setColumnWidth(0, column_widths.get("0"))
            self.setColumnWidth(1, column_widths.get("1"))
            self.setColumnWidth(2, column_widths.get("2"))
            self.setColumnWidth(3, column_widths.get("3"))

        self.add_new_endpoint_row()
        return group

    def handle_menu_button_click(self, event):
        if event.button() == Qt.LeftButton:
            menu = self.get_hidden_columns_menu()
            if menu:
                menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
        else:
            super(QPushButton, self.menu_button).mousePressEvent(event)
    
    def get_hidden_columns_menu(self):
        menu = QMenu()
        hidden = self.config.data.get("table_settings", {}).get("hidden_columns", [])
        if not hidden:
            act = menu.addAction(f"there is no hidden column")
            act.setDisabled(True)
            return menu
        
        for logical_index in hidden:
            header_text = self.horizontalHeaderItem(logical_index).text()
            action = menu.addAction(f"Unhide {header_text}")
            action.triggered.connect(lambda checked=False, idx=logical_index: self.unhide_column(idx))
        
        return menu 


    def unhide_column(self, logical_index):
        self.setColumnHidden(logical_index, False)
        hidden = self.config.data.get("table_settings", {}).get("hidden_columns", [])
        if logical_index in hidden:
            hidden.remove(logical_index)
            self.config.save_config()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = AppConfig("main_configuration.json")

        self.setWindowTitle("Group Manager")
        self.resize(
            self.config.data.get("main_window").get("size").get("width", 700),
            self.config.data.get("main_window").get("size").get("height", 400)
            )
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Top control layout
        save_and_header = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.group_combo = QComboBox()
        self.table = CustomTable(dummy_data, endpoint_pool, self.group_combo)
        self.group_combo.setCurrentIndex(0)
        
        self.group_combo.addItems(dummy_data.keys())
        self.group_combo.currentTextChanged.connect(self.table.load_group_data)

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
        top_layout.addWidget(self.table.return_hidden_menu())

        
        save_and_header.addWidget(self.save_button)
        save_and_header.addLayout(top_layout)

        self.layout.addLayout(save_and_header)
        self.save_button.clicked.connect(self.save_new_data)

        self.layout.addWidget(self.table)

        group = self.table.load_group_data(self.group_combo.currentText())

        self.code_edit.setText(group["code"])
        self.designation_edit.setText(group["designation"])
        self.last_update_label.setText(group["last_update"])

    def save_new_data(self):
        code = self.code_edit.text()
        designation = self.designation_edit.text()
        self.table.save_new_data(code, designation)

    def closeEvent(self, event):
        self.config.data["main_window"]["size"]["width"] = self.width()
        self.config.data["main_window"]["size"]["height"] = self.height()
        self.config.save_config()
        self.table.config.save_config()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
