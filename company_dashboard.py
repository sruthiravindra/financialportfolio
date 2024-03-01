import streamlit as st
import numpy as np
import pandas as pd
from download_from_yahoo import download_financials, download_financials_ds, download_financials_info
from quantitative_analysis import display_statements, display_totals_and_ratios
from charts import drawcharts, draw_historical_data
from summary import display_summary
from datetime import date, timedelta

def display_company_title(financials_ticker):
    
    st.title(f"{financials_ticker.info['longName']} ({financials_ticker.info['symbol']})")
    diff = financials_ticker.info['currentPrice'] - financials_ticker.info['previousClose']
    diff_percent = (diff*100)/(financials_ticker.info['currentPrice'])
    diff_class = "red" if diff < 0 else "green"
    st.markdown(f"""
    <p class="company_title">
                <span>{financials_ticker.info['currentPrice']:,}</span>   
                <span class='sub {diff_class}'>{diff:,.2f}</span>
                <span class='sub {diff_class}'>( {diff_percent:,.2f}% )</span>
    </p>
                """, unsafe_allow_html=True)

def company_dashboard(ticker, start_date, end_date ):

    financials_ticker = download_financials_info(ticker)
    display_company_title(financials_ticker)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summary", "Chart", "Financials", "Historicals", "Quantitative Analysis"])

    with tab1:
        display_summary(financials_ticker)
    with tab2:
        st.header("Chart")
        financials_ticker_ds = download_financials_ds(ticker, start_date, end_date)
        drawcharts(financials_ticker_ds)
    with tab3:
        st.header("Financials")
        income_statement, balance_sheet, cash_flow_statement = download_financials(financials_ticker)
        display_statements(income_statement, balance_sheet, cash_flow_statement, financials_ticker)

    with tab4:
        st.header("Historicals")
        financials_ticker_ds = download_financials_ds(ticker, start_date, end_date)
        draw_historical_data(financials_ticker_ds)  

    with tab5:
        st.header("Quantitative Analysis")
        st.write("Quantitative Analysis to help determine if we should choose this company")
        income_statement, balance_sheet, cash_flow_statement = download_financials(financials_ticker)
        display_totals_and_ratios(income_statement, balance_sheet, cash_flow_statement, financials_ticker)

    

