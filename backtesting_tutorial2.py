from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import pdb


# def find_fvg(candle_open,candle_close):
#     print("in find_fvg")
#     print(candle_open)

def find_fvg(o, c, i):
    row_number_candlestick_1 = 0
    fvg_top = None
    fvg_arr = [None, None, None]
    aa = c - o
    print(aa)
    # for index, row in df.iterrows():
    #     if row_number_candlestick_1  == len(df) - 3:  # Stop at the second-to-last index
    #         break
    #     row_number_candlestick_2 = row_number_candlestick_1 + 1
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
    return True
    #return aa
    

class FvgTrade(Strategy):
    n1 = 10
    n2 = 20

    n = 0

    row_number_candlestick_1 = 0
    fvg_top = None
    fvg_arr = [None, None, None]

    def init(self): 
        self.candle_close = self.data.Close
        self.candle_open = self.data.Open
        self.fvg = self.I(find_fvg, self.data.Open,self.data.Close, self.data.index)
        
    def next(self):
        pdb.set_trace()
        if(self.fvg):
            self.buy()
        
        
        #self.buy()
        
       # print("Current index:", current_index)

        #if row_number_candlestick_1  == len(df) - 3:  # Stop at the second-to-last index
        #    break
        
        #row_number_candlestick_2 = self.row_number_candlestick_1 + 1
        #row_number_candlestick_3 = self.row_number_candlestick_1 + 2

        #print( row_number_candlestick_3 )

        
        # if( df.iloc[row_number_candlestick_1]['h'] < df.iloc[row_number_candlestick_3]['l'] + 0.01
        #     and df.iloc[row_number_candlestick_2]['o'] <  df.iloc[row_number_candlestick_1]['c']
        #     and df.iloc[row_number_candlestick_2]['c'] <  df.iloc[row_number_candlestick_3]['o']
        #    ):
        #     fvg_top = df.iloc[row_number_candlestick_3]['l']
        #     fvg_arr.append(fvg_top)
        # else:
        #     fvg_arr.append(None)
        #     row_number_candlestick_1 = row_number_candlestick_2


bt = Backtest(GOOG, FvgTrade,
              cash=10000, commission=.002, 
              exclusive_orders=True)

output = bt.run()
bt.plot()



# def find_fvg(df):
#     row_number_candlestick_1 = 0
#     fvg_top = None
#     fvg_arr = [None, None, None]
#     for index, row in df.iterrows():
#         if row_number_candlestick_1  == len(df) - 3:  # Stop at the second-to-last index
#             break
#         row_number_candlestick_2 = row_number_candlestick_1 + 1
#         row_number_candlestick_3 = row_number_candlestick_1 + 2
#         if( df.iloc[row_number_candlestick_1]['h'] < df.iloc[row_number_candlestick_3]['l'] + 0.01
#             and df.iloc[row_number_candlestick_2]['o'] <  df.iloc[row_number_candlestick_1]['c']
#             and df.iloc[row_number_candlestick_2]['c'] <  df.iloc[row_number_candlestick_3]['o']
#            ):
#             fvg_top = df.iloc[row_number_candlestick_3]['l']
#             fvg_arr.append(fvg_top)
#         else:
#             fvg_arr.append(None)
#         row_number_candlestick_1 = row_number_candlestick_2
#     df['fvg_top'] = fvg_arr
#     return df


#pdb.set_trace()
