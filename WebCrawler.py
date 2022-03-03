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
import Main_Tab
import Collect_Tab
import Browse_Tab
web_driver = r'../chromedriver/chromedriver.exe'

style_sheets = """ 
    QWidget#Status {
    border: 1px solid black; 
    }

    QWidget#Coll {
    border: 1px solid blue;
    background-color: beige; 
    }
    QFrame#Line {
    color: blue; }
    #weby {
  }
  QWidget#banner {
  border-bottom: 1px dotted black; 
  
  }
  QWidget#eti {
  border: 1px solid black; 
  }
  QWidget#cross{
  border-bottom: 1px solid burlywood; 
  }
  
  QLabel#Title {
  color: blue; }
  
  QLabel#green{
  color: green; 
  }
  QLabel#red {
  color: red; 
  }
  QLabel#tez {
  color: blue; }
  QLabel#complete {
  color: green; }

  QWidget#tab1 {
  background-color: lightgray; }
  
    QWidget#tab2 {
  background-color: lightblue; }
  
    QWidget#tab3 {
  background-color: burlywood; }
  
  QLabel#entry {
  color: blue; }
  
  QWidget#ind {
  background-color: beige;
   border: 1px solid blue; }
   
   QWidget#search_body {
   background-color: beige; }
"""
second_book_urls = []


book_info = ['book_title', 'book_author', 'book_pages', 'book_price']
book_info = ['book_title', 'book_author', 'book_pages', 'book_price']
book_info_df_main = pd.DataFrame(None, columns=book_info)


class MainScraper(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setGeometry(150, 150, 700, 800)
        self.setWindowTitle('Web Crawler')
        self.main_window()
        self.main_()
        self.collect()
        self.browse()
        self.show()

    def main_window(self):

        self.tab = QTabWidget()
        self.tab.setObjectName('Tab')

        self.main_scrape = QWidget()
        self.secondary_scrape = QWidget()
        self.catalogue = QWidget()
        self.main_scrape.setObjectName('tab1')
        self.secondary_scrape.setObjectName('tab2')
        self.catalogue.setObjectName('tab3')

        self.tab.addTab(self.main_scrape, 'Scrape')
        self.tab.addTab(self.secondary_scrape, 'Collect')
        self.tab.addTab(self.catalogue, 'Catalogue')
        main_winds = QHBoxLayout()
        main_winds.addWidget(self.tab)
        self.setLayout(main_winds)

    def main_(self):
        self.status = QWidget()
        crawler_active = QLabel("Current activity: ")
        self.craw_act = QLabel("Idle")
        self.craw_act.setObjectName('green')

        img_sec_path = 'images/web-crawlers.jpg'
        img_sec = self.load_img(img_sec_path)
        status_box = QWidget()

        scrape_status = QLabel("Status: ")
        self.display_status = QLabel("Incomplete")
        self.display_status.setObjectName('red')
        scraped_objects = QLabel("Collected items: ")
        self.collection = QLabel("0")
        line = QFrame()
        line.setFrameShape(QFrame.HLine)

        status_grid = QVBoxLayout()
        status_grid.addWidget(scrape_status)
        status_grid.addWidget(self.display_status)
        status_grid.addWidget(line)
        status_grid.addWidget(scraped_objects)
        status_grid.addWidget(self.collection)
        status_box.setLayout(status_grid)
        status_box.setObjectName('Coll')

        activity_box = QHBoxLayout()
        activity_box.addWidget(crawler_active)
        activity_box.addWidget(self.craw_act)
        activity_box.addStretch()
        activity_box.addWidget(img_sec)
        activity_box.addStretch()
        activity_box.addWidget(status_box)
        self.status.setLayout(activity_box)

        scrape_info = QLabel("Web Crawler Main Window")

        web_view = QWebEngineView()
        web_view.show()

        self.load = QPushButton("Load website")
        self.scrape = QPushButton("Scrape website")
        self.scrape.clicked.connect(lambda: Main_Tab.scrape_url(self))
        # self.llink = Main_Tab.load_main(self)
        self.load.clicked.connect(lambda: web_view.load(QUrl(Main_Tab.load_main(self))))
        main_wind = QVBoxLayout(self)
        main_wind.addWidget(self.status)
        main_wind.addWidget(self.load)
        main_wind.addWidget(web_view, Qt.AlignCenter)
        main_wind.addWidget(self.scrape)
        self.main_scrape.setLayout(main_wind)

    def load_img(self, path):
        try:
            with open(path):
                image = QLabel(self)
                image.setObjectName('image')
                pixmap = QPixmap(path)
                image.setPixmap(pixmap.scaled(152, 152, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

                return image
        except FileNotFoundError:
            print("File not found.")

    def collect(self):
        self.book_info_df = pd.DataFrame(None, columns=book_info)

        self.state = QWidget()
        crawler_a = QLabel("Current activity: ")
        self.craw_mess = QLabel("Idle")
        self.craw_mess.setObjectName('indigo')

        img_sec_p = 'images/sps.png'
        img_sec_ = self.load_img(img_sec_p)
        img_sec_.setObjectName('weby')
        state_box = QWidget()

        scrape_state = QLabel("Status: ")
        self.display_state = QLabel("0/7")

        scraped_obj = QLabel("Collected items: ")
        self.coll_ = QLabel("0")
        lines = QFrame()
        lines.setFrameShape(QFrame.HLine)
        lines.setObjectName('Line')

        state_grid = QVBoxLayout()
        state_grid.addWidget(scrape_state)
        state_grid.addWidget(self.display_state)
        state_grid.addWidget(lines)
        state_grid.addWidget(scraped_obj)
        state_grid.addWidget(self.coll_)
        state_box.setLayout(state_grid)
        state_box.setObjectName('Coll')

        active_box = QHBoxLayout()
        active_box.addWidget(crawler_a)
        active_box.addWidget(self.craw_mess)
        active_box.addStretch()
        active_box.addWidget(img_sec_)
        active_box.addStretch()
        active_box.addWidget(state_box)
        self.state.setLayout(active_box)

        web_v_ = QWebEngineView()
        web_v_.show()

        self.loader = QPushButton("Start process")
        self.next_page = QPushButton("Load next page")
        self.scraper = QPushButton("Scrape page")
        self.save_to = QPushButton("Save to file")
        self.scraper.clicked.connect(lambda: Collect_Tab.scrape_segments(self))
        self.loader.clicked.connect(lambda: web_v_.load(QUrl(Collect_Tab.start_process(self))))
        self.next_page.clicked.connect(lambda: web_v_.load(QUrl(Collect_Tab.forward_click(self))))
        self.save_to.clicked.connect(lambda: Collect_Tab.save_file(self))

        buttons = QWidget()
        processes = QHBoxLayout(self)
        processes.addWidget(self.loader)
        processes.addWidget(self.next_page)
        processes.addWidget(self.save_to)
        buttons.setLayout(processes)

        main_wind_ = QVBoxLayout(self)
        main_wind_.addWidget(self.state)
        main_wind_.addWidget(buttons)
        main_wind_.addWidget(web_v_, Qt.AlignCenter)
        main_wind_.addWidget(self.scraper)

        self.secondary_scrape.setLayout(main_wind_)

    def browse(self):
        status = QWidget()
        title = QLabel("Browse the collected data")
        title.setObjectName('Title')

        img_third_p = 'images/pypy.png'
        img_third_ = self.load_img(img_third_p)
        img_third_.setObjectName('trd')

        state_box = QWidget()
        author = QLabel("APP created by: ")
        self.credentials = QLabel("Vladislav Kostadinov")
        total = QLabel("Total collected items: ")
        self.totl_ = QLabel("0")
        lines = QFrame()
        lines.setFrameShape(QFrame.HLine)
        lines.setObjectName('Line')

        state_grid = QVBoxLayout()
        state_grid.addWidget(author)
        state_grid.addWidget(self.credentials)
        state_grid.addWidget(lines)
        state_grid.addWidget(total)
        state_grid.addWidget(self.totl_)
        state_box.setLayout(state_grid)
        state_box.setObjectName('Coll')

        banner_box = QHBoxLayout()
        banner_box.addWidget(title)
        banner_box.addStretch()
        banner_box.addWidget(img_third_)
        banner_box.addStretch()
        banner_box.addWidget(state_box)
        status.setLayout(banner_box)
        status.setObjectName('banner_box')

        self.book_title = QLabel("Search a book by title")
        self.book_title.setAlignment(Qt.AlignCenter)

        search_menu = QWidget()
        self.book_name = QLineEdit(self)
        self.book_title.setFont(QFont("Verdana", 15))
        self.search_eng = QPushButton("Search")
        self.search_eng.clicked.connect(lambda: Browse_Tab.searching(self))

        e_kets = QWidget()
        book_ttl = QLabel("Title: ")
        book_ttl.setFont(QFont("Verdana", 7))
        book_auth = QLabel("Author: ")
        book_auth.setFont(QFont("Verdana", 7))
        book_pages = QLabel("Pages: ")
        book_pages.setFont(QFont("Verdana", 7))
        book_price = QLabel("Price: ")
        book_price.setFont(QFont("Verdana", 7))

        self.book_price_e = QLabel("")
        self.book_price_e.setFont(QFont("Verdana", 7))
        self.book_price_e.setObjectName('entry')

        self.book_ttl_e = QLabel("")
        self.book_ttl_e.setFont(QFont("Verdana", 7))
        self.book_ttl_e.setObjectName('entry')

        self.book_auth_e = QLabel("")
        self.book_auth_e.setFont(QFont("Verdana", 7))
        self.book_auth_e.setObjectName('entry')

        self.book_pages_e = QLabel("")
        self.book_pages_e.setFont(QFont("Verdana", 7))
        self.book_pages_e.setObjectName('entry')

        greet = QWidget()
        grettings = QHBoxLayout()
        grettings.addWidget(self.book_title)
        greet.setLayout(grettings)
        greet.setObjectName('st')

        search_active = QHBoxLayout()
        search_active.addWidget(self.book_name)
        search_active.addWidget(self.search_eng)
        search_menu.setLayout(search_active)

        search_engine = QVBoxLayout()
        search_engine.addWidget(search_menu, Qt.AlignCenter)
        search_menu.setLayout(search_engine)

        b_title = QWidget()
        titles = QHBoxLayout()
        titles.addWidget(book_ttl)
        titles.addWidget(self.book_ttl_e)
        b_title.setLayout(titles)
        b_title.setObjectName('cross')

        b_author = QWidget()
        authors = QHBoxLayout()
        authors.addWidget(book_auth)
        authors.addWidget(self.book_auth_e)
        b_author.setLayout(authors)
        b_author.setObjectName('cross')

        b_pages = QWidget()
        pages = QHBoxLayout()
        pages.addWidget(book_pages)
        pages.addWidget(self.book_pages_e)
        b_pages.setLayout(pages)
        b_pages.setObjectName('cross')

        b_prices = QWidget()
        prices = QHBoxLayout()
        prices.addWidget(book_price)
        prices.addWidget(self.book_price_e)
        b_prices.setLayout(prices)
        # b_prices.setObjectName('cross')

        book_preview = QVBoxLayout()
        book_preview.addWidget(b_title)
        book_preview.addWidget(b_author)
        book_preview.addWidget(b_pages)
        book_preview.addWidget(b_prices)
        e_kets.setLayout(book_preview)
        e_kets.setObjectName('eti')

        main_title = QWidget()
        welcome = QVBoxLayout()
        welcome.addWidget(greet)
        welcome.addWidget(search_menu)
        main_title.setLayout(welcome)

        main_body = QWidget()
        page_body = QHBoxLayout()
        page_body.addWidget(e_kets, Qt.AlignCenter)
        main_body.setLayout(page_body)

        ind = QWidget()
        complete_banner = QHBoxLayout()
        complete_banner.addWidget(status)
        complete_banner.addWidget(state_box)
        ind.setLayout(complete_banner)
        ind.setObjectName('banner')

        body = QWidget()
        complete_body = QVBoxLayout()
        complete_body.addWidget(main_title)
        complete_body.addStretch()
        complete_body.addWidget(main_body, Qt.AlignCenter)
        body.setLayout(complete_body)
        body.setObjectName('search_body')

        complete_all = QVBoxLayout()
        complete_all.addWidget(ind)
        complete_all.addWidget(body)

        self.catalogue.setLayout(complete_all)

    def mandatory_s(self):
        self.craw_act.setText('Re   ady')
        self.display_status.setText('Data acquired')
        self.craw_act.setObjectName('tez')
        self.display_status.setObjectName('green')
        self.craw_act.style().unpolish(self.craw_act)
        self.display_status.style().unpolish(self.display_status)
        self.collection.setText(str(len(Main_Tab.books_sample[0])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheets)
    window = MainScraper()
    sys.exit(app.exec_())
