from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class MyWebBrowser():

    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Woah My Web Browser")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        # Create and style the URL bar
        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setStyleSheet("""
            QTextEdit {
                background-color: #F0F0F0; /* Light grey background */
                color: #333333; /* Dark text color */
                font-size: 16px; /* Text size */
                border: 1px solid #CCCCCC; /* Border color */
                border-radius: 5px; /* Rounded corners */
                padding: 5px; /* Padding inside the text box */
            }
        """)

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

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)

        self.browser = QWebEngineView()

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.toPlainText()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl("http://google.com"))

        self.window.setLayout(self.layout)
        self.window.show()

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

app = QApplication([])
window = MyWebBrowser()
app.exec_()
