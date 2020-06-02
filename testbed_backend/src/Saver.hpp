/**
 * LOGICAL_NAME:    Saver.hpp
 * FUNCTION:        Output report file.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_SAVER_
#define TESTBED_BACKEND_SAVER_

#include <map>
#include <queue>
#include <string>
#include <vector>
#include "Data.hpp"

class Saver {
 private:
  std::string device;
  std::vector<DwData> data_writer_data;
  std::vector<DrData> data_reader_data;
  std::vector<ResourceData> resource_data;

  double compute_cpu_load(MonitorCpuData val, MonitorCpuData last_val);
  long long compute_bandwidth(long long val, long long last_val);

 public:
  void append_pub(std::string partition, std::string dst_topic, long pub_id,
                  long dw_id, long pub_msg_count,
                  std::map<std::string, std::vector<double>> latency);
  void append_sub(std::string partition, std::string src_topic, long sub_id,
                  long dr_id, std::map<std::string, SubMsgData> data);
  void append_resource(std::vector<MonitorData> data);
  void save(std::string device, std::string path);  // save as file
};

#endif