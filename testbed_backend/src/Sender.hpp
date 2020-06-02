/**
 * LOGICAL_NAME:    Sender.hpp
 * FUNCTION:        Publish message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_SENDER_
#define TESTBED_BACKEND_SENDER_

#include <ctime>
#include <string>
#include "Data.hpp"
#include "MeasureReceiver.hpp"
#include "Runner.hpp"
#include "ccpp_EmulationData.h"
#include "ccpp_dds_dcps.h"

class Sender : public Runner {
 private:
  MeasureReceiver* measure;
  EmulationData::MsgDataWriter_var writer;
  EmulationData::Msg msg;
  long id;
  long pub_id;
  std::string device;
  std::string dst_topic;
  std::string partition;
  std::string message;
  long measure_count_max = 100;
  long measure_count = 1;
  long pub_msg_count = 0;
  timespec wait_timeout = {1, 0};
  void run() override;

 public:
  Sender(MeasureReceiver* measure, long id, long pub_id,
         std::string device_name, std::string topic_name,
         std::string partition_name, long measure_count, long msg_size,
         unsigned long msg_cycletime);
  void set_data_writer(DDS::DataWriter_var dw);
  long get_pub_msg_count();
  timespec get_wait_timeout();
  long get_pub_id();
  long get_dw_id();
  std::string get_device();
  std::string get_partition();
  std::string get_dst_topic();
};

#endif
