import streamlit as st
import numpy as np
import pandas as pd
from download_from_yahoo import download_financials, download_financials_ds, download_financials_info
from quantitative_analysis import display_statements, display_totals_and_ratios
from charts import drawcharts, draw_historical_data
from summary import display_summary
from datetime import date, timedelta
from dashboard import my_portfolio
from company_dashboard import company_dashboard

st.set_page_config(
                   page_icon=':maple_leaf:',
                   layout='wide',
                   initial_sidebar_state="expanded")

# Define custom CSS
custom_css = """
<style>
h2{
    text-align:center;
}
p{
padding:10px
}
.ok{
    background-color:aqua;
    color:black; 
}
.excellent{
    background-color:green;
    color:white; 
}
.orange{
    background-color:orange;
    color:white; 
}
.orange2{
    background-color:#efc266;
    color:white;
}
.orange1{
    background-color:#ff5200;
    color:white;
}
.danger{
    background-color:red;
    color:white; 
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# create a left menu with companies
stocks=['TCS.NS', 'PERSISTENT.NS', 'HCLTECH.NS', 'ITC.NS', 'BRITANNIA.NS', 'HINDUNILVR.NS', 'RELIANCE.NS', 'OIL.NS', 'ONGC.NS']
selected_dropdown = st.sidebar.selectbox("Select:", ["My Profile", "Company Dashboard"])

n_years = st.sidebar.slider("Year duration2:", 1,5, value=5)

period = n_years*365
end_date = date.today()
start_date = end_date - timedelta(days=period)


if selected_dropdown == "Company Dashboard":
    selected_tab = st.sidebar.radio("Select Company", stocks)
    company_dashboard(selected_tab, start_date, end_date)
else:
    my_portfolio(stocks, start_date, end_date)

