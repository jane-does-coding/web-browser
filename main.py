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

    def get_text(self):
        return self.label.text()

class MyWebBrowser():
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Woah My Web Browser")
        self.window.setStyleSheet("background-color: #171717;")

        self.main_layout = QHBoxLayout(self.window)

        # Left side layout for bookmarks
        self.bookmarks_layout = QVBoxLayout()
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.setMinimumWidth(200)
        self.bookmarks_list.setMaximumWidth(200)
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
        self.bookmarks_layout.addWidget(self.bookmarks_list)

        # Right side layout for browser and controls
        self.browser_layout = QVBoxLayout()
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
        self.browser_layout.addWidget(self.url_bar)

        self.browser = QWebEngineView()
        self.browser_layout.addWidget(self.browser)

        # Horizontal layout for controls
        self.controls_layout = QHBoxLayout()
        self.back_btn = QPushButton("<")
        self.forward_btn = QPushButton(">")
        self.go_btn = QPushButton("Go")
        self.bookmark_btn = QPushButton("Bookmark")
        self.remove_bookmark_btn = QPushButton("Remove Bookmark")

        self.controls_layout.addWidget(self.back_btn)
        self.controls_layout.addWidget(self.forward_btn)
        self.controls_layout.addWidget(self.go_btn)
        self.controls_layout.addWidget(self.bookmark_btn)
        self.controls_layout.addWidget(self.remove_bookmark_btn)

        self.browser_layout.addLayout(self.controls_layout)

        self.main_layout.addLayout(self.bookmarks_layout)
        self.main_layout.addLayout(self.browser_layout)

        self.window.resize(800, 600)

        self.window.show()

        # Connect signals and slots
        self.go_btn.clicked.connect(self.navigate)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.remove_bookmark_btn.clicked.connect(self.remove_bookmark)
        self.bookmarks_list.itemClicked.connect(self.load_bookmark)
        self.url_bar.returnPressed.connect(self.navigate)

        self.load_bookmarks()

    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        item_widget = BookmarkItemWidget(current_url)
        list_item = QListWidgetItem(current_url, self.bookmarks_list)
        list_item.setSizeHint(item_widget.sizeHint())
        list_item.setData(Qt.UserRole, current_url)
        self.bookmarks_list.addItem(list_item)
        self.bookmarks_list.setItemWidget(list_item, item_widget)
        self.save_bookmarks()

    def load_bookmark(self, item):
        url = item.data(Qt.UserRole)
        self.browser.setUrl(QUrl(url))

    def remove_bookmark(self):
        for item in self.bookmarks_list.selectedItems():
            self.bookmarks_list.takeItem(self.bookmarks_list.row(item))
        self.save_bookmarks()

    def save_bookmarks(self):
        bookmarks = [self.bookmarks_list.item(index).data(Qt.UserRole) for index in range(self.bookmarks_list.count())]
        with open("bookmarks.json", "w") as file:
            json.dump(bookmarks, file)

    def load_bookmarks(self):
        if os.path.exists("bookmarks.json"):
            with open("bookmarks.json", "r") as file:
                bookmarks = json.load(file)
                for bookmark in bookmarks:
                    item_widget = BookmarkItemWidget(bookmark)
                    list_item = QListWidgetItem(bookmark, self.bookmarks_list)
                    list_item.setSizeHint(item_widget.sizeHint())
                    list_item.setData(Qt.UserRole, bookmark)
                    self.bookmarks_list.addItem(list_item)
                    self.bookmarks_list.setItemWidget(list_item, item_widget)

    def update_autocomplete(self, text):
        suggestions = ["linkedin.com", "gmail.com", "youtube.com"]
        completer = QCompleter(suggestions)
        self.url_bar.setCompleter(completer)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    browser = MyWebBrowser()
    sys.exit(app.exec_())
