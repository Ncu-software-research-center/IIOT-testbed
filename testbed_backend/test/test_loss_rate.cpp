#include <unistd.h>
#include <ctime>
#include <fstream>
#include <set>
#include <string>
#include "DDSEntityManager.hpp"
#include "Data.hpp"
#include "Loader.hpp"
#include "ccpp_dds_dcps.h"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the Sender and Receiver class.

namespace {

std::string msg_id_to_string(std::set<long> msg_id) {
  std::string msg_id_str("");
  for (unsigned int i = 0; i < msg_id.size(); ++i) {
    msg_id_str += std::to_string(*std::next(msg_id.begin(), i));
    if (i < (msg_id.size() - 1)) msg_id_str += "-";
  }
  return msg_id_str;
}

std::string current_date() {
  time_t now = time(0);
  struct tm tm_s;
  char buf[80];
  tm_s = *localtime(&now);
  strftime(buf, sizeof(buf), "%Y-%m-%d-%H%M%S", &tm_s);
  return std::string(buf);
}

void csv_create(std::ofstream& csv) {
  csv << "index,"
      << "loss_rate,"
      << "pub_msg_count,"
      << "sub_msg_count,"
      << "sub_msg_id_count,"
      << "sub_msg_id,"
      << "dw_durability_kind,"
      << "dw_latency_budget_sec,"
      << "dw_latency_budget_nsec,"
      << "dw_reliability_kind,"
      << "dw_history_kind,"
      << "dw_history_depth,"
      << "dr_durability_kind,"
      << "dr_latency_budget_sec,"
      << "dr_latency_budget_nsec,"
      << "dr_reliability_kind,"
      << "dr_history_kind,"
      << "dr_history_depth" << std::endl;
}

void csv_append(std::ofstream& csv, int index, Device device, long pub_count,
                long sub_count, long sub_id_count, std::string msg_id) {
  double loss_rate = 0;
  loss_rate += (pub_count - sub_count);
  loss_rate /= pub_count;
  loss_rate *= 100;
  csv << index << "," << loss_rate << "," << pub_count << "," << sub_count
      << "," << sub_id_count << "," << msg_id << ","
      << device.domain.partitions[0].pubs[0].writers[0].qos.durability.kind
      << ","
      << device.domain.partitions[0]
             .pubs[0]
             .writers[0]
             .qos.latency_budget.duration.sec
      << ","
      << device.domain.partitions[0]
             .pubs[0]
             .writers[0]
             .qos.latency_budget.duration.nanosec
      << ","
      << device.domain.partitions[0].pubs[0].writers[0].qos.reliability.kind
      << "," << device.domain.partitions[0].pubs[0].writers[0].qos.history.kind
      << "," << device.domain.partitions[0].pubs[0].writers[0].qos.history.depth
      << ","
      << device.domain.partitions[0].subs[0].readers[0].qos.durability.kind
      << ","
      << device.domain.partitions[0]
             .subs[0]
             .readers[0]
             .qos.latency_budget.duration.sec
      << ","
      << device.domain.partitions[0]
             .subs[0]
             .readers[0]
             .qos.latency_budget.duration.nanosec
      << ","
      << device.domain.partitions[0].subs[0].readers[0].qos.reliability.kind
      << "," << device.domain.partitions[0].subs[0].readers[0].qos.history.kind
      << "," << device.domain.partitions[0].subs[0].readers[0].qos.history.depth
      << std::endl;
}

void run_test(Device device, std::ofstream& csv, int index) {
  DDSEntityManager dds;
  dds.init(device);
  Receiver* receiver = dds.get_receivers()[0];
  Sender* sender = dds.get_senders()[0];
  TEST_COUT << "begin to test loss rate" << std::endl;

  receiver->start();
  sender->start();
  sleep(device.experiment_time);
  TEST_COUT << " stop test and collect data" << std::endl;
  sender->stop();
  receiver->stop();
  EXPECT_EQ(sender->get_pub_msg_count(),
            receiver->get_data()[sender->get_device()].msg_count);
  csv_append(
      csv, index, device, sender->get_pub_msg_count(),
      receiver->get_data()[sender->get_device()].msg_count,
      receiver->get_data()[sender->get_device()].msg_id.size(),
      msg_id_to_string(receiver->get_data()[sender->get_device()].msg_id));
}

}  // namespace

// Test loss rate
TEST(Sender_Receiver, loss_rate) {
  std::ofstream csv("./report/" + current_date() + ".csv", std::ios::app);
  csv_create(csv);
  Loader loader;
  TEST_COUT << "load test data" << std::endl;
  Device device = loader.load(std::string("./data/test_data.json"));
  for (int i = 0; i < 100; ++i) run_test(device, csv, i);
  csv.close();
}

}  // namespace