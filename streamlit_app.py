import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.title("Stock DashBoard")
mode = st.radio("Choose Input Method", ["Select", "Search"])
if mode == "Select":
    ticker = st.selectbox(
        "Select Stock",
        ["AAPL", "TSLA", "MSFT", "RELIANCE.NS", "TCS.NS", "INFY.NS"]
    )

else:
    ticker = st.text_input("Search Stock (Enter Ticker)", "AAPL")
period = st.sidebar.selectbox(
    "Select Time Period",
    ["3mo", "6mo", "1y", "2y"]
)

stock = yf.download(ticker, period=period)

# Fix multi-index issue
if isinstance(stock.columns, type(stock.columns)):
    try:
        stock.columns = stock.columns.droplevel(1)
    except:
        pass
# Moving averages
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
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3],
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

# Candlestick
fig.add_trace(go.Candlestick(
    x=stock.index,
    open=stock['Open'],
    high=stock['High'],
    low=stock['Low'],
    close=stock['Close'],
    name="Price"
), row=1, col=1)

# MA
fig.add_trace(go.Scatter(
    x=stock.index,
    y=stock['MA20'],
    name="MA20"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=stock.index,
    y=stock['MA50'],
    name="MA50"
), row=1, col=1)

# Volume
fig.add_trace(go.Bar(
    x=stock.index,
    y=stock['Volume'],
    name="Volume",
    opacity=0.3
), row=1, col=1, secondary_y=True)

# RSI
fig.add_trace(go.Scatter(
    x=stock.index,
    y=stock['RSI'],
    name="RSI"
), row=2, col=1)
st.metric("Current Price", round(stock['Close'].iloc[-1], 2))
st.metric("Highest", round(stock['High'].max(), 2))
st.metric("Lowest", round(stock['Low'].min(), 2))

fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
show_ma = st.sidebar.checkbox("Show Moving Averages", True)
show_rsi = st.sidebar.checkbox("Show RSI", True)

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)