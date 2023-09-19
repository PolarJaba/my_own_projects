import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# data loading
station_data = pd.read_csv('wr213602.txt', sep=';', header=None,
                           names=['station_id', 'year', 'month', 'day', 'mean_temperature'])

# data reformat
station_data['date'] = station_data['year'].astype(str) + station_data['month'].astype(str) + station_data['day'].astype(str)
station_data['date'] = pd.to_datetime(station_data['date'], format='%Y%m%d')

# statistics
station = station_data['station_id'].values[0].astype(str)
period = (f"from {pd.to_datetime(station_data['date'][0], format='%Y%m%d')} to "
          f"{pd.to_datetime(station_data['date'].values[-1], format='%Y%m%d')}")
mean_value = np.nanmean(station_data.mean_temperature)
std_temp = station_data['mean_temperature'].std()
cv = std_temp / mean_value
max_value = max(station_data['mean_temperature'])
min_value = min(station_data['mean_temperature'])
range_temp = max_value - min_value
asymm = station_data['mean_temperature'].skew()
ex = station_data['mean_temperature'].kurtosis()

# summary df
params = pd.DataFrame({'parameters': ['STATION', 'PERIOD', 'MEAN', 'MAX', 'MIN', 'RANGE', 'STD', 'DISPERSION',
                                      'VARIATION COEFFICIENT', 'ASYMMETRY COEFFICIENT', 'EXCESS'],
                       'values': [station, period, round(mean_value, 1), round(max_value, 1), round(min_value, 1),
                                  round(range_temp, 1), round(std_temp, 1), round(std_temp ** 2, 1), round(cv, 2),
                                  round(asymm, 2), round(ex, 2)]})

params.to_csv('stat_params_summer_2022.csv', index=False)

# create figure contains graphs
plt.figure(figsize=(8, 10))

# AVG, STD, RANGE on graph
plt.subplot(2, 1, 1)
plt.plot(station_data.date, station_data.mean_temperature, color='red', linewidth=3)
plt.title('Daily mean temperature in summer 2022, Abakan')
plt.xlabel('Date')
plt.xticks(rotation=20)
plt.ylabel('Temperature')

# AVG
plt.axhline(y=mean_value, color='black', linewidth=3, label='AVG')

# RANGE
plt.axhline(y=max_value, color='blue', linestyle='--', linewidth=3, label='RANGE')
plt.axhline(y=min_value, color='blue', linestyle='--', linewidth=3)

# STD
plt.axhline(y=mean_value + std_temp, color='black', linestyle='--', linewidth=3, label='STD')
plt.axhline(y=mean_value - std_temp, color='black', linestyle='--', linewidth=3)

plt.legend()

# histogram count
hist, bins = np.histogram(station_data['mean_temperature'], bins=10)
cumulative_counts = np.cumsum(hist) / len(station_data)
print(cumulative_counts)

# Density histogram
plt.subplot(2, 2, 3)
plt.bar(bins[1:], hist, color='lightblue', edgecolor='darkblue', linewidth=1, width=1)  # bins=int(len(station_data) ** 1/2)
plt.title('Histogram of daily temperature')
plt.xlabel('Temperature')
plt.ylabel('Density')

# Кривая обеспеченности
plt.subplot(2, 2, 4)
plt.bar(bins[1:], cumulative_counts, linewidth=3, width=1, color='black')  # yerr=std_error
plt.title('Density cumulative hist')
plt.xlabel('Temperature')
plt.ylabel('Cumulative density')

# MAX, MEAN, MIN
plt.axvline(x=min_value, color='red', linestyle='--', linewidth=1, label='Extremes')
plt.axvline(x=max_value, color='red', linestyle='--', linewidth=1)
plt.axvline(x=mean_value, color='green', linestyle='--', linewidth=1, label='Mean')
plt.legend()

plt.subplots_adjust(hspace=0.5)

plt.savefig('all_stat_graph.png', dpi=300)
