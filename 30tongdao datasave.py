import pprint
import numpy as np
import matplotlib.pyplot as plt
import artdaq
import pandas as pd
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

# Create a figure for plotting
fig, axs = plt.subplots(6, 5, figsize=(12, 10))

# Initialize data storage
data_storage = {'Timestamp': [], 'Channel': [], 'Value': []}

with artdaq.Task("a") as task1:
    task1.ai_channels.add_ai_voltage_chan("Dev1/ai0:29")  # Add channels from ai0 to ai29

    # Continuous data acquisition and plotting
    while True:
        # Read data from all channels
        data = task1.read()

        # Ensure data has 30 channels and each with enough samples
        if len(data) == 30 and all(isinstance(chan_data, float) for chan_data in data):
            current_time = datetime.now()

            # Plot each channel's data as a colored square
            for i, chan_data in enumerate(data):
                row = i // 5
                col = i % 5
                axs[row, col].cla()  # Clear previous plot
                axs[row, col].imshow([[chan_data]], cmap='coolwarm', aspect='auto',
                                     vmin=-10, vmax=10, extent=[0, 1, 0, 1])
                axs[row, col].set_title(f'Channel {i}')
                axs[row, col].set_xticks([])
                axs[row, col].set_yticks([])

                # Store data for export
                data_storage['Timestamp'].append(current_time)
                data_storage['Channel'].append(i)
                data_storage['Value'].append(chan_data)

            # Export data to Excel every 100 samples (adjust as needed)
            if len(data_storage['Timestamp']) >= 100:
                df = pd.DataFrame(data_storage)
                df.to_excel('channel_data.xlsx', index=False)
                data_storage = {'Timestamp': [], 'Channel': [], 'Value': []}  # Clear storage

            plt.pause(0.1)  # Pause to update plot

plt.tight_layout()
plt.show()  # Ensure plot stays open until manually closed