import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import ta
import plotly.graph_objs as go
import plotly.offline as pyo
from ta.utils import dropna
from ta.volatility import BollingerBands
from plotly.subplots import make_subplots
from plotly.io import write_html
import webbrowser
import plotly.graph_objs as go
import mplfinance as mpf

#Target stock(s)
#Expand, post multiple?
StockTicker = ''
stock = yf.Ticker(input("Which stock ticker would you like to analyze?: ")) 
StockTicker = stock.info['shortName'] #User input test
    #Date parameters that we want to see in our plot
start_date = '2021-02-02'
end_date = '2022-01-01'
stockpanel = stock.history(start=start_date, end=end_date) #Displaying within date range

#Plotting it (Line Chart)
#Try to make interactable in some way? 
#rsi = ta.momentum.RSIIndicator(close=stockpanel['Close'])
#stockpanel['RSI'] = rsi.rsi()
#stockpanel[['Close', 'RSI']].plot(figsize=(10,5))
#plt.title("Apple Inc. Stock Price")
#plt.ylabel("Closing Price")
#plt.xlabel("Date")
#plt.show()

#Using 'ta' Library so I can grab trend indicators for Bollinger Bands
stockpanel['MA'] = ta.trend.sma_indicator(stockpanel['Close'])
stockpanel['STD'] = stockpanel['Close'].rolling(window=10).std()
stockpanel['Upper Band'] = stockpanel['MA'] + 2 * stockpanel['STD']
stockpanel['Lower Band'] = stockpanel['MA'] - 2 * stockpanel['STD']

#Using 'ta' library to implement a MACD line (Moving Average Convergence/Divergence Indicator)
macd_diff = ta.trend.macd_diff(stockpanel['Close'], window_fast=20, window_slow=100)
macd_signal = ta.trend.macd_signal(stockpanel['Close'])
stockpanel['MACD'] = macd_diff
stockpanel['MACD_Signal'] = macd_signal

#Using 'ta' library to implement a MACD line (Moving Average Convergence/Divergence Indicator)


#Using 'ta' library to set Heiken Ashi values
def heiken_ashi(ha):
    ha = ha.copy()
    ha['HA_Open'] = (ha['Open'] + ha['Close']) / 2
    ha['HA_High'] = ha[['High', 'HA_Open']].max(axis=1)
    ha['HA_Low'] = ha[['Low', 'HA_Open']].min(axis=1)
    ha['HA_Close'] = (ha['HA_Open'] + ha['HA_High'] + ha['HA_Low'] + ha['Close']) / 4
    return ha
stockpanel = heiken_ashi(stockpanel)

#Heiken Aishi Candlestick Chart
HeikenAishi = go.Candlestick(x=stockpanel.index,
                            open=stockpanel['HA_Open'],
                            high=stockpanel['HA_High'],
                            low=stockpanel['HA_Low'],
                            close=stockpanel['HA_Close'],
                            name= StockTicker)
#Candle Stick Plot
#Candlestick = go.Candlestick(x=stockpanel.index,
#                    open=stockpanel['Open'],
#                    high=stockpanel['High'],
#                    low=stockpanel['Low'],
#                    close=stockpanel['Close'],
#                    name= StockTicker)
#Tracing variables for our Upper Band and Lower Band, in which case we made green for visibility testing
UpperBoll = go.Scatter(x = stockpanel.index,
                    y=stockpanel['Upper Band'],
                    name= 'Upper Band',
                    line=dict(color="Grey"))

LowerBoll = go.Scatter(x = stockpanel.index,
                    y=stockpanel['Lower Band'],
                    name= 'Lower Band',
                    line=dict(color="Grey"))
#Tracing variables for MACD
MACD = go.Scatter(x=stockpanel.index, y=stockpanel['MACD'],
                name='MACD',
                line=dict(color='blue'))
Signal = go.Scatter(x=stockpanel.index, y=stockpanel['Signal'],
                name='Signal',
                line=dict(color='yellow'),
                row=2, col=1)
                
#Data that's being pulled, as well as Indicators
data = [HeikenAishi, UpperBoll, LowerBoll]

#More layout functionality, cleaner look
#Title scrolling with scrubber 
fig = make_subplots(rows=1, cols=1)
fig.add_trace(HeikenAishi)
fig.add_trace(UpperBoll)
fig.add_trace(LowerBoll)
fig.add_trace(MACD)
fig.add_trace(Signal)
fig.update_layout(xaxis_rangeslider_visible=True)
with open("Candlestick.html", "w", encoding="utf-8") as f:
    fig.write_html(f, auto_open=True)
webbrowser.open("Candlestick.html")