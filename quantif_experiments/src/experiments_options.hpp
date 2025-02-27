/* Software License Agreement (BSD License)
 *
 *  Copyright (c) 2019, iRobot ROS
 *  All rights reserved.
 *
 *  This file is part of ros2-performance, which is released under BSD-3-Clause.
 *  You may use, distribute and modify this code under the BSD-3-Clause license.
 */

#ifndef EXPERIMENTS_OPTIONS_HPP_
#define EXPERIMENTS_OPTIONS_HPP_

#include <string>

#include "cxxopts.hpp"
#include "performance_metrics/tracker.hpp"
#include "performance_test/executors.hpp"

struct ExperimentsOptions
{
public:
  ExperimentsOptions() = delete;

  ExperimentsOptions(int argc, char ** argv)
  {
    cxxopts::Options options(argv[0], "ROS2 performance experiments");

    options.add_options()("h,help", "print help")(
      "rmw", "rmw implementation (fast/cyclone/zenoh)",
      cxxopts::value<std::string>(rmw_implementation)->default_value(rmw_implementation))(
      "arch", "Architecture to test",
      cxxopts::value<std::string>(architecture)->default_value(architecture))(
      "load", "Computational load of the system (low/medium/high)",
      cxxopts::value<std::string>(load)->default_value(load))(
      "executor", "the system executor:\n\t\t\t\t1:SingleThread 2:StaticSingleThread",
      cxxopts::value<int>(executor)->default_value(std::to_string(executor)), "<1/2>")(
      "subs", "Number of subscriber nodes",
      cxxopts::value<int>(n_subscribers)->default_value(std::to_string(n_subscribers)))(
      "pubs", "Number of publisher ndoes",
      cxxopts::value<int>(n_publishers)->default_value(std::to_string(n_publishers)))(
      "clients", "Number of client nodes",
      cxxopts::value<int>(n_clients)->default_value(std::to_string(n_clients)))(
      "services", "Number of service ndoes",
      cxxopts::value<int>(n_services)->default_value(std::to_string(n_services)))(
      "msg_type", "Type of msg/service",
      cxxopts::value<std::string>(msg_type)->default_value(msg_type))(
      "msg_size", "Size of message if dynamic",
      cxxopts::value<int>(msg_size)->default_value(std::to_string(msg_size)))(
      "f,frequency", "Publish/Request frequency",
      cxxopts::value<float>(frequency)->default_value(std::to_string(frequency)))(
      "j, json", "path to the json file to load",
      cxxopts::value<std::string>(json_path)->default_value(json_path))(
      "use_ipc", "Activate IntraProcessCommunication [0/1]",
      cxxopts::value<int>(use_ipc)->default_value(std::to_string(use_ipc)))(
      "use_ros_params", "Use parameter services [0/1]",
      cxxopts::value<int>(use_ros_params)->default_value(std::to_string(use_ros_params)))(
      "ros_namespace", "Create every node under this namespace",
      cxxopts::value<std::string>(ros_namespace)->default_value(ros_namespace))(
      "t, duration", "Duration in seconds",
      cxxopts::value<int>(experiment_duration)->default_value(std::to_string(experiment_duration)))(
      "monitor_stats", "Monitor CPU, RAM and events and print them to file [0/1]",
      cxxopts::value<int>(monitor_stats)->default_value(std::to_string(monitor_stats)))(
      "sampling", "resources sampling period",
      cxxopts::value<int>(resources_sampling_per_ms)->default_value(
        std::to_string(resources_sampling_per_ms)), "msec")(
      "late-percentage",
      "a msg with greater latency than this percentage of the period is considered late",
      cxxopts::value<int>(tracking_options.late_percentage)->default_value(
        std::to_string(tracking_options.late_percentage)), "%")(
      "late-absolute",
      "a msg with greater latency than this is considered late",
      cxxopts::value<int>(tracking_options.late_absolute_us)->default_value(
        std::to_string(tracking_options.late_absolute_us)), "usec")(
      "too-late-percentage",
      "a msg with greater latency than this percentage of period is considered lost",
      cxxopts::value<int>(tracking_options.too_late_percentage)->default_value(
        std::to_string(tracking_options.too_late_percentage)), "%")(
      "too-late-absolute",
      "a msg with greater latency than this is considered lost",
      cxxopts::value<int>(tracking_options.too_late_absolute_us)->default_value(
        std::to_string(tracking_options.too_late_absolute_us)), "usec")(
      "experiment_name", "Experiment name",
      cxxopts::value<std::string>(experiment_name)->default_value(experiment_name))(
      "experiment_path", "Experiment path",
      cxxopts::value<std::string>(experiment_path)->default_value(experiment_path))(
      "verbose", "Print runtime debug information [0/1]",
      cxxopts::value<int>(verbose)->default_value(std::to_string(verbose)));

    try {
      auto result = options.parse(argc, argv);

      if (result.count("help")) {
        std::cout << options.help() << std::endl;
        exit(0);
      }
    } catch (const cxxopts::OptionException & e) {
      std::cout << "Error parsing options. " << e.what() << std::endl;
      exit(1);
    }
  }

  // Default values
  int n_subscribers = 2;
  int n_publishers = 1;
  int n_clients = 2;
  int n_services = 1;
  std::string msg_type = "stamped10b";
  int msg_size = 0;
  float frequency = 10;
  int use_ipc = 0;
  std::string json_path = "";
  int executor =
    static_cast<int>(performance_test::ExecutorType::STATIC_SINGLE_THREADED_EXECUTOR);
  int use_ros_params = 1;
  std::string ros_namespace = "";
  int verbose = 0;
  int experiment_duration = 5;
  int monitor_stats = 0;
  int resources_sampling_per_ms = 500;
  performance_metrics::Tracker::Options tracking_options {};
  std::string experiment_name = "";
  std::string experiment_path = ".";
  std::string events_file_path = "";
  std::string ru_file_path = "";
  std::string latency_file_path = "";
  // just for organization (not really used to set the experiment but for saving results)
  std::string rmw_implementation = "fast";
  std::string architecture = "simple";
  std::string load = "low";
};

#endif  // EXPERIMENTS_OPTIONS_HPP_
