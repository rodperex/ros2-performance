#!/usr/bin/env python3
""" Script to compute and show the lost messages """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parser  # Local quantif parser file

def plot_loss_over_size(lat_data, arch='simple'):
  """ Plot number of lost messages over message size.
  """
  # Filter columns
  lat_data = lat_data[['Size', 'Msg Lost', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['CPU Stress'] == 'high']
  lat_data = lat_data[lat_data['Architecture'] == arch]
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Msg Lost', hue='IPC', col='RMW', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Lost messages (#)', fontsize=15)
  plt.show()

def plot_loss_over_load(lat_data, arch='simple'):
  """ Plot number of lost messages over CPU load.
  """
  # Filter columns
  lat_data = lat_data[['Size', 'Msg Lost', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['IPC'] == 0]
  lat_data = lat_data[lat_data['Architecture'] == arch]
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Msg Lost', hue='CPU Stress', col='RMW', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Lost Messages (#)', fontsize=15)
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
    'Test Duration',
    'CPU Stress',
    'IPC'
  ]
  print(F"Latency data filtered:\n{latency_data[print_cols]}")

  # Save to CSV for outside analysis
  # latency_data.to_csv("latency_data.csv")

  plot_loss_over_size(latency_data, arch='complex')
  plot_loss_over_load(latency_data, arch='complex')

if __name__ == '__main__':
    main()
