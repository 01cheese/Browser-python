from PyQt5.QtWidgets import QAction, QMessageBox, QMenu, QInputDialog
from functools import partial
from PyQt5.QtCore import QUrl


class BookmarkManager:
    def __init__(self, parent):
        self.parent = parent
        self.bookmarks = []

    def add_bookmark(self, title, url):
        self.bookmarks.append((title, url))
        self.update_bookmarks_menu()
        self.update_bookmarks_bar()

    def delete_bookmark(self, title, url):
        self.bookmarks = [(t, u) for t, u in self.bookmarks if t != title or u != url]
        self.update_bookmarks_menu()
        self.update_bookmarks_bar()

    def edit_bookmark(self, old_title, old_url):
        new_title, ok = QInputDialog.getText(self.parent, "Edit Bookmark", "New title:", text=old_title)
        if ok and new_title:
            self.bookmarks = [(new_title, u) if (t == old_title and u == old_url) else (t, u) for t, u in
                              self.bookmarks]
            self.update_bookmarks_menu()
            self.update_bookmarks_bar()

    def populate_bookmarks_menu(self, bookmarks_menu):
        self.bookmarks_menu = bookmarks_menu
        self.update_bookmarks_menu()

    def update_bookmarks_menu(self):
        self.bookmarks_menu.clear()
        for title, url in self.bookmarks:
            bookmark_action = QAction(title, self.parent)
            bookmark_action.triggered.connect(partial(self.parent.add_new_tab, QUrl(url), title))
            edit_action = QAction("Edit", self.parent)
            edit_action.triggered.connect(partial(self.edit_bookmark, title, url))
            delete_action = QAction("Delete", self.parent)
            delete_action.triggered.connect(partial(self.delete_bookmark, title, url))

            submenu = QMenu(title, self.parent)
            submenu.addAction(bookmark_action)
            submenu.addAction(edit_action)
            submenu.addAction(delete_action)
            self.bookmarks_menu.addMenu(submenu)

        self.bookmarks_menu.addSeparator()
        clear_bookmarks_action = QAction("Clear Bookmarks", self.parent)
        clear_bookmarks_action.triggered.connect(self.clear_bookmarks)
        self.bookmarks_menu.addAction(clear_bookmarks_action)

    def update_bookmarks_bar(self):
        self.parent.update_bookmarks_bar()

    def clear_bookmarks(self):
        self.bookmarks.clear()
        self.update_bookmarks_menu()
        self.update_bookmarks_bar()
        QMessageBox.information(self.parent, "Bookmarks Cleared", "All bookmarks have been cleared.")
