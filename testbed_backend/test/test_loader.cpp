#include <unistd.h>
#include <string>
#include "Data.hpp"
#include "Loader.hpp"
#include "gtest/gtest.h"
#include "testbed_test.hpp"

namespace {
// In this test, we test the Loader class.

// Test load
TEST(Loader, load) {
  Loader loader;
  std::string path("./data/test_data.json");
  Device device = loader.load(path);
  // test device
  TEST_COUT << "test device" << std::endl;
  EXPECT_STREQ("sample", device.name.c_str());
  EXPECT_EQ(5, device.experiment_time);
  EXPECT_EQ(100, device.measure_count);
  // test domain
  TEST_COUT << "test domain" << std::endl;
  // test domain qos
  TEST_COUT << "test domain qos" << std::endl;
  EXPECT_STREQ("sample", device.domain.qos.user_data.data.c_str());
  EXPECT_TRUE(device.domain.qos.entity_factory.autoenable_created_entities);
  TEST_COUT << "test domain topic" << std::endl;
  EXPECT_STREQ("topic1", device.domain.topics[0].name.c_str());
  TEST_COUT << "test domain topic qos" << std::endl;
  // topic_data
  EXPECT_STREQ("sample", device.domain.topics[0].qos.topic_data.data.c_str());
  // transport_priority
  EXPECT_EQ(0, device.domain.topics[0].qos.transport_priority.value);
  // lifespan
  EXPECT_EQ(2147483647, device.domain.topics[0].qos.lifespan.duration.sec);
  EXPECT_EQ(2147483647, device.domain.topics[0].qos.lifespan.duration.nanosec);
  // durability
  EXPECT_EQ(0, device.domain.topics[0].qos.durability.kind);
  // deadline
  EXPECT_EQ(2147483647, device.domain.topics[0].qos.deadline.period.sec);
  EXPECT_EQ(2147483647, device.domain.topics[0].qos.deadline.period.nanosec);
  // latency_budget
  EXPECT_EQ(0, device.domain.topics[0].qos.latency_budget.duration.sec);
  EXPECT_EQ(0, device.domain.topics[0].qos.latency_budget.duration.nanosec);
  // ownership
  EXPECT_EQ(0, device.domain.topics[0].qos.ownership.kind);
  // liveliness
  EXPECT_EQ(0, device.domain.topics[0].qos.liveliness.kind);
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.liveliness.lease_duration.nanosec);
  // reliability
  EXPECT_EQ(0, device.domain.topics[0].qos.reliability.kind);
  EXPECT_EQ(0, device.domain.topics[0].qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000,
            device.domain.topics[0].qos.reliability.max_blocking_time.nanosec);
  // destination_order
  EXPECT_EQ(0, device.domain.topics[0].qos.destination_order.kind);
  // history
  EXPECT_EQ(0, device.domain.topics[0].qos.history.kind);
  EXPECT_EQ(1, device.domain.topics[0].qos.history.depth);
  // resource_limits
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.resource_limits.max_instances);
  EXPECT_EQ(
      2147483647,
      device.domain.topics[0].qos.resource_limits.max_samples_per_instance);
  // durability_service
  EXPECT_EQ(
      0,
      device.domain.topics[0].qos.durability_service.service_cleanup_delay.sec);
  EXPECT_EQ(0, device.domain.topics[0]
                   .qos.durability_service.service_cleanup_delay.nanosec);
  EXPECT_EQ(0, device.domain.topics[0].qos.durability_service.kind);
  EXPECT_EQ(1, device.domain.topics[0].qos.durability_service.depth);
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.durability_service.max_samples);
  EXPECT_EQ(2147483647,
            device.domain.topics[0].qos.durability_service.max_instances);
  EXPECT_EQ(
      2147483647,
      device.domain.topics[0].qos.durability_service.max_samples_per_instance);
  TEST_COUT << "test domain partition" << std::endl;
  EXPECT_STREQ("part1", device.domain.partitions[0].name.c_str());
  TEST_COUT << "test domain partition publisher" << std::endl;
  EXPECT_EQ(0, device.domain.partitions[0].pubs[0].id);
  TEST_COUT << "test domain partition publisher qos" << std::endl;
  // gorup_data
  EXPECT_STREQ("sample",
               device.domain.partitions[0].pubs[0].qos.group_data.data.c_str());
  // presentation
  EXPECT_EQ(0, device.domain.partitions[0].pubs[0].qos.presentation.kind);
  EXPECT_FALSE(
      device.domain.partitions[0].pubs[0].qos.presentation.coherent_access);
  EXPECT_FALSE(
      device.domain.partitions[0].pubs[0].qos.presentation.ordered_access);
  // entity_factory
  EXPECT_TRUE(device.domain.partitions[0]
                  .pubs[0]
                  .qos.entity_factory.autoenable_created_entities);
  TEST_COUT << "test domain partition publisher data_writer" << std::endl;
  EXPECT_EQ(0, device.domain.partitions[0].pubs[0].writers[0].id);
  EXPECT_STREQ(
      "topic1",
      device.domain.partitions[0].pubs[0].writers[0].dst_topic.c_str());
  EXPECT_EQ(12, device.domain.partitions[0].pubs[0].writers[0].size);
  EXPECT_EQ(1000, device.domain.partitions[0].pubs[0].writers[0].cycletime);
  TEST_COUT << "test domain partition publisher data_writer qos" << std::endl;
  // user_data
  EXPECT_STREQ("sample", device.domain.partitions[0]
                             .pubs[0]
                             .writers[0]
                             .qos.user_data.data.c_str());
  // transport_priority
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.transport_priority.value);
  // lifespan
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0].pubs[0].writers[0].qos.lifespan.duration.sec);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.lifespan.duration.nanosec);
  // durability
  EXPECT_EQ(0,
            device.domain.partitions[0].pubs[0].writers[0].qos.durability.kind);
  // deadline
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0].pubs[0].writers[0].qos.deadline.period.sec);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.deadline.period.nanosec);
  // latency_budget
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.latency_budget.duration.sec);
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.latency_budget.duration.nanosec);
  // ownership
  EXPECT_EQ(0,
            device.domain.partitions[0].pubs[0].writers[0].qos.ownership.kind);
  // ownership_strength
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.ownership_strength.value);
  // liveliness
  EXPECT_EQ(0,
            device.domain.partitions[0].pubs[0].writers[0].qos.liveliness.kind);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.liveliness.lease_duration.nanosec);
  // reliability
  EXPECT_EQ(
      0, device.domain.partitions[0].pubs[0].writers[0].qos.reliability.kind);
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000, device.domain.partitions[0]
                           .pubs[0]
                           .writers[0]
                           .qos.reliability.max_blocking_time.nanosec);
  // destination_order
  EXPECT_EQ(0, device.domain.partitions[0]
                   .pubs[0]
                   .writers[0]
                   .qos.destination_order.kind);
  // history
  EXPECT_EQ(0, device.domain.partitions[0].pubs[0].writers[0].qos.history.kind);
  EXPECT_EQ(1,
            device.domain.partitions[0].pubs[0].writers[0].qos.history.depth);
  // resource_limits
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.resource_limits.max_instances);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .pubs[0]
                            .writers[0]
                            .qos.resource_limits.max_samples_per_instance);
  // writer_dta_lifecycle
  EXPECT_TRUE(
      device.domain.partitions[0]
          .pubs[0]
          .writers[0]
          .qos.writer_data_lifecycle.autodispose_unregistered_instances);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .pubs[0]
          .writers[0]
          .qos.writer_data_lifecycle.autopurge_suspended_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .pubs[0]
          .writers[0]
          .qos.writer_data_lifecycle.autopurge_suspended_samples_delay.nanosec);
  EXPECT_EQ(2147483647,
            device.domain.partitions[0]
                .pubs[0]
                .writers[0]
                .qos.writer_data_lifecycle.autounregister_instance_delay.sec);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .pubs[0]
          .writers[0]
          .qos.writer_data_lifecycle.autounregister_instance_delay.nanosec);
  TEST_COUT << "test domain partition subscriber" << std::endl;
  EXPECT_EQ(0, device.domain.partitions[0].subs[0].id);
  TEST_COUT << "test domain partition subscriber qos" << std::endl;
  // group_data
  EXPECT_STREQ("sample",
               device.domain.partitions[0].subs[0].qos.group_data.data.c_str());
  // presentation
  EXPECT_EQ(0, device.domain.partitions[0].subs[0].qos.presentation.kind);
  EXPECT_FALSE(
      device.domain.partitions[0].subs[0].qos.presentation.coherent_access);
  EXPECT_FALSE(
      device.domain.partitions[0].subs[0].qos.presentation.ordered_access);
  // entity_factory
  EXPECT_TRUE(device.domain.partitions[0]
                  .subs[0]
                  .qos.entity_factory.autoenable_created_entities);
  TEST_COUT << "test domain partition subscriber data_reader" << std::endl;
  EXPECT_EQ(0, device.domain.partitions[0].subs[0].readers[0].id);
  EXPECT_STREQ(
      "topic1",
      device.domain.partitions[0].subs[0].readers[0].src_topic.c_str());
  TEST_COUT << "test domain partition subscriber data_reader qos" << std::endl;
  // user_data
  EXPECT_STREQ("sample", device.domain.partitions[0]
                             .subs[0]
                             .readers[0]
                             .qos.user_data.data.c_str());
  // durability
  EXPECT_EQ(0,
            device.domain.partitions[0].subs[0].readers[0].qos.durability.kind);
  // deadline
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0].subs[0].readers[0].qos.deadline.period.sec);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.deadline.period.nanosec);
  // latency_budget
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.latency_budget.duration.sec);
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.latency_budget.duration.nanosec);
  // ownership
  EXPECT_EQ(0,
            device.domain.partitions[0].subs[0].readers[0].qos.ownership.kind);
  // liveliness
  EXPECT_EQ(0,
            device.domain.partitions[0].subs[0].readers[0].qos.liveliness.kind);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.liveliness.lease_duration.sec);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.liveliness.lease_duration.nanosec);
  // time_based_filter
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.time_based_filter.minimum_separation.sec);
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.time_based_filter.minimum_separation.nanosec);
  // reliability
  EXPECT_EQ(
      0, device.domain.partitions[0].subs[0].readers[0].qos.reliability.kind);
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.reliability.max_blocking_time.sec);
  EXPECT_EQ(100000000, device.domain.partitions[0]
                           .subs[0]
                           .readers[0]
                           .qos.reliability.max_blocking_time.nanosec);
  // destination_order
  EXPECT_EQ(0, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.destination_order.kind);
  // history
  EXPECT_EQ(0, device.domain.partitions[0].subs[0].readers[0].qos.history.kind);
  EXPECT_EQ(1,
            device.domain.partitions[0].subs[0].readers[0].qos.history.depth);
  // resource_limits
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.resource_limits.max_samples);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.resource_limits.max_instances);
  EXPECT_EQ(2147483647, device.domain.partitions[0]
                            .subs[0]
                            .readers[0]
                            .qos.resource_limits.max_samples_per_instance);
  // reader_data_lifecycle
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .subs[0]
          .readers[0]
          .qos.reader_data_lifecycle.autopurge_nowriter_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .subs[0]
          .readers[0]
          .qos.reader_data_lifecycle.autopurge_nowriter_samples_delay.nanosec);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .subs[0]
          .readers[0]
          .qos.reader_data_lifecycle.autopurge_disposed_samples_delay.sec);
  EXPECT_EQ(
      2147483647,
      device.domain.partitions[0]
          .subs[0]
          .readers[0]
          .qos.reader_data_lifecycle.autopurge_disposed_samples_delay.nanosec);
  EXPECT_FALSE(device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.reader_data_lifecycle.autopurge_dispose_all);
  EXPECT_EQ(1, device.domain.partitions[0]
                   .subs[0]
                   .readers[0]
                   .qos.reader_data_lifecycle.kind);
}

}  // namespace