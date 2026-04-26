import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Money Pulse Pro", layout="wide")

# 2. Vibrant Styling
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #00ffcc;
        padding: 15px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💸 Money Pulse Pro")
    st.markdown("### Track your riches with style.")
with col2:
    st.markdown("<h1 style='font-size: 100px;'>💰</h1>", unsafe_allow_html=True)

st.divider()

# 4. Sidebar
st.sidebar.header("📥 Input Zone")
uploaded_file = st.sidebar.file_uploader("Drop your Bank CSV here", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Ensure 'Date' and 'Amount' columns exist in your CSV!
    if 'Amount' in df.columns:
        total_spent = df[df['Amount'] < 0]['Amount'].sum()
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("EXPENSES", f"${abs(total_spent):,.2f}")
        m2.metric("INCOME", f"${total_income:,.2f}")
        m3.metric("NET", f"${(total_income + total_spent):,.2f}")
        
        st.balloons()
        
        fig = px.pie(df[df['Amount'] < 0], values=df[df['Amount'] < 0]['Amount'].abs(), names='Category', hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("CSV must have an 'Amount' column!")
else:
    st.info("👈 Upload a CSV file in the sidebar to see the magic!")
