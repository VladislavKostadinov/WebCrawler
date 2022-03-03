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
import Browse_Tab

main_page_c = []
book_urls = []
books_sample = []

def scrape_url(self):
    p = 1
    i = 14
    iz = 14
    if len(books_sample) > 0:
        QMessageBox.information(self, 'Main Window', 'Initial website already scraped! Please continue.',
                                QMessageBox.Ok, QMessageBox.Ok)
        return books_sample
    if len(main_page_c) == 1:

        browser = webdriver.Chrome(WebCrawler.web_driver)
        browser.maximize_window()
        browser.implicitly_wait(20)

        browser.get('https://www.bookdepository.com/category/355/Fantasy/browse/viewmode/all?=page=' + str(p))
        time.sleep(3)
        page_body = browser.find_element(By.TAG_NAME, "body")

        scroll_downs = 2

        while scroll_downs:
            page_body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            scroll_downs -= 1
        time.sleep(2)
        p += 1
        # b_tag = browser.find_elements(By.CLASS_NAME, "item-img a")
        book_inst = browser.find_elements(By.CLASS_NAME, 'book-item')
        # date = browser.find_elements(By.CLASS_NAME, 'published')
        # for a in b_tag:
        for book in book_inst:
            date = book.find_element(By.CLASS_NAME, 'published')
            b_tag = book.find_element(By.CLASS_NAME, 'item-img a')
            if int(date.text[-4:]) > 2015:
                book_urls.append(b_tag.get_attribute("href"))
        books_sample.append(book_urls[:i])
        WebCrawler.MainScraper.mandatory_s(self)
        btn = browser.find_element(By.XPATH, '//a[text()="' + str(p) + '"]')
        if not scroll_downs:
            btn.click()
            time.sleep(2)

        while p < 3:
            p += 1
            iz += 14
            scroll_downs = 2
            page_body = browser.find_element(By.TAG_NAME, "body")

            while scroll_downs:
                page_body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                scroll_downs -= 1
            books_ss = browser.find_elements(By.CLASS_NAME, 'book-item')
            for books in books_ss:
                dats = books.find_element(By.CLASS_NAME, 'published')
                bs_tag = books.find_element(By.CLASS_NAME, "item-img a")
                if int(dats.text[-4:]) > 2015:
                    book_urls.append(bs_tag.get_attribute("href"))
            for x in book_urls[i:iz]:
                books_sample[0].append(x)
            WebCrawler.MainScraper.mandatory_s(self)
            btn = browser.find_element(By.XPATH, '//a[text()="' + str(p) + '"]')

            if not scroll_downs and p < 4:
                i += 14
                iz += 14
                btn.click()
                time.sleep(2)

            browser.quit()

            QMessageBox.information(self, 'Main Window', 'Initial website scraped! Please continue.',
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            print(books_sample)
            print(len(main_page_c))
            return books_sample
    else:
        QMessageBox.information(self, 'Main Window', 'Please load the initial site!', QMessageBox.Ok,
                                QMessageBox.Ok)
        return


def load_main(self):
    if len(main_page_c) == 0:
        main_page_c.append('Main')
        return 'https://www.bookdepository.com/category/355/Fantasy/browse/viewmode/all'
    else:
        QMessageBox.information(self, 'Main Window', 'Initial site already loaded. Please scrape.',
                                QMessageBox.Ok, QMessageBox.Ok)
        return 'https://www.bookdepository.com/category/355/Fantasy/browse/viewmode/all'
