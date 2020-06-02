/**
 * LOGICAL_NAME:    Manager.cpp
 * FUNCTION:        Manage lifecycle of emulation.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Manager.hpp"
#include <unistd.h>
#include <fstream>

using namespace std;

void Manager::load() { device = loader.load(DATA_SETTING_DIR); }

void Manager::init() {
  dds.init(device);
  measure_receiver = dds.get_measure_receiver();
  measure_sender = dds.get_measure_sender();
  senders = dds.get_senders();
  receivers = dds.get_receivers();
}

void Manager::ready() {
  ofstream file(READY_PATH);
  if (file) {
    file << "ready\n";
    file.close();
  }
  wait_start();
}

void Manager::run() {
  monitor.start();
  measure_receiver->start();
  measure_sender->start();
  for (auto receiver : receivers) receiver->start();
  for (auto sender : senders) sender->start();
  sleep(device.experiment_time);
  for (auto sender : senders) sender->stop();
  for (auto receiver : receivers) receiver->stop();
  measure_sender->stop();
  measure_receiver->stop();
  monitor.stop();
}

void Manager::save() {
  for (auto sender : senders) {
    map<string, vector<double>> latency = measure_receiver->get_latency(
        sender->get_partition(), sender->get_pub_id(), sender->get_dw_id());
    saver.append_pub(sender->get_partition(), sender->get_dst_topic(),
                     sender->get_pub_id(), sender->get_dw_id(),
                     sender->get_pub_msg_count(), latency);
  }
  for (auto receiver : receivers) {
    saver.append_sub(receiver->get_partition(), receiver->get_src_topic(),
                     receiver->get_sub_id(), receiver->get_dr_id(),
                     receiver->get_data());
  }
  saver.append_resource(monitor.get_data());
  saver.save(device.name, REPORT_DIR);
}

void Manager::wait_start() {
  while (1) {
    ifstream file(START_PATH);
    if (file.good()) {
      file.close();
      break;
    }
    sleep(1);
  }
}
