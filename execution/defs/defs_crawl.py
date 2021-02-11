# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import openpyxl


class Crawl:
    def __init__(self):
        self.lists_sheet =[[1, 2, 3], [4, 5, 7], [14, 15, 16], ['p', 10, 11, 6]]
        self.lists_sheet_num = [[3, 3], [3, 3], [2, 3], [3, 2]]
        self.issimple = 0
        self.line_list = []
    #     3 4 5 (2020) 2 3 4 (2019


    def update_single(self, name, code):
        self.get_html(code)
        self.name = name
        if self.resp.status_code == 200:
            self.soup = BeautifulSoup(self.html, 'html.parser')
            if self.issimple == 1:
                return self.price_check()
            else:
                self.crawl_it()

    def crawl_it(self):
        for x in range(0, 4):
            self.count = 0
            for y in range(len(self.lists_sheet[x])):
                for z in range(0, self.lists_sheet_num[x][1]):
                    if self.lists_sheet[x][y] == 'p':
                        url = 'p.no_today'
                        if z ==0:
                            self.make_element(url, z, self.lists_sheet_num[x][1], x, 'p')
                    else:
                        first = str(self.lists_sheet[x][y])
                        second = str(self.lists_sheet_num[x][0]+z)
                        url = 'div.cop_analysis table tbody tr:nth-child('+ first +') td:nth-child('+ second +')'
                        self.make_element(url, z, self.lists_sheet_num[x][1], x, ' ')

    def make_element(self, url, east, west, x, p):
        print('***********************************')
        print('east = ', east)
        print('west = ', west)
        print('x = ', x)
        print('p = ', p)
        print('***********************************')
        if self.count == 0:
            self.line_list.append(self.name)
            self.count = 1
        else:
            element = self.soup.select_one(url).text.strip()
            if p == 'p':
                element = element.split('\n')
                self.line_list.append(element[0])
            else:
                self.line_list.append(element)
        if west - east == 1:
            excel = Excel()
            excel.save_excel(x, self.line_list)

    def get_html(self, code):
        url = 'https://finance.naver.com/item/main.nhn?code='+code
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
        self.list_sheet = ['손익계산서', '비율지표', '배당지표', '투자지표']
        self.name = 'stock.xlsx'

    def save_excel(self, where, list):
        print('EXCEL!!!!!!!!!')
        wb = openpyxl.load_workbook(self.name)

        sheet = wb.get_sheet_by_name(self.list_sheet[where])
        sheet.append(list)
        wb.save(self.name)
