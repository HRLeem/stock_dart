#
# def parse_it ():
#     answer = '%BB%EF%BC%BA'
#     raw = '현대'
#
#     euc_data = raw.encode('euc-kr')
#     result = str(euc_data).replace("\\x", "%")[2:-1]
#     print(result)
#     if answer.lower() == result.lower():
#         print('GOOD')
#     else :
#         print("no")
#         print(result)
#
# def split():
#     msg = '<td class="tit"><a href="/item/main.nhn?code=291230">삼성스팩2호</a>\n' \
#           '<img alt="코스닥" height="15" src="https://ssl.pstatic.net/static/nfinance/ico_kosdaq.gif" width="32"/>\n' \
#           '</td>'
#     split = msg.split('"')
#     code = split[3][-6:]
#     name = split[4]
#     len_name = len(name)
#     name = name[1:len_name].split('<')[0]
#     print(split)
#     print(name)
#     kospikosdaq = split[5]
#
# def split_name ():
#     raw = '코스피 | 삼성물산     - 028260'
#     msg = raw.split('|')[1].split('-')[0].strip()
#     print(msg)
#     code = raw[-6:]
#     print(code)
#
# split_name()

# from bs4 import BeautifulSoup
# import requests
#
# def c():
#     url = 'https://finance.naver.com/item/main.nhn?code=187870#'
#     resp = requests.get(url)
#     html = resp.text
#     if resp.status_code == 200:
#         soup = BeautifulSoup(html, 'html.parser')
#         url = 'div.cop_analysis thead tr:nth-child(2) th:nth-child(4)'
#         this_one = soup.select_one(url).text.strip()[:4]
#         print(this_one)
#
# c()

def insert_to_list():
    list = ['삼성전자', '80,900', '482조\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t9,554억', '2,437,714', '2,304,009', '2,368,070', '588,867', '277,685', '359,939', '24.16', '12.05', '15.20', '443,449', '217,389', '264,078', '18.19', '9.44', '11.15', '6,024', '3,166', '6.42', '17.63', '19.63', '8.69']
    x = rc(list[3])
    y = rc(list[6])
    result =round( y/x*100, 1 )
    dumi_list = []
    # dumi_list2 = []

    for i in range(2):
        # print( round( (rc(list[i+4]) - rc(list[i+3]))/rc(list[i+3])*100, 1 ) )
        this_one = round( (rc(list[i+4]) - rc(list[i+3]))/rc(list[i+3])*100, 1 )
        dumi_list.append(this_one)
    # for j in range(3):
    #     this_one = round( rc(list[j+6]) / rc(list[j+3]) *100, 1 )
    #     dumi_list2.append(this_one)
    dumi_list.reverse()
    # dumi_list2.reverse()
    for item in dumi_list:
        list.insert(3, item)
    # for dumi in dumi_list2:
    #     list.insert(7, dumi)
    print(list)


def rc(x):
    return int(x.replace(',', ''))
insert_to_list()