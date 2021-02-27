# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import execution.defs.defs_crawl as crawl
import execution.sosok as sosok

class Search:
    def __init__(self):
        self.count = 0
        self.mcount = 0
        self.mclist = []
        self.isq = 0
        self.code = ''

    def make_list(self, raw):
        result_list = []
        encoded = raw.encode('euc-kr')
        encoded = str(encoded).replace("\\x", "%")[2:-1]
        # page = 1
        url = f'https://finance.naver.com/search/searchList.nhn?query={encoded}'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        # self.page = len(soup.select('div.paging>a'))
        # print(self.page)
        # for i in range(1, self.page+1):
        results = soup.select('td.tit')
        for j in range(0, len(results)):
            one_line = str(results[j])
            split = one_line.split('"')
            code = split[3][-6:]
            name = split[4]
            name = name[1:].split('<')[0]
            kospikosdaq = split[5]
            if self.isq == 1:
                if raw.lower() == name.lower():
                    result_list.append(f"{kospikosdaq} | {name}     - {code}")
            else:
                result_list.append(f"{kospikosdaq} | {name}     - {code}")
        if result_list:
            return result_list
        else:
            return False

    def pick_corp(self):
        while (True):
            self.count = 0
            self.mcount = 0
            self.mclist = []
            self.isq = 0
            data_keyin = input('\n> 회사명을 입력해주세요. \033[38;5;216m[ 종료 = \'x\' | 사용방법 = \'?\' ]\033[0m : ')

            if data_keyin.find('-') > 0:
                self.isq = 1
                data_keyin = data_keyin[:-1]
            if data_keyin == 'x':
                break
            elif data_keyin == '시가총액':
                self.sosoks()
            elif data_keyin == '업데이트':
                a = crawl.Crawl()
                a.update_price()
                print('주가 업데이트가 완료되었습니다 !\n')
            elif data_keyin == '?':
                self.guide()
            else:
                # p = re.compile(r'.*({}).*'.format(data_keyin), re.IGNORECASE)

                # print('{}을 검색한 결과는 아래와 같습니다.'.format(data_keyin))
                # print('=' * 100)
                name = ''
                code = ''
                self.count = 0
                print('='*45+' 검색결과 '+'='*45)
                result = self.make_list(data_keyin)
                if result:
                    if self.isq:
                        self.count = 1
                    else:
                        for i in range(0, len(result)):
                            self.count+=1
                            print(result[i])
                    if self.count == 1:
                        name = result[0].split('|')[1].split('-')[0].strip()
                        code = result[0][-6:]
                print('=' * 100)
                j = self.count_case(name, code)
                if j == 'refresh':
                    continue
                elif j == 'done':
                    print('\033[33m*\033[0m \033[38;5;2mExcel\033[0m에 작성이 완료되었습니다 ! ')
                elif j == 'exactly' and data_keyin !='시가총액':
                    print('>> Excel에 작성하기 위해서는 \033[91m\"정확한 회사명\"\033[0m을 입력하셔야 합니다.')
                    print('>> 검색하고자 하는 기업이름 마지막에 \033[91m\"-\"\033[0m를 붙여보면 어떨까요? < ex) sk => sk- >')
        print('='*100)


    def count_case(self, result, code):
        if self.count == 0:
            print('검색결과가 없습니다.')
            return 'refresh'
        elif self.count == 1:
            print('\033[48;5;146m   \033[0m 찾으시는 회사가 맞나요? << {} >> \033[48;5;146m   \033[0m'.format(result))
            final_ask = input('> \033[91m맞다면 "엔터"\033[0m, 아니면 "x"를 눌러주세요 : ')
            if final_ask == 'x':
                return 'refresh'
            else:
                write = crawl.Crawl()
                write.update_single(result, code)
                return 'done'
        elif self.count > 1:
            if self.isq:
                for c in range(len(self.mclist)):
                    check = crawl.Crawl()
                    print('\033[48;5;146m   \033[0m 찾으시는 회사가 맞나요? << {} >> \033[48;5;146m   \033[0m'.format(result))
                    final_ask = input('> \033[91m맞다면 "엔터"\033[0m, 아니면 "x"를 눌러주세요 : ')
                    if final_ask == 'x':
                        continue
                    else:
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

    def guide(self):
        print('-'*40+'사용 가이드'+'-'*40+'\n'
              '-----| 검색이 잘 안될때 |\n'
              '- 검색결과가 많아서 원하는 회사가 검색이 안될때는 "회사이름-"과 같이 끝에 느낌표를 붙여주세요.\n'
              '- "현대차" 등은 "현대자동차"로 등록되어 있어서 검색결과가 안나올 수도 있습니다.\n'
              '   > 이때는 "현대"를 먼저 검색 한 후 어떻게 등록되어있는지 확인 후 재검색을 시도해주세요.\n'
              '   !! 검색결과가 너무 많아서 "찾기 힘들때"는, Ctrl+F 를 눌러서 확인해보세요!\n'
              '   > Ctrl+F 입력 후 "차"입력 후 엔터\n'
              '-----| 시가총액 |\n'
              '- 시가총액 순위를 파일로 저장할때는 입력창에 "시가총액" 을 입력 후 엔터를 눌러주세요.\n'
              '-----| 주가 업데이트 |\n'
              '- 엑셀파일의 주가를 "업데이트"하고 싶으실때는 입력창에 "업데이트" 를 입력 후 엔터를 눌러주세요.\n'
              '-----| 에러 처리 |\n'
              '- 만약 성공 메세지가 안나오고\n'
              +'>>>  \033[31m'+'PermissionError: [Errno 13] Permission denied: \'stock.xlsx\''
              +'\033[0m  <<<\n'+'     이런 에러 메세지가 나온다면, \n'
              '     이는 엑셀파일을 닫지 않고 프로그램을 실행할 때 나오는 에러입니다.\n'
              '     켜져있는 엑셀을 닫고 다시 진행해주세요.\n\n'
              +'*'*17+' 이 외의 에러 및 개선 요구사항 등은 관리자에게 문의해주세요 '+'*'*17+'\n'
              +'-'*90)