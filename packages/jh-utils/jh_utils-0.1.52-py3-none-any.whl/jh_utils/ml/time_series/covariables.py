import pandas as pd
import numpy as np
from jh_utils.data.pandas.preprocessing import make_dummies


def create_time_series_dataframe(df,
                                 weekday_dummies=True,
                                 month_dummies=True,
                                 hour_dummies=True,
                                 datetime_column_name='datetime'):
    # shape = df.shape
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


def get_number_hours_by_day(freq='1H'):
    freq = freq.upper()
    if freq == '1H':
        return 24
    if freq == '2H':
        return 12
    if freq == '3H':
        return 8
    if freq == '4H':
        return 6
    if freq == '6H':
        return 4
    if freq == '8H':
        return 3
    if freq == '12H':
        return 2


def create_sincos_year_array(n, start_date, end_date, n_days_in_year=366):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # day distance
    first_date = pd.to_datetime('{year}-01-01'.format(year=start_date.year))
    day_of_the_year_start = (start_date - first_date).days

    # year distance
    distance = (end_date - first_date).days

    ##
    start = (np.pi*2)*(day_of_the_year_start/n_days_in_year)
    end = np.pi*2*(distance/n_days_in_year)

    length = np.arange(start, end, (end-start)/n)
    df = pd.concat([pd.Series(np.sin(length)),
                   pd.Series(np.cos(length))], axis=1)
    df.columns = ['sin_year', 'cos_year']
    return df


def create_sincos_hour_array(hours_by_day, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # ! year distance
    distance = (end_date - start_date).days

    start = 0
    end = np.pi*2*distance
    length = np.arange(start, end, np.pi*2/(hours_by_day))
    df = pd.concat([pd.Series(np.sin(length)),
                   pd.Series(np.cos(length))], axis=1)
    df.columns = ['sin_day', 'cos_day']
    return df.iloc[:-1]
