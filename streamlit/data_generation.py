import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# Generate sample data for the given time range
def generate_sample_data(num_entries=100):
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i * 15) for i in range(num_entries)]
    stations = np.random.randint(1, 5, num_entries)
    pf = np.random.uniform(0.9, 1.0, num_entries)
    voltage = np.random.uniform(225, 235, num_entries)
    current = np.random.uniform(10, 15, num_entries)
    energy = np.random.uniform(1000, 1300, num_entries)

    data = {
        "station": stations,
        "pf": pf,
        "voltage": voltage,
        "current": current,
        "energy": energy,
        "timestamp": timestamps,
    }
    return pd.DataFrame(data)
