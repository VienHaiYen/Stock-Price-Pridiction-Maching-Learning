import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import date, timedelta
from trading_data import getDataFromCoin
from constant import coin_labels, algorithms, timeframes, day_number, windowSize
import pandas as pd
from model.factory import ModelPredictServiceFactory
from model.utils import ROCCalculator

# initialize
app = dash.Dash()
server = app.server

# implement ui
app.layout = html.Div(
    style={"font-family": "Arial"},
    children=[
        # header
        html.Div(
            children=[html.Span("Trading Price Analysis"), html.Span("Team 3")],
            className="header",
        ),
        # tool bar
        html.Div(
            style={
                "padding": "12px 20px",
            },
            children=[
                html.Div(
                    style={"display": "flex", "gap": "20px", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            id="coin-dropdown",
                            options=coin_labels,
                            value=coin_labels[0]['value'],
                            clearable=False,
                            style={"width": "200px"},
                        ),
                        dcc.Dropdown(
                            id="algorithm-dropdown",
                            options=algorithms,
                            value=algorithms[0]['value'],
                            clearable=False,
                            style={"width": "200px"},
                        ),
                        html.H5("Timeframe:", style={"marginLeft": "20px"}),
                        dcc.Dropdown(
                            id="timeframe",
                            options=list(timeframes.values()),
                            value=list(timeframes.values())[0]['value'],
                            clearable=False,
                            style={"width": "200px"},
                        ),
                        html.H5("Number of timeframe:", style={"marginLeft": "20px"}),
                        dcc.Dropdown(
                            id="day-number",
                            options=day_number,
                            value=day_number[0],
                            clearable=False,
                            style={"width": "200px"},
                        ),
                    ],
                ),
                dcc.Dropdown(
                    placeholder="Select attributes",
                    multi=True,
                    id="feature-dropdown",
                    options=[
                        {"label": "Close Price", "value": "close"},
                        {"label": "ROC", "value": "ROC"},
                    ],
                    value=["close", "ROC"],
                    clearable=False,
                    style={"width": "auto", "width": "250px"},
                ),
            ],
        ),
        # title
        html.H1(
            "Trading Price Analysis Dashboard",
            style={"textAlign": "left", "margin": "20px"},
        ),
        # graph presentation
        html.Div(
            children=[
                # dcc.Loading(
                dcc.Graph(
                    id="candlestick-graph",
                )
                # ),
            ],
            style={"border": "solid 1px gray", "marginTop": "10px"},
        ),
        dcc.Interval(id="interval-component", interval=2 * 1000, n_intervals=0),
    ],
)


# TRADING PRICE
@app.callback(
    Output("candlestick-graph", "figure"),
    [
        Input("coin-dropdown", "value"),
        Input("algorithm-dropdown", "value"),
        Input("feature-dropdown", "value"),
        Input("day-number", "value"),
        Input("timeframe", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_trading_price_graph(
    coin, algorithm, features, day_number, timeframe, n_intervals
):
    # GET dữ liệu dựa trên coin được chọn theo ngày
    df = getDataFromCoin(coin, timeframe, day_number)
    # Tạo biểu đồ nến
    figure = go.Figure(
                data = [
                    go.Candlestick(
                        x = df.timestamp,
                        open = df.open,
                        high = df.high,
                        low = df.low,
                        close = df.close,
                        name='Trading Price'
                        )])
    # Thêm dự đoán vào biểu đồ
    if timeframe == timeframes["day"]["value"] and day_number >= windowSize:
        df['ROC'] = ROCCalculator().fromClose(df['close'])
        predictService = ModelPredictServiceFactory.getModelPredictService(
            modelName=algorithm, features=features, coin=coin
        )
        prediction = predictService.execute(df)
        addPredictCandle(figure, df.timestamp.max() + timedelta(1), prediction)

    figure.update_layout(
        title=f"Trading Price Analysis ({coin})",
        yaxis_title="Trading Price (USD)",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False,
    )

    return figure


def addPredictCandle(figure, date, candel_df: pd.DataFrame):
    # Thêm cây nến mới với màu sắc khác (ví dụ: màu xanh dương)
    new_candle = go.Candlestick(
        x=[date],  # Ngày của cây nến mới
        open=candel_df["open"],  # Giá mở cửa của cây nến mới
        high=candel_df["high"],  # Giá cao nhất của cây nến mới
        low=candel_df["low"],  # Giá thấp nhất của cây nến mới
        close=candel_df["close"],  # Giá đóng cửa của cây nến mới
        increasing=dict(line=dict(color="blue")),
        decreasing=dict(line=dict(color="yellow")),
        name="Predicted Trading Price",
    )

    figure.add_trace(new_candle)


# start app
if __name__ == "__main__":
    app.run_server(debug=True)
