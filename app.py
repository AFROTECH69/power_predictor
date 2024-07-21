import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import mean_squared_error

# Load the data
data = pd.read_csv('combined_output.csv')

# Load the model and scaler
with open('src/randomforest_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('x_scaler.pkl', 'rb') as f:
    scaler_x = pickle.load(f)

# Convert 'timestamp' column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y_%m_%d_%H_%M')

# Filter data for the 19th of any month
# data = data[data['timestamp'].dt.day == 20]

# Streamlit app
st.title('Energy Consumption Dashboard')

tab1, tab2 = st.tabs(["Energy Consumption Status", "Predicted Power"])

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
    



