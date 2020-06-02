/**
 * LOGICAL_NAME:    Monitor.hpp
 * FUNCTION:        Monitor cpu usage, memory consumption and network bandwidth.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_MONITOR_
#define TESTBED_BACKEND_MONITOR_

#include <string>
#include <vector>
#include "Data.hpp"
#include "Runner.hpp"

class Monitor : public Runner {
 private:
  void run() override;
  std::vector<MonitorData> data;
  std::string interface;
  long long get_bandwidth(std::string bandwidth);
  void get_interface();
  void get_cpu_time(unsigned long long &total_user,
                    unsigned long long &total_user_low,
                    unsigned long long &total_sys,
                    unsigned long long &total_idle);

 public:
  Monitor();
  std::vector<MonitorData> get_data();
  MonitorCpuData get_cpu();  // return value is percentage.
  double get_ram();          // return value is percentage.
  long long get_rx();        // return value unit is byte.
  long long get_tx();        // return value unit is byte.
};

#endif