#!/usr/bin/env python3
""" Script to compute and show different latency metrics """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parser  # Local quantif parser file

def plot_latency_over_size(lat_data, arch='simple'):
  """ Plot latency (avg and std) over message size.
  """
  # Filter columns
  lat_data = lat_data[['Size', 'Mean', 'Std', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['CPU Stress'] == 'low']
  lat_data = lat_data[lat_data['Architecture'] == arch]
  # Use only the publishers latency for first subplot and subscription for second
  lat_data_pubs = lat_data[lat_data['Pub/Sub Type'] == 'Publisher']
  lat_data_subs = lat_data[lat_data['Pub/Sub Type'] == 'Subscription']
  print(F"Publishers Latency:\n{lat_data_pubs}")
  print(F"Subscriptions Latency:\n{lat_data_subs}")
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Mean', hue='IPC', col='RMW', row='Pub/Sub Type', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Average Latency (µs)', fontsize=15)
  plt.show()

def plot_latency_over_load(lat_data, arch='simple'):
  """ Plot latency (avg and std) over CPU load.
  """
  # Filter columns
  lat_data = lat_data[['Size', 'Mean', 'Std', 'Pub/Sub Type', 'Architecture', 'CPU Stress', 'RMW', 'IPC']]
  # Use only the experiments without CPU stress
  lat_data = lat_data[lat_data['IPC'] == 1]
  lat_data = lat_data[lat_data['Architecture'] == arch]
  # Use only the publishers latency for first subplot and subscription for second
  lat_data_pubs = lat_data[lat_data['Pub/Sub Type'] == 'Publisher']
  lat_data_subs = lat_data[lat_data['Pub/Sub Type'] == 'Subscription']
  print(F"Publishers Latency:\n{lat_data_pubs}")
  print(F"Subscriptions Latency:\n{lat_data_subs}")
  g = sns.catplot(kind='bar', data=lat_data, x='Size', y='Mean', hue='CPU Stress', col='RMW', row='Pub/Sub Type', errorbar=None)
  g.set_xlabels('Message Size (Bytes)', fontsize=15)
  g.set_ylabels('Average Latency (µs)', fontsize=15)
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

  plot_latency_over_size(latency_data, arch='complex')
  plot_latency_over_load(latency_data, arch='complex')

if __name__ == '__main__':
    main()
