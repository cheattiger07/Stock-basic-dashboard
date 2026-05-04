import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Fetch data
stock = yf.download("AAPL", period='6mo')
stock.columns = stock.columns.droplevel(1)

# Indicators
stock['MA20'] = stock['Close'].rolling(window=20).mean()
stock['MA50'] = stock['Close'].rolling(window=50).mean()

# RSI
delta = stock['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss
stock['RSI'] = 100 - (100 / (1 + rs))

# ✅ CREATE SUBPLOTS FIRST
chart = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3]
)

# ✅ Price (Row 1)
chart.add_trace(go.Candlestick(
    x=stock.index,
    open=stock['Open'],
    high=stock['High'],
    low=stock['Low'],
    close=stock['Close'],
    name="Price"
), row=1, col=1)

# ✅ Moving Averages
chart.add_trace(go.Scatter(
    x=stock.index,
    y=stock['MA20'],
    mode='lines',
    name='MA20',
    line=dict(color='blue')
), row=1, col=1)

chart.add_trace(go.Scatter(
    x=stock.index,
    y=stock['MA50'],
    mode='lines',
    name='MA50',
    line=dict(color='orange')
), row=1, col=1)


chart.add_trace(go.Bar(
    x=stock.index,
    y=stock['Volume'],
    name='Volume',
    marker_color='blue',
    yaxis='y2'
), row=1, col=1)


chart.add_trace(go.Scatter(
    x=stock.index,
    y=stock['RSI'],
    mode='lines',
    name='RSI'
), row=2, col=1)


chart.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
chart.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

chart.update_layout(
    title="Stock Dashboard (RSI)",
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    yaxis2=dict(
        title='Volume',
        overlaying='y',
        side='right'
    )
)

chart.show()