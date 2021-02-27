
def parse_it ():
    answer = '%BB%EF%BC%BA'
    raw = '현대'

    euc_data = raw.encode('euc-kr')
    result = str(euc_data).replace("\\x", "%")[2:-1]
    print(result)
    if answer.lower() == result.lower():
        print('GOOD')
    else :
        print("no")
        print(result)

def split():
    msg = '<td class="tit"><a href="/item/main.nhn?code=291230">삼성스팩2호</a>\n' \
          '<img alt="코스닥" height="15" src="https://ssl.pstatic.net/static/nfinance/ico_kosdaq.gif" width="32"/>\n' \
          '</td>'
    split = msg.split('"')
    code = split[3][-6:]
    name = split[4]
    len_name = len(name)
    name = name[1:len_name].split('<')[0]
    print(split)
    print(name)
    kospikosdaq = split[5]

def split_name ():
    raw = '코스피 | 삼성물산     - 028260'
    msg = raw.split('|')[1].split('-')[0].strip()
    print(msg)
    code = raw[-6:]
    print(code)

split_name()