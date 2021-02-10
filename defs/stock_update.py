# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import defs.stock_defs as defs

class Update:
    def __init__(self):
        self.numc = ['6', '10', '11']
        self.numi = ['4', '5']
        self.list_indicator = []

    def get_html(self, code):
        url = 'https://finance.naver.com/item/main.nhn?code='+code
        self.resp = requests.get(url)
        self.html = self.resp.text

    def make_soup(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def make_url(self, first, second, p):
        if p == 'p':
            url = 'p.no_today'
        else:
            url = 'div.cop_analysis table tbody tr:nth-child('+first+') td:nth-child('+second+')'
        self.make_this_one(url, p)

    def make_this_one(self, url, p):
        this_one = self.soup.select_one(url).text.strip()
        if p == 'p':
            this_one = this_one.split('\n')
            self.list_indicator.append(this_one[0])
        else:
            self.list_indicator.append(this_one)

    # total work
    def update_single(self, name, code):
        self.get_html(code)
        if self.resp.status_code == 200:
            self.list_indicator.append(name)
            self.make_soup()
            self.make_url('', '', 'p')
            for i in range(len(self.numc)):
                for j in range(len(self.numi)):
                    self.make_url(self.numc[i], self.numi[j], ' ')
            excel = defs.Excel()
            excel.switch('indicator', self.list_indicator)
            excel.save_excel()