import pandas as pd
import defs.stock_defs as defs


def stock_report( name, code ):
    # Setting
    # 순서대로 최대 줄 수 설정, 최대 열 수 설정, 표시할 가로의 길이
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # 재무제표 전문 받아내기
    df = defs.response(code)

    # 재무제표 필요한부분 걸러내기
    dfs = defs.process_df(df)
    df_j = dfs[0]
    df_s = dfs[1]

    # 엑셀에 작성할 이쁜 형태로 뽑아내기
    jgod_list = defs.make_jgod_list(df_j, name)
    sgod_list = defs.make_sgod_list(df_s, name)

    # 엑셀에 써갈기기
    defs.write_xlsx(jgod_list, 'j')
    defs.write_xlsx(sgod_list, 's')


