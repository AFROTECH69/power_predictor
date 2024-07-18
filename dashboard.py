import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Generate sample data
def generate_sample_data(days=30):
    date_range = pd.date_range(end=datetime.now(), periods=days)
    actual_usage = np.random.randint(100, 200, size=days)
    predicted_usage = actual_usage + np.random.randint(-20, 20, size=days)
    
    df = pd.DataFrame({
        'Date': date_range,
        'Actual Usage': actual_usage,
        'Predicted Usage': predicted_usage
    })
    return df

# Calculate weekly and monthly averages
def calculate_averages(df):
    df['Week'] = df['Date'].dt.to_period('W')
    df['Month'] = df['Date'].dt.to_period('M')
    
    weekly_avg = df.groupby('Week').agg({
        'Actual Usage': 'mean',
        'Predicted Usage': 'mean'
    }).reset_index()
    weekly_avg['Week'] = weekly_avg['Week'].astype(str)
    
    monthly_avg = df.groupby('Month').agg({
        'Actual Usage': 'mean',
        'Predicted Usage': 'mean'
    }).reset_index()
    monthly_avg['Month'] = monthly_avg['Month'].astype(str)
    
    return weekly_avg, monthly_avg

# Create the Streamlit app
def main():
    st.set_page_config(page_title="Power Usage Dashboard", layout="wide")
    st.title("Power Usage Dashboard")

    # Generate sample data
    df = generate_sample_data()
    weekly_avg, monthly_avg = calculate_averages(df)

    # Daily comparison
    st.header("Daily Power Usage: Predicted vs Actual")
    daily_fig = go.Figure()
    daily_fig.add_trace(go.Scatter(x=df['Date'], y=df['Actual Usage'], name='Actual Usage', line=dict(color='blue')))
    daily_fig.add_trace(go.Scatter(x=df['Date'], y=df['Predicted Usage'], name='Predicted Usage', line=dict(color='red')))
    daily_fig.update_layout(xaxis_title="Date", yaxis_title="Power Usage (kWh)")
    st.plotly_chart(daily_fig, use_container_width=True)

    # Weekly average comparison
    st.header("Weekly Average Power Usage")
    weekly_fig = go.Figure()
    weekly_fig.add_trace(go.Bar(x=weekly_avg['Week'], y=weekly_avg['Actual Usage'], name='Actual Usage', marker_color='blue'))
    weekly_fig.add_trace(go.Bar(x=weekly_avg['Week'], y=weekly_avg['Predicted Usage'], name='Predicted Usage', marker_color='red'))
    weekly_fig.update_layout(xaxis_title="Week", yaxis_title="Average Power Usage (kWh)", barmode='group')
    st.plotly_chart(weekly_fig, use_container_width=True)

    # Monthly average comparison
    st.header("Monthly Average Power Usage")
    monthly_fig = go.Figure()
    monthly_fig.add_trace(go.Bar(x=monthly_avg['Month'], y=monthly_avg['Actual Usage'], name='Actual Usage', marker_color='blue'))
    monthly_fig.add_trace(go.Bar(x=monthly_avg['Month'], y=monthly_avg['Predicted Usage'], name='Predicted Usage', marker_color='red'))
    monthly_fig.update_layout(xaxis_title="Month", yaxis_title="Average Power Usage (kWh)", barmode='group')
    st.plotly_chart(monthly_fig, use_container_width=True)

if __name__ == "__main__":
    main()
