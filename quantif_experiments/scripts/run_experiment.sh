#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

rmw=$1
arch=$2

# Define the experiment parameters
times=(1 2) # senconds
use_ipc_values=(0 1)
load_values=("low" "medium" "high")
experiment_path=$THIS_DIR/../results

# Validate RMW implementation
if [[ "$rmw" == "fast" ]]; then
  RMW=rmw_fastrtps_cpp
elif [[ "$rmw" == "cyclone" ]]; then
  RMW=rmw_cyclonedds_cpp
else
  echo "Unknown RMW implementation: $rmw"
  return
fi

# Validate architecture
if [[ "$arch" != "simple" && "$arch" != "medium" && "$arch" != "complex" ]]; then
  echo "Invalid architecture: $arch. Valid options are 'simple', 'medium', or 'complex'."
  return
fi

echo "Using RMW_IMPLEMENTATION=${RMW}"
export RMW_IMPLEMENTATION=$RMW

RMW_SPECIFIC_SETUP_SCRIPT=$THIS_DIR/../../scripts/rmw/$RMW/setup.sh
if [ ! -f "$RMW_SPECIFIC_SETUP_SCRIPT" ]; then
    echo "$RMW_SPECIFIC_SETUP_SCRIPT does not exist."
    echo "Can't run RMW configuration for this RMW implementation."
fi

# Invoke RMW-specific script forwarding all command-line arguments to it
source $RMW_SPECIFIC_SETUP_SCRIPT "$@"

# Function to run high stress command
run_high_stress() {
  local duration=$1
  echo "Running stress command in background for $duration seconds"
  stress -c 4 -i 4 -m 6 --vm-bytes 256M -t "${duration}s" &
  stress_pid=$!
}

exp=0
# Loop over the times, use_ipc values, and load values
for t in "${times[@]}"; do
  for use_ipc in "${use_ipc_values[@]}"; do
    for load in "${load_values[@]}"; do
      exp=$((exp+1))
      echo "-------------------------------------------------"
      echo "Running experiment $exp, with -t $t, --use_ipc $use_ipc, and --load $load"
      # Run stress command
      if [ "$load" == "high" ]; then
        run_high_stress $t
      fi

      ros2 run quantif_experiments quantif --use_ipc $use_ipc -t $t --experiment_path "$experiment_path" --arch $arch --rmw $rmw --load $load --verbose 0
      
      echo "Experiment with -t $t, --use_ipc $use_ipc, and --load $load completed"
      echo "-------------------------------------------------"
    done
  done
done

echo ""
echo "ALL $exp EXPERIMENTS COMPLETED"
echo ""
echo "-------------------------------------------------"
