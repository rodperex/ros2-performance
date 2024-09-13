#!/bin/bash

archs=(complex_rt)
use_ipc_values=(1)
rmws=(fast cyclone) # Zenoh runs isolated after these


# First run all fast and cyclone tests
for arch in "${archs[@]}"; do
  for rmw in "${rmws[@]}"; do
    for use_ipc in "${use_ipc_values[@]}"; do
      bash run_experiment.sh $rmw $arch $use_ipc
      sleep 4
    done
  done
done

# Then run zenoh tests without IPC
# for arch in "${archs[@]}"; do
#   bash run_experiment.sh zenoh $arch 0
#   sleep 4
# done

# Finally run zenoh tests with IPC (with its special config)
export ZENOH_ROUTER_CONFIG_URI=/home/franmore/ros2/quantif_ws/src/ros2-performance/scripts/rmw/rmw_zenoh_cpp/rmw_zenoh_router_shared_config.json5
export ZENOH_SESSION_CONFIG_URI=/home/franmore/ros2/quantif_ws/src/ros2-performance/scripts/rmw/rmw_zenoh_cpp/rmw_zenoh_session_shared_config.json5
for arch in "${archs[@]}"; do
    bash run_experiment.sh zenoh $arch 1
    sleep 4
done
