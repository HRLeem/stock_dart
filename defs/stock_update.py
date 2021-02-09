from bs4 import BeautifulSoup
import requests
class Update:
    def __init__(self):
        print('업데이트!')
        self.numc = ['6', '10', '11']
        self.numi = ['4', '5']
        self.eng = ['ROE', 'EPS', 'PER']

    def get_html(self, code):
        url = 'https://finance.naver.com/item/main.nhn?code='+code
        response = requests.get(url)
        return response

    def make_soup(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def filter_indicator(self, first, second ):
        url = 'div.cop_analysis table tbody tr:nth-child('+first+') td:nth-child('+second+')'
        this_one = self.make_this_one(url, ' ')
        return this_one

    def make_this_one(self, url, p):
        this_one = self.soup.select_one(url).text.strip()
        if p == 'p':
            this_one = this_one.split('\n')
        return this_one

def update_single( name, code ):
    # =============================================
    update = Update()
    response = update.get_html(code)
    full_list = []
    if response.status_code == 200:
        html = response.text
        update.make_soup(html)
        for i in range(len(update.numc)):
            print(update.eng[i])
            for j in range(len(update.numi)):
                this_one = update.filter_indicator(update.numc[i], update.numi[j])
                full_list.append(this_one)
    print(full_list)
    # =============================================
    # url = 'https://finance.naver.com/item/main.nhn?code='+code
    # response = requests.get(url)
    #
    # print(name, ' 크롤링')
    # if response.status_code == 200:
    #     html = response.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     nums = [' ', '6', '10', '11']
    #     nums_s = ['4', '5']
    #     # urls = 'div.cop_analysis table tbody tr:nth-child('+nums[0]+') td:nth-child('+nums_s[0]+')'
    #     # title = soup.select_one( urls ).text
    #     for i in range( len(nums) ):
    #         if i==0:
    #             urls = 'p.no_today'
    #             this_one = soup.select_one( urls ).text.strip()
    #             this_one = this_one.split('\n')
    #             print('>>주가')
    #             print(this_one[0])
    #             pass
    #         elif i==1:
    #             print('>>ROE')
    #         elif i==2:
    #             print('>>EPS')
    #         elif i==3:
    #             print('>>PER')
    #         if i!=0:
    #             for j in range( len(nums_s) ):
    #                 urls = 'div.cop_analysis table tbody tr:nth-child('+nums[i]+') td:nth-child('+nums_s[j]+')'
    #                 this_one = soup.select_one( urls ).text.strip()
    #                 print(this_one)
    #     # print(title.strip())
    #         print('\n')
    #
    # else:
    #     print('>>  !!! 인터넷 연결을 확인해주세요! 그래도 에러가 나올시에는 개발자에게 문의해주세요')

#
# def price(name, code):
#     url = 'p.no_today'
#     this_one = soup.select_one( url ).text.strip().split('\n')
