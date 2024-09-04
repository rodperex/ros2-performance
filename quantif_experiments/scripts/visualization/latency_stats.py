#!/usr/bin/env python3
""" Script to compute and show different latency metrics """

import pandas as pd
import parser  # Local quantif parser file



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
  latency_data.to_csv("latency_data.csv")


if __name__ == '__main__':
    main()
