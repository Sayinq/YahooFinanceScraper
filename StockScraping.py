import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import ta
import plotly.graph_objs as go
import plotly.offline as pyo

#Target stock(s)
#Expand, post multiple?
APPLE = yf.Ticker("AAPL") 

#Date parameters that we want to see in our plot
start_date = '2021-02-02'
end_date = '2022-01-01'

#Finding the history within our date parameters we set.
stockpanel = APPLE.history(start=start_date, end=end_date)

#Plotting it (Line Chart)
#Try to make interactable in some way? 

#rsi = ta.momentum.RSIIndicator(close=stockpanel['Close'])
#stockpanel['RSI'] = rsi.rsi()
#stockpanel[['Close', 'RSI']].plot(figsize=(10,5))
#plt.title("Apple Inc. Stock Price")
#plt.ylabel("Closing Price")
#plt.xlabel("Date")
#plt.show()

#Candle Stick Plot
#Hoverable with active scrolling for close detail.
#Trying to make this possibly realtime?
trace = go.Candlestick(x=stockpanel.index,
                        open=stockpanel['Open'],
                        high=stockpanel['High'],
                        low=stockpanel['Low'],
                        close=stockpanel['Close'])
                        
data = [trace]

layout = go.Layout(title='Apple Inc. Stock Price (Candlestick)', 
                    xaxis=dict(title='Date'),
                    yaxis=dict(title='Closing Price'),
                    hovermode='x')

fig = go.Figure(data=data, layout=layout)
fig.show()

#print(stock_df.head())