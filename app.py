from trading_data import getTradeData, getTradeDataByMinute

import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import date, timedelta
import pandas as pd

# getAllDataToCSV()
algorithms = [
  {'label': 'LSTM', 'value': 'lstm'},
  {'label': 'RNN', 'value': 'rnn'},
  {'label': 'XGBoost', 'value': 'xgboost'},
]
coins = ["BTC-USD", "ETH-USD",
     "BNB-USD", "ADA-USD", "XRP-USD",
     "SOL-USD", "DOT-USD", "DOGE-USD", "SHIB-USD", "LTC-USD"
      ]
day_number = [10, 20, 30, 60, 120]

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
                html.Span("Trading Price Analysis"),
                html.Span("Team 3")
              ],
              style={
                  'display': 'flex',
                  'justifyContent': 'space-between',
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

            html.H5("Number of days:",style={"marginLeft": "20px"}),
            dcc.Dropdown(
                id='day-number',
                options=day_number,
                value=60,
                clearable=False,
                style={"width": "200px"},
            ),
        ]),
        dcc.Dropdown(
            placeholder='Select attributes',
            multi=True,
            id='price-type-dropdown',
            options=[
                # {'label': 'Open Price', 'value': 'Open'},
                {'label': 'Close Price', 'value': 'Close'},
                # {'label': 'Low Price', 'value': 'Low'},
                # {'label': 'High Price', 'value': 'High'},
                {'label': 'ROC', 'value': 'ROC'},
            ],
            value=['Close', 'ROC'],
            clearable=False,
						style={"width": "auto", 'min-width': '200px'}
            ),
      ]
    ),

    # title
    html.H1("Trading Price Analysis Dashboard", style={"textAlign": "left", "margin": "20px"}),
    # graph presentation
    html.Div(
        children = [
            # dcc.Loading(
                dcc.Graph(
                    id='candlestick-graph',
                )
            # ),
        ],
        style={"border": "solid 1px gray", "marginTop": "10px"}  
    ),
	dcc.Interval(id='interval-component', 
                 interval=2 * 1000, 
                 n_intervals=0)
])

# TRADING PRICE
@app.callback(
    Output('candlestick-graph', 'figure'),
    [
        Input('coin-dropdown', 'value'),
        Input('algorithm-dropdown', 'value'),
        Input('price-type-dropdown', 'value'),
        Input('day-number', 'value'),
		Input('interval-component', 'n_intervals')
    ]
)
def update_trading_price_graph(coin, algorithm, price_type, day_number, n_intervals):
    # Đọc dữ liệu dựa trên coin được chọn theo ngày
    df = getTradeData(coin, date.today() - timedelta(day_number), date.today())
    new_row = getTradeDataByMinute(coin)

    df['Date'] = df.index
    new_row['Date'] = new_row.index

    df['Date'] = df['Date'].apply(lambda x: x.date())
    new_row['Date'] = new_row['Date']

    if df['Date'].max() != new_row['Date'].max():
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df.iloc[-1] = new_row

    # Tạo biểu đồ nến
    figure = go.Figure(data=[
			go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Trading Price'
			),
		])
    # Thêm dự đoán vào biểu đồ
    addPredictCandle(figure, df['Date'].max() + timedelta(1))

    figure.update_layout(
        title=f'Trading Price Analysis ({coin})',
        yaxis_title='Trading Price (USD)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )

    return figure

def addPredictCandle(figure, date):
	# Thêm cây nến mới với màu sắc khác (ví dụ: màu xanh dương)
	new_candle = go.Candlestick(
			x=[date],  # Ngày của cây nến mới
			open=[63000.00],  # Giá mở cửa của cây nến mới
			high=[68000.00],  # Giá cao nhất của cây nến mới
			low=[61000.00],  # Giá thấp nhất của cây nến mới
			close=[67500.00],  # Giá đóng cửa của cây nến mới
			increasing=dict(line=dict(color='blue')),
			decreasing=dict(line=dict(color='yellow')),
			name='Predicted Trading Price'
	)

	figure.add_trace(new_candle)



# start app
if __name__=='__main__':
	app.run_server(debug=True)
