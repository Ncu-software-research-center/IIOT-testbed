/**
 * LOGICAL_NAME:    Receiver.cpp
 * FUNCTION:        Subscribe normal message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Receiver.hpp"
#include "dds_debug.hpp"

using namespace std;

Receiver::Receiver(MeasureSender* measure, long id, long sub_id,
                   string device_name, string topic_name,
                   string partition_name) {
  this->measure = measure;
  this->id = id;
  this->sub_id = sub_id;
  this->device = device_name + "-" + to_string(sub_id) + "-" + to_string(id);
  this->src_topic = topic_name;
  this->partition = partition_name;
}

void Receiver::set_data_reader(DDS::DataReader_var dr) {
  DDS::ReturnCode_t status;
  // set data reader
  reader = EmulationData::MsgDataReader::_narrow(dr);
  _check_handle(reader.in(),
                DEBUG_MSG("EmulationData::MsgDataReader::_narrow failed"));
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

void Receiver::run() {
  DDS::ReturnCode_t status;
  DDS::ConditionSeq guard_list;
  guard_list.length(2);
  EmulationData::MsgSeq msg_seq;
  DDS::SampleInfoSeq info_seq;
  // wait until new_msg_condition triggers
  status = wait_set->wait(guard_list, wait_timeout);
  if (status == DDS::RETCODE_OK) {
    for (DDS::ULong i = 0; i < guard_list.length(); ++i) {
      if (guard_list[i].in() == new_msg_condition.in()) {
        // take message
        status = reader->take_w_condition(
            msg_seq, info_seq, 1, new_msg_condition);
        _check_status(
            status,
            DEBUG_MSG("EmulationData::MsgDataReader::take_w_condition failed"));
        // measure latency
        for (DDS::ULong j = 0; j < msg_seq.length(); ++j) {
          if (info_seq[j].valid_data &&
              info_seq[j].sample_state == DDS::NOT_READ_SAMPLE_STATE) {
            DEBUG_LOG(string(msg_seq[j].device_name.in()) + ", " + device +
                      ", " + to_string(msg_seq[j].msg_id));
            if (msg_seq[j].prob_id != 0) {
              measure->request_measure(device, string(msg_seq[j].device_name.in()),
                                       msg_seq[j].prob_id);
            }
          }
        }
        // record messages and sample_infos
        data_queue.push(msg_seq);
        info_queue.push(info_seq);
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

void Receiver::before_join() {
  DDS::ReturnCode_t status;
  status = escape->set_trigger_value(true);
  _check_status(status, "DDS::GuardCondition::set_trigger_value failed");
}

void Receiver::after_stop() {
  while (!data_queue.empty()) {
    EmulationData::MsgSeq msg = data_queue.front();
    DDS::SampleInfoSeq info = info_queue.front();
    for (DDS::ULong i = 0; i < msg.length(); ++i) {
      if (info[i].valid_data &&
          info[i].sample_state == DDS::NOT_READ_SAMPLE_STATE) {
        DEBUG_LOG(string(msg[i].device_name.in()) + ", " + device + ", " +
                  to_string(msg[i].msg_id));
        data[string(msg[i].device_name.in())].msg_count++;
        data[string(msg[i].device_name.in())].msg_id.insert(msg[i].msg_id);
      }
    }
    data_queue.pop();
    info_queue.pop();
  }
}

long Receiver::get_sub_id() { return sub_id; }

long Receiver::get_dr_id() { return id; }

string Receiver::get_partition() { return partition; }

string Receiver::get_src_topic() { return src_topic; }

map<string, SubMsgData> Receiver::get_data() { return data; }
