/**
 * LOGICAL_NAME:    Receiver.hpp
 * FUNCTION:        Subscribe normal message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_RECEIVER_
#define TESTBED_BACKEND_RECEIVER_

#include <map>
#include <queue>
#include <set>
#include <string>
#include "Data.hpp"
#include "MeasureSender.hpp"
#include "Runner.hpp"
#include "ccpp_EmulationData.h"
#include "ccpp_dds_dcps.h"

class Receiver : public Runner {
 private:
  MeasureSender* measure;
  EmulationData::MsgDataReader_var reader;
  DDS::WaitSet_var wait_set;
  DDS::ReadCondition_var new_msg_condition;
  DDS::GuardCondition_var escape;
  long id;
  long sub_id;
  std::string device;
  std::string src_topic;
  std::string partition;
  std::queue<EmulationData::MsgSeq> data_queue;
  std::queue<DDS::SampleInfoSeq> info_queue;
  std::map<std::string, SubMsgData> data;  // device_name:SubMsgData
  DDS::Duration_t wait_timeout = {60, 0};
  void run() override;
  void before_join() override;
  void after_stop() override;

 public:
  Receiver(MeasureSender* measure, long id, long sub_id,
           std::string device_name, std::string topic_name,
           std::string partition_name);
  void set_data_reader(DDS::DataReader_var dr);
  long get_sub_id();
  long get_dr_id();
  std::string get_partition();
  std::string get_src_topic();
  std::map<std::string, SubMsgData> get_data();
};

#endif
