import pandas as pd
import stock_defs as defs


def stock_report( name, code ):
    # =====================================================입력창===========================================
    API_KEY = "9603774f25edc5686b1d7df2e3d1f8788a864fe3"
    PARAMS = {
        'crtfc_key': API_KEY,
        # !!!!! 여기에 "고유코드"를 입력해주세요
        'corp_code': code,
        # 사업연도(4자리)
        'bsns_year': '2019',
        # 사업보고서
        # 1분기보고서 : 11013
        # 반기보고서 : 11012
        # 3분기보고서 : 11014
        # 사업보고서 : 11011
        'reprt_code': '11011',
    }
    # 엑셀에 입력될 회사 이름으로 바꿔주세요
    company_name = name
    # =====================================================입력창===========================================

    URL = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'

    # Setting
    # 최대 줄 수 설정
    pd.set_option('display.max_rows', 500)
    # 최대 열 수 설정
    pd.set_option('display.max_columns', 500)
    # 표시할 가로의 길이
    pd.set_option('display.width', 1000)

    # 재무제표 전문 받아내기
    df = defs.response(URL, PARAMS)

    # 재무제표 필요한부분 걸러내기
    dfs = defs.process_df(df)
    df_j = dfs[0]
    df_s = dfs[1]
    df_cfsofs = dfs[2]

    # 엑셀에 작성할 이쁜 형태로 뽑아내기
    jgod_list = defs.make_jgod_list(df_j, company_name)
    sgod_list = defs.make_sgod_list(df_s, company_name)

    # 엑셀에 써갈기기
    defs.write_xlsx(jgod_list, 'j')
    defs.write_xlsx(sgod_list, 's')


