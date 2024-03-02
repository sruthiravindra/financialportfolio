import yfinance as yf
import streamlit as st
from tabulate import tabulate
from utilities import format_key_to_month_year
import locale

# Set the locale to the user's default locale
locale.setlocale(locale.LC_ALL, '')

def display_statements(income_statement, balance_sheet, cash_flow_statement, financials_ticker):

    statement = st.radio("Select Statement Type", ("Income Statement", "Balance Sheet", "Cash Flow Statement"))

    if statement == "Income Statement":
        st.subheader("Income Statement")
        st.write(income_statement)
    elif statement == "Balance Sheet":
        st.subheader("Balance Sheet")
        st.write(balance_sheet)
    else:
        st.subheader("Cash Flow Statement")
        st.write(cash_flow_statement)

    return True

def display_totals_and_ratios(income_statement, balance_sheet, cash_flow_statement, financials_ticker):
    display_cgar(income_statement, balance_sheet, cash_flow_statement)
    display_debt_to_equity(income_statement, balance_sheet, cash_flow_statement)
    display_pe_ratio(income_statement, balance_sheet, cash_flow_statement, financials_ticker)
    display_roe(income_statement, balance_sheet, cash_flow_statement, financials_ticker)
    display_cash_flow(income_statement, balance_sheet, cash_flow_statement, financials_ticker)

    return True


# Calculate CAGR function
def calculate_cagr(final_value, initial_value, num_years):
    return ((final_value / initial_value) ** (1 / num_years)) - 1

    
def display_cgar(income_statement, balance_sheet, cash_flow_statement):

    st.header("Analysis Based on CAGR (Compunded Annual Growth Rate)")

    # Assuming you have historical data for these metrics in your DataFrame
    total_revenue_values = income_statement.loc['Total Revenue']
    pat_values = income_statement.loc['Net Income From Continuing Operation Net Minority Interest']
    ebitda_values = income_statement.loc['EBITDA']

    y_period = len(total_revenue_values)-1
    # Calculate CAGR for each metric
    total_revenue_cagr = calculate_cagr(total_revenue_values.iloc[0], total_revenue_values.iloc[-1], len(total_revenue_values) - 1)
    pat_cagr = calculate_cagr(pat_values.iloc[0], pat_values.iloc[-1], len(pat_values) - 1)
    ebitda_cagr = calculate_cagr(ebitda_values.iloc[0], ebitda_values.iloc[-1], len(ebitda_values) - 1)


    total_revenue = {
        'Total Revenue': total_revenue_values,
        'EBITDA': ebitda_values,
        'PAT': pat_values,
    }

    total_revenue['Total Revenue']['CAGR'] = '{:.2%}'.format(total_revenue_cagr)
    total_revenue['PAT']['CAGR'] = '{:.2%}'.format(pat_cagr)
    total_revenue['EBITDA']['CAGR'] = '{:.2%}'.format(ebitda_cagr)
    
    if total_revenue_cagr <= 0.15:
        style_rev = 'medium'
        style_edi = 'medium'
    elif total_revenue_cagr < 0.25:
        style_rev = 'good'
        style_edi = 'good'
    else:
        style_rev = 'excellent'
        style_edi = 'excellent'
    
    if ebitda_cagr <= 0.15:
        style_ebi = 'medium'
    elif ebitda_cagr < 0.25:
        style_ebi = 'good'
    else:
        style_ebi = 'excellent'
            
    if pat_cagr <= 0.10:
        style_pat = 'medium'
    elif pat_cagr < 0.15:
        style_pat = 'good'
    else:
        style_pat = 'excellent'

    # Display table
    try:
        st.table(total_revenue)
        st.markdown(f"""
<p class='ok'>
Sales CAGR metric shows the average annual growth rate of the company's sales revenue over last {y_period} years.<br>
EBIDTA CAGR metric represents the profitability of a company's core operations over last {y_period} years.<br>
PAT CAGR shows the average annual growth rate of the company's net profit over last {y_period} years.<br>
We can see Sales CAGR is <span class='{style_rev}'>{total_revenue['Total Revenue']['CAGR']}</span>, 
EBITDA CAGR is <span class='{style_ebi}'>{total_revenue['EBITDA']['CAGR']}</span> and 
PAT CAGR is <span class='{style_pat}'>{total_revenue['PAT']['CAGR']}</spam>.<br>

</p>
""", unsafe_allow_html=True)
#         From this we can infer that there may be an increase in the operating expense is higher than revenue which has caused the EBITDA average growth to be lower than the sales.<br>
# Also, PAT average growth being lower than EBITA means than depreciation and tax may be increasing. <br>
# Since the margin of differences in these percentages are not too high hence its still not very alarming 
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return True


def display_debt_to_equity(income_statement, balance_sheet, cash_flow_statement):
    total_debt = balance_sheet.loc['Total Debt'].iloc[-1]  # Get the most recent value
    total_equity = balance_sheet.loc['Total Equity Gross Minority Interest'].iloc[-1]  # Get the most recent value

    # calcualte the debt-to-equity-ratio
    debt_to_equity_ratio = total_debt/total_equity

    st.header("Analysis Based on Debt To Equity Ratio")
    st.markdown(f"Debt-to-Equity Ratio is : {debt_to_equity_ratio:.2f}")
    if(debt_to_equity_ratio > 1):
        st.markdown("<p class='danger'>Debt-to-Equity Ratio is greater than 1 indicating danger. <p>", unsafe_allow_html=True)
    elif(debt_to_equity_ratio > 0.01):
        st.markdown("<p class='good'>Debt-to-Equity Ratio indicating a balanced or conservative approach to financing.<p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='excellent'>Debt-to-Equity ratio of 0, implying no debt in its capital structure. <p>", unsafe_allow_html=True)



def display_pe_ratio(income_statement, balance_sheet, cash_flow_statement, financials_ticker):

    # Get the current market price (price of the last trade)
    market_price = financials_ticker.history(period='1d')['Close'].iloc[-1]

    # get the PAT for current year
    pat = income_statement.loc['Net Income From Continuing Operation Net Minority Interest'].iloc[0]

    # Get the number of shares outstanding
    shares_outstanding = financials_ticker.info.get('sharesOutstanding')
    PE_ratio = market_price/(pat/shares_outstanding)

    display_table = {
        "Market Price per Share": format(market_price, '.2f'),
        "Profit After Tax": locale.format_string("%d", pat, grouping=True),
        "No of Shares" : format(shares_outstanding, '.2f'),
        "Earnings per Share" : locale.format_string("%g", pat/shares_outstanding, grouping=True),
        "PE Ratio" : format(PE_ratio, '.2f')
    }


    st.header("Analysis Based on PE Ratio")
    st.table(display_table)
    st.markdown("This ratio compares a company's stock price to its earnings per share. ")
    if(PE_ratio < 20 ):
        st.markdown("<p class='orange'>suggests a moderate valuation for the company's stock, with moderate growth expectations and a balanced risk profile.<p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='danger'> a P/E ratio suggests that the company is trading at a relatively high valuation compared to its earnings, indicating investor optimism and expectations of future growth. <p>", unsafe_allow_html=True)




def display_roe(income_statement, balance_sheet, cash_flow_statement, financials_ticker):

    # Get the net income and shareholders' equity
    net_income = financials_ticker.financials.loc['Net Income'].iloc[-1]
    shareholders_equity = financials_ticker.balance_sheet.loc['Total Equity Gross Minority Interest'].iloc[-1]

    # Calculate the ROE
    roe = (net_income / shareholders_equity) * 100  # Multiply by 100 to express as percentage
    
    display_table = {
        "Net Income": net_income,
        "Total Equity": shareholders_equity,
        "ROE" : roe
    }
    st.header("Analysis Based on ROE")
    st.table(display_table)
    st.markdown(f"Return on Equity (ROE): {roe:.2f}%")
    st.markdown("This metric shows how much profit a company generates from its shareholders' equity. ")
    if(roe < 30 ):
        st.markdown("<p class='orange'>indicates moderate profitability and suggests that the company is generating a reasonable return on its shareholders' equity. <p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='excellent'>The ROE considered quite high and indicates that the company is generating significant profits relative to its equity base. <p>", unsafe_allow_html=True)


def display_cash_flow(income_statement, balance_sheet, cash_flow_statement, financials_ticker):
    
    # Extract the operating cash flow
    operating_cash_flow = cash_flow_statement.loc['Operating Cash Flow'].iloc[-1]
    capital_expenditure = cash_flow_statement.loc['Capital Expenditure'].iloc[-1]
    free_cash = operating_cash_flow + capital_expenditure

    display_table = {
        "Operating Cash Flow": operating_cash_flow,
        "Cash Expenditure": capital_expenditure,
        "Free Cash or Cash Equivalent Flow" : free_cash
    }
    st.header("Analysis Based on Cash Flow")
    st.table(display_table)

    st.markdown("<p>There’s no specific percentage of sales that is a benchmark for free cash flow. However, higher levels of free cash flow indicate that a company is more profitably serving its customers. Strong free cash flow can indicate that a company is well-run and making money off its operations. It can also be affected by investing more or less in long-term capital assets, changing the way a company collects from customers and pays suppliers and by selling off corporate assets. <p>", unsafe_allow_html=True)


    