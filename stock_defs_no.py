# -*- coding: utf-8 -*-
from urllib.request import urlopen # HTTP 요청처리
from zipfile import ZipFile        # 공시회사정보 zipfile 처리
from io import BytesIO             # stream 데이터를 메모리에 적재
import os                          # 현재 디렉토리 정보를 얻기 위해
import xmltodict                   # xml을 dict로 파싱
from pathlib import Path           # file 존재유무 체크 유틸
import re
import stock_report as report


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


def check_correct(corp_list_has_stockcode):
    while (True):
        count = 0
        mcount = 0
        mname = ''

        mname_list = []

        code = ''
        data_keyin = input('회사명을 입력하세요(종료하려면 x를 입력하고 엔터를 눌러주세요!):')


        if data_keyin.find('!') == 2:
            mcount = 1
            data_keyin = data_keyin[:-1]
        # 'exit'가 입력되면 대화형 콘솔을 종료한다.
        if data_keyin == 'x':
            break

        # 대소문자 구분 없이 조회한다. re.IGNORECASE 는 re.I와 동일한 표현이다.
        p = re.compile(r'.*({}).*'.format(data_keyin), re.IGNORECASE)

        print('{}을 검색한 결과는 아래와 같습니다.'.format(data_keyin))
        print('=' * 100)

        for x in corp_list_has_stockcode:
            # 정규식 매칭
            data = re.search(p, x['corp_name'])

            if data:
                result = data.group()
                count += 1

                if mcount == 1:
                    print('data_keyin = ', data_keyin)
                    print('format(result)', format(result))
                    if data_keyin.lower() == format(result).lower():
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print('data_keyin = ', data_keyin)
                        print('format(result)', format(result))
                        # mname = format(result)
                        mname_list.append( format(result) )
                code = x['corp_code']
                print('회사명:{}, 고유코드:{}, 종목코드:{}'.format(result, x['corp_code'], x['stock_code']))

        print('mcount = ', mcount)

        if count == 0:
            print('검색결과가 없습니다.')

        if count == 1 or mcount == 1:
            if mcount == 1:
                name = mname
                # 1. 정확한 이름을 가진 그 기업의 리스트가 하나이냐.
            else:
                name = format(result)

            print(name, code)
            report.stock_report(name, code)
            print('* Excel에 작성 완료되었습니다 !')

        if count > 1 and mcount != 1:
            print('>> Excel에 작성하기 위해서는 \"정확한 회사명\"을 입력하셔야 합니다.')
            print('>> sk를 검색하고 싶은데 결과가 많아서 입력이 안된다면, !를 붙여주세요 < ex) sk! >')

        print('=' * 100)







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
