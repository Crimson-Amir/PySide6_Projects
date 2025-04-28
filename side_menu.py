from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QFrame, QSizePolicy, QApplication)
from PySide6.QtCore import Qt, QPoint, Signal, QTimer
from PySide6.QtGui import QGuiApplication

class SideMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Side Menu Example")
        self.setMinimumSize(800, 200)
        self.submenu = None
        self.current_menu_btn = None
        
        # Main container setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Horizontal layout for side menu + content
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Side panel setup
        self.side_panel = QFrame()
        # self.side_panel.setFixedWidth(200)x
        self.side_panel.setStyleSheet("""
            background: #f5f5f5;
            border-right: 1px solid #ddd;
        """)
        main_layout.addWidget(self.side_panel, stretch=1)

        # Content area setup
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background: white;")
        main_layout.addWidget(self.content_area, stretch=4)

        # Initialize menu
        self.setup_menu()
        
        # Submenu container (initially hidden)
        self.submenu_container = QWidget(self)
        # self.submenu_container.setStyleSheet("background: #444;")
        self.submenu_container.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.submenu_container.hide()

    def setup_menu(self):
        menu_layout = QVBoxLayout(self.side_panel)
        menu_layout.setContentsMargins(0, 10, 0, 10)
        menu_layout.setSpacing(5)

        self.menu_buttons = []
        options = ["Dashboard", "Projects", "Team", 
                  "Analytics", "Settings", "Help"]
        
        for text in options:
            btn = SubMenuButton(text)
            btn.setFixedHeight(40)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(self.toggle_submenu)
            
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 15px;
                    border: none;
                    font-size: 14px;
                    color: #444;
                }
                QPushButton:hover {
                    background: #e8e8e8;
                }
                QPushButton[active="true"] {
                    background: #e0e0e0;
                }
            """)
            
            menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        menu_layout.addStretch()

    def toggle_submenu(self):
        clicked_btn = self.sender()

        if self.submenu_container.isVisible() and clicked_btn == self.current_menu_btn:
            # Clicked the same button - close submenu
            self.close_submenu()
            return

        # Close previous submenu and create new one
        self.close_submenu()
        self.current_menu_btn = clicked_btn
        clicked_btn.setProperty("active", "true")
        clicked_btn.style().polish(clicked_btn)
        
        # Create submenu content
        self.create_submenu_content(clicked_btn.text())
        
        # Calculate and set position
        self.position_submenu(clicked_btn)
        self.submenu_container.show()

    def create_submenu_content(self, parent_text):
        # Clear previous content
        if self.submenu_container.layout():
            QWidget().setLayout(self.submenu_container.layout())
        
        submenu_layout = QVBoxLayout(self.submenu_container)
        submenu_layout.setContentsMargins(5, 10, 5, 10)
        submenu_layout.setSpacing(5)
        
        # Add sample submenu items
        sub_items = {
            "Dashboard": ["Overview", "Activity", "Statistics"],
            "Projects": ["New Project", "Templates", "Archive"],
            "Team": ["Members", "Roles", "Permissions"],
            "Analytics": ["Reports", "Exports", "Integrations"],
            "Settings": ["Account", "Preferences", "Security"],
            "Help": ["Documentation", "Support", "Feedback"]
        }.get(parent_text, [])
        
        for item in sub_items:
            sub_btn = QPushButton(item)
            sub_btn.setFixedHeight(35)
            sub_btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 20px;
                    border-radius: 3px;
                    font-size: 13px;
                    color: white;
                }
                QPushButton:hover {
                    background: red;
                }
            """)
            submenu_layout.addWidget(sub_btn)
        
        self.submenu_container.adjustSize()

    def position_submenu(self, parent_btn):
        # Get button position relative to main window
        btn_global_pos = parent_btn.mapToGlobal(QPoint(0, 0))
        btn_bottom = btn_global_pos.y() + parent_btn.height()
        
        # Get available screen geometry
        screen = QGuiApplication.primaryScreen().availableGeometry()
        screen_bottom = screen.bottom()
        
        # Calculate available space below the button
        space_below = screen_bottom - btn_bottom
        submenu_height = self.submenu_container.sizeHint().height()
        
        # Determine position based on available space
        if space_below >= submenu_height or btn_global_pos.y() < screen.center().y():
            # Position below, align top edges
            pos = QPoint(
                btn_global_pos.x() + parent_btn.width(),
                btn_global_pos.y()
            )
        else:
            # Position above, align bottom edges
            pos = QPoint(
                btn_global_pos.x() + parent_btn.width(),
                btn_global_pos.y() + parent_btn.height() - submenu_height
            )
        
        # Adjust for window position
        window_pos = self.mapToGlobal(QPoint(0, 0))
        final_pos = pos - window_pos
        
        # Ensure it stays within window bounds
        max_x = self.width() - self.submenu_container.width()
        final_pos.setX(min(final_pos.x(), max_x))
        
        self.submenu_container.move(final_pos)

    def close_submenu(self):
        if self.current_menu_btn:
            self.current_menu_btn.setProperty("active", "false")
            self.current_menu_btn.style().polish(self.current_menu_btn)
            self.current_menu_btn = None
        self.submenu_container.hide()

    def mousePressEvent(self, event):
        # Close submenu when clicking outside
        if not self.submenu_container.geometry().contains(event.globalPos()):
            self.close_submenu()
        super().mousePressEvent(event)

class SubMenuButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SideMenu()
    window.show()
    sys.exit(app.exec())