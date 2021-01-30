# -*- coding: utf-8 -*-
from urllib.request import urlopen # HTTP 요청처리
from zipfile import ZipFile        # 공시회사정보 zipfile 처리
from io import BytesIO             # stream 데이터를 메모리에 적재
import os                          # 현재 디렉토리 정보를 얻기 위해
import xmltodict                   # xml을 dict로 파싱
from pathlib import Path           # file 존재유무 체크 유틸

API_KEY = "9603774f25edc5686b1d7df2e3d1f8788a864fe3"

url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key="+API_KEY


def bind_params(params: dict):
  url_params = []
  for key in params:
    url_params.append(key + '=' + params[key])
  return url_params


def has_corpfile():
  dirpath = os.getcwd()

  if Path(dirpath + '\CORPCODE.xml').is_file():
    return True
  else:
    return False

  # 파일존재 체크 다른 방법들..
  # if os.path.isfile(dirpath + '\CORPCODE.xml'):


#     return True
# else:
#     return False
# try:
#     open(dirpath + '\CORPCODE.xml', 'r')
#     return True
# except FileNotFoundError:
#     return False

def get_corp_xml(url, params):
  if has_corpfile():
    dirpath = os.getcwd()
    return open(dirpath + '\CORPCODE.xml', 'r').read()
  else:
    url = url + '&'.join(bind_params(params))
    resp = urlopen(url)

    # zip으로 저장할경우
    # f = open( 'corpCode.zip', 'wb' )
    # f.write(resp.read())
    # f.close()

    # zip파일내용을 풀어 저장한다.
    zipfile = ZipFile(BytesIO(resp.read()))
    print(zipfile.namelist())
    for name in zipfile.namelist():
      z = zipfile.open(name)
      with open(name, 'w') as codefile:
        for l in z.readlines():
          codefile.write(l.decode())
    dirpath = os.getcwd()
    return open(dirpath + '\CORPCODE.xml', 'r').read()


""" Biz Start """

url = 'https://opendart.fss.or.kr/api/corpCode.xml?'
params = {
  'crtfc_key': API_KEY,  # API 인증키
}

corp_xml = get_corp_xml(url, params)

corp_dict = xmltodict.parse(corp_xml)

# print(type(corp_dict))
#
# print(corp_dict)

# reulst > list 추출
corp_list = corp_dict['result']['list']

# stock_code가 None이 아닌 대상만 다시 추출한다.
corp_list_has_stockcode = [x for x in corp_list if x['stock_code'] is not None]

# print(len(corp_list_has_stockcode))



import re
import stock_report as sival

corp_list_has_stockcode = [x for x in corp_list if x['stock_code'] is not None]

while(True):
    data_keyin = input('회사명을 입력하세요(종료하려면 x를 입력하고 엔터를 눌러주세요!):')

	# 대소문자 구분 없이 조회한다. re.IGNORECASE 는 re.I와 동일한 표현이다.
    p = re.compile(r'.*({}).*'.format(data_keyin), re.IGNORECASE)

	# 'exit'가 입력되면 대화형 콘솔을 종료한다.
    if data_keyin == 'x':
        break

    print('{}을 검색한 결과는 아래와 같습니다.'.format(data_keyin))
    print('=' * 100)


    count = 0
    mcount = 0
    code = ''
    for x in corp_list_has_stockcode:
    	# 정규식 매칭
        data = re.search(p, x['corp_name'])

        if data:
            result = data.group()
            count+=1
            code = x['corp_code']
            if data_keyin == format(result):
                mcount +=1
            print('회사명:{}, 고유코드:{}, 종목코드:{}'.format(result, x['corp_code'], x['stock_code']))

    if count == 0:
        print('검색결과가 없습니다.')

    # if mcount == 1:
    #     print('finbdhfjbdshkjfbsjhfhbkgjvgvkjhbhkjvkjvkfgh')

    if count == 1 or mcount == 1:
        name = format(result)

        print(name, code)
        sival.stock_report( name, code)
        print('* Excel에 작성 완료되었습니다 !')

    if count > 1 and mcount != 1:
        print('>> Excel에 작성하기 위해서는 \"정확한 회사명\"을 입력하셔야 합니다.')

    print('=' * 100)