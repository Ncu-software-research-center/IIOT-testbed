/**
 * LOGICAL_NAME:    Sender.cpp
 * FUNCTION:        Publish message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Sender.hpp"
#include "dds_debug.hpp"

using namespace std;

#define TIMER_RELATIVE 0
#define MS_PER_SEC 1000
#define MS_PER_NSEC 1000000
#define WAKE_UP_TIME_NSEC 0

namespace {

string spawn_message(long size) { return string(size, '@'); }

timespec ms_to_timespec(unsigned long ms) {
  timespec tmp;
  tmp.tv_sec = ms / MS_PER_SEC;
  tmp.tv_nsec = (ms % MS_PER_SEC) * MS_PER_NSEC - WAKE_UP_TIME_NSEC;
  return tmp;
}

}  // namespace

Sender::Sender(MeasureReceiver* measure, long id, long pub_id,
               std::string device_name, std::string topic_name,
               std::string partition_name, long measure_count, long msg_size,
               unsigned long msg_cycletime) {
  this->measure = measure;
  this->id = id;
  this->pub_id = pub_id;
  this->device = device_name + "-" + to_string(pub_id) + "-" + to_string(id);
  this->dst_topic = topic_name;
  this->partition = partition_name;
  this->measure_count_max = measure_count;
  this->measure_count = measure_count;
  this->message = spawn_message(msg_size);
  this->wait_timeout = ms_to_timespec(msg_cycletime);
}

void Sender::set_data_writer(DDS::DataWriter_var dw) {
  // set data writer
  writer = EmulationData::MsgDataWriter::_narrow(dw);
  _check_handle(writer.in(),
                DEBUG_MSG("EmulationData::MsgDataWriter::_narrow failed"));
  // create msg
  msg.device_name = DDS::string_dup(device.c_str());
  msg.msg_id = 0;
  msg.prob_id = 0;
  msg.message = DDS::string_dup(message.c_str());
}

void Sender::run() {
  clock_nanosleep(CLOCK_MONOTONIC, TIMER_RELATIVE, &wait_timeout, NULL);
  DDS::ReturnCode_t status;
  unsigned long prob_id = 0;
  if (measure_count == measure_count_max) {
    prob_id = measure->request_measure(device, partition, pub_id, id);
    measure_count = 1;
  } else {
    measure_count++;
  }
  msg.prob_id = prob_id;
  status = writer->write(msg, DDS::HANDLE_NIL);
  _check_status(status,
                DEBUG_MSG("EmulationData::MsgDataWriter::write failed"));
  DEBUG_LOG(device + ", " + string(msg.device_name.in()) + ", " +
            to_string(msg.msg_id));
  msg.msg_id++;
  pub_msg_count++;
}

long Sender::get_pub_msg_count() { return pub_msg_count; }

timespec Sender::get_wait_timeout() { return wait_timeout; }

long Sender::get_pub_id() { return pub_id; }

long Sender::get_dw_id() { return id; }

string Sender::get_device() { return device; }

string Sender::get_partition() { return partition; }

string Sender::get_dst_topic() { return dst_topic; }
