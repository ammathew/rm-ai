from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover


import fvg_detector
import pandas as pd
import numpy as np

from bokeh.models.tools import Toolbar


# Generate some sample price data
np.random.seed(42)
#dates = pd.date_range(start='2022-01-01', end='2023-01-01', freq='D')
#data = pd.DataFrame({'Date': dates, 'Price': prices})
#data.set_index('Date', inplace=True)

import talib


import pdb

def indicator(data):
   return data.Close.s.pct_change(periods=7) * 100

def find_fvg(data):
    row_number_candlestick_1 = 0
    fvg_top = None
    fvg_arr = [None, None, None]

    rows = data.Open.shape[0]

    while row_number_candlestick_1 < rows:
        if row_number_candlestick_1  == rows - 3:  # Stop at the third-to-last index
            break
        row_number_candlestick_2 = row_number_candlestick_1 + 1
        row_number_candlestick_3 = row_number_candlestick_1 + 2

        if( data.Close[row_number_candlestick_1] < data.Low[row_number_candlestick_3] + 0.01
            and data.Open[row_number_candlestick_2] <  data.Close[row_number_candlestick_1]
            and data.Close[row_number_candlestick_2] <  data.Open[row_number_candlestick_3]
           ):
            fvg_top = data.Low[row_number_candlestick_3]
            fvg_arr.append(fvg_top)
        else:
            fvg_arr.append(0)
        row_number_candlestick_1 = row_number_candlestick_2

    #pdb.set_trace()
    return fvg_arr
        
    
    #if( df.iloc[row_number_candlestick_1]['h'] < df.iloc[row_number_candlestick_3]['l'] + 0.01
    
    # for index, row in df.iterrows():
    #     if row_number_candlestick_1  == len(df) - 3:  # Stop at the second-to-last index
    #         break
    #     row_number_candlestick_2 = row_number_candlestick_1 + 1d
    #     row_number_candlestick_3 = row_number_candlestick_1 + 2
    #     if( df.iloc[row_number_candlestick_1]['h'] < df.iloc[row_number_candlestick_3]['l'] + 0.01
    #         and df.iloc[row_number_candlestick_2]['o'] <  df.iloc[row_number_candlestick_1]['c']
    #         and df.iloc[row_number_candlestick_2]['c'] <  df.iloc[row_number_candlestick_3]['o']
    #        ):
    #         fvg_top = df.iloc[row_number_candlestick_3]['l']
    #         fvg_arr.append(fvg_top)
    #     else:
    #         fvg_arr.append(None)
    #     row_number_candlestick_1 = row_number_candlestick_2
    # df['fvg_top'] = fvg_arr
    # return df

class MomentumStrategy(Strategy):

    def init(self):
        self.find_fvg = self.I(find_fvg, self.data)
        print("THIS IS FVG")
        print(self.find_fvg)
         
    def next(self):
        is_fvg = self.find_fvg[-1]
        if(is_fvg):
            if(self.position):
                self.position.close()
            self.buy()
            print("bought!")
        else:
            print("not bought")





bt = Backtest(GOOG, MomentumStrategy , cash=10_000)
results = bt.run()
#print(results)
import pdb
#pdb.set_trace()
bt.plot()
