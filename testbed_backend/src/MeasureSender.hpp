/**
 * LOGICAL_NAME:    MeasureSender.hpp
 * FUNCTION:        Publish measure message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_MEASURE_SENDER_
#define TESTBED_BACKEND_MEASURE_SENDER_

#include <condition_variable>
#include <mutex>
#include <queue>
#include <string>
#include "Data.hpp"
#include "Runner.hpp"
#include "ccpp_EmulationData.h"
#include "ccpp_dds_dcps.h"

class MeasureSender : public Runner {
 private:
  std::mutex mtx;
  std::condition_variable cv;
  EmulationData::ProbMsgDataWriter_var writer;
  std::queue<ProbMsgData> data_queue;
  EmulationData::ProbMsg msg;
  std::string device;

  void run() override;
  void before_join() override;

 public:
  MeasureSender(std::string device_name);
  void set_data_writer(DDS::DataWriter_var dw_var);
  void request_measure(std::string dst_device, std::string src_device, long prob_id);
};

#endif