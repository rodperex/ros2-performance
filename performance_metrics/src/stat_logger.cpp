/* Software License Agreement (BSD License)
 *
 *  Copyright (c) 2019, iRobot ROS
 *  All rights reserved.
 *
 *  This file is part of ros2-performance, which is released under BSD-3-Clause.
 *  You may use, distribute and modify this code under the BSD-3-Clause license.
 */

#include <cmath>
#include <iomanip>
#include <ostream>
#include <string>
#include <utility>
#include <vector>

#include "performance_metrics/stat_logger.hpp"

namespace performance_metrics
{

void log_total_stats(
  uint64_t total_received,
  uint64_t total_lost,
  uint64_t total_late,
  uint64_t total_too_late,
  double average_latency,
  std::ostream & stream)
{
  double total_lost_percentage =
    static_cast<double>(total_lost) / (total_received + total_lost) * 100;
  double total_late_percentage =
    static_cast<double>(total_late) / total_received * 100;
  double total_too_late_percentage =
    static_cast<double>(total_too_late) / total_received * 100;

  // log header
  stream << "received[#]";
  stream << ";mean[us]";
  stream << ";late[#]";
  stream << ";late[%]";
  stream << ";too_late[#]";
  stream << ";too_late[%]";
  stream << ";lost[#]";
  stream << ";lost[%]";
  stream << std::endl;

  // log total values
  stream << total_received << ";";
  stream << average_latency << ";";
  stream << total_late << ";";
  stream << std::setprecision(4) << total_late_percentage << ";";
  stream << total_too_late << ";";
  stream << std::setprecision(4) << total_too_late_percentage << ";";
  stream << total_lost << ";";
  stream << std::setprecision(4) << total_lost_percentage;
  stream << std::endl;
}

void log_trackers_latency_all_stats(
  std::ostream & stream,
  const std::vector<Tracker> & trackers,
  const std::string & title)
{

  auto log_header = [&stream](const std::string & header_title)
    {
      stream << std::endl;
      stream << header_title << std::endl;
      stream << "node" << ";";
      stream << "topic" << ";";
      stream << "size[b]" << ";";
      stream << "received[#]" << ";";
      stream << "late[#]" << ";";
      stream << "too_late[#]" << ";";
      stream << "lost[#]" << ";";
      stream << "mean[us]" << ";";
      stream << "sd[us]" << ";";
      stream << "min[us]" << ";";
      stream << "max[us]" << ";";
      stream << "freq[hz]" << ";";
      stream << "throughput[Kb/s]";
      stream << std::endl;
    };

  auto log_stats_line = [&stream](
    const Tracker & tracker)
    {
      stream << tracker.get_node_name() << ";";
      stream << tracker.get_entity_name() << ";";
      stream << tracker.size() << ";";
      stream << tracker.received() << ";";
      stream << tracker.late() << ";";
      stream << tracker.too_late() << ";";
      stream << tracker.lost() << ";";
      stream << std::round(tracker.stat().mean()) << ";";
      stream << std::round(tracker.stat().stddev()) << ";";
      stream << std::round(tracker.stat().min()) << ";";
      stream << std::round(tracker.stat().max()) << ";";
      stream << tracker.frequency() << ";";
      stream << (tracker.throughput() / 1024);

      stream << std::endl;
    };

  if (trackers.empty()) {
    return;
  }

  log_header(title);
  for (const auto & tracker : trackers) {
    log_stats_line(tracker);
  }
}

void log_trackers_latency_total_stats(
  std::ostream & stream,
  const std::vector<Tracker> & trackers)
{
  uint64_t total_received = 0;
  uint64_t total_lost = 0;
  uint64_t total_late = 0;
  uint64_t total_too_late = 0;
  double total_latency = 0;

  // collect total data
  for (const auto & tracker : trackers) {
    total_received += tracker.received();
    total_lost += tracker.lost();
    total_late += tracker.late();
    total_too_late += tracker.too_late();
    total_latency += tracker.received() * tracker.stat().mean();
  }

  double average_latency = std::round(total_latency / total_received);

  log_total_stats(
    total_received, total_lost, total_late, total_too_late,
    average_latency, stream);
}

}  // namespace performance_metrics
