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


def get_last_fvg_arrays(data):
   row_number_candlestick_1 = 0
   fvg_top = None
   fvg_bottom = None
   fvg_arr_top = [None, None, None]
   fvg_arr_bottom = [None, None, None]


   rows = data.Open.shape[0]

   while row_number_candlestick_1 < rows:
      if row_number_candlestick_1  == rows - 3:  # Stop at the third-to-last index
         break
      row_number_candlestick_2 = row_number_candlestick_1 + 1
      row_number_candlestick_3 = row_number_candlestick_1 + 2

      if( data.High[row_number_candlestick_1] < data.Low[row_number_candlestick_3] + 0.01
          and data.Low[row_number_candlestick_2] < data.High[row_number_candlestick_2]
          #and data.Open[row_number_candlestick_2] < data.Close[row_number_candlestick_1]
          #and data.Close[row_number_candlestick_2] < data.Open[row_number_candlestick_3]
         ):
         fvg_top = data.Low[row_number_candlestick_3]
         fvg_bottom = data.High[row_number_candlestick_1]
      elif(fvg_top and data.Low[row_number_candlestick_3] <  fvg_top):
         fvg_top = None
         fvg_bottom = None
      fvg_arr_top.append(fvg_top)
      fvg_arr_bottom.append(fvg_bottom)
           
      row_number_candlestick_1 = row_number_candlestick_2

   return fvg_arr_top, fvg_arr_bottom


def get_last_fvg_top_array(data):
   arr = get_last_fvg_arrays(data)
   return arr[0]

def get_last_fvg_bottom_array(data):
   arr = get_last_fvg_arrays(data)
   return arr[1]


def get_swing_highs_arr(data):
    length_data = data.High.shape[0]
    last_swing_high = data.High[0]
    swing_high_arr = [last_swing_high]
    for i in range(1, length_data - 1 ):
        if( (data.High[i-1] <  data.High[i]) and
            ( data.High[i+1] < data.High[i] )
           ):
            last_swing_high = data.High[i]
        swing_high_arr.append(last_swing_high)
    swing_high_arr.append(last_swing_high)

    return swing_high_arr


def get_swing_lows_arr(data):
   length_data = data.Low.shape[0]
   last_swing_low = data.Low[0]
   swing_low_arr = [last_swing_low]
   for i in range(1, length_data - 1 ):
      if( (data.Low[i-1] >  data.Low[i]) and
            ( data.Low[i+1] > data.Low[i] )
         ):
         last_swing_low = data.Low[i]
      swing_low_arr.append(last_swing_low)
   swing_low_arr.append(last_swing_low)

   return swing_low_arr


def get_lows(data):
   length_data = data.Low.shape[0]
   lows = []
   for i in range(0, length_data ):
      lows.append( data.Low[i] )

   return lows

class MomentumStrategy(Strategy):

    def init(self):
        self.swing_highs = self.I(get_swing_highs_arr, self.data, color="blue")
        self.swing_lows = self.I(get_swing_lows_arr, self.data, color="yellow")
        self.last_fvg_arr_top = self.I(get_last_fvg_top_array, self.data, overlay=True, color='red')
        self.last_fvg_arr_bottom = self.I(get_last_fvg_bottom_array, self.data, overlay=True, color='red')
   
        self.lows = self.I(get_lows, self.data, overlay=False)

         
    def next(self):
        last_fvg = self.last_fvg_arr_top[-1]

        if(last_fvg
           and self.lows[-1] < last_fvg
           and self.lows[-1] >= self.last_fvg_arr_bottom[-1]):
           try:
              self.buy(sl=self.swing_lows[-1], tp=self.swing_highs[-1], limit=last_fvg, stop=last_fvg-1) #in a try/catch be cause in many cases swing low is greater than price backtesting.py is trying to buy at)
           except:
              print("EXCEPTED")
              self.swing_lows[-1]
               
              pass
 

import pdb


price_data = GOOG.truncate(before=pd.Timestamp("2010-01-28"), after=pd.Timestamp("2011-05-05"))


bt = Backtest(price_data, MomentumStrategy , cash=10_000)

results = bt.run()
print(results._strategy)
bt.plot()
