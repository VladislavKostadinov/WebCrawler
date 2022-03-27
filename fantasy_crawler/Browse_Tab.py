import re
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QTabWidget, QLabel, QHBoxLayout, QButtonGroup, QVBoxLayout, \
    QRadioButton, QGroupBox, QPushButton, QGridLayout, QMessageBox, QCheckBox, QMainWindow, QFrame, QLineEdit
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from final import FantasyCrawler
from final.fantasy_crawler import Main_Tab
from final.fantasy_crawler import Browse_Tab

# Browse the data, collected by the Scraper, using pandas.loc[] to find the correct row by title, containing the
# book info and extract the chosen item() from the located row.


def searching(self):
    if self.book_name.text() == '':
        QMessageBox.information(self, 'Search Box', 'Please enter a value first.', QMessageBox.Ok,
                                QMessageBox.Ok)
    else:
        try:
            self.book_info_df = self.book_info_df.drop_duplicates(subset='book_title', keep='last')
            auth = self.book_info_df.loc[self.book_info_df['book_title'].str.lower() ==
                                         self.book_name.text().lower(), 'book_author'].item()
            self.book_auth_e.setText(str(auth))
            ttl = self.book_info_df.loc[self.book_info_df['book_title'].str.lower() ==
                                        self.book_name.text().lower(), 'book_title'].item()
            self.book_ttl_e.setText(str(ttl))
            pages = self.book_info_df.loc[self.book_info_df['book_title'].str.lower() ==
                                          self.book_name.text().lower(),
                                          'book_pages'].item()
            self.book_pages_e.setText(str(pages))
            price = self.book_info_df.loc[self.book_info_df['book_title'].str.lower() ==
                                          self.book_name.text().lower(),
                                          'book_price'].item()
            self.book_price_e.setText(str(price))
        except:
            QMessageBox.information(self, 'Search Box', 'Invalid title. Try again', QMessageBox.Ok,
                                    QMessageBox.Ok)
            return
