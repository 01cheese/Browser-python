from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QApplication
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class ThemeManager:
    def __init__(self, parent):
        self.parent = parent
        self.dark_mode_enabled = False

    def show_theme_dialog(self):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Change Theme")

        layout = QVBoxLayout()

        light_theme_button = QRadioButton("Light Theme")
        dark_theme_button = QRadioButton("Dark Theme")

        if self.dark_mode_enabled:
            dark_theme_button.setChecked(True)
        else:
            light_theme_button.setChecked(True)

        layout.addWidget(light_theme_button)
        layout.addWidget(dark_theme_button)

        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

        ok_button.clicked.connect(lambda: self.change_theme(dark_theme_button.isChecked()))
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()

    def change_theme(self, dark_mode):
        if dark_mode:
            self.enable_dark_mode()
        else:
            self.disable_dark_mode()

    def enable_dark_mode(self):
        self.dark_mode_enabled = True
        self.apply_theme_to_app()

    def disable_dark_mode(self):
        self.dark_mode_enabled = False
        self.apply_theme_to_app()

    def apply_theme_to_app(self):
        if self.dark_mode_enabled:
            QApplication.setStyle("Fusion")
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(dark_palette)
            QApplication.setStyleSheet(self.dark_qss())
        else:
            QApplication.setStyle("Fusion")
            QApplication.setPalette(QApplication.style().standardPalette())
            QApplication.setStyleSheet("")

    def dark_qss(self):
        return """
        QMainWindow {
            background-color: #353535;
        }
        QMenuBar {
            background-color: #444444;
            color: #ffffff;
        }
        QMenuBar::item {
            background: #444444;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background: #666666;
        }
        QMenu {
            background-color: #444444;
            color: #ffffff;
        }
        QMenu::item {
            background-color: #444444;
            color: #ffffff;
        }
        QMenu::item:selected {
            background-color: #666666;
        }
        QTabBar::tab {
            background: #555555;
            color: #ffffff;
            padding: 5px;
        }
        QTabBar::tab:selected {
            background: #777777;
        }
        QToolBar {
            background: #444444;
        }
        QToolBar QToolButton {
            background: #555555;
            color: #ffffff;
            border: none;
            padding: 5px;
        }
        QToolBar QToolButton:hover {
            background: #666666;
        }
        QStatusBar {
            background: #444444;
            color: #ffffff;
        }
        QLineEdit {
            background: #555555;
            color: #ffffff;
            border: 1px solid #777777;
        }
        QProgressBar {
            background: #555555;
            color: #ffffff;
            border: 1px solid #777777;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: #555555;
        }
        QSlider::handle:horizontal {
            background: #777777;
            border: 1px solid #444444;
            width: 18px;
            margin: -6px 0;
        }
        QPushButton {
            background-color: #555555;
            color: #ffffff;
            border: none;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #777777;
        }
        """
