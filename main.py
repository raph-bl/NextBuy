import streamlit as st

# def des pages
main_page = st.Page("nextbuy_dashboard.py", title="Main Page")
page_2    = st.Page("dashboard_page2.py", title="Product Reorder Prediction")

pg = st.navigation([main_page, page_2])
pg.run()