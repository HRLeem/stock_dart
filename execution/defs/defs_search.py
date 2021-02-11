# -*- coding: utf-8 -*-
from urllib.request import urlopen # HTTP 요청처리
from zipfile import ZipFile        # 공시회사정보 zipfile 처리
from io import BytesIO             # stream 데이터를 메모리에 적재
import os                          # 현재 디렉토리 정보를 얻기 위해
from pathlib import Path           # file 존재유무 체크 유틸
import re
import xmltodict

import execution.defs.defs_crawl as crawl
import execution.sosok as sosok

class Request_list:
    def __init__(self):
        self.API_KEY = "9603774f25edc5686b1d7df2e3d1f8788a864fe3"
        self.url = "https://opendart.fss.or.kr/api/corpCode.xml?"
        self.params = {'crtfc_key':self.API_KEY}

    def get_corp_xml(self):
        if self.has_corpfile():
            self.corp_xml =  open(self.dirpath + '\CORPCODE.xml', 'r').read()
        else:
            url = self.url + '&'.join(self.bind_params(self.params))
            resp = urlopen(url)
            zipfile = ZipFile(BytesIO(resp.read()))
            print('defs_search - 25line')
            print(zipfile.namelist())
            for name in zipfile.namelist():
                z = zipfile.open(name)
                with open(name, 'w') as codefile:
                    for l in z.readlines():
                        codefile.wrote(l.decode())
            self.corp_xml = open(self.dirpath + '\CORPCODE.xml' , 'r').read()



    def has_corpfile(self):
        self.dirpath = os.getcwd()
        if Path(self.dirpath + '\CORPCODE.xml').is_file():
            return True
        else:
            return False

    def bind_params(self, params: dict):
        url_params = []
        for key in params:
            url_params.append(key + '=' + params[key])
        return url_params


    def xml_to_list(self):
        corp_dict = xmltodict.parse(self.corp_xml)
        corp_list = corp_dict['result']['list']
        self.corp_list_has_stockcode = [x for x in corp_list if x['stock_code'] is not None]


class Search:
    def __init__(self):
        self.count = 0
        self.mcount = 0
        self.mclist = []
        self.isq = 0
        self.code = ''

    def pick_corp(self):
        while (True):
            self.count = 0
            self.mcount = 0
            self.mclist = []
            self.isq = 0
            data_keyin = input('회사명을 입력해주세요. (종료하시려면 x를 입력하고 엔터를 눌러주세요!) : ')

            if data_keyin.find('!') > 0:
                self.isq = 1
                data_keyin = data_keyin[:-1]
            if data_keyin == 'x':
                break
            if data_keyin == '시가총액':
                self.sosoks()
            else:
                p = re.compile(r'.*({}).*'.format(data_keyin), re.IGNORECASE)

                print('{}을 검색한 결과는 아래와 같습니다.'.format(data_keyin))
                print('=' * 100)
                result = ''
                for x in self.corp_list:
                    data = re.search(p, x['corp_name'])

                    if data:
                        result = data.group()
                        self.count +=1
                        print(self.count)
                        if self.isq == 1:
                            if data_keyin.lower() == format(result).lower():
                                self.mcount += 1
                                self.mname = format(result)
                                self.mclist.append(x['stock_code'])
                        self.code = x['stock_code']
                        print('회사명:{}, 종목코드:{}'.format(result, x['stock_code']))
                j = self.count_case(format(result))
                if j == 'refresh':
                    continue
                elif j == 'done':
                    print('* Excel에 작성이 완료되었습니다 ! ')
                elif j == 'exactly' and data_keyin !='시가총액':
                    print('>> Excel에 작성하기 위해서는 \"정확한 회사명\"을 입력하셔야 합니다.')
                    print('>> sk를 검색하고 싶은데 결과가 많아서 입력이 안된다면, !를 붙여주세요 < ex) sk! >')
        print('='*100)


    def count_case(self, result):
        if self.count == 0:
            print('검색결과가 없습니다.')
            return 'refresh'
        elif self.count == 1:
            print('찾으시는 회사가 맞나요? << {} >>'.format(result))
            final_ask = input('(o/x) 입력 후 엔터를 눌러주세요 : ')
            if final_ask == 'o':
                write = crawl.Crawl()
                write.update_single(result, self.code)
                return 'done'
            elif final_ask == 'x':
                return 'refresh'
        elif self.count > 1:
            if self.isq:
                for c in range(len(self.mclist)):
                    check = crawl.Crawl()
                    j = check.simple_check(self.mclist[c])
                    if j is not False:
                        write = crawl.Crawl()
                        write.update_single(self.mname, self.mclist[c])
                        return 'done'
            else:
                return 'exactly'
    def sosoks(self):
        while(True):
            inputed = input('입력창에 KOSPI (kospi) 혹은 KOSDAQ (kosdaq) 을 입력해주세요 : ')
            if inputed == 'kospi' or inputed == 'kosdaq' or inputed == 'KOSPI' or inputed == 'KOSDAQ':
                sosok50 = sosok.crawl_sosok()
                if inputed == 'kospi' or inputed == 'KOSPI':
                    sosok50.crawl(0)
                    return
                elif inputed == 'kosdaq' or inputed == 'KOSDAQ':
                    sosok50.crawl(1)
                    return
                else:
                    print('ERROR!!! 에러발생 in self.sosoks(self): || defs_search.py')
            else:
                print('-'*50)
                print('> 입력하신 내용 << {} >>'.format(inputed))
                print('> 입력한 내용을 확인하시고 다시 입력해주세요')