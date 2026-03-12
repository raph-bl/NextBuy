import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

@st.cache_data
def load_data():
    aisles         = pd.read_csv('./datasets/aisles.csv')
    departments    = pd.read_csv('./datasets/departments.csv')
    products       = pd.read_csv('./datasets/products.csv')
    orders         = pd.read_csv('./datasets/orders.csv')
    order_products = pd.read_csv('./datasets/order_products.csv')
    return aisles, departments, products, orders, order_products

aisles, departments, products, orders, order_products = load_data()

@st.cache_resource
def load_models():
    return joblib.load('./models/random_forest.pkl'), joblib.load('./models/logistic_regression.pkl')

model_rf, model_lr = load_models()

@st.cache_data
def precompute():
    user_op = order_products.merge(orders[['order_id', 'user_id']], on='order_id')

    user_stats = (
        user_op.groupby('user_id')
        .agg(
            user_total_com    =('order_id', 'nunique'),
            user_total_product=('product_id', 'nunique'),
        )
        .join(user_op.groupby(['user_id', 'order_id']).size()
              .groupby('user_id').mean().rename('user_cart_mean'))
        .reset_index()
    )

    product_stats = (
        order_products.groupby('product_id')
        .agg(
            product_total_achat=('product_id', 'count'),
            product_reorder    =('reordered', 'mean'),
        )
        .reset_index()
    )

    rep_achat = (
        user_op.groupby(['user_id', 'product_id'])['reordered']
        .mean().rename('rep_achat').reset_index()
    )

    return user_stats, product_stats, rep_achat

user_stats, product_stats, rep_achat_df = precompute()

def build_features(user_id, prod_id):
    u = user_stats[user_stats['user_id'] == user_id]
    p = product_stats[product_stats['product_id'] == prod_id]
    r = rep_achat_df[(rep_achat_df['user_id'] == user_id) & (rep_achat_df['product_id'] == prod_id)]

    return pd.DataFrame([{
        'rep_achat':           r['rep_achat'].values[0] if len(r) else 0.0,
        'user_total_com':      u['user_total_com'].values[0] if len(u) else 0,
        'user_total_product':  u['user_total_product'].values[0] if len(u) else 0,
        'user_cart_mean':      u['user_cart_mean'].values[0] if len(u) else 0.0,
        'product_total_achat': p['product_total_achat'].values[0] if len(p) else 0,
        'product_reorder':     p['product_reorder'].values[0] if len(p) else 0.0,
    }])

st.title("Prédiction de rachat")
st.caption("Estimez la probabilité qu'un utilisateur rachète un produit donné.")

st.divider()

user_min, user_max = int(orders['user_id'].min()), int(orders['user_id'].max())

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        selected_prod = st.selectbox("Produit", products['product_name'].tolist())
    with col2:
        selected_user = st.number_input(
            f"ID utilisateur ({user_min} – {user_max})",
            min_value=user_min, max_value=user_max, value=user_min, step=1
        )
    submit = st.form_submit_button("Prédire", use_container_width=True)

if submit:
    prod_id = products[products['product_name'] == selected_prod]['product_id'].values[0]
    X = build_features(int(selected_user), prod_id)

    prob_rf   = model_rf.predict_proba(X)[0][1]
    prob_lr   = model_lr.predict_proba(X)[0][1]
    prob_mean = (prob_rf + prob_lr) / 2

    st.divider()

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob_mean * 100, 1),
        number={'suffix': '%'},
        title={'text': "Probabilité de rachat (moyenne RF + LR)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#6a0dad"},
            'steps': [
                {'range': [0, 40],  'color': '#f0e6ff'},
                {'range': [40, 70], 'color': '#c89be0'},
                {'range': [70, 100],'color': '#9b59b6'},
            ],
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    c1.metric("Random Forest",        f"{prob_rf * 100:.1f}%")
    c2.metric("Régression Logistique", f"{prob_lr * 100:.1f}%")

    st.divider()

    with st.expander("Détail des features utilisées"):
        labels = {
            'rep_achat':           "Taux de rachat user×produit",
            'user_total_com':      "Nb commandes utilisateur",
            'user_total_product':  "Nb produits distincts achetés",
            'user_cart_mean':      "Taille moyenne du panier",
            'product_total_achat': "Nb achats totaux du produit",
            'product_reorder':     "Taux de rachat global du produit",
        }
        for col, label in labels.items():
            st.markdown(f"**{label}** : `{X[col].values[0]:.2f}`")
