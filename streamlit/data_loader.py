import pandas as pd
import joblib
import os
import asyncio
import websockets
import yaml
import io

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)


# Function to load data from a CSV file and generate predictions
def load_data_from_csv():
    try:
        file_path = config["data_sources"]["batch"]["file_path"]
        data = pd.read_csv(file_path, parse_dates=["Timestamp"])
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return pd.DataFrame()

    try:
        # Load the trained model and scaler
        model_dir = config["model"]["directory"]
        model_filename = sorted(
            [
                f
                for f in os.listdir(model_dir)
                if f.endswith(".pkl") and config["model"]["prediction_model_name"] in f
            ]
        )[-1]
        scaler_filename = sorted(
            [
                f
                for f in os.listdir(model_dir)
                if f.endswith(".pkl") and config["model"]["scaler_name"] in f
            ]
        )[-1]

        model = joblib.load(os.path.join(model_dir, model_filename))
        scaler = joblib.load(os.path.join(model_dir, scaler_filename))
    except (FileNotFoundError, IndexError):
        print("Error: Model or scaler file not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        return pd.DataFrame()

    try:
        # Create features
        data["Hour"] = data["Timestamp"].dt.hour
        data["Minute"] = data["Timestamp"].dt.minute
        data["Second"] = data["Timestamp"].dt.second

        # Select the same features as used during training
        features = [
            "Voltage",
            "Current",
            "Energy",
            "Frequency",
            "PF",
            "Hour",
            "Minute",
            "Second",
        ]
        X = data[features]

        # Scale the features
        X_scaled = scaler.transform(X)

        # Generate predictions using the trained model
        data["Predictions"] = model.predict(X_scaled)
    except Exception as e:
        print(f"Error generating predictions: {e}")
        return pd.DataFrame()

    return data


# Function to load data from a WebSocket and update the DataFrame
async def load_data_from_websocket(
    df_all,
    station_option,
    chart_placeholder,
    actual_energy_placeholder,
    predicted_energy_placeholder,
    get_current_status,
    plot_realtime_data,
):
    uri = config["data_sources"]["streaming"]["uri"]
    update_interval = config["update_interval"]

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    data = await websocket.recv()
                    # Assume data is received as a CSV string, then load it into a DataFrame
                    new_data = pd.read_csv(io.StringIO(data), parse_dates=["Timestamp"])

                    # Append new data to the existing DataFrame
                    df_all = pd.concat([df_all, new_data], ignore_index=True)

                    # Update the existing plot in the placeholder
                    chart_placeholder.altair_chart(
                        plot_realtime_data(df_all, station=station_option),
                        use_container_width=True,
                    )

                    # Get the current status (latest actual and predicted energy)
                    actual_energy, predicted_energy = get_current_status(
                        df_all, station_option
                    )

                    # Update current status metrics
                    actual_energy_placeholder.metric(
                        "Current Actual Energy (kWh)", f"{actual_energy:.2f}"
                    )
                    predicted_energy_placeholder.metric(
                        "Current Predicted Energy (kWh)", f"{predicted_energy:.2f}"
                    )
                except Exception as e:
                    print(f"Error processing data from WebSocket: {e}")
                await asyncio.sleep(update_interval)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Error: WebSocket connection closed - {e}")
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")
