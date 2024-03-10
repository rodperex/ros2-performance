import yaml


def create_topology(num_publishers, num_subscribers, topics, msg_types, publisher_configs=None):
    """
    Creates a ROS topology dictionary based on provided information.

    Args:
        num_publishers: Dictionary mapping topic names to number of publishers.
        num_subscribers: Dictionary mapping topic names to number of subscribers.
        topics: List of topic names.
        msg_types: List of message types corresponding to topics.
        publisher_configs (optional): Dictionary where keys are topic names and values are lists of publisher configurations.
            Each publisher configuration is a dictionary with keys:
                - "period_ms": Publishing period in milliseconds.
                - "msg_pass_by": Message passing mechanism.

    Returns:
        A dictionary representing the ROS topology.
    """

    nodes = []

    # Publisher node
    publisher_info = {
        "node_name": "publisher",
        "publishers": []
    }
    for topic, num_pub in num_publishers.items():
        for _ in range(num_pub):  # Loop to add publishers for each topic
            publisher_config = {}  # Initialize empty config for this publisher
            if publisher_configs and topic in publisher_configs:
                # Use configuration specific to this topic if available
                publisher_config = publisher_configs[topic][0]  # Assuming first config for now (can be extended to handle a list)
            publisher_info["publishers"].append({
                "topic_name": topic,
                "msg_type": msg_types[topics.index(topic)],
                "period_ms": publisher_config.get("period_ms", 10),  # Use default if no config provided
                "msg_pass_by": publisher_config.get("msg_pass_by", "shared_ptr")  # Use default if no config provided
            })
    nodes.append(publisher_info)

    # Subscriber node (unchanged)
    subscriber_info = {
        "node_name": "subscriber",
        "subscribers": []
    }
    for topic, num_sub in num_subscribers.items():
        for _ in range(num_sub):  # Loop to add subscribers for each topic
            subscriber_info["subscribers"].append({
                "topic_name": topic,
                "msg_type": msg_types[topics.index(topic)]
            })
    nodes.append(subscriber_info)

    return {"nodes": nodes}


def load_topology_params(filename):
    """
    Loads ROS topology parameters from a YAML file.

    Args:
        filename: Path to the YAML file containing topology parameters.

    Returns:
        A dictionary containing the loaded parameters.
    """
    with open(filename) as f:
        params = yaml.safe_load(f)  # Use safe_load for security

    # Perform basic validation or transformation on loaded parameters if needed (optional)
    return params


# Example usage
import json
import os

pkg_dir = os.path.dirname(os.path.dirname(__file__))
topology = "adv_topology"
config_file = topology + ".yaml"
out_file = topology + ".json"
config_file = os.path.join(pkg_dir, "config", "topologies", config_file)
out_file = os.path.join(pkg_dir, "scripts", "topologies", out_file)

params = load_topology_params(config_file)

num_publishers = params["num_publishers"]
num_subscribers = params["num_subscribers"]
topics = params["topics"]
msg_types = params["msg_types"]
publisher_configs = params.get("publisher_configs", None)  # Optional publisher configs

# Create topology using loaded parameters
topology = create_topology(num_publishers, num_subscribers, topics, msg_types, publisher_configs)

# Print or save the topology dictionary in JSON format

with open(out_file, "w") as f:
    json.dump(topology, f, indent=4)

