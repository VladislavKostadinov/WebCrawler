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
import WebCrawler
import Main_Tab
import Browse_Tab

actions_f = []
beginning = []
forward_btn = []
actions_s = []
scrape_btn = []
counter = []
collectibles = []
book_info = ['book_title', 'book_author', 'book_pages', 'book_price']
book_info_df_main = pd.DataFrame(None, columns=book_info)


def start_process(self):
    actions_f.append('Action')
    beginning.append('Start')
    if self.display_state.text() == '7/7':
        QMessageBox.information(self, 'Scrape Box', 'Search finished, please carry on', QMessageBox.Ok,
                                QMessageBox.Ok)
        return
    if len(forward_btn) > 0:
        QMessageBox.information(self, 'Scrape Box', 'Process already started.', QMessageBox.Ok,
                                QMessageBox.Ok)
        return Main_Tab.books_sample[0][0]
    else:
        forward_btn.append(Main_Tab.books_sample)
        # print(len(Main_Tab.books_sample))
        # print(actions_s)
        # print(actions_f)
        # print(actions_s)
        return Main_Tab.books_sample[0][0]


def forward_click(self):

    if self.display_state.text() == '7/7':
        QMessageBox.information(self, 'Scrape Box', 'Search finished, please carry on', QMessageBox.Ok,
                                QMessageBox.Ok)

        return

    if len(beginning) == 0:

        QMessageBox.information(self, 'Scrape Box', 'Please start the process first', QMessageBox.Ok,
                                QMessageBox.Ok)
        return
        # actions_f.pop(0)
    else:
        if len(actions_f) <= len(actions_s):
            actions_f.append('Action')
            try:
                forward_btn[0][0].pop(0)
            except IndexError:
                QMessageBox.information(self, 'Scrape Box', 'An error occured!', QMessageBox.Ok,
                                        QMessageBox.Ok)
                return
            if len(forward_btn[0]) == 0:
                print("End")
                QMessageBox.information(self, 'Scrape Box', 'No more pages to load', QMessageBox.Ok,
                                        QMessageBox.Ok)
                return
            print(actions_f)
            return forward_btn[0][0][0]
        else:
            QMessageBox.information(self, 'Scraper window', "Scrape page first!", QMessageBox.Ok,
                                    QMessageBox.Ok)
            print(forward_btn[0][0][0])
            return forward_btn[0][0][0]


def scrape_segments(self):
    mismatch = 0

    if len(beginning) == 0:
        QMessageBox.information(self, 'Scrape Box', 'Start process first', QMessageBox.Ok,
                                QMessageBox.Ok)
        # actions_s.pop(0)
        return
    else:
        if self.display_state.text() == '7/7':
            QMessageBox.information(self, 'Scrape Box', 'Search finished, please carry on', QMessageBox.Ok,
                                    QMessageBox.Ok)
            return
        else:
            if len(actions_f) > len(actions_s):
                actions_s.append('Scrape')

                title, author, pages, price = [], [], [], []
                scrape_btn.append(Main_Tab.books_sample[0])
                browser = webdriver.Chrome(WebCrawler.web_driver)
                browser.maximize_window()
                browser.implicitly_wait(10)
                browser.get(scrape_btn[0][0])
                time.sleep(3)
                scrape_btn[0].pop(0)
                page_body = browser.find_element(By.TAG_NAME, 'body')
                scroll_downs = 2
                while scroll_downs:
                    page_body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                    scroll_downs -= 1

                find_tag = browser.find_element(By.CLASS_NAME, 'item-info h1')
                title.append(find_tag.text)

                find_tag = browser.find_element(By.CLASS_NAME, 'author-info span a span')
                author.append(find_tag.text)

                find_tag = browser.find_element(By.CLASS_NAME, 'biblio-info li span span')
                pages.append(find_tag.text)

                find_tag = browser.find_element(By.CLASS_NAME, 'sale-price')
                priced = find_tag.text[3:]
                price.append(priced)

                book_profile = {
                    'book_title': title,
                    'book_author': author,
                    'book_pages': pages,
                    'book_price': price
                }

                try:
                    add_new_sample = pd.DataFrame(book_profile, columns=book_info)
                    self.book_info_df = self.book_info_df.append(add_new_sample, ignore_index=True)
                    time.sleep(1)
                except:
                    mismatch += 1
                    print(mismatch)
                    pass
                browser.quit()
                counter.append('Object')
                collectibles.append('Item')
                collectibles.append('Item')
                collectibles.append('Item')
                collectibles.append('Item')
                self.display_state.setText(str(len(counter)) + '/7')
                self.coll_.setText(str(len(collectibles)))
                self.totl_.setText(str(len(collectibles)))
                if self.display_state.text() == '7/7':
                    self.display_state.setObjectName('complete')
                    self.craw_mess.setObjectName('tez')
                    self.display_state.style().unpolish(self.display_state)
                    self.craw_mess.style().unpolish(self.craw_mess)
                    self.craw_mess.setText('Finished')
                    QMessageBox.information(self, 'Scrape Box', 'Search finished, please carry on.', QMessageBox.Ok,
                                            QMessageBox.Ok)
                    return
                print(actions_s)
                return self.book_info_df, mismatch
            else:
                QMessageBox.information(self, 'Scrape Box', 'Please load next page first!', QMessageBox.Ok,
                                        QMessageBox.Ok)
                return self.book_info_df, mismatch


def save_file(self):
    try:
        if not self.display_state.text() == '0/7':
            self.book_info_df.to_csv(r'files/books.csv')
            QMessageBox.information(self, 'Depository Window', 'Your data has been saved.', QMessageBox.Ok,
                                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'Depository Window', 'No collected data yet.', QMessageBox.Ok,
                                    QMessageBox.Ok)
    except:
        QMessageBox.information(self, 'Depository Window', 'An error occurred!', QMessageBox.Ok,
                                QMessageBox.Ok)