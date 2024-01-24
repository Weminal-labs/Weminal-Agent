
import pandas as pd
import time
import os
import datetime
import numpy as np
import requests
import json
import pickle 
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from Oraidex_models.config import Config
from secret import load_secrets


from Oraidex_models.Finanace import  getRSI
load_secrets()
config = Config()


class OraidexSceener():
    def __init__(self, verbose=False):
        self.screener_df = None
        self.verbose = verbose
        self.startime = "1701166429"
        self.endtime =  int(datetime.datetime.now().timestamp())        
        self.timeframe = "3600" # 1h: 3600 4h: 14400 1d: 86400 1w: 604800 1m: 2592000 1y: 31536000

        screener_df_path = "./datasets/" + self.timeframe + ".pickle"
        if os.path.exists(screener_df_path):
            self.screener_df = pickle.load(open(screener_df_path, "rb"))
            self.screener_df = self.fetch_for_all_symbols()
            print("loading")
        else:
            self.screener_df = self.fetch_for_all_symbols()
            self.screener_df.to_pickle(screener_df_path)

            # self.screener_df = self.fetch_for_all_symbols()
            # self.screener_df.to_pickle(screener_df_path)
            # if the screener_df doesn't exist, then we need to get all the symbols
            print(screener_df_path, "does not exist, so we will get all symbols")
               
        self.screener_df = self.fetch_for_all_symbols()
        self.screener_df.to_pickle(screener_df_path)
        
        self.custom_prefix = "You are weminal AI created by wechainlabs. You give insights cryptos from Oraidex of Oraichain"
        self.custom_suffix = "You also give that what user can use in this chat."
        print(self.screener_df)
        #initialize the internal agent
        self.agent = create_pandas_dataframe_agent(
                ChatOpenAI(model_name='gpt-3.5-turbo-1106', temperature=0),
                self.screener_df,
                max_iterations=4,
                verbose=True,
                handle_parsing_errors=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,

            )
        
    def fetch_for_all_symbols(self):
        url = "https://price.market.orai.io/simple/price?ids=airight%2Coraichain-token%2Coraidex%2CAtom&vs_currencies=usd"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        symbols = list(response.keys())
        all_date_frame = pd.DataFrame()


        for symbol in symbols: 
           
            pair_contract = config.get_symbol_address(symbol)
            #test_df = self.fetch_specific_symbol(pair_contract)  
            #test_df['symbol'] = symbol
        
            open, close, high, low, returns, average_daily_volume = self.fetch_specific_symbol(pair_contract)  

            high_20_week = np.max(high[-20 * 5 * 8:])
            low_20_week = np.min(low[-20 * 5 * 8:])
        
            # get 14 week high and low
            high_14_week = np.max(high[-14 * 5 * 8:])
            low_14_week = np.min(low[-14 * 5 * 8:])

            # get current percent change from 26 week high
            pct_from_20_week_high = (close[-1] - high_20_week) / high_20_week
            # get current percent change from 26 week low
            pct_from_20_week_low = (close[-1] - low_20_week) / low_20_week
            # get current percent change from 13 week high
            pct_from_14_week_high = (close[-1] - high_14_week) / high_14_week
            # get current percent change from 13 week low
            pct_from_14_week_low = (close[-1] - low_14_week) / low_14_week

            short_term_volatility = np.std(close[-13 * 5 * 8:])
            medium_term_volatility = np.std(close[-26 * 5 * 8:])
            long_term_volatility = np.std(close[-52 * 5 * 8:])


            # get some moving averages at different time scales
            # 5 day
            ma_5_day = np.mean(close[-5 * 5 * 8:])
            # 10 day
            ma_10_day = np.mean(close[-10 * 5 * 8:])
            # 20 day
            ma_20_day = np.mean(close[-20 * 5 * 8:])
            # 50 day
            ma_50_day = np.mean(close[-50 * 5 * 8:])
            # 100 day
            ma_100_day = np.mean(close[-100 * 5 * 8:])

            # get current percent change from 100 day moving average
            pct_from_100_day_ma = (close[-1] - ma_100_day) / ma_100_day
            # get current percent change from 50 day moving average
            pct_from_50_day_ma = (close[-1] - ma_50_day) / ma_50_day
            # get current percent change from 20 day moving average
            pct_from_20_day_ma = (close[-1] - ma_20_day) / ma_20_day
            # get current percent change from 10 day moving average
            pct_from_10_day_ma = (close[-1] - ma_10_day) / ma_10_day
            # get current percent change from 5 day moving average
            pct_from_5_day_ma = (close[-1] - ma_5_day) / ma_5_day

            # get 14 day RSI (last value only)
            rsi = getRSI(close, n=14)[0]

            new_row = pd.DataFrame([{"symbol":symbol,
                                    "last_updated":datetime.datetime.now(),
                                    "current_price": close[0],
                                    "high_20_week": high_20_week,
                                    "low_20_week": low_20_week,
                                    "high_14_week": high_14_week,
                                    "low_14_week": low_14_week,
                                    "short_term_volatility": short_term_volatility,
                                     "medium_term_volatility": medium_term_volatility,
                                     "long_term_volatility": long_term_volatility, "ma_5_day": ma_5_day,
                                     "ma_10_day": ma_10_day, "ma_20_day": ma_20_day, "ma_50_day": ma_50_day,
                                     "ma_100_day": ma_100_day, 
                                     "pct_from_20_week_high": pct_from_20_week_high,
                                     "pct_from_20_week_low": pct_from_20_week_low,
                                     "pct_from_14_week_high": pct_from_14_week_high,
                                     "pct_from_14_week_low": pct_from_14_week_low,
                                     "pct_from_100_day_ma": pct_from_100_day_ma,
                                     "pct_from_50_day_ma": pct_from_50_day_ma,
                                     "pct_from_20_day_ma": pct_from_20_day_ma,
                                     "pct_from_10_day_ma": pct_from_10_day_ma,
                                     "pct_from_5_day_ma": pct_from_5_day_ma,
                                     "rsi_14": rsi, "beta": "asd", "avg_daily_volume": average_daily_volume}])
                                    
           
           
           
        
            all_date_frame = pd.concat([all_date_frame, new_row], ignore_index=True)

        return all_date_frame
           

        
    def fetch_specific_symbol(self, url_pair):
        """
        Fetches specific symbol data from the Oraidex API.

        Args:
            url_pair (str): The symbol pair to fetch data for.

        Returns:
            dataframe: The response as a dataframe.
        """
        url = "https://api.oraidex.io/v1/candles?pair=" + url_pair + "&startTime=" + str(self.startime) + "&endTime=" + str(self.endtime) + "&tf=" + self.timeframe
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        
        # json data to dataframe
        data_dump = json.dumps({"data":response})
        data = json.loads(data_dump)
    
        return self.format_data(data)
    

    def format_data(self, data):
        df = pd.DataFrame(data['data'])
        df['time'] = df['time'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)))
       
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values(by='time', ascending=False)
        
        open= df.open.values
        close = df.close.values
        high = df.high.values
        low = df.low.values
        returns = (close - open) / open


        #  Calculate daily volumes
        daily_volumes = df.groupby('time')['volume'].sum()

        # Calculate average daily volume
        average_daily_volume = daily_volumes.mean()

        return open, close, high, low, returns, average_daily_volume
    
    def run(self, query):
        safety = "Ensure that valid json is used with internal tools and functions. Also, outputs should be in well formatted JSON." \
        "You have to give number output price, date if it relevant." 
        return self.agent.run("Please use this natural prompt: " + query + " " + safety)





