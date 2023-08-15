import json
import mplfinance as mpf
import pandas as pd

file_path = "data.txt"
import pdb


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import requests




def get_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # Load JSON data from the file
            #print(data)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



data = get_data(file_path)


df = pd.DataFrame(data['results'])
df['t'] = pd.to_datetime(df['t'], unit='ms')
df.set_index('t',inplace=True)



#pdb.set_trace()


def find_fvg(df):
    row_number_candlestick_1 = 0
    fvg_top = None
    fvg_arr = [None, None, None]
    for index, row in df.iterrows():
        if row_number_candlestick_1  == len(df) - 3:  # Stop at the second-to-last index
            break
        row_number_candlestick_2 = row_number_candlestick_1 + 1
        row_number_candlestick_3 = row_number_candlestick_1 + 2
        if( df.iloc[row_number_candlestick_1]['h'] < df.iloc[row_number_candlestick_3]['l'] + 0.01):
            fvg_top = df.iloc[row_number_candlestick_3]['l']
            fvg_arr.append(fvg_top)
        else:
            fvg_arr.append(None)
        row_number_candlestick_1 = row_number_candlestick_2
    df['fvg_top'] = fvg_arr
    return df

#df = find_fvg(df)

#print(df)
