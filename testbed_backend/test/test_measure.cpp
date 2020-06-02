#include <unistd.h>
#include <fstream>
#include <string>
#include "DDSEntityManager.hpp"
#include "Data.hpp"
#include "Loader.hpp"
#include "ccpp_dds_dcps.h"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the MeasureSender and MeasureReceiver class.

// test measure
TEST(MeasureSender_MeasureReceiver, measure) {
  DDSEntityManager dds;
  Loader loader;
  Device device = loader.load(std::string("./data/test_data.json"));
  dds.init(device);
  Receiver* receiver = dds.get_receivers()[0];
  Sender* sender = dds.get_senders()[0];
  MeasureReceiver* measure_receiver = dds.get_measure_receiver();
  MeasureSender* measure_sender = dds.get_measure_sender();
  TEST_COUT << "begin to test loss rate" << std::endl;
  receiver->start();
  measure_receiver->start();
  measure_sender->start();
  sender->start();
  sleep(device.experiment_time);
  TEST_COUT << " stop test and collect data" << std::endl;
  sender->stop();
  measure_sender->stop();
  measure_receiver->stop();
  receiver->stop();
}

}  // namespace
