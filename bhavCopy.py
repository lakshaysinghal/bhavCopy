import requests
import datetime
import calendar
from zipfile import ZipFile
from io import BytesIO
import sys

def bhavcopy():
    url_prefix = "https://www1.nseindia.com/content/historical/EQUITIES/" #2020/APR/cm10APR2020"
    url_suffix = "bhav.csv.zip"
    cnt = 0
    while True:
        dt = datetime.datetime.now() - datetime.timedelta(days=cnt)
        value = str(dt.year) + "/" + calendar.month_abbr[dt.month].upper() + "/cm" + f"{dt:%d}" + calendar.month_abbr[dt.month].upper() + str(dt.year)
        url = url_prefix + value + url_suffix
        #print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            zip_file = ZipFile(BytesIO(resp.content))
            data_tmp = zip_file.open(zip_file.namelist()[0]).read()
            data = [x.split(',') for x in data_tmp.decode('utf-8').split('\n')]

            field = data.pop(0)
            data.pop(-1)
            cnt_5p =  cnt_5n = cnt_0p = cnt_0n = 0 
            for row in data:
                a = float(row[5])
                b = float(row[7])
                row[-1] = 100*(a-b)/b
                if row[-1] > 0:
                    cnt_0p+=1
                else:
                    cnt_0n+=1

                if row[-1] > 5:
                    cnt_5p+=1
                if row[-1] < 5:
                    cnt_5n+=1

            print()                    
            print("Number of Stocks which advanced more than 5% on NSE today : ",cnt_5p)
            print("Number of Stocks which declined more than 5% on NSE today : ",cnt_5n)
            bbr = cnt_5p/cnt_5n if cnt_5p > cnt_5n else -1*(cnt_5n/cnt_5p)
            print("Bull/Bear ratio                                           : ",bbr)
            adr = cnt_0p/cnt_0n if cnt_0p > cnt_0n else -1*(cnt_0n/cnt_0p)
            print("Advance/Decline ratio                                     : ",adr)
            break
        else:
            print("Data not available for ",dt)
            cnt+=1

if __name__ == "__main__":
    bhavcopy()