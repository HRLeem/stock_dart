import requests
import json
import pandas as pd
import numpy as np
import openpyxl

def make_params(code):
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
    return PARAMS
# 응답확인하고 전체 재무제표를 df변수로 넘겨주는 함수
def response(code):
    URL = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
    PARAMS = make_params(code)
    resp = requests.get(url=URL, params=PARAMS)

    # http 정상응답시 처리
    if resp.status_code == 200:
        data_json = resp.json()

        # OUTPUT
        data_str = json.dumps(data_json, indent=4, ensure_ascii=False)
        # print(data_str)

        if data_json['status'] == "000":
            detail = data_json['list']

            # for x in detail:
            # if x['fs_div'] == 'CFS' and x['sj_div'] == 'IS' and x['account_nm'] == '당기순이익':
            # print(json.dumps(x, indent=4, ensure_ascii=False))

            # Json 코드 DataFrame으로 변환
            df = pd.json_normalize(detail)
            # print('2feiwnif', df)
            # print(df)
            return df
        else:
            return False
            # print(data_json['message'])

def process_df(df):
    # CFS / OFS check
    for_check = df['fs_div']
    total = 0
    num_ofs = 0
    for i, item in for_check.iteritems():
        total += 1
        if for_check.loc[i] == "OFS":
            num_ofs += 1
    # 같다면 연결없는 회사 ==> OFS  ||| 다르다면 연결있는 회사 ==> CFS
    if total == num_ofs:
        cfsofs = "OFS"
    else:
        cfsofs = "CFS"
    # Actual function
    dfs = [real_process(df, cfsofs, 'BS'), real_process(df, cfsofs , 'IS'), cfsofs]

    return dfs


    # CFS == 연결회계. OFS == 단독재무제표(!! 모회사가 없는 경우) 그렇기 때문에 자꾸 연결회계가 없는 회사에서 삑이 났던것.
    # BS = 재무상태표 || IS = 손익계산서


def real_process(df, sort, bsis):

    # Series로 선언한 후 조립
    _fs = df['fs_div'] == sort
    _sj = df['sj_div'] == bsis
    df_long = df[_fs & _sj]

    # 계정과목명, 당기금액, 전기금액 추출
    terms = ['account_nm', 'bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']
    result_df = df_long.loc[:, terms]


    # comma(,) 제거 후 np.int64 파싱
    result_df.loc[:, ['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']] = result_df[['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']].apply(
        lambda x: x.str.replace(',', '').astype(np.int64))

    return result_df



# GOD-LIST
def make_jgod_list(df_j, company_name):
    jgod_list = []
    jgod_list.append(company_name)
    navi1 = [0,5,3,2,5,8,8]
    navi2 = [3,8,0,0,0,2,6]
    for m in range(0,7):
        if m==2 or m==3 or m==4:
            df_tolist = list(np.array(df_j.iloc[ navi1[m] ].tolist()))
            jgod_list.append( katarina(df_tolist[1], df_tolist[2], 1))
            jgod_list.append( katarina(df_tolist[2], df_tolist[3], 1))
        else:
            df_tolist1 = list(np.array(df_j.iloc[ navi1[m] ].tolist()))
            df_tolist2 = list(np.array(df_j.iloc[ navi2[m] ].tolist()))
            if m==6:
                if katarina(df_tolist1[3], df_tolist2[3], 6):
                    jgod_list.append('!!!')
                else:
                    jgod_list.append(' ')
            else:
                jgod_list.append( katarina(df_tolist1[2], df_tolist2[2], 0) )
                jgod_list.append( katarina(df_tolist1[3], df_tolist2[3], 0) )
    return jgod_list


def make_sgod_list(df_s, company_name):
    sgod_list = []
    sgod_list.append(company_name)
    per_m_list = []
    per_y_list = []
    for i in range(0,4):
        if i != 2:
            df_tolist = list(np.array(df_s.iloc[i].tolist()))
            del df_tolist[0]
            for j in range (0,3):
                change_num = int(df_tolist[j])

                if i==0:
                    per_m_list.append(change_num)
                if i==1:
                    per_y_list.append(change_num)

                if change_num < 100000000000:
                    list_new = round( change_num /100000000, 1)
                else:
                    list_new = round( change_num /100000000 )
                list_new = make_comma(list_new)
                sgod_list.append(list_new)
        if i == 2:
            for z in range(0,3):
                this_one = round( per_y_list[z]/per_m_list[z]*100, 1)
                this_one = str(this_one)+"%"
                sgod_list.append(this_one)
    return sgod_list


def make_comma(num):
    return "{:,}".format(num)


# a/b || a==전기 b==당기
def katarina(a, b, c):
    if c == 0:
        this_one = round( int(a) / int(b) * 100, 1)
        return str(this_one)+'%'
    elif c == 1:
        a = int(a)
        b = int(b)
        b_a = b-a
        this_one = round( b_a/a * 100, 1)
        return str(this_one)+'%'
    elif c == 6:
        a = int(a)
        b = int(b)
        if a < b:
            return 1
        else:
            return 0


# ABOUT EXCEL ***

def write_xlsx(god_list, js):
    name = 'stock.xlsx'
    filename = ''
    wb = openpyxl.load_workbook(name)

    if js == 'j':
        filename = '재무상태표'
    elif js == 's':
        filename = '손익계산서'
    elif js == 'i':
        filename = '투자지표'
    cell_check(filename)

    sheet = wb.get_sheet_by_name(filename)
    sheet.append(god_list)
    wb.save(name)

def cell_check(fn):
    sheet = openpyxl.load_workbook('stock.xlsx').get_sheet_by_name(fn)
    print('1 : ', sheet['A1'].value)
    print('2 : ', sheet['B1'].value)



#     ********************* process_df 전문.
# # 특정컬럼 추출
#     # _account_nm_sr = df['account_nm']
#     # print('_account_nm_sr: ', type(_account_nm_sr))
#     # print(_account_nm_sr)
#     # N개 컬럼 추출
#     _main_columns = df[['account_nm', 'fs_div', 'sj_div']]
#     # print('_main_columns: ', type(_main_columns))
#     # print(_main_columns)
#
#     # 1. 조건을 Series로 선언한 후 조립
#     # CFS == 연결회계. OFS == 단독재무제표(!! 모회사가 없는 경우) 그렇기 때문에 자꾸 연결회계가 없는 회사에서 삑이 났던것.
#     _fs = df['fs_div'] == 'CFS'
#     _sj = df['sj_div'] == 'IS'
#     result_01 = df[_fs & _sj]
#     # # 2. 내부에 바로 선언, 각 조건은 ()을 묶어줘야한다.
#     # result_02 = df[
#     #     (df['fs_div'] == 'CFS')
#     #     & (df['sj_div'] == 'IS')
#     #     ]
#     # ** 내맘대로 조건 2로 재무생태표를 출력하게 함.
#     _fs = df['fs_div'] == 'CFS'
#     _sj = df['sj_div'] == 'BS'
#     result_02 = df[_fs & _sj]
#
#     # 계정과목명, 당기금액, 전기금액 추출
#     _extract_cols = ['account_nm', 'bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']
#     df_j = result_02.loc[:, _extract_cols]
#     # print('==========재무상태표==========')
#     # print(df_j)
#     # 계정과목명, 당기금액, 전기금액 추출
#     _extract_cols = ['account_nm', 'bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']
#     df_s = result_01.loc[:, _extract_cols]
#     # print('==========손익계산서==========')
#     # print(df_s)
#
#
#
#     # comma(,) 제거 후 np.int64 파싱
#     df_s.loc[:, ['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']] = df_s[['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']].apply(
#         lambda x: x.str.replace(',', '').astype(np.int64))
#     df_j.loc[:, ['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']] = df_j[['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']].apply(
#         lambda x: x.str.replace(',', '').astype(np.int64))
#
#     # extracted_df.loc[:, 'ratio'] = extracted_df.thstrm_amount / extracted_df.frmtrm_amount * 100
#     #
#     # extracted_df.loc[:, 'gap'] = extracted_df.thstrm_amount - extracted_df.frmtrm_amount
#     #
#     # print(extracted_df)
#
#     # **** dataframe to list
#     # list = np.array(extracted_df_j[1].tolist())
#     # print(list)

# stock_report.py 밑에 남아있던 똥..이아닌 침전물....혹시몰라서

#=======================================================================================

# # *** to Excel
# base_dir = "C:/Users/HR/double/stock"
# file_nm = "df.xlsx"
# xlsx_dir = os.path.join(base_dir, file_nm)
#
# new_df = extracted_df_j
#
# new_df.to_excel(xlsx_dir,
#                 sheet_name = 'Sheet1',
#                 na_rep = 'NaN',
#                 float_format= "%.sf",
#                 header= True,
#                 index = True,
#                 index_label = "id" ,
#                 startrow=1,
#                 startcol=1,
#                 freeze_panes= (2,0)
#                 )