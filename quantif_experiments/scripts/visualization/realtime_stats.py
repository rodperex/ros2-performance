#!/usr/bin/env python3
""" Script to compute and show different latency metrics """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parser  # Local quantif parser file

def plot_latency_over_load(lat_data, arch='complex'):
  """ Plot latency (avg and std) over CPU load.
  """
  # Filter columns
  lat_data = lat_data[['Size', 'Mean', 'Std', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['IPC'] == 1]
  # lat_data = lat_data[(lat_data['Architecture'] == 'complex') | (lat_data['Architecture'] == 'complex_rt')]
  lat_data = lat_data[lat_data['Architecture'] == arch]
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Mean', hue='CPU Stress', col='RMW', row='Pub/Sub Type', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Average Latency (µs)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'Latency over msg size, RMW and load  -  Architecture: {arch} | IPC: ON')
  plt.show()


def main():
  latency_data = parser.aggregate_latency_results('../../results')
  print(F"Latency data columns:\n{latency_data.columns}")
  print(F"Latency data:\n{latency_data}")
  print_cols = [
    'Node',
    'Topic',
    'Pub/Sub Type',
    'Architecture',
    'RMW',
    'CPU Stress',
    'Mean',
  ]

  # Filter dataset by architecture
  filt_data = latency_data[(latency_data['Architecture'] == 'complex') | (latency_data['Architecture'] == 'complex_rt')]
  # Keep only experiments with IPC enabled
  filt_data = filt_data[filt_data['IPC'] == 1]

  # Filter dataset and keep only topics from critical path
  critical_path_topics = parser.get_critical_path('../../test_archs/social_rt.json')
  print(F"Topics in critical path:\n{critical_path_topics}")
  filt_data = filt_data[filt_data['Topic'].isin(critical_path_topics)]

  print(F"Latency data filtered:\n{filt_data[print_cols]}")

  # Group by architecture and add latencies
  grouped_lat = filt_data.groupby(['Architecture', 'RMW', 'CPU Stress'], as_index=False).sum()

  print_cols = [
    'Mean',
  ]
  print(grouped_lat[print_cols])
  # grouped_lat.plot(kind='bar', y='Mean')
  g = sns.catplot(kind='bar', data=grouped_lat, x='RMW', y='Mean',
                  hue='Architecture', col='CPU Stress',
                  order=['fast', 'cyclone', 'zenoh'],
                  col_order=['low', 'medium', 'high'],
                  errorbar=None)

  g.set_xlabels('RMW', fontsize=15)
  g.set_ylabels('End-to-End Latency (µs)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'End-to-end latency on critical path   -   IPC: ON')

  plt.show()
  # Save to CSV for outside analysis
  # latency_data.to_csv("latency_data.csv")

  # plot_latency_over_load(latency_data, arch='complex')
  # plot_latency_over_load(latency_data, arch='complex_rt')

if __name__ == '__main__':
    main()
