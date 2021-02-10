# -*- coding: utf-8 -*-
from urllib.request import urlopen # HTTP 요청처리
from zipfile import ZipFile        # 공시회사정보 zipfile 처리
from io import BytesIO             # stream 데이터를 메모리에 적재
import os                          # 현재 디렉토리 정보를 얻기 위해
from pathlib import Path           # file 존재유무 체크 유틸
import re
import defs.stock_report as report
import defs.stock_update as update_defs
import defs.stock_defs as defs


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
        isq = 0
        mcount = 0
        mclist = []
        msclist = []
        mname = ''

        code = ''
        data_keyin = input('회사명을 입력하세요(종료하려면 x를 입력하고 엔터를 눌러주세요!) : ')


        if data_keyin.find('!') > 0:
            isq = 1
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

                if isq == 1:
                    if data_keyin.lower() == format(result).lower():
                        mcount += 1
                        mname = format(result)
                        mclist.append( x['corp_code'] )
                        msclist.append( x['stock_code'] )
                code = x['corp_code']
                scode = x['stock_code']
                print('회사명:{}, 고유코드:{}, 종목코드:{}'.format(result, x['corp_code'], x['stock_code']))

        update = update_defs.Update()
        if count == 0:
            print('검색결과가 없습니다.')
        elif count == 1:
            rightornot = input('찾으시는 회사가 맞나요? << {} >> || (o/x) 입력 후 엔터를 눌러주세요 : '.format(result))
            if rightornot == 'o':
                report.stock_report( format(result) , code)
                update.update_single( format(result), scode)
                print('* Excel에 작성 완료되었습니다 !')
            elif rightornot == 'x':
                continue
        elif count > 1:
            if isq:
                for c in range( len( mclist ) ):
                    print(isq)
                    print(mclist)
                    print(mname)
                    judge = defs.Defs()
                    judge.yamishogun(mname, mclist[c])
                    j = judge.j
                    if j is not False:
                        report.stock_report( mname , mclist[c] )
                        update.update_single( mname, msclist[c] )
                        print('* Excel에 작성 완료되었습니다 !')
            else:
                print('>> Excel에 작성하기 위해서는 \"정확한 회사명\"을 입력하셔야 합니다.')
                print('>> sk를 검색하고 싶은데 결과가 많아서 입력이 안된다면, !를 붙여주세요 < ex) sk! >')

        print('=' * 100)
