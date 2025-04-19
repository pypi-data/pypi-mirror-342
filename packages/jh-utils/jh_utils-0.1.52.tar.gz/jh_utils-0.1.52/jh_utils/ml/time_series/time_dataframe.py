import pandas as pd
import numpy as np
from jh_utils.time_series.covariables import year_sincos_array, hour_sincos_array, hours_by_day
from jh_utils.data.pandas.preprocessing import make_dummies


def create_date_range_dataframe(start_date, end_date, freq='1H', column_name='hours'):
    df = pd.DataFrame({column_name: pd.date_range(
        start_date, end_date, freq=freq, closed='left')})
    return df


def create_time_series_dataframe(start_date, end_date, freq='1H', datetime_column_name='hours',
                                 weekday_dummies=True,
                                 month_dummies=True,
                                 hour_dummies=True):
    df = create_date_range_dataframe(start_date, end_date,
                                     freq=freq, column_name=datetime_column_name)
    if weekday_dummies:
        df = pd.concat([df, make_dummies(
            pd.Series(df.iloc[:, 0].dt.weekday, name='weekday_dummie'))], axis=1)
    if month_dummies:
        df = pd.concat([df, make_dummies(
            pd.Series(df.iloc[:, 0].dt.month, name='month_dummie'))], axis=1)
    if hour_dummies:
        df = pd.concat([df, make_dummies(
            pd.Series(df.iloc[:, 0].dt.hour, name='hour_dummie'))], axis=1)

    df.index = df[datetime_column_name]
    df = df.iloc[:, 1:]
    return df


def make_date_hour_crossjoin(column_1, column_2):
    """
    Create a crossjoin dataframe based on 2 columns
    """
    column_1 = pd.DataFrame(column_1.unique())
    column_2 = pd.DataFrame(column_2.unique())
    column_1['key'], column_2['key'] = 0, 0
    date_time = column_1.merge(column_2, on='key').drop(columns='key')
    date_time.columns = ['data', 'hora']
    date_time.sort_values(['data', 'hora'], inplace=True)
    date_time.reset_index(inplace=True, drop=True)
    return date_time
