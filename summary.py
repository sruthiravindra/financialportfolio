import streamlit as st
from download_from_yahoo import download_financials_info

def display_summary(financials_ticker):
    info = financials_ticker.info
    # st.write(info)

    currency = info['currency']

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Sector:** {info['sector']}")
        st.markdown(f"**Industry:** {info['industry']}")
        st.markdown(f"**Website:** [{info['website']}]({info['website']})")
        st.markdown(f"**Previous Close:** {info['previousClose']:,}")
        st.markdown(f"**Open:** {info['open']:,}")
    with col2:
        st.markdown(f"**Market Cap:** {info['marketCap']:,}")
        st.markdown(f"**P/E Ratio:** {info['forwardPE']}")
        st.markdown(f"**Dividend Yield:** {info['dividendYield'] * 100:.2f}%")
        st.markdown(f"**EPS (TTM):** {info['trailingEps']}")



    st.subheader("Financials")
    st.markdown(f"**Revenue (TTM):** {info['totalRevenue']:,}")
    st.markdown(f"**Net Income (TTM):** {info['netIncomeToCommon']:,}")
    # st.subheader("Recent News")
    # for item in info['summary'].split('\n'):
    #     st.markdown(f"- {item}")
    return