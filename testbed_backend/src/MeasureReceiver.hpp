/**
 * LOGICAL_NAME:    MeasureReceiver.hpp
 * FUNCTION:        Subscribe and record measure message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_MEASURE_RECEIVER_
#define TESTBED_BACKEND_MEASURE_RECEIVER_

#include <condition_variable>
#include <map>
#include <mutex>
#include <string>
#include <vector>
#include "Data.hpp"
#include "Runner.hpp"
#include "ccpp_EmulationData.h"
#include "ccpp_dds_dcps.h"

class MeasureReceiver : public Runner {
 private:
  std::mutex mtx;
  std::condition_variable cv;
  EmulationData::ProbMsgDataReader_var reader;
  DDS::WaitSet_var wait_set;
  DDS::ReadCondition_var new_msg_condition;
  DDS::GuardCondition_var escape;
  std::string device;
  std::map<long, MeasureData> data_map;
  std::map<std::string, std::map<std::string, std::vector<double>>> latencys;
  DDS::Duration_t wait_timeout = {60, 0};
  void before_join() override;
  void run() override;
  std::string to_key(std::string partition, long pub_id, long dw_id);

 public:
  MeasureReceiver(std::string device_name);
  void set_data_reader(DDS::DataReader_var dr_var);
  long request_measure(std::string dst_device, std::string partition,
                       long pub_id, long dw_id);
  std::map<std::string, std::vector<double>> get_latency(std::string partition,
                                                         long pub_id,
                                                         long dw_id);
};

#endif