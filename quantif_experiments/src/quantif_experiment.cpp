/* Software License Agreement (BSD License)
 *
 *  Copyright (c) 2019, iRobot ROS
 *  All rights reserved.
 *
 *  This file is part of ros2-performance, which is released under BSD-3-Clause.
 *  You may use, distribute and modify this code under the BSD-3-Clause license.
 */

#include <chrono>
#include <iostream>
#include <string>
#include <vector>

#include "cxxopts.hpp"
#include "performance_metrics/resource_usage_logger.hpp"
#include "performance_metrics/tracker.hpp"
#include "performance_test/system.hpp"
#include "performance_test_factory/factory.hpp"
#include "experiments_options.hpp"

using namespace std::chrono_literals;

int main(int argc, char ** argv)
{
  auto options = ExperimentsOptions(argc, argv);

  if (options.json_path.empty()) {
    std::string this_file_path = __FILE__;
    std::string this_dir_path = this_file_path.substr(0, this_file_path.rfind("/"));
    if (options.architecture == "simple")
      options.json_path = this_dir_path + std::string("/../test_archs/vff.json");
    else if (options.architecture == "medium")
      options.json_path = this_dir_path + std::string("/../test_archs/nav.json");
    else if (options.architecture == "complex")
      options.json_path = this_dir_path + std::string("/../test_archs/social.json");
    else if (options.architecture == "complex_rt")
      options.json_path = this_dir_path + std::string("/../test_archs/social_rt.json");
    else {
      std::cerr << "Architecture not recognized" << std::endl;
      return -1;
    }
  }

  std::string tail = std::string("_ipc-") + std::to_string(options.use_ipc) +
    std::string("_") + std::to_string(options.experiment_duration) +
    std::string("s_") + options.load; 

  std::cout << "Json file to load: " << options.json_path << std::endl;
  std::cout << "Intra-process-communication: " << (options.use_ipc ? "on" : "off") << std::endl;
  std::cout << "Run test for: " << options.experiment_duration << " seconds" << std::endl;
  std::cout << "Sampling resources every " << options.resources_sampling_per_ms << "ms" <<
    std::endl;
  std::cout << "Start test" << std::endl;


  std::string head = options.experiment_path +
    std::string("/") + options.architecture + std::string("/") +
    options.rmw_implementation + std::string("/");
  std::string create_output_dir_command = std::string("mkdir -p ") + head;
  auto ret = system(create_output_dir_command.c_str());
  static_cast<void>(ret);
  std::string resources_output_path =
    head + std::string("resources") + tail + std::string(".txt");
  std::string events_output_path =
    head + std::string("events") + tail + std::string(".txt");
  std::string latency_all_output_path =
    head + std::string("latency_all") + tail + std::string(".txt");
  std::string latency_total_output_path =
    head + std::string("latency_total") + tail + std::string(".txt");
  // Start resources logger
  performance_metrics::ResourceUsageLogger ru_logger(resources_output_path);
  ru_logger.start(std::chrono::milliseconds(options.resources_sampling_per_ms));

  rclcpp::init(argc, argv);

  // Architecture
  performance_test::System ros2_system(
    static_cast<performance_test::ExecutorType>(options.executor),
    performance_test::SpinType::SPIN,
    events_output_path);

  performance_test_factory::TemplateFactory factory(options.use_ipc);

  auto nodes_vec = factory.parse_topology_from_json(
    options.json_path,
    performance_metrics::Tracker::Options());

  ros2_system.add_nodes(nodes_vec);

  ros2_system.spin(std::chrono::seconds(options.experiment_duration));

  ru_logger.stop();

  std::this_thread::sleep_for(500ms);

  ros2_system.log_latency_all_stats();
  std::cout << std::endl;
  std::cout << "System total:" << std::endl;
  ros2_system.log_latency_total_stats();
  ros2_system.save_latency_all_stats(latency_all_output_path);
  ros2_system.save_latency_total_stats(latency_total_output_path);

  std::cout << std::endl;

  /* Note:
  * The shutdown was moved here because of a segfault that is
  * caused by zenoh rmw with the share_memory option enabled.
  * The cause of the segfault is still unknown.
  * This "fix" only allows us to delay the crash until the stats have been saved to disk.
  */
  rclcpp::shutdown();
}
