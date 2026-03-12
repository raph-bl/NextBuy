import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
# dataframes 
aisles         = pd.read_csv('./datasets/aisles.csv')
departments    = pd.read_csv('./datasets/departments.csv')
products       = pd.read_csv('./datasets/products.csv')
orders         = pd.read_csv('./datasets/orders.csv')
order_products = pd.read_csv('./datasets/order_products.csv')
# code 
st.title("Welcome to NextBuy!")
st.subheader('Most popular product')

cart_first=order_products[order_products['add_to_cart_order']==1]
count_first_product=cart_first['product_id'].value_counts().reset_index()
count_first_product.columns=['product_id', 'count']
top_merged=pd.merge(count_first_product, products[['product_id', 'product_name']], on='product_id', how='left')
top = top_merged.sort_values('count', ascending=True).tail(10)
st.bar_chart(
    data=top.set_index('product_name')['count'],
    horizontal=True,
    color="#6a0dad" 
)