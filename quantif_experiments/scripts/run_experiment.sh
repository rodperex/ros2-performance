#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

rmw=$1
arch=$2
use_ipc=$3

# Define the experiment parameters
times=(1200) # seconds
# use_ipc_values=(0 1)
load_values=("low" "medium" "high")
# load_values=("high")
experiment_path=$THIS_DIR/../results

# Validate RMW implementation
if [[ "$rmw" == "fast" ]]; then
  RMW=rmw_fastrtps_cpp
elif [[ "$rmw" == "cyclone" ]]; then
  RMW=rmw_cyclonedds_cpp
elif [[ "$rmw" == "zenoh" ]]; then
  RMW=rmw_zenoh_cpp
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

num_cpus=$(nproc)
total_ram=$(free -m | awk '/^Mem:/ {print $2}')

# Function to run stress command
run_stress() {
  local level=$1
  local duration=$2
  local stressing=0

  if [ -z "$total_ram" ] || [ -z "$num_cpus" ]; then
    echo "Error: total_ram or num_cpus is not set."
    return
  fi

  if ! command -v stress &> /dev/null; then
    echo "Error: stress command not found. Please install it and try again."
    return
  fi

  case $level in
    "high")
      local mem=$((total_ram / 2))
      local cpus=$num_cpus
      local io_ops=$((num_cpus / 2))
      stressing=1
      ;;
    "medium")
      local mem=$((total_ram / 4))
      local cpus=$((num_cpus / 2))
      local io_ops=$((num_cpus / 4))
      stressing=1
      ;;
    "low")
      stressing=0
      ;;
    *)
      echo "Invalid level specified. Use 'low', 'high' or 'medium'."
      exit 1
      ;;
  esac

  if [ $stressing -eq 0 ]; then
    echo "Not running stress command"
    return
  elif [ $stressing -eq 1 ]; then
    echo "Running stress command with the following parameters:"
    echo "  - Memory: ${mem}M"
    echo "  - CPUs: $cpus"
    echo "  - IO operations: $io_ops"
    stress -c $cpus -i $io_ops -m 1 --vm-bytes "${mem}M" -t "${duration}s" &
    stress_pid=$!
  fi
}

exp=0
# Loop over the times and load values
for t in "${times[@]}"; do
  for load in "${load_values[@]}"; do
    exp=$((exp+1))
    echo "-------------------------------------------------"
    echo "Running experiment $exp, with -t $t, --use_ipc $use_ipc, and --load $load"

    run_stress $load $t

    ros2 run quantif_experiments quantif --use_ipc $use_ipc -t $t --experiment_path "$experiment_path" --arch $arch --rmw $rmw --load $load --verbose 0

    # Wait for stress command to finish if it was started in the background
    if [ "$load" = "high" ] || [ "$load" = "medium" ]; then
      echo "Waiting for stress command to finish"
      wait "$stress_pid"
    fi

    echo "Experiment with -t $t, --use_ipc $use_ipc, and --load $load completed"
    echo "-------------------------------------------------"
  done
done

# After running experiments, stop shared-memory routers
if [[ "$rmw" == "cyclone" ]]; then
  echo "Stopping iox-roudi router..."
  killall iox-roudi
elif [[ "$rmw" == "zenoh" ]]; then
  echo "Stopping zenoh router..."
  killall rmw_zenohd
fi

echo ""
echo "ALL $exp EXPERIMENTS COMPLETED"
echo ""
echo "-------------------------------------------------"
