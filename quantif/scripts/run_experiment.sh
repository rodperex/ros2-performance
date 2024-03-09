#!/bin/bash

# Function to pause execution and wait for keypress
pause() {
    read -n 1 -s -r -p "Press any key to continue..."
    echo
}

# Check for required arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <config_file>"
    pause
    exit 1
fi

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "Error: yq is not installed. Please install yq (https://github.com/mikefarah/yq) and try again."
    pause
    exit 1
fi

# Get script directory (portable across locations)
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Build package root directory (assuming same directory structure as Python)
pkg_dir="$(dirname "$script_dir")"

# Load parameters from YAML file
config_file="$1"
if [ ! -f "$pkg_dir/config/experiments/$config_file" ]; then
    echo "Error: Configuration file '$config_file' not found in '$pkg_dir/config/experiments/'."
    pause
    exit 1
fi

# Read parameters from YAML file using yq
topology_file=$(yq eval '.topology_file' "$pkg_dir/config/experiments/$config_file")
duration=$(yq eval '.duration // 1' "$pkg_dir/config/experiments/$config_file")  # Default duration to 1 if not provided


# Construct topology path
topology_path="$pkg_dir/scripts/topologies/$topology_file"

# Build ROS 2 command   
ros2_cmd="ros2 run irobot_benchmark irobot_benchmark $topology_path -t $duration"

# Execute the ROS 2 command
echo "Executing ROS 2 command:"
echo "$ros2_cmd"
$ros2_cmd

