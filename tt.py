import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup


with open('files/books.csv', 'rb') as f:
    z = f.readlines()
    print(z)