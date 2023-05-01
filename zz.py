import datetime

import pandas as pd
import numpy as np

def count_nan(series):
    return np.isnan(series).sum()
def xxx():
    str = 'C:\\Users\\223037435\\Desktop\\Plant II\\df.csv'
    df = pd.read_csv(str)
    df['Open Actions'] = df['is_date1_after_date2']
    df['DUEDATE'] = pd.to_datetime(df['DUEDATE'])
    today = datetime.datetime.now().date()
    df['Over Due'] = ((df['DUEDATE'].dt.date < today) & (df['COMPDATE'].isna())).astype(int)
    df = df.rename(columns={'is_date1_after_date2': 'Late'})
    df['Completed'] = df['Late'] + df['On Time']
    df0 = df
    print(df.columns)
    df =df.groupby(['Category', 'PRIM_DESC', 'PRIM_OWNER']).agg({'On Time': 'sum', 'Late': 'sum','Open Actions': count_nan, 'Completed':'sum', 'Over Due': 'sum'})
    df = pd.DataFrame(df).reset_index()
    df['% on Time'] = (df['On Time'] / df['Completed'] *100).map('{:.1f}%'.format)
    df['% on Time'] = df['% on Time'].replace('nan%','')
    return df, df0