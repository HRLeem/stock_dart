# -*- coding: utf-8 -*-
from urllib.request import urlopen # HTTP 요청처리
from zipfile import ZipFile        # 공시회사정보 zipfile 처리
from io import BytesIO             # stream 데이터를 메모리에 적재
import os                          # 현재 디렉토리 정보를 얻기 위해
import xmltodict                   # xml을 dict로 파싱
from pathlib import Path           # file 존재유무 체크 유틸

import re
import stock_report as report
import stock_defs_no as defs_no

API_KEY = "9603774f25edc5686b1d7df2e3d1f8788a864fe3"

url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key="+API_KEY

""" Biz Start """
url = 'https://opendart.fss.or.kr/api/corpCode.xml?'
params = {
  'crtfc_key': API_KEY,  # API 인증키
}

corp_xml = defs_no.get_corp_xml(url, params)
corp_dict = xmltodict.parse(corp_xml)

# reulst > list 추출
corp_list = corp_dict['result']['list']

# stock_code가 None이 아닌 대상만 다시 추출한다.
corp_list_has_stockcode = [x for x in corp_list if x['stock_code'] is not None]
# print(len(corp_list_has_stockcode))



corp_list_has_stockcode = [x for x in corp_list if x['stock_code'] is not None]

