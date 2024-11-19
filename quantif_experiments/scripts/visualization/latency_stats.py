#!/usr/bin/env python3
""" Script to compute and show different latency metrics """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parser  # Local quantif parser file

archs = {
  'simple': '../../test_archs/vff.json',
  'medium': '../../test_archs/nav.json',
  'complex': '../../test_archs/social.json',
}
ARCH = 'complex'

def plot_latency_over_size(lat_data, arch='simple'):
  """ Plot latency (avg and std) over message size. """
  # Filter columns
  lat_data = lat_data[['Size', 'Mean', 'Std', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  test_load = 'high'
  lat_data = lat_data[lat_data['CPU Stress'] == test_load]
  lat_data = lat_data[lat_data['Architecture'] == arch]
  # Use only the subscription latency, because it includes the total time between publish and callback
  lat_data = lat_data[lat_data['Pub/Sub Type'] == 'Subscription']
  print(F"Latency data:\n{lat_data}")
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Mean', hue='IPC', col='RMW', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Average Latency (µs)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'Latency over msg size, RMW and IPC  -  Architecture: {ARCH} | CPU load: {test_load}')
  plt.show()

def plot_latency_over_load(lat_data, arch='simple'):
  """ Plot latency (avg and std) over CPU load. """
  # Filter columns
  lat_data = lat_data[['Size', 'Mean', 'Std', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['IPC'] == 1]
  lat_data = lat_data[lat_data['Architecture'] == arch]
  # Use only the subscription latency, because it includes the total time between publish and callback
  lat_data = lat_data[lat_data['Pub/Sub Type'] == 'Subscription']
  print(F"Latency data:\n{lat_data}")
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Mean', hue='CPU Stress', col='RMW', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Average Latency (µs)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'Latency over msg size, RMW and load  -  Architecture: {ARCH} | IPC: ON')
  plt.show()

def main():
  latency_data = parser.aggregate_latency_results('../../results/roscon_sevilla')
  print(F"Latency data columns:\n{latency_data.columns}")
  print(F"Latency data:\n{latency_data}")
  print_cols = [
    'Node',
    'Topic',
    'Pub/Sub Type',
    'Architecture',
    'RMW',
    'Test Duration',
    'CPU Stress',
    'IPC'
  ]
  print(F"Latency data filtered:\n{latency_data[print_cols]}")

  # Save to CSV for outside analysis
  # latency_data.to_csv("latency_data.csv")

  plot_latency_over_size(latency_data, arch=ARCH)
  plot_latency_over_load(latency_data, arch=ARCH)

  # Filter dataset by visualization topics in the selected architecture
  viz_topics = parser.get_visualization_topics(archs[ARCH])
  print(F"Visualization topics:\n{viz_topics}")
  filt_data = filter_dataframe_by_viz_topics(latency_data, viz_topics)
  df_display = filt_data[['Topic','Node']].drop_duplicates()
  print(F"Filtered data:\n{filt_data}")
  print(F"Filtered data disp:\n{df_display}")

if __name__ == '__main__':
    main()
