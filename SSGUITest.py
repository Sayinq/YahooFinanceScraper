import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import ta
import plotly.graph_objs as go
import plotly.offline as pyo
import tkinter as tk
from tkinter import ttk
APPLE = yf.Ticker("AAPL")

#Date parameters that we want to see in our plot
start_date = '2021-02-02'
end_date = '2022-01-01'

#Finding the history within our date parameters we set.
stockpanel = APPLE.history(start=start_date, end=end_date)

def open_line_chart():
    fig, ax = plt.subplots(figsize=(10,5))
    stockpanel[['Close', 'RSI']].plot(ax=ax)
    ax.set_title("Apple Inc. Stock Price")
    ax.set_ylabel("Closing Price")
    ax.set_xlabel("Date")
    plt.show()

def open_candlestick_chart():
    trace = go.Candlestick(x=stockpanel.index,
                       open=stockpanel['Open'],
                       high=stockpanel['High'],
                       low=stockpanel['Low'],
                       close=stockpanel['Close'])
    data = [trace]
    layout = go.Layout(title='Apple Inc. Stock Price (Candlestick)',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Closing Price'))
    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename='candlestick-chart.html',auto_open=True, show_link=False)

root = tk.Tk()
root.title("Stock Chart")

line_chart_button = ttk.Button(root, text = "Line Chart", command = open_line_chart)
line_chart_button.pack()

candlestick_chart_button = ttk.Button(root, text = "Candlestick Chart", command = open_candlestick_chart)
candlestick_chart_button.pack()

root.mainloop()
