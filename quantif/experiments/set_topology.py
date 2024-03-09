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

# Example usage
filename = "test_topology.json"
topics = ["laser_topic", "image_topic", "pcl_topic", "speed_topic", "vector_topic", "byte_topic"]
msg_types = ["laser_scan", "image", "point_cloud2", "twist", "vector3", "stamped8mb"]

num_publishers = {"laser_topic": 100, "image_topic": 2, "pcl_topic": 1, "speed_topic": 1, "vector_topic": 2, "byte_topic": 1}
num_subscribers = {"laser_topic": 2, "image_topic": 1, "pcl_topic": 3, "speed_topic": 2, "vector_topic": 1, "byte_topic": 1}

# Example publisher configurations (assuming only one configuration per topic for now)
publisher_configs = {
    "laser_topic": [{
        "period_ms": 20,
        "msg_pass_by": "shared_ptr"
    }],
    "image_topic": [{
        "period_ms": 30,
        "msg_pass_by": "shared_ptr"
    }],
    "pcl_topic": [{ 
        "period_ms": 15,
        "msg_pass_by": "shared_ptr"
    }]
}

topology = create_topology(num_publishers, num_subscribers, topics, msg_types, publisher_configs)

# Print or save the topology dictionary in JSON format
import json
import os
ws_dir = os.getcwd()
filename = os.path.join(ws_dir, "src/ros2-performance/irobot_benchmark/topology", filename)
with open(filename, "w") as f:
    json.dump(topology, f, indent=4)
