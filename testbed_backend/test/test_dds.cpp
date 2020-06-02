#include <unistd.h>
#include <map>
#include <string>
#include "DDSEntityManager.hpp"
#include "Data.hpp"
#include "Loader.hpp"
#include "ccpp_dds_dcps.h"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the DDSEntityManager class.

std::string octetseq_to_str(DDS::octSeq seq) {
  std::string s;
  for (unsigned long i = 0; i < seq.length(); ++i) {
    s += seq[i];
  }
  return s;
}

// Test init
TEST(DDSEntityManager, init) {
  Loader loader;
  DDSEntityManager dds;
  TEST_COUT << "load test data" << std::endl;
  std::string path("./data/test_data.json");
  Device device = loader.load(path);
  TEST_COUT << "dds init" << std::endl;
  dds.init(device);
  TEST_COUT << "check qos" << std::endl;
  DDS::TopicQos t_qos;
  TEST_COUT << "get topics" << std::endl;
  std::map<std::string, DDS::Topic_var> topics = dds.get_topics();
  for (std::map<std::string, DDS::Topic_var>::iterator it = topics.begin();
       it != topics.end(); it++)
    TEST_COUT << "topic name: " << it->first << std::endl;
  TEST_COUT << "get topic1" << std::endl;
  DDS::Topic_var topic = topics["topic1"];
  if (!topic) TEST_COUT << "get topic1 failed" << std::endl;
  TEST_COUT << "get topic1 qos" << std::endl;
  topic->get_qos(t_qos);
  TEST_COUT << "check topic1 qos" << std::endl;
  EXPECT_STREQ("sample", octetseq_to_str(t_qos.topic_data.value).c_str());
  EXPECT_EQ(0, t_qos.durability.kind);
  EXPECT_EQ(0, t_qos.durability_service.service_cleanup_delay.sec);
  EXPECT_EQ(0, t_qos.durability_service.service_cleanup_delay.nanosec);
  EXPECT_EQ(0, t_qos.durability_service.history_kind);
  EXPECT_EQ(1, t_qos.durability_service.history_depth);
  EXPECT_EQ(2147483647, t_qos.durability_service.max_samples);
  EXPECT_EQ(2147483647, t_qos.durability_service.max_instances);
  EXPECT_EQ(2147483647, t_qos.durability_service.max_samples_per_instance);
  EXPECT_EQ(2147483647, t_qos.deadline.period.sec);
  EXPECT_EQ(2147483647, t_qos.deadline.period.nanosec);
  EXPECT_EQ(0, t_qos.latency_budget.duration.sec);
  EXPECT_EQ(0, t_qos.latency_budget.duration.nanosec);
  EXPECT_EQ(0, t_qos.liveliness.kind);
  EXPECT_EQ(2147483647, t_qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647, t_qos.liveliness.lease_duration.nanosec);
  EXPECT_EQ(0, t_qos.reliability.kind);
  EXPECT_EQ(0, t_qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000, t_qos.reliability.max_blocking_time.nanosec);
  EXPECT_EQ(0, t_qos.destination_order.kind);
  EXPECT_EQ(0, t_qos.history.kind);
  EXPECT_EQ(1, t_qos.history.depth);
  EXPECT_EQ(2147483647, t_qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647, t_qos.resource_limits.max_instances);
  EXPECT_EQ(2147483647, t_qos.resource_limits.max_samples_per_instance);
  EXPECT_EQ(0, t_qos.transport_priority.value);
  EXPECT_EQ(2147483647, t_qos.lifespan.duration.sec);
  EXPECT_EQ(2147483647, t_qos.lifespan.duration.nanosec);
  EXPECT_EQ(0, t_qos.ownership.kind);
  TEST_COUT << "get publishers" << std::endl;
  std::vector<DDS::Publisher_var> pubs = dds.get_pubs();
  TEST_COUT << "get publisher 1" << std::endl;
  DDS::Publisher_var pub = pubs[1];
  TEST_COUT << "get publisher 1 qos" << std::endl;
  DDS::PublisherQos p_qos;
  pub->get_qos(p_qos);
  TEST_COUT << "check publisher 1 qos" << std::endl;
  EXPECT_STREQ("sample", octetseq_to_str(p_qos.group_data.value).c_str());
  EXPECT_EQ(0, p_qos.presentation.access_scope);
  EXPECT_FALSE(p_qos.presentation.coherent_access);
  EXPECT_FALSE(p_qos.presentation.ordered_access);
  TEST_COUT << "get data writers" << std::endl;
  std::vector<DDS::DataWriter_var> dws = dds.get_writers();
  TEST_COUT << "get data writer 1" << std::endl;
  DDS::DataWriter_var dw = dws[1];
  TEST_COUT << "get data writer 1 qos" << std::endl;
  DDS::DataWriterQos dw_qos;
  dw->get_qos(dw_qos);
  TEST_COUT << "check data writer 1 qos" << std::endl;
  EXPECT_STREQ("sample", octetseq_to_str(dw_qos.user_data.value).c_str());
  EXPECT_EQ(0, dw_qos.transport_priority.value);
  EXPECT_EQ(2147483647, dw_qos.lifespan.duration.sec);
  EXPECT_EQ(2147483647, dw_qos.lifespan.duration.nanosec);
  EXPECT_EQ(0, dw_qos.durability.kind);
  EXPECT_EQ(2147483647, dw_qos.deadline.period.sec);
  EXPECT_EQ(2147483647, dw_qos.deadline.period.nanosec);
  EXPECT_EQ(0, dw_qos.latency_budget.duration.sec);
  EXPECT_EQ(0, dw_qos.latency_budget.duration.nanosec);
  EXPECT_EQ(0, dw_qos.ownership.kind);
  EXPECT_EQ(0, dw_qos.ownership_strength.value);
  EXPECT_EQ(0, dw_qos.liveliness.kind);
  EXPECT_EQ(2147483647, dw_qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647, dw_qos.liveliness.lease_duration.nanosec);
  EXPECT_EQ(0, dw_qos.reliability.kind);
  EXPECT_EQ(0, dw_qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000, dw_qos.reliability.max_blocking_time.nanosec);
  EXPECT_EQ(0, dw_qos.destination_order.kind);
  EXPECT_EQ(0, dw_qos.history.kind);
  EXPECT_EQ(1, dw_qos.history.depth);
  EXPECT_EQ(2147483647, dw_qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647, dw_qos.resource_limits.max_instances);
  EXPECT_EQ(2147483647, dw_qos.resource_limits.max_samples_per_instance);
  EXPECT_TRUE(dw_qos.writer_data_lifecycle.autodispose_unregistered_instances);
  EXPECT_EQ(2147483647,
            dw_qos.writer_data_lifecycle.autopurge_suspended_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      dw_qos.writer_data_lifecycle.autopurge_suspended_samples_delay.nanosec);
  EXPECT_EQ(2147483647,
            dw_qos.writer_data_lifecycle.autounregister_instance_delay.sec);
  EXPECT_EQ(2147483647,
            dw_qos.writer_data_lifecycle.autounregister_instance_delay.nanosec);
  TEST_COUT << "get subscribers" << std::endl;
  std::vector<DDS::Subscriber_var> subs = dds.get_subs();
  TEST_COUT << "get subscriber 1" << std::endl;
  DDS::Subscriber_var sub = subs[1];
  TEST_COUT << "get subscriber 1 qos" << std::endl;
  DDS::SubscriberQos s_qos;
  sub->get_qos(s_qos);
  TEST_COUT << "check subscriber 1 qos" << std::endl;
  EXPECT_STREQ("sample", octetseq_to_str(s_qos.group_data.value).c_str());
  EXPECT_EQ(0, s_qos.presentation.access_scope);
  EXPECT_FALSE(s_qos.presentation.coherent_access);
  EXPECT_FALSE(s_qos.presentation.ordered_access);
  TEST_COUT << "get data readers" << std::endl;
  std::vector<DDS::DataReader_var> drs = dds.get_readers();
  TEST_COUT << "get data reader 1" << std::endl;
  DDS::DataReader_var dr = drs[1];
  TEST_COUT << "get data reader 1 qos" << std::endl;
  DDS::DataReaderQos dr_qos;
  dr->get_qos(dr_qos);
  TEST_COUT << "check data reader 1 qos" << std::endl;
  EXPECT_STREQ("sample", octetseq_to_str(dr_qos.user_data.value).c_str());
  EXPECT_EQ(0, dr_qos.durability.kind);
  EXPECT_EQ(2147483647, dr_qos.deadline.period.sec);
  EXPECT_EQ(2147483647, dr_qos.deadline.period.nanosec);
  EXPECT_EQ(0, dr_qos.latency_budget.duration.sec);
  EXPECT_EQ(0, dr_qos.latency_budget.duration.nanosec);
  EXPECT_EQ(0, dr_qos.ownership.kind);
  EXPECT_EQ(0, dr_qos.liveliness.kind);
  EXPECT_EQ(2147483647, dr_qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647, dr_qos.liveliness.lease_duration.nanosec);
  EXPECT_EQ(0, dr_qos.time_based_filter.minimum_separation.sec);
  EXPECT_EQ(0, dr_qos.time_based_filter.minimum_separation.nanosec);
  EXPECT_EQ(0, dr_qos.reliability.kind);
  EXPECT_EQ(0, dr_qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000, dr_qos.reliability.max_blocking_time.nanosec);
  EXPECT_EQ(0, dr_qos.destination_order.kind);
  EXPECT_EQ(0, dr_qos.history.kind);
  EXPECT_EQ(1, dr_qos.history.depth);
  EXPECT_EQ(2147483647, dr_qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647, dr_qos.resource_limits.max_instances);
  EXPECT_EQ(2147483647, dr_qos.resource_limits.max_samples_per_instance);
  EXPECT_EQ(2147483647,
            dr_qos.reader_data_lifecycle.autopurge_nowriter_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      dr_qos.reader_data_lifecycle.autopurge_nowriter_samples_delay.nanosec);
  EXPECT_EQ(2147483647,
            dr_qos.reader_data_lifecycle.autopurge_disposed_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      dr_qos.reader_data_lifecycle.autopurge_disposed_samples_delay.nanosec);
  EXPECT_EQ(1, dr_qos.reader_data_lifecycle.invalid_sample_visibility.kind);
}

}  // namespace