#include <unistd.h>
#include "Monitor.hpp"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the Monitor class.

// Test get_cpu
TEST(Monitor, get_cpu) {
  Monitor m;
  MonitorCpuData val = m.get_cpu();
  EXPECT_LE(0, val.user);
  TEST_COUT << "(" << val.user << ", " << val.user_low << ", " << val.sys
            << ", " << val.idle << ")" << std::endl;
}

// Test get_ram
TEST(Monitor, get_ram) {
  Monitor m;
  double val = m.get_ram();
  EXPECT_LT(0, val);
  TEST_COUT << "(" << val << ")" << std::endl;
}

// Test get_rx
TEST(Monitor, get_rx) {
  Monitor m;
  long long val = m.get_rx();
  EXPECT_LT(0, val);
  TEST_COUT << "(" << val << ")" << std::endl;
}

// Test get_tx
TEST(Monitor, get_tx) {
  Monitor m;
  long long val = m.get_tx();
  EXPECT_LT(0, val);
  TEST_COUT << "(" << val << ")" << std::endl;
}

// Test get_data
TEST(Monitor, get_data) {
  Monitor m;
  m.start();
  sleep(10);
  m.stop();
  std::vector<MonitorData> data = m.get_data();
  EXPECT_LT(0, data.size());
  for (unsigned int i = 0; i < data.size(); ++i)
    TEST_COUT << "(" << data[i].cpu.user << ", " << data[i].cpu.user_low << ", "
              << data[i].cpu.sys << ", " << data[i].cpu.idle << ", "
              << data[i].ram << ", " << data[i].rx << ", " << data[i].tx << ")"
              << std::endl;
}

}  // namespace