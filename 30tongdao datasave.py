import pprint
import numpy as np
import matplotlib.pyplot as plt
import artdaq
import pandas as pd
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

fig, axs = plt.subplots(6, 5, figsize=(12, 10))

data_storage = {'Timestamp': [], 'Channel': [], 'Value': []}

with artdaq.Task("a") as task1:
    task1.ai_channels.add_ai_voltage_chan("Dev1/ai0:29")  

   
    while True:
     
        data = task1.read()

    
        if len(data) == 30 and all(isinstance(chan_data, float) for chan_data in data):
            current_time = datetime.now()

    
            for i, chan_data in enumerate(data):
                row = i // 5
                col = i % 5
                axs[row, col].cla()  # Clear previous plot
                axs[row, col].imshow([[chan_data]], cmap='coolwarm', aspect='auto',
                                     vmin=-10, vmax=10, extent=[0, 1, 0, 1])
                axs[row, col].set_title(f'Channel {i}')
                axs[row, col].set_xticks([])
                axs[row, col].set_yticks([])

    
                data_storage['Timestamp'].append(current_time)
                data_storage['Channel'].append(i)
                data_storage['Value'].append(chan_data)

        
            if len(data_storage['Timestamp']) >= 100:
                df = pd.DataFrame(data_storage)
                df.to_excel('channel_data.xlsx', index=False)
                data_storage = {'Timestamp': [], 'Channel': [], 'Value': []}  

            plt.pause(0.1)  

plt.tight_layout()
plt.show() 
