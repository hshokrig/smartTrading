from __future__ import print_function
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import seaborn as sns

import six


def get_root_dir():
    load_dotenv()
    return os.getenv('DISCORD_PATH')


def get_history(symbol):
    day_technicals = yf.Ticker(symbol).history(interval='1d', period='10y', actions=False)
    day_technicals['ChangePercentage'] = (day_technicals['Close'] - day_technicals['Open'])/day_technicals['Open'] * 100
    day_technicals.to_csv(os.getcwd()+'/src/datasets/{}-daily-{}.csv'.format(symbol.lower(), str(datetime.today().date())))
    return day_technicals


def mean_return_1D(symbol, days_future=30, reference=10000, price_change_bound_tr=0.2):
    root_dir = get_root_dir()
    path_ = '{}/src/datasets/{}-daily-{}.csv'.format(root_dir, symbol, str(datetime.today().date()))
    if os.path.isfile(path_):
        data = pd.read_csv(path_)
    else:
        data = get_history(symbol)

    try:
        last_change = data['ChangePercentage'].values[-1]
        if reference == 10000:
            reference_change = last_change.copy()
        else:
            reference_change = reference

        changes_range = [reference_change * (1 - price_change_bound_tr), reference_change * (1 + price_change_bound_tr)]
        changes_range.sort()
        price_changes_in_interval = (data['ChangePercentage'] >= changes_range[0]) & (data['ChangePercentage'] <= changes_range[1])
        start_dates_list = [i for i, x in enumerate(price_changes_in_interval) if x]
        number_of_events = sum(price_changes_in_interval)
        column_names = ['{}'.format(i + 1) for i in range(days_future)]
        contents_list = [data.iloc[start_date
                                   + 1:start_date + days_future + 1]['ChangePercentage'].values for start_date in start_dates_list]
        array_sizes = np.array([contents_list[i].size for i in range(len(contents_list))])
        idx = np.argmax(array_sizes < array_sizes[0])
        contents = np.array(contents_list[:idx])
        daily_changes_df = pd.DataFrame(contents, columns=column_names)
        return_df = daily_changes_df.cumsum(axis=1)
        mean_return = return_df.mean(axis=0)
        fig, ax = plt.subplots()
        ax.plot(mean_return, linewidth=2, markersize=12)

        ax.set(xlabel='Days', ylabel='Mean return %')
        ax.grid(axis='y', linestyle='--')
        if mean_return.size > 10:
            xticks = np.ceil(np.linspace(1, mean_return.size, num=10, endpoint=True)).astype(int)
            plt.xticks(xticks - 1, rotation=300)
        else:
            plt.xticks(rotation=300)

        file_address = './src/images/mean_return_{}_{}_1D.png'.format(symbol.lower(), days_future)
        fig.savefig(file_address)

        return file_address, number_of_events, reference_change
    except:
        print('Exception occured')


def mean_return_kD(symbol, days_future=30, days_past=5, price_change_bound_tr=0.2):
    root_dir = get_root_dir()
    path_ = '{}/src/datasets/{}_daily.csv'.format(root_dir, symbol)
    if os.path.isfile(path_):
        data = pd.read_csv(path_)
    else:
        data = get_history(symbol)

    try:
        reference_change = data['ChangePercentage'].values[-days_past].sum()

        changes_range = [reference_change * (1 - price_change_bound_tr), reference_change * (1 + price_change_bound_tr)]
        changes_range.sort()
        data_kD = [data['ChangePercentage'].values[i-days_past:i].sum() for i in range(days_past,data.shape[0])]
        price_changes_in_interval = (data_kD >= changes_range[0]) & (data_kD <= changes_range[1])
        start_dates_list = [i for i, x in enumerate(price_changes_in_interval) if x]
        number_of_events = sum(price_changes_in_interval)
        column_names = ['{}'.format(i + 1) for i in range(days_future)]

        contents_list = [data.iloc[start_date
                                   + 1:start_date + days_future + 1]['ChangePercentage'].values for start_date in start_dates_list]
        array_sizes = np.array([contents_list[i].size for i in range(len(contents_list))])
        if array_sizes[-1] < array_sizes[0]:
            idx = np.argmax(array_sizes < array_sizes[0])
            contents = np.array(contents_list[:idx])
        else:
            contents = np.array(contents_list)

        daily_changes_df = pd.DataFrame(contents, columns=column_names)

        return_df = daily_changes_df.cumsum(axis=1)
        mean_return = return_df.mean(axis=0)

        fig, ax = plt.subplots()
        ax.plot(mean_return, linewidth=2, markersize=12)

        print(4)

        ax.set(xlabel='Days', ylabel='Mean return %')
        ax.grid(axis='y', linestyle='--')
        if mean_return.size > 10:
            xticks = np.ceil(np.linspace(1, mean_return.size, num=10, endpoint=True)).astype(int)
            plt.xticks(xticks - 1, rotation=300)
        else:
            plt.xticks(rotation=300)

        print(5)

        file_address = os.getcwd()+'/src/images/mean_return_{}_{}_{}D.png'.format(symbol.lower(), days_future, days_past)
        fig.savefig(file_address)

        return file_address, number_of_events, reference_change
    except:
        print('Exception occured')


def get_price(symbol):
    try:
        url = 'https://www.marketwatch.com/investing/stock/' + symbol
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        if soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'pre':        # Premarket
            market_hour = 'pre'
        elif soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'after':    # Aftermarket
            market_hour = 'after'
        else:                                                                                 # day market
            market_hour = 'RH'

        price_change = soup.select("span.change--percent--q>bg-quote")[0].get_text()

        return market_hour, price_change

    except:
        print('Exception occured')


def SPY_AH(yesterday_change, today_change, intra_day_change, followed_by_weekend):
    symbol = 'SPY'
    root_dir = get_root_dir()
    path_ = '{}/src/datasets/{}CloseDataset.csv'.format(root_dir, symbol)

    try:
        dataset = pd.read_csv(path_)

        # distribution of 80-percentile after-hours changes for the last year
        if yesterday_change >= 0:
            cond1 = dataset.daily_changes_1 > yesterday_change
        else:
            cond1 = dataset.daily_changes_1 < yesterday_change

        if today_change >= 0:
            cond2 = dataset.daily_changes_0 > today_change
        else:
            cond2 = dataset.daily_changes_0 < today_change

        if intra_day_change >= 0:
            cond3 = dataset.intra_day_changes > intra_day_change
        else:
            cond3 = dataset.intra_day_changes < intra_day_change

        if followed_by_weekend:
            cond4 = dataset.followed_by_weekend == 1
        else:
            cond4 = True

        data = dataset[cond1 & cond2 & cond3 & cond4]['percentile_AH_gain']
        number_of_events = len(data)
        mean_gain = data.mean()

        fig, ax = plt.subplots()

        plot_data = sns.ecdfplot(ax=ax, data=data, linewidth=2)

        (x_data, y_data) = plot_data.get_lines()[0].get_data()
        win_chance = 1-y_data[np.where(abs(x_data) == np.amin(abs(x_data)))[0][0]]

        fig1, ax1 = plt.subplots()

        ax1.plot(x_data, 1-y_data, linewidth=2)
        ax1.plot([0, 0], [0, 1], linewidth=1, linestyle='--')

        ax1.set(xlabel='AH gain %', ylabel='Complementary CDF')
        ax1.grid(axis='y', linestyle='--')
        plt.ylim([0, 1])

        file_address = os.getcwd()+'/src/images/{}_AH_gain_{}_{}_{}.png'.format(symbol.upper(), yesterday_change, today_change, intra_day_change)
        fig1.savefig(file_address)

        return file_address, number_of_events, mean_gain, win_chance
    except:
        print('Exception occured')

