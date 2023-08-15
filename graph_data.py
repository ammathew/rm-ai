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

from fvg_detector import find_fvg

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Input(id='input-component', type='text', value=''),
    dcc.Dropdown(
        id='dropdown-component',
        options=[
            {'label': 'Option 1', 'value': 'option1'},
            {'label': 'Option 2', 'value': 'option2'},
            {'label': 'Option 3', 'value': 'option3'}
        ],
        value='option1'
    ),
    dcc.Graph(id='candlestick-chart'),
])



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

df = find_fvg(df)

print("this is df")
print(df)

@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('input-component', 'value'), Input('dropdown-component', 'value')]  # Inputs that trigger the callback

)
def update_candlestick_chart(input_value, dropdown_value):
    print("callback called")
    figure = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['o'],
        high=df['h'],
        low=df['l'],
        close=df['c']
    )])
    figure.update_layout(
        title=f'Candlestick Chart for TQQQ',
        xaxis_title='Date',
        yaxis_title='Price',
    )
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)




