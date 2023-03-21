#Holding for reconstruction

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