import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# 1. Page Config & Custom Vibrant Styling
st.set_page_config(page_title="Money Pulse Pro", layout="wide")

# Injecting CSS for vibrant colors and animations
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.3);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5);
    }
    h1 {
        background: -webkit-linear-gradient(#00ffcc, #33ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Function to load Lottie Animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_money = load_lottieurl("https://lottie.host/8047910d-2b47-49f3-85b2-38e93f9c5d03/GfX5vX8L1S.json")# Floating Money


# 3. Header Section
col_title, col_anim = st.columns([2, 1])
with col_title:
    st.title("💸 Money Pulse Pro")
    st.write("### Track your riches with style.")

with col_anim:
    st_lottie(lottie_money, height=150, key="money_anim")

st.divider()
debar Upload
st.sidebar.markdown("## 📥 Input Zone")
uploaded_file = st.sidebar.file_uploader("Drop your Bank CSV here", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Financial Logic
    total_spent = df[df['Amount'] < 0]['Amount'].sum()
    total_income = df[df['Amount'] > 0]['Amount'].sum()
    net = total_income + total_spent

    # Vibrant Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("EXPENSES", f"${abs(total_spent):,.2f}")
    m2.metric("INCOME", f"${total_income:,.2f}")
    m3.metric("NET BALANCE", f"${net:,.2f}")

    if net > 0:
        st.balloons() # Animated celebration!
        st.success("🎉 You're making a profit this month!")

    # 5. Charts with Neon Colors
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🌈 Spending Breakdown")
        expenses = df[df['Amount'] < 0].copy()
        expenses['Amount'] = expenses['Amount'].abs()
        fig_pie = px.pie(expenses, values='Amount', names='Category', 
                         color_discrete_sequence=px.colors.sequential.Electric_r,
                         hole=0.5)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("📈 Wealth Timeline")
        df_daily = df.groupby('Date')['Amount'].sum().reset_index()
        fig_line = px.area(df_daily, x='Date', y='Amount', 
                           color_discrete_sequence=['#00ffcc'])
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.warning("👈 Upload a CSV in the sidebar to ignite the dashboard!")
