import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from download_from_yahoo import download_financials_ds_for_portfolio, get_sectors_for_tickers, download_financials_info

def get_filter_table_dataset(ticker_symbols, portfolio_allocation):


    data = {
    'Ticker': [],
    'Company Name': [],
    'Current Price': [],
    'Change in Price': [],
    'Quantity': [],
    'Total': [],
    'Sector': []
    }

    for ticker in ticker_symbols:
        company = download_financials_info(ticker)



        total = portfolio_allocation[portfolio_allocation['Asset'] == ticker]['Value (INR)'].iloc[0]
        quantity = total/company.info['currentPrice']

        data['Ticker'].append(ticker)
        data['Company Name'].append(company.info.get('longName', 'N/A'))
        data['Current Price'].append(company.info.get('currentPrice', 'N/A'))
        data['Change in Price'].append(company.info['currentPrice'] - company.info['previousClose'])
        data['Quantity'].append(int(quantity))
        data['Total'].append(total)
        data['Sector'].append(company.info.get('sector', 'N/A'))
        # # Add more fields as needed

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Display the filterable table
    st.table(df)
  

# Define a function to download historical data and calculate variance-covariance matrix
def calculate_covariance_matrix(ticker_symbols, start_date, end_date):
    # Download historical data for the tickers
    data = download_financials_ds_for_portfolio(ticker_symbols, start_date, end_date)['Adj Close']
    
    # Calculate lognormal returns
    log_returns = np.log(data / data.shift(1)).dropna()

    # Calculate covariance matrix
    cov_matrix = log_returns.cov()*252
    
    return cov_matrix, log_returns, data

# We define the assets for the portfolio (e.g., stock tickers).
# We download historical data for these assets using yfinance.
# We calculate the daily returns, expected returns, and covariance matrix for the assets.
# We define the objective function to minimize portfolio risk (standard deviation).
# We define constraints (weights sum to 1) and bounds (weights between 0 and 1).
# We perform optimization using the Sequential Least Squares Programming (SLSQP) method from scipy.optimize to obtain the optimal portfolio weights.
# We display the optimal portfolio weights.
def my_portfolio(ticker_symbols, start_date, end_date):

    st.markdown("<h1 style='text-align: center;;'>My Portfolio</h1>", unsafe_allow_html=True)


    # And you have a dictionary mapping assets to their sectors
    asset_to_sector =get_sectors_for_tickers(ticker_symbols)

    # Calculate covariance matrix
    cov_matrix, log_returns, data = calculate_covariance_matrix(ticker_symbols, start_date, end_date)

    # function to calculate portfolios standard deviation
    def standard_deviation(weights, cov_matrix):
        variance = weights.transpose() @ cov_matrix @ weights
        return np.sqrt(variance)
    
    # function to calculate the expected returns
    def expected_returns(weights, log_returns):
        return np.sum(log_returns.mean()*weights) * 252

    # function to calculate the sharpe ratio
    def sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
        return(expected_returns(weights, log_returns) - risk_free_rate ) / standard_deviation(weights, cov_matrix)
    
    risk_free_rate = 0.02

    # function to minimize the negative sharpe ratio
    def neg_sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
        return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)

    # Define constraints: weights sum to 1
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

    # Define bounds: each weight between 0 and 0.5
    bounds = tuple((0, 0.5) for asset in range(len(ticker_symbols)))

    # Initial guess: equal weights for each asset
    inital_weights = np.array([1/len(ticker_symbols)]*len(ticker_symbols))

    # Perform optimization to obtain optimal portfolio weights
    optimized_results = minimize(neg_sharpe_ratio, inital_weights, args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Get optimal weights
    optimal_weights = optimized_results.x


    # Calculate value of each asset in the portfolio
    initial_investment = 10000000  # INR 1 crore
    asset_values = optimal_weights * initial_investment

    # Create a DataFrame for asset values
    portfolio_allocation = pd.DataFrame({'Asset': ticker_symbols, 'Value (INR)': asset_values})

    # Add a new 'Sector' column to portfolio_allocation based on the dictionary mapping
    portfolio_allocation['Sector'] = portfolio_allocation['Asset'].map(asset_to_sector)

    # Group assets by sector and sum the values for each sector
    sector_allocation = portfolio_allocation.groupby('Sector')['Value (INR)'].sum().reset_index()


    # Calculate optimal portfolio return
    optimal_portfolio_return = expected_returns(optimal_weights, log_returns)

    # Calculate optimal volatality
    optimal_portfolio_volatality = standard_deviation(optimal_weights, cov_matrix)

    # Calculate optimal sharpe ratio
    optimal_sharpe_ratio = sharpe_ratio(optimal_weights,log_returns, cov_matrix, risk_free_rate)

    
    col1, col2 = st.columns(2)
    with col1:
        # Plot a pie chart to visualize portfolio allocation
        fig =plt.figure(figsize=(5, 5))
        plt.pie(portfolio_allocation['Value (INR)'], labels=portfolio_allocation['Asset'], autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Allocation')
        plt.axis('equal')
        st.pyplot(fig)
    with col2:
        # Plot a pie chart to visualize sector-wise allocation
        fig = plt.figure(figsize=(5, 5))
        plt.pie(sector_allocation['Value (INR)'], labels=sector_allocation['Sector'], autopct='%1.1f%%', startangle=140)
        plt.title('Sector-wise Portfolio Allocation')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)


    get_filter_table_dataset(ticker_symbols, portfolio_allocation)

    st.write(f"Adjusted Close Stock Price for all tickers for the period {start_date} to {end_date}")
    st.write(data) 

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Portfolio Allocation:')
        st.write(portfolio_allocation)
    with col2:
        st.write('Optimal portfolio weights')
        # Display optimal portfolio weights
        portfolio_weights = pd.DataFrame({'Asset': ticker_symbols, 'Weight': optimal_weights})
        st.write(portfolio_weights)
    with col3:
        st.write("Analytics Of Optimal Portfolio")
        st.markdown(f"""
        <p class='ok'>
        Expected Annual Returns: {optimal_portfolio_return:.4f}<br><br>
        Expected Volatality: {optimal_portfolio_volatality:.4f}<br><br>
        Sharpe Ratio: {optimal_sharpe_ratio:.4f}
        </p>
        """, unsafe_allow_html=True)
 

          
    col1, col2 = st.columns(2)
    with col1:
        # Plot a pie chart to visualize portfolio allocation
        fig =plt.figure(figsize=(4, 4))
        plt.bar(ticker_symbols, optimal_weights)
        plt.xticks(rotation=90)
        plt.xlabel("Assets")
        plt.ylabel("Optimal weights")
        plt.title('Optimal Portfolio Weights')
        st.pyplot(fig) 
    with col2:
        fig =plt.figure(figsize=(10, 8))
        sns.heatmap(cov_matrix, annot=True, cmap='coolwarm', fmt=".5f", linewidths=.5)
        plt.title('Heatmap of Correlation')
        st.pyplot(fig)


    # Create heatmap
    st.write('Variance-Covariance Matrix:')
    st.write(cov_matrix)


    
    

    return