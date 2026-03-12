import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    aisles         = pd.read_csv('./datasets/aisles.csv')
    departments    = pd.read_csv('./datasets/departments.csv')
    products       = pd.read_csv('./datasets/products.csv')
    orders         = pd.read_csv('./datasets/orders.csv')
    order_products = pd.read_csv('./datasets/order_products.csv')
    return aisles, departments, products, orders, order_products

aisles, departments, products, orders, order_products = load_data()

st.title("Welcome to NextBuy!")

# KPI metrics
col1, col2, col3 = st.columns(3)
col1.metric("Commandes", f"{orders['order_id'].nunique():,}")
col2.metric("Utilisateurs", f"{orders['user_id'].nunique():,}")
col3.metric("Produits", f"{products['product_id'].nunique():,}")

st.divider()

# Top 10 most popular products (first added to cart)
st.subheader("Top 10 produits les plus populaires")

cart_first = order_products[order_products['add_to_cart_order'] == 1]
count_first = cart_first['product_id'].value_counts().reset_index()
count_first.columns = ['product_id', 'count']
top = pd.merge(count_first, products[['product_id', 'product_name']], on='product_id', how='left')
top = top.sort_values('count', ascending=True).tail(10)

fig = px.bar(top, x='count', y='product_name', orientation='h',
             color='count', color_continuous_scale='Purples',
             labels={'count': "Nombre d'ajouts", 'product_name': ''})
fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Orders by day of week
st.subheader("Commandes par jour de la semaine")
day_map = {0: 'Dim', 1: 'Lun', 2: 'Mar', 3: 'Mer', 4: 'Jeu', 5: 'Ven', 6: 'Sam'}
orders_by_day = orders['order_dow'].value_counts().sort_index().reset_index()
orders_by_day.columns = ['day', 'count']
orders_by_day['day'] = orders_by_day['day'].map(day_map)

fig2 = px.bar(orders_by_day, x='day', y='count',
              color='count', color_continuous_scale='Purples',
              labels={'count': 'Nombre de commandes', 'day': ''})
fig2.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig2, use_container_width=True)
