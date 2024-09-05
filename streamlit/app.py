import streamlit as st
import asyncio
import yaml
from data_loader import load_data_from_csv, load_data_from_websocket
from visualization import plot_historical_data, plot_realtime_data

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

df_all = load_data_from_csv()

st.sidebar.title("Navigation")
view_option = st.sidebar.selectbox(
    "Select a view", ["Historical Data", "Real-Time Data"]
)
station_option = st.sidebar.selectbox(
    "Select a station", ["Overall"] + list(df_all["Process_ID"].unique())
)

def get_current_status(data, station=None):
    try:
        if station and station != "Overall":
            station_data = data[data["Process_ID"] == station]
        else:
            station_data = data

        latest_entry = station_data.iloc[-1]
        actual_energy = latest_entry["Energy"]
        predicted_energy = latest_entry["Predictions"]

        return actual_energy, predicted_energy
    except IndexError:
        print("Error: No data available for the selected station.")
        return 0.0, 0.0
    except Exception as e:
        print(f"Error retrieving current status: {e}")
        return 0.0, 0.0

async def main():
    if view_option == "Historical Data":
        st.subheader(f"Historical Data - {station_option}")
        st.altair_chart(
            plot_historical_data(df_all, station=station_option),
            use_container_width=True,
        )
    elif view_option == "Real-Time Data":
        st.subheader(f"Real-Time Data - {station_option}")
        chart_placeholder = st.empty()
        actual_energy_placeholder = st.metric("Current Actual Energy (kWh)", "0.00")
        predicted_energy_placeholder = st.metric("Current Predicted Energy (kWh)", "0.00")
        await load_data_from_websocket(
            df_all,
            station_option,
            chart_placeholder,
            actual_energy_placeholder,
            predicted_energy_placeholder,
            get_current_status,
            plot_realtime_data,
        )

if __name__ == "__main__":
    asyncio.run(main())
