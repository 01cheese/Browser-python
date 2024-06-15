from PyQt5.QtWidgets import QAction, QMessageBox
from functools import partial
from PyQt5.QtCore import QUrl

class BookmarkManager:
    def __init__(self, parent):
        self.parent = parent
        self.bookmarks = []

    def add_bookmark(self, title, url):
        self.bookmarks.append((title, url))
        self.update_bookmarks_menu()

    def populate_bookmarks_menu(self, bookmarks_menu):
        self.bookmarks_menu = bookmarks_menu
        self.update_bookmarks_menu()

    def update_bookmarks_menu(self):
        self.bookmarks_menu.clear()
        for title, url in self.bookmarks:
            bookmark_action = QAction(title, self.parent)
            bookmark_action.triggered.connect(partial(self.parent.add_new_tab, QUrl(url), title))
            self.bookmarks_menu.addAction(bookmark_action)

        self.bookmarks_menu.addSeparator()
        clear_bookmarks_action = QAction("Clear Bookmarks", self.parent)
        clear_bookmarks_action.triggered.connect(self.clear_bookmarks)
        self.bookmarks_menu.addAction(clear_bookmarks_action)

    def clear_bookmarks(self):
        self.bookmarks.clear()
        self.update_bookmarks_menu()
        QMessageBox.information(self.parent, "Bookmarks Cleared", "All bookmarks have been cleared.")
