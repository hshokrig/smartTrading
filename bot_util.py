from __future__ import print_function
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import os

import requests
from bs4 import BeautifulSoup
import six



def get_history(symbol):
    day_technicals = yf.Ticker(symbol).history(interval='1d', period='10y', actions=False)
    day_technicals['ChangePercentage'] = (day_technicals['Close'] - day_technicals['Open'])/day_technicals['Open'] * 100
    day_technicals.to_csv('./src/datasets/{}_daily.csv'.format(symbol.lower()))
    return day_technicals


def mean_return_1D(symbol, days_future=30, reference=10000, price_change_bound_tr=0.2):
    cwd = os.getcwd()
    path = cwd+'/src/datasets/{}_daily.csv'.format(symbol)
    if os.path.isfile(path):
        data = pd.read_csv(cwd+'/src/datasets/{}_daily.csv'.format(symbol))
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

        file_address = cwd+'/src/images/mean_return_{}_{}_1D.png'.format(symbol.lower(), days_future)
        fig.savefig(file_address)

        return file_address, number_of_events, reference_change
    except:
        print('Exception occured')


def mean_return_kD(symbol, days_future=30, days_past=5, price_change_bound_tr=0.2):
    cwd = os.getcwd()
    path = cwd+'/src/datasets/{}_daily.csv'.format(symbol)
    if os.path.isfile(path):
        data = pd.read_csv(cwd+'/src/datasets/{}_daily.csv'.format(symbol))
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

        file_address = cwd+'/src/images/mean_return_{}_{}_{}D.png'.format(symbol.lower(), days_future, days_past)
        fig.savefig(file_address)

        return file_address, number_of_events, reference_change
    except:
        print('Exception occured')

def pre_ah_change(symbol): 
    try:
        url = 'https://www.marketwatch.com/investing/stock/'+symbol
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content,'html.parser')
        if soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'pre':
            #Premarket
            pre_market_change = soup.select("span.change--percent--q>bg-quote")[0].get_text()

        elif soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'after':
            #Aftermarket
            after_market_change = soup.select("span.change--percent--q>bg-quote")[0].get_text()
            
        elif soup.select("span.change--percent--q>bg-quote")[0].get('session') ==  None:
            #day market
            day_market_change = soup.select("span.change--percent--q>bg-quote")[0].get_text()
        
        if soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'pre':
            msg = 'In the premarket '+ symbol+' changed '+ pre_market_change
        elif soup.select("span.change--percent--q>bg-quote")[0].get('session') == 'after':
            msg = 'In the afterhours '+ symbol+' changed '+ after_market_change
        elif soup.select("span.change--percent--q>bg-quote")[0].get('session') == None:
            msg = 'The market is open and '+ symbol+' changed '+ day_market_change
        return msg
    except:
        print('Exception occured')