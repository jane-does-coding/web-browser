from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import json
import os

class MyWebBrowser():

    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Woah My Web Browser")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        # Create and style the URL bar with autocomplete
        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0; /* Light grey background */
                color: #333333; /* Dark text color */
                font-size: 16px; /* Text size */
                border: 1px solid #CCCCCC; /* Border color */
                border-radius: 5px; /* Rounded corners */
                padding: 5px; /* Padding inside the text box */
            }
        """)

        # Create a completer for autocomplete suggestions
        self.completer = QCompleter()
        self.completion_model = QStringListModel()
        self.completer.setModel(self.completion_model)
        self.url_bar.setCompleter(self.completer)

        # Create and style the "Go" button
        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)
        self.go_btn.setStyleSheet("""
            QPushButton {
                background-color: #6172f2; /* Green background */
                color: white; /* White text */
                font-size: 16px; /* Text size */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                padding: 5px; /* Padding */
            }
            QPushButton:hover {
                background-color: #45A049; /* Darker green on hover */
            }
        """)

        # Create and style the "Back" button
        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6172f2; /* Blue background */
                color: white; /* White text */
                font-size: 16px; /* Text size */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                padding: 5px 10px; /* Padding */
            }
            QPushButton:hover {
                background-color: #1976D2; /* Darker blue on hover */
            }
        """)

        # Create and style the "Forward" button
        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setStyleSheet("""
            QPushButton {
                background-color: #6172f2; /* Orange background */
                color: white; /* White text */
                font-size: 16px; /* Text size */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                padding: 5px 10px; /* Padding */
            }
            QPushButton:hover {
                background-color: #FB8C00; /* Darker orange on hover */
            }
        """)

        # Create and style the "Bookmark" button
        self.bookmark_btn = QPushButton("Bookmark")
        self.bookmark_btn.setMinimumHeight(30)
        self.bookmark_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFB74D; /* Orange background */
                color: white; /* White text */
                font-size: 16px; /* Text size */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                padding: 5px 10px; /* Padding */
            }
            QPushButton:hover {
                background-color: #FF9800; /* Darker orange on hover */
            }
        """)

        # Create and style the "Remove Bookmark" button
        self.remove_bookmark_btn = QPushButton("Remove Bookmark")
        self.remove_bookmark_btn.setMinimumHeight(30)
        self.remove_bookmark_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF5350; /* Red background */
                color: white; /* White text */
                font-size: 16px; /* Text size */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                padding: 5px 10px; /* Padding */
            }
            QPushButton:hover {
                background-color: #E53935; /* Darker red on hover */
            }
        """)

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.bookmark_btn)
        self.horizontal.addWidget(self.remove_bookmark_btn)

        # Create and style the bookmarks list
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.setMaximumHeight(150)
        self.bookmarks_list.setStyleSheet("""
            QListWidget {
                background-color: #F0F0F0; /* Light grey background */
                color: #333333; /* Dark text color */
                font-size: 16px; /* Text size */
                border: 1px solid #CCCCCC; /* Border color */
                border-radius: 5px; /* Rounded corners */
                padding: 5px; /* Padding */
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
        self.window.show()

        self.load_bookmarks()

        # Connect textChanged signal of QLineEdit to update autocomplete suggestions
        self.url_bar.textChanged.connect(self.update_autocomplete)

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))
        self.url_bar.clearFocus()  # Clear focus after navigating

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        self.bookmarks_list.addItem(current_url)
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
            bookmarks.append(self.bookmarks_list.item(index).text())
        with open("bookmarks.json", "w") as file:
            json.dump(bookmarks, file)

    def load_bookmarks(self):
        if os.path.exists("bookmarks.json"):
            with open("bookmarks.json", "r") as file:
                bookmarks = json.load(file)
                for bookmark in bookmarks:
                    self.bookmarks_list.addItem(bookmark)

    def update_autocomplete(self, text):
        # Implement logic to update autocomplete suggestions based on 'text'
        # Here's a simple example where suggestions are hardcoded for demonstration
        suggestions = ["http://example.com", "http://example.org", "http://google.com"]
        self.completion_model.setStringList(suggestions)

app = QApplication([])
window = MyWebBrowser()
app.exec_()
