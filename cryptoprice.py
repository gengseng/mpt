import time
import json
from pandas.core.frame import DataFrame
import requests
from datetime import datetime, timedelta
import pandas as pd
import requests_cache

#cache work install
#requests_cache.install_cache()

#Market id to call
### need to get input for ticker
MARKET_ID = "bitcoin"

#payload inputs are vs_currency(usd) and 
#days(Minutely data for duration within 1 day, Hourly data for duration between 1 day and 90 days, Daily data for duration above 90 days)
payload = {
    "vs_currency": "usd",
    "days": "max"
}

def main():
    r = getcoinprice(payload)
    #print(r.status_code)
    f_df = convert_to_df(r)
    print(f_df)
    print(f_df.loc[str(datetime.today().date() - timedelta(days=180))]["Price"].item())
    print(f_df.loc[str(datetime.today().date() - timedelta(days=30))]["Price"].item())
    print(f_df.loc[str(datetime.today().date() - timedelta(days=7))]["Price"].item())
    print(f_df.loc[str(datetime.today().date() - timedelta(days=1))]["Price"].item())
    #print(datetime.today().date() - timedelta(days=30))
    
def getcoinprice(payload):
    #Coingecko API => get coin price data for specific market id
    url = "https://api.coingecko.com/api/v3/coins/" + MARKET_ID + "/market_chart"
    payload["format"] = "json"
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        print(response.text)
    else:
        #print(response.json())
        return response
    
    #if it's not cached result, sleep 0.25 -> ~4 calls per second
    #if not getattr(response, 'from_cache', False):
    #   time.sleep(0.25)

def convert_to_df(response):
    #convert json to DataFrame and show prices only
    df = pd.DataFrame(response.json()["prices"])
    #change column names
    df.columns = ["Date", "Price"]
    #format price data to include commas
    df["Price"] = df["Price"].map("{0:,.0f}".format)
    #format date data from timestamp/epoch to datetime
    df["Date"] = pd.to_datetime(df["Date"], unit="ms")#.dt.date
    #drop second to last row with the most recent today data
    #df = df.drop(df.index[-2])
    #set date to index
    df = df.set_index(["Date"], inplace=False)
    #df.info()
    #df.describe()
    #print(type(df.index))
    #print(df.loc['2020-10-25'])
    
    return df

if __name__ == "__main__":
    main()


"""def jprint(obj):
    #create a formatted string of the Python JSON object
    textdata = json.dumps(obj, sort_keys=True, indent=4)
    print(textdata)
    
jprint(r.json())"""

