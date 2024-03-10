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


config_file = "adv.yaml"

if len(sys.argv) == 3: # Poor error handling
    config_file = sys.argv[1]
    topology_file = sys.argv[2]

dir_path = os.path.dirname(__file__)
pkg_dir = os.path.dirname(dir_path)
config_file = os.path.join(pkg_dir, "config", "experiments", config_file)

params = load_experiment(config_file)

topology_path = os.path.join(pkg_dir, "scripts", "topologies", params["topology_file"])

ros2_cmd = ["ros2", "run", "irobot_benchmark", "irobot_benchmark",
            topology_path, "-t", str(params.get("duration", 1))]  # Set duration from params (optional)

subprocess.run(ros2_cmd)