
#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# TODO: The shared memory configuration breaks something. Must review.
# export ZENOH_ROUTER_CONFIG_URI=$THIS_DIR/rmw_zenoh_router_shared_config.json5
# export ZENOH_SESSION_CONFIG_URI=$THIS_DIR/rmw_zenoh_session_shared_config.json5

echo "Enablig shared memory zero-copy transport for zenoh"

# Run zenoh router from here.
# It must be stopped/killed after finishing all experiments (in main script?)
echo "Running zenoh router..."
ros2 run rmw_zenoh_cpp rmw_zenohd &
# Wait a bit until everything is up
sleep 2
