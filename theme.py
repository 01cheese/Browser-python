from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QApplication
from PyQt5.QtGui import QPalette, QColor
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
        for i in range(self.parent.tabs.count()):
            self.apply_theme_to_page(self.parent.tabs.widget(i))

    def disable_dark_mode(self):
        self.dark_mode_enabled = False
        self.apply_theme_to_app()
        for i in range(self.parent.tabs.count()):
            self.apply_theme_to_page(self.parent.tabs.widget(i))

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
        else:
            QApplication.setStyle("Fusion")
            QApplication.setPalette(QApplication.style().standardPalette())

    def apply_theme_to_page(self, browser):
        if self.dark_mode_enabled:
            browser.page().runJavaScript("""
                (function() {
                    var css = 'html, body { background-color: #333; color: #ccc; } a { color: #42a2da; }';
                    var head = document.head || document.getElementsByTagName('head')[0];
                    var style = document.createElement('style');
                    style.type = 'text/css';
                    if (style.styleSheet) {
                        style.styleSheet.cssText = css;
                    } else {
                        style.appendChild(document.createTextNode(css));
                    }
                    head.appendChild(style);
                })();
            """)
        else:
            browser.page().runJavaScript("""
                (function() {
                    var css = 'html, body { background-color: #fff; color: #000; } a { color: #1a0dab; }';
                    var head = document.head || document.getElementsByTagName('head')[0];
                    var style = document.createElement('style');
                    style.type = 'text/css';
                    if (style.styleSheet) {
                        style.styleSheet.cssText = css;
                    } else {
                        style.appendChild(document.createTextNode(css));
                    }
                    head.appendChild(style);
                })();
            """)

