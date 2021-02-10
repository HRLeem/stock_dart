# -*- coding: utf-8 -*-
import requests
import pandas as pd
import numpy as np
import openpyxl


class Defs:
    def __init__(self):
        self.API_KEY = "9603774f25edc5686b1d7df2e3d1f8788a864fe3"
        self.URL = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
        self.total = 0
        self.num_ofs = 0
        self.cfsofs ='ㅁㅇㄻㅇㄹ'

    def make_params(self, code):
        params = { 'crtfc_key': self.API_KEY, 'corp_code': code, 'bsns_year': '2019', 'reprt_code': '11011'}
        self.PARAMS = params

    def response(self, code):
        self.make_params(code)
        resp = requests.get(url=self.URL, params=self.PARAMS)
        self.resp = resp

    # total work
    def yamishogun(self, name, code):
        self.name = name
        self.response(code)
        if self.resp.status_code == 200:
            data_json = self.resp.json()
            if data_json['status'] == '000':
                self.j = True
                self.df = pd.json_normalize(data_json['list'])
                self.process_df()
            else:
                self.j = False

    def process_df(self):
        for_check = self.df['fs_div']
        for i, item in for_check.iteritems():
            self.total +=1
            if for_check.loc[i] == "OFS":
                self.num_ofs +=1
        self.check_cfsofs()
        self.real_process('BS')
        self.real_process('IS')
        self.dfs = [self.df_j, self.df_s, self.name]
        print(self.dfs)

    def check_cfsofs(self):
        if self.total == self.num_ofs:
            self.cfsofs = 'OFS'
        else:
            self.cfsofs = 'CFS'

    def real_process(self, bsis):
        # Series로 선언한 후 조립
        _fs = self.df['fs_div'] == self.cfsofs
        _sj = self.df['sj_div'] == bsis
        df_long = self.df[_fs & _sj]

        # 계정과목명, 당기금액, 전기금액 추출
        terms = ['account_nm', 'bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']
        result_df = df_long.loc[:, terms]

        # comma(,) 제거 후 np.int64 파싱
        result_df.loc[:, ['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']] = result_df[
            ['bfefrmtrm_amount', 'frmtrm_amount', 'thstrm_amount']].apply(
            lambda x: x.str.replace(',', '').astype(np.int64))
        if bsis == 'BS':
            self.df_j = result_df
        elif bsis == 'IS':
            self.df_s = result_df



class Defs_list:
    def __init__(self):
        self.navi1 = [0,5,3,2,5,8,8]
        self.navi2 = [3,8,0,0,0,2,6]
        self.jgod_list = []
        self.sgod_list = []
        self.per_m_list = []
        self.per_y_list = []

    # def receive_dfs(self, a, b, name):
    #     self.df_j = a
    #     self.df_s = b
    #     self.name = name
    def receive_dfs(self):
        self.df_j = self.dfs[0]
        self.df_s = self.dfs[1]
        self.name = self.dfs[2]

    def list_plz(self):
        self.receive_dfs()
        self.make_jgod_list()
        self.make_sgod_list()
        self.lists = [self.jgod_list, self.sgod_list]

    def make_jgod_list(self):
        self.jgod_list.append(self.name)
        for m in range(0, 7):
            if m == 2 or m == 3 or m == 4:
                df_tolist = list(np.array(self.df_j.iloc[self.navi1[m]].tolist()))
                self.jgod_list.append(self.katarina(df_tolist[1], df_tolist[2], 1))
                self.jgod_list.append(self.katarina(df_tolist[2], df_tolist[3], 1))
            else:
                df_tolist1 = list(np.array(self.df_j.iloc[self.navi1[m]].tolist()))
                df_tolist2 = list(np.array(self.df_j.iloc[self.navi2[m]].tolist()))
                if m == 6:
                    if self.katarina(df_tolist1[3], df_tolist2[3], 6):
                        self.jgod_list.append('!!!')
                else:
                    self.jgod_list.append(self.katarina(df_tolist1[2], df_tolist2[2], 0))
                    self.jgod_list.append(self.katarina(df_tolist1[3], df_tolist2[3], 0))

    def make_sgod_list(self):
        self.sgod_list.append(self.name)
        for i in range(0, 4):
            if i != 2:
                df_tolist = list(np.array(self.df_s.iloc[i].tolist()))
                del df_tolist[0]
                for j in range(0, 3):
                    change_num = int(df_tolist[j])

                    if i == 0:
                        self.per_m_list.append(change_num)
                    if i == 1:
                        self.per_y_list.append(change_num)

                    if change_num < 100000000000:
                        list_new = round(change_num / 100000000, 1)
                    else:
                        list_new = round(change_num / 100000000)
                    list_new = self.make_comma(list_new)
                    self.sgod_list.append(list_new)
            if i == 2:
                for z in range(0, 3):
                    this_one = round(self.per_y_list[z] / self.per_m_list[z] * 100, 1)
                    this_one = str(this_one) + "%"
                    self.sgod_list.append(this_one)

    def make_comma(self, num):
        return "{:,}".format(num)

    # a/b || a==전기 b==당기
    def katarina(self, a, b, c):
        if c == 0:
            this_one = round(int(a) / int(b) * 100, 1)
            return str(this_one) + '%'
        elif c == 1:
            a = int(a)
            b = int(b)
            b_a = b - a
            this_one = round(b_a / a * 100, 1)
            return str(this_one) + '%'
        elif c == 6:
            a = int(a)
            b = int(b)
            if a < b:
                return 1
            else:
                return 0


# ABOUT EXCEL ***

class Excel:
    def __init__(self):
        self.name = 'stock.xlsx'
        self.basic = ['재무상태표', '손익계산서']
        self.indicator = ''

    def switch(self, indicator, list):
        if indicator == 'indicator':
            self.indicator = '투자지표'
            self.list_indicator = list

    def save_excel(self):
        if self.indicator != '투자지표':
            for i in range(0,2):
                self.write_xlsx(self.lists[i], self.basic[i])
        else:
            self.write_xlsx(self.list_indicator, self.indicator)

    def write_xlsx(self, god_list, filename):
        wb = openpyxl.load_workbook(self.name)

        sheet = wb.get_sheet_by_name(filename)
        sheet.append(god_list)
        wb.save(self.name)