    #!/bin/bash

    # Check for required arguments
    if [ $# -lt 1 ]; then
        echo "Usage: $0 <topology_file> [duration=1]"
        exit 1
    fi

    # Set variables from arguments
    topology_file="$1"
    duration="${2:-1}"  # Use default 1 if duration not provided

    # Get script directory (portable across locations)
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    # Build package root directory (assuming same directory structure as Python)
    pkg_dir="$(dirname "$script_dir")"

    # Construct topology path
    topology_path="$pkg_dir/scripts/topologies/$topology_file"

    # Build ROS 2 command
    ros2_cmd="ros2 run irobot_benchmark irobot_benchmark $topology_path -t $duration"

    # Execute the ROS 2 command
    $ros2_cmd
