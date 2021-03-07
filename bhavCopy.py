#!/usr/bin/python3.6
import requests
import datetime
import math
import calendar
from zipfile import ZipFile
from io import BytesIO
import sys
import random
from time import sleep
import matplotlib.pyplot as plt
import matplotlib 
import matplotlib.dates as mdates


list_number_of_stocks_advancing_5p = []
list_number_of_stocks_declining_5p = []
list_bull_bear_ratio = []
list_advance_decline_ratio = []
list_dates = []
lookup_days = int(input("Number of lookup days:"))


def bhavcopy():
    url_prefix = "https://www1.nseindia.com/content/historical/EQUITIES/" #2020/APR/cm10APR2020"
    url_suffix = "bhav.csv.zip"
    header = {
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
    'Host': 'www1.nseindia.com',
    'Referer': 'https://www1.nseindia.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    count = 0
    while(count < lookup_days):
        dt = datetime.datetime.now() - datetime.timedelta(days=count)
        print("Fetching data for date:", dt)
        value = str(dt.year) + "/" + calendar.month_abbr[dt.month].upper() + "/cm" + f"{dt:%d}" + calendar.month_abbr[dt.month].upper() + str(dt.year)
        url = url_prefix + value + url_suffix
        resp = requests.get(url, headers=header)
        print(resp)
        print(resp.status_code)
        if resp.status_code == 200:
            print("Data available for ",dt)
            zip_file = ZipFile(BytesIO(resp.content))
            data_tmp = zip_file.open(zip_file.namelist()[0]).read()
            data = [x.split(',') for x in data_tmp.decode('utf-8').split('\n')]

            field = data.pop(0)
            data.pop(-1)
            number_of_stocks_advancing_5p =  number_of_stocks_declining_5p = number_of_positive_stocks = number_of_negative_stocks = 0 
            for row in data:
                close = float(row[5])
                prev_close = float(row[7])
                row[-1] = 100*(close-prev_close)/prev_close
                if row[-1] > 0:
                    number_of_positive_stocks+=1
                elif row[-1] < 0:
                    number_of_negative_stocks+=1

                if row[-1] > 5:
                    number_of_stocks_advancing_5p+=1
                if row[-1] < -5:
                    number_of_stocks_declining_5p+=1
                    
            print("Number of Stocks which advanced more than 5% on NSE today : ",number_of_stocks_advancing_5p)
            print("Number of Stocks which declined more than 5% on NSE today : ",number_of_stocks_declining_5p)
            bull_bear_ratio = round( number_of_stocks_advancing_5p/number_of_stocks_declining_5p if number_of_stocks_advancing_5p > number_of_stocks_declining_5p else -1*(number_of_stocks_declining_5p/number_of_stocks_advancing_5p),2)
            print("Bull/Bear ratio                                           : ",bull_bear_ratio)
            advance_decline_ratio = round(number_of_positive_stocks/number_of_negative_stocks if number_of_positive_stocks > number_of_negative_stocks else -1*(number_of_negative_stocks/number_of_positive_stocks),2)
            print("Advance/Decline ratio                                     : ",advance_decline_ratio)

            list_number_of_stocks_advancing_5p.append(number_of_stocks_advancing_5p)
            list_number_of_stocks_declining_5p.append(number_of_stocks_declining_5p)
            list_bull_bear_ratio.append(bull_bear_ratio)
            list_advance_decline_ratio.append(advance_decline_ratio)
            list_dates.append(dt)

            count+=1
            sleep(random.uniform(1, 3))
        else:
            print("Data not available for ",dt)
            count+=1
            sleep(random.uniform(1, 3))

def visualize():
    print("Cumilative Data:")
    print("Dates                                                     : ",list_dates)
    print("Number of Stocks which advanced more than 5% on NSE today : ",list_number_of_stocks_advancing_5p)
    print("Number of Stocks which declined more than 5% on NSE today : ",list_number_of_stocks_declining_5p)
    print("Bull/Bear ratio                                           : ",list_bull_bear_ratio)
    print("Advance/Decline ratio                                     : ",list_advance_decline_ratio)

    dates = matplotlib.dates.date2num(list_dates)
    print(dates)
    
    plt.xlabel('Dates')
    plt.ylabel('Number of stocks') 
    plt.title('NSE Market Breadth')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plot_interval = math.ceil(lookup_days/5)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=plot_interval))
    plt.gcf().autofmt_xdate()
    plt.plot(dates,list_number_of_stocks_advancing_5p, label = "5% Advancing") 
    plt.plot(dates,list_number_of_stocks_declining_5p, label = "5% Declining")
    plt.legend()
    
    # function to show the plot 
    plt.savefig("plot.png") 



if __name__ == "__main__":
    bhavcopy()
    visualize()
