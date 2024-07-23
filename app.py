import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import mean_squared_error
from datetime import timedelta

# Load the data
data = pd.read_csv('combined_output.csv')

# Load the model and scaler
with open('src/randomforest_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('x_scaler.pkl', 'rb') as f:
    scaler_x = pickle.load(f)

# Convert 'timestamp' column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y_%m_%d_%H_%M')

# Streamlit app
st.title('Energy Consumption Dashboard')

tab1, tab2, tab3 = st.tabs(["Energy Consumption Status", "Predicted Power", "Delta Dashboard"])

with tab1:
    st.header("Energy Consumption Status")
    
    # Line chart of power over time
    st.subheader("Power Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['power'], mode='lines', name='Power'))
    fig.update_layout(title='Power Over Time', xaxis_title='Time', yaxis_title='Power')
    st.plotly_chart(fig, use_container_width=True)
    
    # Histogram of energy distribution
    st.subheader("Energy Distribution")
    fig = px.histogram(data, x='energy', nbins=50, title='Energy Distribution', labels={'energy': 'Energy'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart of power by date
    st.subheader("Power by Date")
    data['date'] = data['timestamp'].dt.date
    daily_power = data.groupby('date')['power'].mean().reset_index()
    fig = px.bar(daily_power, x='date', y='power', title='Power by Date', labels={'date': 'Date', 'power': 'Power'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Predicted Power Over Time")
    
    # Generate predictions using the model
    predictions = model.predict(scaler_x)
    
    # Plot actual vs predicted power
    st.subheader("Actual vs Predicted Power")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['power'], mode='lines', name='Actual Power'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=predictions, mode='lines', name='Predicted Power', line=dict(dash='dash')))
    fig.update_layout(title='Actual vs Predicted Power', xaxis_title='Time', yaxis_title='Power')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Delta Dashboard - Past Hour Average")

    # Function to calculate average of past hour
    def past_hour_average(df, column, current_time):
        past_hour = df[(df['timestamp'] > current_time - timedelta(hours=1)) & (df['timestamp'] <= current_time)]
        return past_hour[column].mean()

    # Slider for selecting time
    max_time = data['timestamp'].max()
    min_time = data['timestamp'].min()
    selected_time = st.slider("Select Time", min_value=min_time, max_value=max_time, value=max_time, format="YYYY-MM-DD HH:mm")

    # Calculate averages
    power_avg = past_hour_average(data, 'power', selected_time)
    voltage_avg = past_hour_average(data, 'voltage', selected_time)
    current_avg = past_hour_average(data, 'current', selected_time)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Power (Past Hour Avg)", f"{power_avg:.2f}")
    col2.metric("Voltage (Past Hour Avg)", f"{voltage_avg:.2f}")
    col3.metric("Current (Past Hour Avg)", f"{current_avg:.2f}")

    # Line charts for each metric
    st.subheader("Power, Voltage, and Current Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['power'], mode='lines', name='Power'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['voltage'], mode='lines', name='Voltage'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['current'], mode='lines', name='Current'))
    fig.add_vline(x=selected_time, line_dash="dash", line_color="red")
    fig.update_layout(title='Power, Voltage, and Current Over Time', xaxis_title='Time', yaxis_title='Value')
    st.plotly_chart(fig, use_container_width=True)