import plotly as plt
from plotly import graph_objs as go
import streamlit as st
import numpy as np
import pandas as pd


def drawcharts(financials_ticker):
    col1, col2 = st.columns(2)

    with col1:
        drawcharts_price_movements(financials_ticker)
    with col2:
        drawcharts_open_close(financials_ticker)
    return

def drawcharts_open_close(financials_ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=financials_ticker['Date'], y=financials_ticker['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=financials_ticker['Date'], y=financials_ticker['Close'], name="stock_close"))
    fig.layout.update(title_text='Stock Open and Close ', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    return

def drawcharts_price_movements(financials_ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=financials_ticker['Date'], y=financials_ticker['Adj Close'], name="price movements"))
    fig.layout.update(title_text='Price Movements ', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    return

def draw_historical_data(financials_ticker):
    data = financials_ticker
    data['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data.dropna(inplace=True)
    annual_return = data['% Change'].mean()*252*100
    stand_dev = np.std(data['% Change'])*np.sqrt(252) # inorder to annualize we are multiplying with number of working days
    risk_adjusted_data = annual_return / (stand_dev*100)


    # Format the string with the computed annual return
    if annual_return < 0:
        annual_return_style = 'danger'
    elif annual_return < 10:
        annual_return_style = 'orange1'
    elif annual_return < 20:
        annual_return_style = 'orange'
    elif annual_return < 30:
        annual_return_style = 'orange2'
    else:
        annual_return_style = 'excellent'
    annual_return_text = f"Annual Return: <span class='{annual_return_style}'>{annual_return:.2f}%</span>"


    
    # Format the string with the computed annual return
    stand_dev_style = 'excellent' if stand_dev > 0 else 'danger'
    stand_dev_text = f"Standard Deviation: <span class='{stand_dev_style}'>{stand_dev * 100:.2f}%</span>"


    
    # Format the string with the computed annual return
    if risk_adjusted_data < 0.3:
        risk_adjusted_data_style = 'danger'
    elif risk_adjusted_data < 0.6:
        risk_adjusted_data_style = 'orange1'
    elif risk_adjusted_data < 1.0:
        risk_adjusted_data_style = 'orange'
    else:
        risk_adjusted_data_style = 'excellent'   
    risk_adjusted_data_text = f"Risk Adjusted:  <span class='{risk_adjusted_data_style}'>{risk_adjusted_data:.2f}%</span>"



    # Create a DataFrame for annualized returns and standard deviation
    returns_std_dev_df = pd.DataFrame({'Annualized_Return': [annual_return_text], 
                                    'Annualized_Std_Dev': [stand_dev_text], 
                                    'Risk Adjusted': [risk_adjusted_data_text]})


    # Display the formatted text using markdown
    st.markdown(annual_return_text, unsafe_allow_html=True)
    st.markdown(stand_dev_text, unsafe_allow_html=True)
    st.markdown(risk_adjusted_data_text, unsafe_allow_html=True)
    st.write(data.sort_index(ascending=False))

    return
