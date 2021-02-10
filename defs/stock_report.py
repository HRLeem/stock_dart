# -*- coding: utf-8 -*-
import pandas as pd
import defs.stock_defs as defs


def stock_report( name, code ):
    # Setting
    # 순서대로 최대 줄 수 설정, 최대 열 수 설정, 표시할 가로의 길이
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # Make Instances
    go = defs.Defs()
    list = defs.Defs_list()
    excel = defs.Excel()

    # Work
    go.yamishogun(name, code)
    list.dfs = go.dfs
    list.list_plz()
    excel.lists = list.lists
    excel.save_excel()


