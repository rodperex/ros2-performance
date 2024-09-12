#!/usr/bin/env python3
""" Script to compute and show different resources usage metrics """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parser  # Local quantif parser file

ARCH = 'simple'


def plot_cpu_time(res_data):
  """ Plot CPU usage data over time """
  # Filter columns
  cpu_data = res_data[['Time', 'Architecture', 'CPU', 'RMW', 'IPC']]
  # cpu_data = cpu_data[cpu_data['Architecture'] == ARCH]
  # cpu_data = cpu_data[cpu_data['Time'] >= 20000]
  # Option 1: Combine RMW and IPC as hue. Here we should manually set line colors and styles
  # hue = cpu_data['RMW'].astype(str) + ', ' + cpu_data['IPC'].astype(str)
  # g = sns.lineplot(data=cpu_data, x='Time', y='CPU', hue=hue)
  # Option 2: Use RMW as hue and IPC as style
  # g = sns.lineplot(data=cpu_data, x='Time', y='CPU', hue='RMW', style='IPC')
  # Adjust legend title
  # g.legend().set_title('RMW and IPC use')
  # Option 3: facet grid by architecture
  g = sns.relplot(kind='line', data=cpu_data, x='Time', y='CPU', hue='RMW', style='IPC', col='Architecture')
  g.set_xlabels('Time (ms)', fontsize=15)
  g.set_ylabels('CPU (%)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'CPU usage by architecture')
  plt.show()

def plot_memory_usage(res_data):
  """ Plot Memory (rss) usage data over time """
  mem_key = 'rss'
  # Filter columns
  mem_data = res_data[['Time', 'Architecture', mem_key, 'RMW', 'IPC']]
  # mem_data = mem_data[mem_data['Architecture'] == ARCH]
  # Option 1: Combine RMW and IPC as hue. Here we should manually set line colors and styles
  # hue = mem_data['RMW'].astype(str) + ', ' + mem_data['IPC'].astype(str)
  # g = sns.lineplot(data=mem_data, x='Time', y=mem_key, hue=hue)
  # Option 2: Use RMW as hue and IPC as style
  # g = sns.lineplot(data=mem_data, x='Time', y=mem_key, hue='RMW', style='IPC')
  # Adjust legend title
  # g.legend().set_title('RMW and IPC use')
  # Option 3: facet grid by architecture
  g = sns.relplot(kind='line', data=mem_data, x='Time', y=mem_key, hue='RMW', style='IPC', col='Architecture')
  g.set_xlabels('Time (ms)', fontsize=15)
  g.set_ylabels('Memory - RSS (KB)', fontsize=15)
  # Put a global title to the plot
  g.fig.subplots_adjust(top=0.92)
  g.fig.suptitle(F'Memory usage by architecture')
  plt.show()


def main():
  res_data = parser.aggregate_resources_results('../../results')
  print(F"Resources data columns:\n{res_data.columns}")
  # Use only the data from experiments with no extra CPU stress
  res_data = res_data[res_data['CPU Stress'] == 'low']
  print(F"Resources data:\n{res_data}")
  print_cols = [
    'Time',
    'CPU',
    'arena',
    'in_use',
    'Architecture',
    'RMW',
    'IPC'
  ]
  print(F"Resources data filtered:\n{res_data[print_cols]}")

  plot_cpu_time(res_data)
  plot_memory_usage(res_data)

if __name__ == '__main__':
    main()
