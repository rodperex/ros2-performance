#!/usr/bin/env python3
""" This python file contains functions to
    read and parse the result files generated by
    the experiments run from "run_experiments.sh" script.

    The data is converted to Pandas DataFrame objects
    to facilitate its posterior analysis.
"""

import os
import io
import pandas as pd

# Experiment configuration to load result files
EXPERIMENT_ARCHS = ['simple', 'medium', 'complex']
RMW_IMPLEMENTATIONS = ['fast', 'cyclone', 'zenoh']
EXPERIMENT_TIMES = [300]
EXPERIMENT_STRESS = ['low', 'medium', 'high']

# Format of result files
LATENCY_RESULT_FILE_FORMAT = 'latency_all_ipc-{ipc}_{time}s_{stress}.txt'
RESOURCES_RESULT_FILE_FORMAT = 'resources_ipc-{ipc}_{time}s_{stress}.txt'

# CSV Header remapping. Original names are not used, only here for backup
ORIGINAL_LATENCY_HEADER = [
  'node',
  'topic',
  'size[b]',
  'received[#]',
  'late[#]',
  'too_late[#]',
  'lost[#]',
  'mean[us]',
  'sd[us]',
  'min[us]',
  'max[us]',
  'freq[hz]',
  'throughput[Kb/s]',
]
NEW_LATENCY_HEADER = [
  'Node',
  'Topic',
  'Size',
  'Msg Received',
  'Msg Late',
  'Msg Too Late',
  'Msg Lost',
  'Mean',
  'Std',
  'Min',
  'Max',
  'Freq',
  'Throughput',
]
ORIGINAL_RES_HEADER = [
  'time[ms]',
  'cpu[%]',
  'arena[KB]',
  'in_use[KB]',
  'mmap[KB]',
  'rss[KB]',
  'vsz[KB]',
]
NEW_RES_HEADER = [
  'Time',
  'CPU',
  # TODO: Decide which one is the important one (rss?)
  'arena',
  'in_use',
  'mmap',
  'rss',
  'vsz',
]

def add_extra_cols(data, extra_cols):
  """ Add extra columns with experiment metadata (ipc, rmw, etc) """
  for col_name, col_val in extra_cols.items():
    data[col_name] = col_val

def read_latency_file(latency_file, extra_cols={}):
  """ Read the file with the latency (all) results data and return a DataFrame """
  if not os.path.isfile(latency_file):
    print(F"ERROR: File {latency_file} does not exist! Skipping...")
  # First, manually parse the file to separate publisher/subscriber sections
  with open(latency_file, 'r') as f:
    file_lines = f.readlines()
  # Find the lines where Pubs / Subs start
  subs_idx = file_lines.index('Subscriptions stats:\n')
  pubs_idx = file_lines.index('Publishers stats:\n')
  # Read stats and convert to a single string
  sub_stats_str = ''.join(file_lines[subs_idx + 1 : pubs_idx - 1])
  pub_stats_str = ''.join(file_lines[pubs_idx + 1:])
  # Feed the stats strings to pandas and build dataframes
  data_subs = pd.read_csv(io.StringIO(sub_stats_str), sep=';', names=NEW_LATENCY_HEADER, header=0)
  data_pubs = pd.read_csv(io.StringIO(pub_stats_str), sep=';', names=NEW_LATENCY_HEADER, header=0)
  # Add a new column to differentiate between pubs and subs stats
  data_subs['Pub/Sub Type'] = 'Subscription'
  data_pubs['Pub/Sub Type'] = 'Publisher'
  data = pd.concat([data_subs, data_pubs], ignore_index=True)
  # Add extra columns with experiment metadata (ipc, rmw, etc)
  add_extra_cols(data, extra_cols)
  return data

def read_resources_file(resources_file, extra_cols={}):
  """ Read the file with the resources results data and return a DataFrame """
  data = pd.read_csv(resources_file, delim_whitespace=True, names=NEW_RES_HEADER, header=0)
  add_extra_cols(data, extra_cols)
  return data

def aggregate_results(results_path, file_template, read_file_func):
  """ Generic function to read and aggregate result files.
      Returns a DataFrame with all the data merged.
  """
  total_data = None
  for arch in EXPERIMENT_ARCHS:
    # Check if the architecture results dir exists
    if os.path.isdir(os.path.join(results_path, arch)):
      # Check if the rmw results dir exists
      for rmw in RMW_IMPLEMENTATIONS:
        test_path = os.path.join(results_path, arch, rmw)
        if os.path.isdir(test_path):
          for t in EXPERIMENT_TIMES:
            for stress in EXPERIMENT_STRESS:
              latency_file_no_ipc = file_template.format(
                ipc=0, time=t, stress=stress)
              latency_file_ipc = file_template.format(
                ipc=1, time=t, stress=stress)
              extra_cols = {
                'Architecture': arch,
                'RMW': rmw,
                'Test Duration': t,
                'CPU Stress': stress,
                'IPC': 0,
              }
              test_data_no_ipc = read_file_func(
                os.path.join(test_path, latency_file_no_ipc),
                extra_cols)
              extra_cols['IPC'] = 1
              test_data_ipc = read_file_func(
                os.path.join(test_path, latency_file_ipc),
                extra_cols)
              total_data = pd.concat(
                [total_data, test_data_no_ipc, test_data_ipc],
                ignore_index=True)
  return total_data

def aggregate_latency_results(results_path):
  """ Read all latency result files from the "results" dir.
      Return a DataFrame with all the data merged.
  """
  return aggregate_results(results_path, LATENCY_RESULT_FILE_FORMAT, read_latency_file)

def aggregate_resources_results(results_path):
  """ Read all resources result files from the "results" dir.
      Return a DataFrame with all the data merged.
  """
  return aggregate_results(results_path, RESOURCES_RESULT_FILE_FORMAT, read_resources_file)


if __name__ == '__main__':
  """ This main is for testing purposes only """
  single_latency_data = read_latency_file('../../results/simple/fast/latency_all_ipc-0_5s_low.txt')
  print(F"Single latency file data:\n{single_latency_data}")
  single_resources_data = read_resources_file('../../results/simple/fast/resources_ipc-0_5s_low.txt')
  print(F"Single resources file data:\n{single_resources_data}")
  latency_data = aggregate_latency_results('../../results')
  print(F"Latency data columns:\n{latency_data.columns}")
  print(F"Latency data:\n{latency_data}")
  latency_print_cols = [
    'Node',
    'Topic',
    'Pub/Sub Type',
    'Architecture',
    'RMW',
    'Test Duration',
    'CPU Stress',
    'IPC'
  ]
  print(F"Latency data filtered:\n{latency_data[latency_print_cols]}")
  print(F"Resources data columns:\n{res_data.columns}")
  print(F"Resources data:\n{res_data}")
  res_print_cols = [
    'Time',
    'CPU',
    'arena',
    'in_use',
    'Architecture',
    'RMW',
    'CPU Stress',
    'IPC'
  ]
  print(F"Resources data filtered:\n{res_data[res_print_cols]}")
