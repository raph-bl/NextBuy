import streamlit as st
import pandas as pd 
import joblib
# dataframes 

@st.cache_data
def load_data():
    aisles         = pd.read_csv('./datasets/aisles.csv')
    departments    = pd.read_csv('./datasets/departments.csv')
    products       = pd.read_csv('./datasets/products.csv')
    orders         = pd.read_csv('./datasets/orders.csv')
    order_products = pd.read_csv('./datasets/order_products.csv')
    return aisles, departments, products, orders, order_products
aisles, departments, products, orders, order_products = load_data()
# model
model   = joblib.load('./models/random_forest.pkl')
model_2 = joblib.load('./models/logistic_regression.pkl')

st.markdown("# Product reorder prediction")
prod_options = products['product_name'].tolist()
prod_user    = orders['user_id'].unique().tolist()
with st.form("prediction_name"):
    selected_prod = st.selectbox("product", prod_options)
    selected_user = st.selectbox("user", prod_user)
    submit        = st.form_submit_button("prédire les chances de rachat")

if submit:
    prod_id = products[products['product_name'] == selected_prod]['product_id'].values[0]