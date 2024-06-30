from stock_data import getAllDataToCSV, coins

import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import date, timedelta

# getAllDataToCSV()
algorithms = [
  {'label': 'LSTM', 'value': 'lstm'},
  {'label': 'RNN', 'value': 'rnn'},
  {'label': 'XGBoost', 'value': 'xgboost'},
]


# initialize
app = dash.Dash()
server = app.server

# implement ui
app.layout = html.Div(
	style={'font-family': 'Arial'},
	children=[
    #header
    html.Div(
              children=[
								html.Span("Stock Price Analysis"),
                html.Span("Team 3")
              ],
              style={
                  'display': 'flex',
									'justify-content': 'space-between',
                  'backgroundColor': 'black',
                  'color': 'white',
                  'padding': '12px 20px',
                  'textAlign': 'center',
									'fontWeight': 'bold'
              }
          ),

    # tool bar
		html.Div(
      style={'padding': '12px 20px',},
			children=[
				html.Div(
        style={"display": "flex", "gap": "20px", "align-items": "center"},
        children=[
            dcc.Dropdown(
                id='coin-dropdown',
                options=coins, 
                value='BTC-USD', 
                clearable=False,
                style={"width": "200px"}),
            dcc.Dropdown(
                id='algorithm-dropdown',
                options=algorithms,
                value='lstm',
                clearable=False,
                style={"width": "200px"}),

            html.H5("Start Date:",style={"margin-left": "20px"}),
            dcc.DatePickerSingle(
                id='start-date',
                min_date_allowed=date(2018, 1, 1),
                max_date_allowed=date.today(),
                initial_visible_month=date(2020, 1, 1),
                date=date.today() - timedelta(days=365*5),
                clearable=False,
                display_format="DD/MM/YYYY",
                day_size=30
            ),

            html.H5("End Date:"),
            dcc.DatePickerSingle(
                id='end-date',
                min_date_allowed=date(2018, 1, 1),
                max_date_allowed=date.today(),
                initial_visible_month=date.today(),
                date=date.today(),
                clearable=False,
                display_format="DD/MM/YYYY",
                day_size=30
            ),
        ]),
        dcc.Dropdown(
            placeholder='Select attributes',
            multi=True,
            id='price-type-dropdown',
            options=[
                {'label': 'Open Price', 'value': 'Open'},
                {'label': 'Close Price', 'value': 'Close'},
                {'label': 'Low Price', 'value': 'Low'},
                {'label': 'High Price', 'value': 'High'},
                {'label': 'ROC', 'value': 'ROC'},
            ],
            value='Open',
            clearable=False,
						style={"width": "auto", 'min-width': '200px'}
            ),
      ]
    ),

    # title
    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "left", "margin": "20px"}),

])


# start app
if __name__=='__main__':
	app.run_server(debug=True)
