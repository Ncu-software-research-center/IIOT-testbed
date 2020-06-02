/**
 * LOGICAL_NAME:    MeasureSender.cpp
 * FUNCTION:        Publish measure message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "MeasureSender.hpp"
#include <ctime>
#include "Data.hpp"
#include "dds_debug.hpp"

using namespace std;

static bool data_queue_is_empty = true;

MeasureSender::MeasureSender(string device_name) { this->device = device_name; }

void MeasureSender::set_data_writer(DDS::DataWriter_var dw_var) {
  // create writer
  writer = EmulationData::ProbMsgDataWriter::_narrow(dw_var);
  _check_handle(writer.in(),
                DEBUG_MSG("EmulationData::ProbMsgDAtaWriter::_narrow failed"));
}

void MeasureSender::run() {
  DDS::ReturnCode_t status;
  unique_lock<mutex> lock(mtx);
  cv.wait(lock, [] { return !data_queue_is_empty; });
  // consume data
  while (!data_queue.empty()) {
    ProbMsgData data = data_queue.front();
    timespec send_time;
    clock_gettime(CLOCK_MONOTONIC, &send_time);
    msg.dst_device_name = DDS::string_dup(data.dst_device.c_str());
    msg.src_device_name = DDS::string_dup(data.src_device.c_str());
    msg.prob_id = data.prob_id;
    msg.received_point_sec = data.receive_sec;
    msg.received_point_nanosec = data.receive_nanosec;
    msg.sent_point_sec = send_time.tv_sec;
    msg.sent_point_nanosec = send_time.tv_nsec;
    // send data
    status = writer->write(msg, DDS::HANDLE_NIL);
    _check_status(status,
                  DEBUG_MSG("EmulationData::MsgDataWriter::write failed"));
    data_queue.pop();
    DEBUG_LOG("measure send: " + data.src_device + ", " + device + ", " +
              to_string(msg.prob_id));
  }
  data_queue_is_empty = true;
}

void MeasureSender::before_join() {
  data_queue_is_empty = false;
  cv.notify_all();
}

void MeasureSender::request_measure(string dst_device, string src_device, long prob_id) {
  // get receive time
  timespec receive_time;
  clock_gettime(CLOCK_MONOTONIC, &receive_time);
  {
    lock_guard<mutex> lock(mtx);
    // push data
    data_queue.push(
        {dst_device, src_device, prob_id, receive_time.tv_sec, receive_time.tv_nsec});
    data_queue_is_empty = false;
  }
  // nofify run
  cv.notify_one();
  DEBUG_LOG("measure request send: " + src_device + ", " + dst_device + ", " +
            to_string(prob_id));
}
