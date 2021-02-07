# 모듈 불러오기
import dart_fss as dart

api_key='9603774f25edc5686b1d7df2e3d1f8788a864fe3' # api key 변수 설정
dart.set_api_key(api_key=api_key) # 인증 설정
# crp_list = dart.get_corp_list() # 상장회사 정보 리스트 받아오기
# basic_info = crp_list.find_by_corp_code('005930') # 삼성전자 종목코드를 파라미터로 넣어 삼성전자 기본 정보 가져오기
# financial_reports = basic_info.get_financial_statement(start_dt=20180101) # 크롤링을 원하는 시작일자 설정
# the_statements = financial_reports['fs'[0]] # 크롤링한 데이터 중 재무상태표(fs : financial statements)만 선택하여 변수 할당

# print(the_statements)
print( dart.get_corp_list())
print( dart.search('005930') )