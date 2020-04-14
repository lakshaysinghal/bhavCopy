import requests
import datetime
import calendar
from zipfile import ZipFile
from io import BytesIO
import sys

def bhavcopy():
    url_prefix = "https://www1.nseindia.com/content/historical/EQUITIES/" #2020/APR/cm10APR2020"
    url_suffix = "bhav.csv.zip"
    lookup_days = int(input("Number of lookup days:"))
    count = 0
    while(count < lookup_days):
        dt = datetime.datetime.now() - datetime.timedelta(days=count)
        print("Fetching data for date:", dt)
        value = str(dt.year) + "/" + calendar.month_abbr[dt.month].upper() + "/cm" + f"{dt:%d}" + calendar.month_abbr[dt.month].upper() + str(dt.year)
        url = url_prefix + value + url_suffix
        resp = requests.get(url)
        if resp.status_code == 200:
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
                else:
                    number_of_negative_stocks+=1

                if row[-1] > 5:
                    number_of_stocks_advancing_5p+=1
                if row[-1] < 5:
                    number_of_stocks_declining_5p+=1
                    
            print("Number of Stocks which advanced more than 5% on NSE today : ",number_of_stocks_advancing_5p)
            print("Number of Stocks which declined more than 5% on NSE today : ",number_of_stocks_declining_5p)
            bull_bear_ratio = number_of_stocks_advancing_5p/number_of_stocks_declining_5p if number_of_stocks_advancing_5p > number_of_stocks_declining_5p else -1*(number_of_stocks_declining_5p/number_of_stocks_advancing_5p)
            print("Bull/Bear ratio                                           : ",bull_bear_ratio)
            advance_decline_ratio = number_of_positive_stocks/number_of_negative_stocks if number_of_positive_stocks > number_of_negative_stocks else -1*(number_of_negative_stocks/number_of_positive_stocks)
            print("Advance/Decline ratio                                     : ",advance_decline_ratio)
            count+=1
        else:
            print("Data not available for ",dt)
            count+=1

if __name__ == "__main__":
    bhavcopy()