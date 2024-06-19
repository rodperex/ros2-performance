#!/bin/bash

# Define the experiment parameters
times=(1 2)
use_ipc_values=(0 1)
load_values=("low" "medium" "high")
experiment_path="$HOME/robots/ros2/perf_ws/src/ros2-performance/quantif_experiments/results"
arch="simple"
rmw="fast"

# Function to run stress command
run_high_stress() {
  local duration=$1
  echo "Running stress command in background for $duration seconds"
  stress -c 4 -i 4 -m 6 --vm-bytes 256M -t "${duration}s" &
  stress_pid=$!
}

# Loop over the times, use_ipc values, and load values
for t in "${times[@]}"; do
  for use_ipc in "${use_ipc_values[@]}"; do
    for load in "${load_values[@]}"; do
      echo "Running experiment with -t $t, --use_ipc $use_ipc, and --load $load"

    # Run stress command
      if [ "$load" == "high" ]; then
        run_high_stress $t
      fi

      ros2 run quantif_experiments quantif --use_ipc $use_ipc -t $t --experiment_path "$experiment_path" --arch $arch --rmw $rmw --load $load --verbose 0
      echo "Experiment with -t $t, --use_ipc $use_ipc, and --load $load completed"
    done
  done
done

echo "All experiments completed"
