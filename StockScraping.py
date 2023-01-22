import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import ta
import plotly.graph_objs as go
import plotly.offline as pyo
from ta.utils import dropna
from ta.volatility import BollingerBands

#Target stock(s)
#Expand, post multiple?
APPLE = yf.Ticker("AAPL") 

#Date parameters that we want to see in our plot
start_date = '2021-02-02'
end_date = '2022-01-01'

#Finding the history within our date parameters we set.
StockTicker = APPLE.info['shortName'] #User input test
stockpanel = APPLE.history(start=start_date, end=end_date)
Cleaning = dropna(stockpanel) #Cleaning possible NaN values (ew)


#Plotting it (Line Chart)
#Try to make interactable in some way? 

#rsi = ta.momentum.RSIIndicator(close=stockpanel['Close'])
#stockpanel['RSI'] = rsi.rsi()
#stockpanel[['Close', 'RSI']].plot(figsize=(10,5))
#plt.title("Apple Inc. Stock Price")
#plt.ylabel("Closing Price")
#plt.xlabel("Date")
#plt.show()

#Using 'ta' Library so I can grab trend indicators
stockpanel['MA'] = ta.trend.sma_indicator(stockpanel['Close'])
stockpanel['STD'] = stockpanel['Close'].rolling(window=20).std()
stockpanel['Upper Band'] = stockpanel['MA'] + 2*stockpanel['STD']
stockpanel['Lower Band'] = stockpanel['MA'] - 2*stockpanel['STD']

#Candle Stick Plot
#Setting traces for bollinger bands
#Trying to make this possibly realtime?
Candlestick = go.Candlestick(x=stockpanel.index,
                    open=stockpanel['Open'],
                    high=stockpanel['High'],
                    low=stockpanel['Low'],
                    close=stockpanel['Close'],
                    name= StockTicker)
#Tracing variables for our Upper Band and Lower Band, in which case we made green for visibility testing
trace2 = go.Scatter(x = stockpanel.index,
                    y=stockpanel['Upper Band'],
                    name= 'Upper Band',
                    line=dict(color="Green"))

trace3 = go.Scatter(x = stockpanel.index,
                    y=stockpanel['Lower Band'],
                    name= 'Lower Band',
                    line=dict(color="Green"))
                        
data = [Candlestick, trace2, trace3]

#More layout functionality, cleaner look
#Title scrolling with scrubber 
layout = go.Layout(title=f'{StockTicker} Stock Ticker', 
                    xaxis=dict(title='Date'),
                    yaxis=dict(title='Closing Price'),
                    hovermode='x',
                    annotations=[dict(text='Bollinger Bands Analysis', #Subtitle for chart
                    x=0.5, y=1.05, xref='paper', yref='paper', showarrow=False, align ='center')]
)
#Making our Data scrubber smaller
layout = go.Layout(title=f'{StockTicker} Stock Ticker',
                    xaxis=dict(title='Date',
                    rangeselector=dict(
                        buttons=list([
                                dict(
                                    count=1,
                                    label='1m',
                                    step='month',
                                    stepmode='backward'
                                ),
                                dict(
                                    count=6,
                                    label='6m',
                                    step='month',
                                    stepmode='backward'
                                ),
                                dict(
                                    count=1,
                                    label='YTD',
                                    step='year',
                                    stepmode='todate'
                                ),
                                dict(
                                    count=1,
                                    label='YTD',
                                    step='year',
                                    stepmode='backward'
                                ),
                                dict(step='all')
                                ]
                            ),
                        rangeslider=dict(visible=True),
                        type='date'
    ))
)

fig = go.Figure(data=data, layout=layout)
fig.update_layout(layout)
fig.show(config= {'displayModeBar': True})
#print(stock_df.head())