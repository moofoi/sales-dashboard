import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_with_ai(summary):
    prompt = f"""
    You are a business analyst. Based on this sales data summary:
    {summary}
    
    Please provide:
    1. Key insights (3-5 points)
    2. Top performing areas
    3. Areas that need improvement
    4. Actionable recommendations
    
    Keep it concise and business-focused.
    """
    response = model.generate_content(prompt)
    return response.text

# UI
st.title("📊 Sales Data Analysis Dashboard")
st.write("Upload your sales data and get AI-powered insights instantly")

uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    
    st.success("✅ Data loaded successfully!")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
    col2.metric("Total Units Sold", f"{df['units_sold'].sum():,}")
    col3.metric("Avg Order Value", f"${df['revenue'].mean():,.0f}")
    col4.metric("Total Records", f"{len(df):,}")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Product")
        product_rev = df.groupby('product')['revenue'].sum().reset_index()
        fig1 = px.bar(product_rev, x='product', y='revenue',
                     color='revenue', color_continuous_scale='blues')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Region")
        region_rev = df.groupby('region')['revenue'].sum().reset_index()
        fig2 = px.pie(region_rev, values='revenue', names='region')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Revenue Over Time")
    daily_rev = df.groupby('date')['revenue'].sum().reset_index()
    fig3 = px.line(daily_rev, x='date', y='revenue',
                   color_discrete_sequence=['#2563eb'])
    st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    # AI Insights
    st.subheader("🤖 AI Business Insights")
    if st.button("Generate AI Insights"):
        summary = f"""
        Total Revenue: ${df['revenue'].sum():,.0f}
        Total Units Sold: {df['units_sold'].sum():,}
        Best Product: {df.groupby('product')['revenue'].sum().idxmax()}
        Best Region: {df.groupby('region')['revenue'].sum().idxmax()}
        Date Range: {df['date'].min().date()} to {df['date'].max().date()}
        """
        with st.spinner("AI is analyzing your data..."):
            insights = analyze_with_ai(summary)
        st.write(insights)
    
    # Raw Data
    with st.expander("📄 View Raw Data"):
        st.dataframe(df, use_container_width=True)