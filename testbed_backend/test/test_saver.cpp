#include <unistd.h>
#include <fstream>
#include <string>
#include "DDSEntityManager.hpp"
#include "Data.hpp"
#include "Loader.hpp"
#include "Monitor.hpp"
#include "Saver.hpp"
#include "ccpp_dds_dcps.h"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the Saver class.

// test save
TEST(Saver, save) {
  Loader loader;
  Saver saver;
  DDSEntityManager dds;
  Monitor monitor;
  Device device = loader.load(std::string("./data/test_data.json"));
  dds.init(device);
  monitor.start();
  dds.get_measure_receiver()->start();
  dds.get_measure_sender()->start();
  for (auto receiver : dds.get_receivers()) receiver->start();
  for (auto sender : dds.get_senders()) sender->start();
  sleep(device.experiment_time);
  for (auto sender : dds.get_senders()) sender->stop();
  for (auto receiver : dds.get_receivers()) receiver->stop();
  dds.get_measure_sender()->stop();
  dds.get_measure_receiver()->stop();
  monitor.stop();

  for (auto sender : dds.get_senders()) {
    std::map<std::string, std::vector<double>> latency =
        dds.get_measure_receiver()->get_latency(
            sender->get_partition(), sender->get_pub_id(), sender->get_dw_id());
    saver.append_pub(sender->get_partition(), sender->get_dst_topic(),
                     sender->get_pub_id(), sender->get_dw_id(),
                     sender->get_pub_msg_count(), latency);
  }
  for (auto receiver : dds.get_receivers()) {
    saver.append_sub(receiver->get_partition(), receiver->get_src_topic(),
                     receiver->get_sub_id(), receiver->get_dr_id(),
                     receiver->get_data());
  }
  saver.append_resource(monitor.get_data());

  saver.save(device.name, std::string("./report/"));
}

}  // namespace