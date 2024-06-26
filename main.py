from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import json
import os

class BookmarkDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(BookmarkDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        rect = option.rect.adjusted(0, 5, 0, -5)  # Adding top and bottom space
        painter.setRenderHint(QPainter.Antialiasing, True)

        text = index.data(Qt.DisplayRole)

        painter.setBrush(QColor("#2c2c2c"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 5, 5)

        painter.setPen(QColor("#ffffff"))
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(rect.adjusted(10, 0, 0, 0), Qt.AlignVCenter | Qt.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 50)  # Increased size for space

class BookmarkItemWidget(QWidget):
    def __init__(self, text, parent=None):
        super(BookmarkItemWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.label.setStyleSheet("color: white; background-color: #2c2c2c; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 5, 0, 5)  # Add spacing between items
        self.setLayout(layout)

class MyWebBrowser():
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Woah My Web Browser")
        self.window.setStyleSheet("background-color: #171717;")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                color: #333333;
                font-size: 16px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.completer = QCompleter()
        self.completion_model = QStringListModel()
        self.completer.setModel(self.completion_model)
        self.url_bar.setCompleter(self.completer)

        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)
        self.go_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        self.bookmark_btn = QPushButton("Bookmark")
        self.bookmark_btn.setMinimumHeight(30)
        self.bookmark_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        self.remove_bookmark_btn = QPushButton("Remove Bookmark")
        self.remove_bookmark_btn.setMinimumHeight(30)
        self.remove_bookmark_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.bookmark_btn)
        self.horizontal.addWidget(self.remove_bookmark_btn)

        self.bookmarks_list = QListWidget()
        self.bookmarks_list.setMaximumHeight(150)
        self.bookmarks_list.setItemDelegate(BookmarkDelegate(self.bookmarks_list))
        self.bookmarks_list.setStyleSheet("""
            QListWidget {
                background-color: #0a0a0a;
                color: white;
                font-size: 16px;
                border: 1px solid #0a0a0a;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.browser = QWebEngineView()

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.remove_bookmark_btn.clicked.connect(self.remove_bookmark)
        self.bookmarks_list.itemClicked.connect(self.load_bookmark)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.bookmarks_list)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl("http://google.com"))

        self.window.setLayout(self.layout)
        self.window.resize(800, 600)
        self.window.show()

        self.load_bookmarks()

        self.url_bar.textChanged.connect(self.update_autocomplete)

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))
        self.url_bar.clearFocus()

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        item_widget = BookmarkItemWidget(current_url)
        list_item = QListWidgetItem(self.bookmarks_list)
        list_item.setSizeHint(item_widget.sizeHint())

        self.bookmarks_list.addItem(list_item)
        self.bookmarks_list.setItemWidget(list_item, item_widget)
        self.save_bookmarks()

    def load_bookmark(self, item):
        self.browser.setUrl(QUrl(item.text()))

    def remove_bookmark(self):
        selected_items = self.bookmarks_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.bookmarks_list.takeItem(self.bookmarks_list.row(item))
        self.save_bookmarks()

    def save_bookmarks(self):
        bookmarks = []
        for index in range(self.bookmarks_list.count()):
            item = self.bookmarks_list.item(index)
            widget = self.bookmarks_list.itemWidget(item)
            bookmarks.append(widget.label.text())
        with open("bookmarks.json", "w") as file:
            json.dump(bookmarks, file)

    def load_bookmarks(self):
        if os.path.exists("bookmarks.json"):
            with open("bookmarks.json", "r") as file:
                bookmarks = json.load(file)
                for bookmark in bookmarks:
                    item_widget = BookmarkItemWidget(bookmark)
                    list_item = QListWidgetItem(self.bookmarks_list)
                    list_item.setSizeHint(item_widget.sizeHint())

                    self.bookmarks_list.addItem(list_item)
                    self.bookmarks_list.setItemWidget(list_item, item_widget)

    def update_autocomplete(self, text):
        suggestions = ["linkedin.com", "gmail.com", "youtube.com"]
        self.completion_model.setStringList(suggestions)

app = QApplication([])
window = MyWebBrowser()
app.exec_()
