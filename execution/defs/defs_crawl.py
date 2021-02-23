# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import openpyxl
from tqdm import tqdm

class Crawl:
    def __init__(self):
        self.c_indicator = ['p', 1, 2, 4, 3, 5, 10, 11, 6]
        self.issimple = 0
        self.line_list = []

    def update_price(self):
        excel = Excel()
        code_list = excel.update_price_excel()
        count = 3
        for code in tqdm(code_list):
            self.code = code
            self.get_html()
            if self.resp.status_code == 200:
                element = BeautifulSoup(self.html, 'html.parser').select_one('p.no_today').text.strip().split('\n')
                excel.save_a_price(element[0], count)
                count += 1
            else:
                print('ERROR ! in update_price, class Crawl')

    def update_single(self, name, code):
        self.code = code
        self.get_html()
        self.name = name
        if self.resp.status_code == 200:
            self.soup = BeautifulSoup(self.html, 'html.parser')
            if self.issimple == 1:
                return self.price_check()
            else:
                self.crawl_it()

    def crawl_it(self):
        for x in self.c_indicator:
            if x == 'p':
                url = 'p.no_today'
                self.insert_list(url)
            else:
                if x == 10 or x == 11 or x == 6:
                    for i in range(3, 5):
                        url = 'div.cop_analysis table tbody tr:nth-child(' + str(x) + ') td:nth-child(' + str(i) + ')'
                        self.insert_list(url)
                else:
                    for i in range(3, 6):
                        url = 'div.cop_analysis table tbody tr:nth-child(' + str(x) + ') td:nth-child(' + str(i) + ')'
                        self.insert_list(url)
        code_list = self.make_code_list()
        excel = Excel()
        excel.save_excel(self.line_list, code_list)

    def insert_list(self, url):
        element = self.soup.select_one(url).text.strip()
        if url == 'p.no_today':
            self.line_list.append(self.name)
            element = element.split('\n')
            self.line_list.append(element[0])
        else:
            self.line_list.append(element)

    def make_code_list(self):
        result = ['', self.code]
        return result

    def get_html(self):
        url = 'https://finance.naver.com/item/main.nhn?code='+self.code
        self.resp = requests.get(url)
        self.html = self.resp.text

    def price_check(self):
        url = 'p.no_today'
        element = self.soup.select_one(url).text.strip()
        if element:
            return True
        else:
            return False

    def simple_check(self, code):
        self.issimple = 1
        result = self.update_single('', code)
        return result


class Excel:
    def __init__(self):
        self.name = 'stock.xlsx'
        self.code_list = []

    def save_excel(self, list, code):
        wb = openpyxl.load_workbook(self.name)

        sheet = wb.get_sheet_by_name('기업정보')
        sheet.append(list)
        wb.save(self.name)

        sheet = wb.get_sheet_by_name('for_code')
        sheet.append(code)
        wb.save(self.name)

    def update_price_excel(self):
        self.wb = openpyxl.load_workbook(self.name)
        self.ws = self.wb.get_sheet_by_name('기업정보')
        self.take_code_list()
        return self.code_list

    def take_code_list(self):
        ws = self.wb.get_sheet_by_name('for_code')
        for i in range(3, 999):
            element = ws['B'+str(i)].value
            if element is None:
                break
            else:
                self.code_list.append(element)

    def save_a_price(self, element, count):
        self.ws['B'+str(count)] = element
        self.wb.save(self.name)
        return