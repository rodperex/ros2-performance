
#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

export CYCLONEDDS_URI=file://$THIS_DIR/zero-copy-shm.xml

echo "Enablig shared memory zero-copy transport for cyclonedds"

# Run iox-roudi from here.
# It must be stopped/killed after finishing all experiments (in main script?)
echo "Running iox-roudi router"
iox-roudi &
# Wait a bit until everything is up
sleep 2
