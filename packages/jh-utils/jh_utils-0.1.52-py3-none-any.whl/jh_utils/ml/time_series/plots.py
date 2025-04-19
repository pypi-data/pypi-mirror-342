import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


figsize = (20, 5)


def two_line_plot(df, x1, x2, freq='M', figsize=(20, 5), tittle=''):
    temp = df[['date_time', x1, x2]]
    temp.index = temp.date_time
    temp = temp.resample(freq).mean()
    temp.reset_index(inplace=True)
    plt.figure(figsize=figsize)
    _ = sns.lineplot(x=temp['date_time'], y=temp[x1]
                     ).set_title(tittle, fontsize=20)
    _ = sns.lineplot(x=temp['date_time'], y=temp[x2])


def two_hist_plot(df, x1, x2, freq='M', figsize=figsize, tittle=''):
    temp = df[['date_time', x1, x2]]
    temp.index = temp.date_time
    temp = temp.resample(freq).mean()
    temp.reset_index(inplace=True)
    plt.figure(figsize=figsize)
    _ = sns.histplot(df[x1], color='red').set_title(tittle, fontsize=20)
    _ = sns.histplot(df[x2])


def one_line_plot(df, x1, freq='M', figsize=figsize, tittle=''):
    temp = df[['date_time', x1]]
    temp.index = temp.date_time
    temp = temp.resample(freq).mean()
    temp.reset_index(inplace=True)
    plt.figure(figsize=figsize)
    _ = sns.lineplot(x=temp['date_time'], y=temp[x1]
                     ).set_title(tittle, fontsize=20)


def one_hist_plot(df, x1, freq='M', figsize=figsize, tittle=''):
    temp = df[['date_time', x1]]
    temp.index = temp.date_time
    temp = temp.resample(freq).mean()
    temp.reset_index(inplace=True)
    plt.figure(figsize=figsize)
    _ = sns.histplot(df[x1], color='red').set_title(tittle, fontsize=20)
