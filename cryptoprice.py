import time
import json
from pandas.core.frame import DataFrame
import requests
from datetime import datetime, timedelta
import pandas as pd
import requests_cache

#cache work install
requests_cache.install_cache()

#Market id to call
### need to get input for ticker

#Example: MARKET_ID = "bitcoin"
MARKET_ID = input("Enter name of crypto for price info(lower case): ")
day_input = input("Get price data from how many days ago? ")

#payload inputs are vs_currency(usd) and 
#days(Minutely data for duration within 1 day, Hourly data for duration between 1 day and 90 days, Daily data for duration above 90 days)
payload = {
    "vs_currency": "usd",
    "days": "max"
}

def main():
    coinname = convert_coin_name()
    coinprice = convert_price_to_df(getcoinprice(payload, coinname))
    print(coinprice)
    print(coinprice.loc[str(datetime.today().date() - timedelta(days=int(day_input)))]["Price"].item())

def convert_coin_name():
    #Coingecko API => get coin lists, convert to DataFrame(may not be needed), and get id name of symbol
    payload = {
        "include_platform": "false",
        "format": "json"
    }
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        print(response.text)
    else:
        #print(response.json())
        df = pd.DataFrame(response.json())
        print(df[(df["id"] == MARKET_ID) | (df["symbol"] == MARKET_ID)].iloc[:,:2])
        return df[(df["id"] == MARKET_ID) | (df["symbol"] == MARKET_ID)]["id"].item()
            
    if not getattr(response, 'from_cache', False):
       time.sleep(0.25)
    
def getcoinprice(payload, coinname):
    #Coingecko API => get coin price data for specific market id
    url = "https://api.coingecko.com/api/v3/coins/" + coinname + "/market_chart"
    payload["format"] = "json"
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        print(response.text)
        print("Crypto name of " + coinname + " does not exist.")
    else:
        #print(response.json())
        return response
    
    #if it's not cached result, sleep 0.25 -> ~4 calls per second
    if not getattr(response, 'from_cache', False):
       time.sleep(0.25)

def convert_price_to_df(response):
    #convert price data json to DataFrame and show prices only
    df = pd.DataFrame(response.json()["prices"])
    #change column names
    df.columns = ["Date", "Price"]
    #format price data to include commas
    df["Price"] = df["Price"].map("{0:,.0f}".format)
    #format date data from timestamp/epoch to datetime
    df["Date"] = pd.to_datetime(df["Date"], unit="ms")#.dt.date
    #drop second to last row with the most recent today data
    df = df.drop(df.index[-2])
    #set date to index
    df = df.set_index(["Date"], inplace=False)
    
    return df

    #df.info()
    #df.describe()
    #print(type(df.index))
    #print(df.loc['2020-10-25'])

if __name__ == "__main__":
    main()




"""def jprint(obj):
    #create a formatted string of the Python JSON object
    textdata = json.dumps(obj, sort_keys=True, indent=4)
    print(textdata)
    
jprint(r.json())"""


