import altair as alt


# Function to plot historical data with Altair
def plot_historical_data(data, station=None):
    if station and station != "Overall":
        station_data = data[data["Process_ID"] == station]
    else:
        station_data = data

    # Convert kWh to watts
    station_data = station_data.copy()
    station_data["Energy"] *= 1000  # Convert kWh to Wh
    station_data["Predictions"] *= 1000  # Convert kWh to Wh

    actual_chart = (
        alt.Chart(station_data)
        .mark_line(color="blue", interpolate="basis")
        .encode(
            x=alt.X(
                "Timestamp:T", title="Timestamp", axis=alt.Axis(format="%Y-%m-%d %H:%M")
            ),
            y=alt.Y("Energy:Q", title="Actual Energy (W)"),
            tooltip=["Timestamp:T", "Energy:Q"],
        )
        .properties(title="Historical Energy Data")
    )

    predicted_chart = (
        alt.Chart(station_data)
        .mark_line(color="green", interpolate="basis")
        .encode(
            x=alt.X("Timestamp:T"),
            y=alt.Y("Predictions:Q", title="Predicted Energy (W)"),
            tooltip=["Timestamp:T", "Predictions:Q"],
        )
    )

    return actual_chart + predicted_chart


# Function to plot real-time data with Altair
def plot_realtime_data(data, station=None):
    if station and station != "Overall":
        station_data = data[data["Process_ID"] == station]
    else:
        station_data = data

    # Convert kWh to watts
    station_data = station_data.copy()
    station_data["Energy"] *= 1000  # Convert kWh to Wh
    station_data["Predictions"] *= 1000  # Convert kWh to Wh

    actual_chart = (
        alt.Chart(station_data)
        .mark_line(color="blue", interpolate="basis")
        .encode(
            x=alt.X(
                "Timestamp:T", title="Timestamp", axis=alt.Axis(format="%Y-%m-%d %H:%M")
            ),
            y=alt.Y("Energy:Q", title="Actual Energy (W)"),
            tooltip=["Timestamp:T", "Energy:Q"],
        )
        .properties(title="Real-Time Energy Predictions")
    )

    predicted_chart = (
        alt.Chart(station_data)
        .mark_line(color="green", interpolate="basis")
        .encode(
            x=alt.X("Timestamp:T"),
            y=alt.Y("Predictions:Q", title="Predicted Energy (W)"),
            tooltip=["Timestamp:T", "Predictions:Q"],
        )
    )

    return actual_chart + predicted_chart
