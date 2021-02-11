from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

class crawl_sosok:
    def __init__(self):
        pass

    def crawl(self, code):

        name = ' 시가총액 TOP50.xlsx'
        if code == 0:
            name = 'KOSPI'+name
        elif code == 1:
            name = 'KOSDAQ'+name
        else:
            print("ERROR!!! 어케들어왔냐... sosok.py || class crawl_sosok || def crawl(code)")
            return

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        url = 'https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D' + str(code)+ '&fieldIds=market_sum&fieldIds=property_total&fieldIds=debt_total&fieldIds=sales&fieldIds=sales_increasing_rate&fieldIds=operating_profit&fieldIds=operating_profit_increasing_rate&fieldIds=net_income&fieldIds=eps&fieldIds=dividend&fieldIds=per&fieldIds=roe'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        table_html = soup.select_one('div.box_type_l')

        # Column명
        header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]
        sival = table_html.find_all(lambda x: (x.name == 'a' and 'tltle' in x.get('class', [])) or ( x.name == 'td' and 'number' in x.get('class', [])))
        count = 1
        list = []
        # for item in sival:
        for i in range(0, len(sival)):
            num = 17
            if count % num == 3 or count % num == 4 or count % num == 5:
                pass
            else:
                list.append(sival[i].text)
            count+=1

        # 줄 리스트 잘라서 50-50줄, 14-14items 씩 줄줄이 붙임
        number_data = np.resize(list,(50, 14) )
        # 필요없는 등락 이딴거 다 잘라버리고, frame과 밑에 내용 연결시킴.
        del header_data[2:5]
        df = pd.DataFrame(data=number_data, columns=header_data)
        df.to_excel(name)
        print('>> {}이 성공적으로 저장되었습니다'.format(name[0:-5]))

    def change_num(self):
        # 엑셀에 있는 순번이 불편하다고 하시면 그때 바꿀 함수
        return

'''
kosdaq
https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D1
kospi
https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D0&fieldIds=market_sum&fieldIds=property_total&fieldIds=debt_total&fieldIds=sales&fieldIds=sales_increasing_rate&fieldIds=operating_profit&fieldIds=operating_profit_increasing_rate&fieldIds=net_income&fieldIds=eps&fieldIds=dividend&fieldIds=per&fieldIds=roe
https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D0
시가총액
&fieldIds=market_sum
%3Fsosok%3D0&fieldIds=market_sum
자산총계
&fieldIds=property_total
부채총계
&fieldIds=debt_total
매출액
&fieldIds=sales
매출액증가율
&fieldIds=sales_increasing_rate
영업이익
&fieldIds=operating_profit
영업이익증가율/
&fieldIds=operating_profit_increasing_rate
당기순이익
&fieldIds=net_income
주당순이익
&fieldIds=eps
?보통주 배당금
&fieldIds=dividend
PER
&fieldIds=per
ROE
&fieldIds=roe

'''