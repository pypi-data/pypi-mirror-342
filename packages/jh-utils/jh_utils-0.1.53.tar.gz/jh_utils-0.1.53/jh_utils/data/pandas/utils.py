import pandas as pd
import numpy as np


def crossjoin(column_1, column_2):
    """
    Create a crossjoin dataframe based on 2 columns
    """
    columns_name = [column_1.name, column_2.name]
    column_1 = pd.DataFrame(column_1.unique())
    column_2 = pd.DataFrame(column_2.unique())
    column_1['key'], column_2['key'] = 0, 0
    df_ret = column_1.merge(column_2, on='key').drop(columns='key')
    df_ret.columns = columns_name
    return df_ret

##


def get_na_by_column(df):
    ret = df.isnull().mean()
    return ret


def clean_na(df, na_value=''):
    # Na from dataset

    df.index = df['date_time']
    df = df.drop(columns=['date_time'])

    df = df.replace(to_replace=na_value, value=np.NaN)
    df = df[df.iloc[:, 1].first_valid_index():]
    df = df.fillna(method='ffill')
    return df
