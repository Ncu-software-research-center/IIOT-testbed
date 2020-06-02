/**
 * LOGICAL_NAME:    MeasureReceiver.cpp
 * FUNCTION:        Subscribe and record measure message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "MeasureReceiver.hpp"
#include <ctime>
#include <iomanip>
#include <sstream>
#include "dds_debug.hpp"

using namespace std;

static long prob_id = 0;

namespace {

double convert_time_to_double(long sec, long nanosec) {
  stringstream ss;
  ss << sec;
  ss << "." << setfill('0') << setw(9) << nanosec;
  return stod(ss.str());
}

double measure_latency(timespec receive_time, long send_sec, long send_nanosec,
                       long dst_receive_sec, long dst_receive_nanosec,
                       long dst_send_sec, long dst_send_nanosec) {
  // dst_delay: internal delay in destination device (receive message to send
  // measure message) dst_delay = dst_send_time - dst_receive_time latency:
  // message latency (send message to receive measure message) function: latency
  // = (receive_time - send_time)/2 - dst_delay
  double dst_delay = 0;
  double latency = 0;
  dst_delay += convert_time_to_double(dst_send_sec, dst_send_nanosec);
  dst_delay -= convert_time_to_double(dst_receive_sec, dst_receive_nanosec);
  latency += convert_time_to_double(receive_time.tv_sec, receive_time.tv_nsec);
  latency -= convert_time_to_double(send_sec, send_nanosec);
  latency /= 2;
  latency -= dst_delay;
  return latency;
}

string get_device_name(const char* src_device) {
  string tmp = string(src_device);
  size_t pos = tmp.find("-");
  string device_name = tmp.substr(0, pos);
  return device_name;
}

long get_prob_id() {
  prob_id++;
  return prob_id;
}

}  // namespace

MeasureReceiver::MeasureReceiver(string device_name) {
  this->device = device_name;
}

void MeasureReceiver::set_data_reader(DDS::DataReader_var dr_var) {
  DDS::ReturnCode_t status;
  reader = EmulationData::ProbMsgDataReader::_narrow(dr_var);
  _check_handle(reader.in(),
                DEBUG_MSG("EmulationData::ProbMsgDataReader::_narrow failed"));
  // create read condition that will contain new Msg only
  new_msg_condition = reader->create_readcondition(
      DDS::NOT_READ_SAMPLE_STATE, DDS::NEW_VIEW_STATE | DDS::NOT_NEW_VIEW_STATE,
      DDS::ANY_INSTANCE_STATE);
  _check_handle(
      new_msg_condition.in(),
      DEBUG_MSG("EmulationData::MsgDataReader::create_readcondition failed"));
  escape = new DDS::GuardCondition();
  // create waitset and attach condition
  wait_set = new DDS::WaitSet();
  status = wait_set->attach_condition(new_msg_condition.in());
  _check_status(status, DEBUG_MSG("DDS::WaitSet::attach_condition failed"));
  status = wait_set->attach_condition(escape.in());  // GuardCondition
  _check_status(status, DEBUG_MSG("DDS::WaitSet::attach_condition failed"));
}

void MeasureReceiver::run() {
  DDS::ReturnCode_t status;
  DDS::ConditionSeq guard_list;
  guard_list.length(2);
  EmulationData::ProbMsgSeq msg_seq;
  DDS::SampleInfoSeq info_seq;
  // wait until new_msg_condition triggers
  status = wait_set->wait(guard_list, wait_timeout);
  if (status == DDS::RETCODE_OK) {
    for (DDS::ULong i = 0; i < guard_list.length(); ++i) {
      if (guard_list[i].in() == new_msg_condition.in()) {
        // take message
        status = reader->take_w_condition(
            msg_seq, info_seq, DDS::LENGTH_UNLIMITED, new_msg_condition);
        _check_status(
            status,
            DEBUG_MSG(
                "EmulationData::ProbMsgDataReader::take_w_condition failed"));
        // compute latency
        for (DDS::ULong j = 0; j < msg_seq.length(); ++j) {
          if (info_seq[j].valid_data &&
              info_seq[j].sample_state == DDS::NOT_READ_SAMPLE_STATE) {
            timespec receive_time;
            clock_gettime(CLOCK_MONOTONIC, &receive_time);
            map<long, MeasureData>::iterator it =
                data_map.find(msg_seq[j].prob_id);
            if (it != data_map.end()) {
              if (device == get_device_name(msg_seq[j].src_device_name.in())) {
                double latency = measure_latency(
                    receive_time, it->second.send_sec, it->second.send_nanosec,
                    msg_seq[j].received_point_sec,
                    msg_seq[j].received_point_nanosec,
                    msg_seq[j].sent_point_sec, msg_seq[j].sent_point_nanosec);
                string data_writer = to_key(
                    it->second.partition, it->second.pub_id, it->second.dw_id);
                string dst_device = string(msg_seq[j].dst_device_name.in());
                latencys[data_writer][dst_device].push_back(latency);
                DEBUG_LOG("measure receive: " + data_writer + ", " +
                          dst_device + ", " + to_string(msg_seq[j].prob_id) +
                          ", " + to_string(latency));
              }
            }
          }
        }
        status = reader->return_loan(msg_seq, info_seq);
        _check_status(status, "MsgDataReader::return_loan failed");
      } else if (guard_list[i].in() == escape.in()) {
        status = escape->set_trigger_value(false);
        _check_status(status, "DDS::GuardCondition::set_trigger_value failed");
      } else {
        // unexpected DDS error
        DEBUG_LOG("unknow condition error");
        exit(1);
      }
    }
  }
}

void MeasureReceiver::before_join() {
  DDS::ReturnCode_t status;
  status = escape->set_trigger_value(true);
  _check_status(status, "DDS::GuardCondition::set_trigger_value failed");
}

long MeasureReceiver::request_measure(string dst_device, string partition,
                                      long pub_id, long dw_id) {
  long id = get_prob_id();
  timespec send_time;
  clock_gettime(CLOCK_MONOTONIC, &send_time);
  {
    lock_guard<mutex> lock(mtx);
    data_map[id] = {partition,  pub_id,           dw_id,
                    dst_device, send_time.tv_sec, send_time.tv_nsec};
  }
  DEBUG_LOG("measure request receive: " + dst_device + ", " + to_string(id));
  return id;
}

string MeasureReceiver::to_key(string partition, long pub_id, long dw_id) {
  return partition + "." + to_string(pub_id) + "." + to_string(dw_id);
}

map<string, vector<double>> MeasureReceiver::get_latency(string partition,
                                                         long pub_id,
                                                         long dw_id) {
  return latencys[to_key(partition, pub_id, dw_id)];
}
