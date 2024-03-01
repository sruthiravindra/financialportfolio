import yfinance as yf
import streamlit as st

@st.cache_resource
def download_financials_info(ticker_code):
    financials_ticker = yf.Ticker(ticker_code)
    return financials_ticker

@st.cache_resource
def download_financials_ds_for_portfolio(ticker_code, start_date, end_date):
    financials_ticker_ds = yf.download(ticker_code, start_date, end_date)
    return financials_ticker_ds

@st.cache_resource
def download_financials_ds(ticker_code, start_date, end_date):
    financials_ticker_ds = yf.download(ticker_code, start_date, end_date)
    financials_ticker_ds.reset_index(inplace=True, drop=False)
    return financials_ticker_ds


def download_financials(financials_ticker):
    income_statement = financials_ticker.financials
    balance_sheet = financials_ticker.balancesheet
    cash_flow_statement = financials_ticker.cashflow
    return income_statement, balance_sheet, cash_flow_statement

def get_sector(ticker):
    # Fetch ticker information
    ticker_info = yf.Ticker(ticker)
    
    # Get sector information
    sector = ticker_info.info.get('sector', 'N/A')
    
    return sector

@st.cache_resource
def get_sectors_for_tickers(tickers):
    sectors = {}
    for ticker in tickers:
        sector = get_sector(ticker)
        sectors[ticker] = sector
    return sectors