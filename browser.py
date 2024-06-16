import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from theme import ThemeManager
from bookmarks import BookmarkManager
from functools import partial
import favicon
import asyncio
import threading


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.theme_manager = ThemeManager(self)
        self.bookmark_manager = BookmarkManager(self)

        self.downloads = []

        self.create_navbar()
        self.create_bookmarks_bar()
        self.create_status_bar()
        self.create_menu()

        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")

        self.showMaximized()

    def create_navbar(self):
        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.setIcon(QIcon("icons/back.png"))
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.setIcon(QIcon("icons/forward.png"))
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.setIcon(QIcon("icons/reload.png"))
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.setIcon(QIcon("icons/home.png"))
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        bookmark_btn = QAction(QIcon("icons/bookmark.png"), "Bookmark", self)
        bookmark_btn.triggered.connect(self.bookmark_page)
        navbar.addAction(bookmark_btn)

        self.downloads_btn = QAction(QIcon("icons/download.png"), "Downloads", self)
        self.downloads_btn.triggered.connect(self.show_downloads)
        navbar.addAction(self.downloads_btn)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        navbar.addWidget(self.progress)

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(25)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.valueChanged.connect(self.change_zoom)
        navbar.addWidget(self.zoom_slider)

    def create_bookmarks_bar(self):
        self.bookmarks_bar = QToolBar("Bookmarks")
        self.addToolBar(Qt.TopToolBarArea, self.bookmarks_bar)
        self.bookmarks_bar.setMovable(False)
        self.update_bookmarks_bar()

    def update_bookmarks_bar(self):
        self.bookmarks_bar.clear()
        for title, url in self.bookmark_manager.bookmarks:
            icon = self.get_favicon(url)
            bookmark_btn = QAction(QIcon(icon), title, self)
            bookmark_btn.triggered.connect(partial(self.add_new_tab, QUrl(url), title))
            self.bookmarks_bar.addAction(bookmark_btn)

    def get_favicon(self, url):
        icons = favicon.get(url)
        icon = icons[0] if icons else None
        if icon:
            return QIcon(QPixmap(icon.url))
        else:
            return QIcon()

    def create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(lambda: self.add_new_tab(QUrl("http://www.google.com"), "New Tab"))
        file_menu.addAction(new_tab_action)

        new_window_action = QAction("New Window", self)
        new_window_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_window_action)

        new_incognito_action = QAction("New Incognito Window", self)
        new_incognito_action.setShortcut("Ctrl+Shift+N")
        file_menu.addAction(new_incognito_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menubar.addMenu("&Settings")

        change_theme_action = QAction("Change Theme", self)
        change_theme_action.triggered.connect(self.theme_manager.show_theme_dialog)
        settings_menu.addAction(change_theme_action)

        view_history_action = QAction("View History", self)
        view_history_action.triggered.connect(self.view_history)
        settings_menu.addAction(view_history_action)

        bookmarks_menu = menubar.addMenu("&Bookmarks")
        self.bookmark_manager.populate_bookmarks_menu(bookmarks_menu)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(partial(self.update_url, browser=browser))
        browser.loadProgress.connect(self.update_progress)
        browser.loadFinished.connect(partial(self.update_tab_title, i=i, browser=browser))

        browser.page().profile().downloadRequested.connect(self.on_download_requested)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())
        self.update_zoom(self.tabs.currentWidget().zoomFactor())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())

    def update_progress(self, progress):
        self.progress.setValue(progress)
        if progress == 100:
            self.progress.hide()
        else:
            self.progress.show()

    def update_tab_title(self, _, i, browser):
        self.tabs.setTabText(i, browser.page().title())

    def change_zoom(self, value):
        self.tabs.currentWidget().setZoomFactor(value / 50.0)

    def update_zoom(self, value):
        self.zoom_slider.setValue(int(value * 125))

    def view_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("History")
        history_layout = QVBoxLayout()
        history_view = QListWidget()
        history_items = self.tabs.currentWidget().history().items()
        for item in history_items:
            history_view.addItem(item.url().toString())
        history_layout.addWidget(history_view)
        history_dialog.setLayout(history_layout)
        history_dialog.exec_()

    def bookmark_page(self):
        current_url = self.tabs.currentWidget().url().toString()
        current_title = self.tabs.currentWidget().page().title()
        title, ok = QInputDialog.getText(self, "Bookmark", "Enter title:", text=current_title)
        if ok and title:
            self.bookmark_manager.add_bookmark(title, current_url)
            self.update_bookmarks_bar()

    def on_download_requested(self, download):
        self.downloads.append(download)
        self.handle_download(download)

    def handle_download(self, download):
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if download_path:
            download.setPath(download_path)
            download.accept()
            self.start_download_progress(download, download_path)
        else:
            download.cancel()

    def start_download_progress(self, download, download_path):
        dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self)
        dialog.setWindowTitle("Download")
        dialog.setWindowModality(Qt.WindowModal)
        dialog.setValue(0)
        dialog.show()

        def progress_callback(received, total):
            dialog.setValue(int(received / total * 100))

        def state_callback(state):
            if state == QWebEngineDownloadItem.DownloadCompleted:
                dialog.close()
                QMessageBox.information(self, "Download Completed", "File downloaded successfully!")
            elif state == QWebEngineDownloadItem.DownloadCancelled:
                dialog.close()
                QMessageBox.warning(self, "Download Cancelled", "File download was cancelled.")
            elif state == QWebEngineDownloadItem.DownloadInterrupted:
                dialog.close()
                QMessageBox.critical(self, "Download Interrupted", "File download was interrupted.")

        download.downloadProgress.connect(progress_callback)
        download.stateChanged.connect(state_callback)

        download.downloadProgress.connect(lambda received, total: progress_callback(received, total))
        download.stateChanged.connect(lambda state: state_callback(state))

    async def download_file(self, download, download_path):
        dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self)
        dialog.setWindowTitle("Download")
        dialog.setWindowModality(Qt.WindowModal)
        dialog.setValue(0)
        dialog.show()

        def progress_callback(received, total):
            dialog.setValue(int(received / total * 100))

        def state_callback(state):
            if state == QWebEngineDownloadItem.DownloadCompleted:
                dialog.close()
                QMessageBox.information(self, "Download Completed", "File downloaded successfully!")
            elif state == QWebEngineDownloadItem.DownloadCancelled:
                dialog.close()
                QMessageBox.warning(self, "Download Cancelled", "File download was cancelled.")
            elif state == QWebEngineDownloadItem.DownloadInterrupted:
                dialog.close()
                QMessageBox.critical(self, "Download Interrupted", "File download was interrupted.")

        download.downloadProgress.connect(progress_callback)
        download.stateChanged.connect(state_callback)

        while download.state() in [QWebEngineDownloadItem.DownloadRequested, QWebEngineDownloadItem.DownloadInProgress]:
            await asyncio.sleep(0.1)

    def show_downloads(self):
        downloads_dialog = QDialog(self)
        downloads_dialog.setWindowTitle("Downloads")
        layout = QVBoxLayout()

        for download in self.downloads:
            download_info = f"{download.path().split('/')[-1]} - {download.state()}"
            label = QLabel(download_info)
            layout.addWidget(label)

        downloads_dialog.setLayout(layout)
        downloads_dialog.exec_()


app = QApplication(sys.argv)
QApplication.setApplicationName("My Browser")
window = Browser()
app.exec_()
