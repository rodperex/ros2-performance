import subprocess
import os
import yaml
import sys

def load_experiment(filename):
    """
    Loads experiment parameters from a YAML file.

    Args:
        filename: Path to the YAML file containing topology parameters.

    Returns:
        A dictionary containing the loaded parameters.
    """
    with open(filename) as f:
        params = yaml.safe_load(f)  # Use safe_load for security

    # Perform basic validation or transformation on loaded parameters if needed (optional)
    return params

ws_dir = os.getcwd()
config_file = "basic.yaml"
topology_file = "test_topology.json"
# config_file = sys.argv[1]
# topology_file = sys.argv[2]

dir_path = os.path.dirname(__file__)
pkg_dir = os.path.dirname(os.path.dirname(os.path.dirname(dir_path)))
config_file = os.path.join(pkg_dir, "irobot_benchmark", "config", "experiments", config_file)

params = load_experiment(config_file)

topology_path = os.path.join(pkg_dir, "irobot_benchmark", "topology", params["topology_file"])

ros2_cmd = ["ros2", "run", "irobot_benchmark", "irobot_benchmark",
            topology_path, "-t", str(params.get("duration", 1))]  # Set duration from params (optional)

subprocess.run(ros2_cmd)