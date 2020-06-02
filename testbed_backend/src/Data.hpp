/**
 * LOGICAL_NAME:    Data.hpp
 * FUNCTION:        Define data structure used in Testbed.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_DATA_
#define TESTBED_BACKEND_DATA_

#include <set>
#include <string>
#include <vector>

#define EMPTY_DATA ""
#define DURATION_MIN 0
#define DURATION_MAX 2147483647
#define DEFAULT_BLOCK_TIME_SEC 0
#define DEFAULT_BLOCK_TIME_NANOSEC 100000000
#define VALUE_MIN 0
#define VALUE_MAX 2147483647
#define VALUE_UNLIMIT -1
#define DEPTH_MIN 1
#define DEFAULT_KIND 0
#define DEFAULT_READER_DATA_LIFECYCLE_KIND 1
#define DEFAULT_DW_RELIABILITY_KIND 1

struct SubMsgData {
  long msg_count;
  std::set<long> msg_id;
};

struct ProbMsgData {
  std::string dst_device;
  std::string src_device;
  long prob_id;
  long receive_sec;
  long receive_nanosec;
};

struct ResourceData {
  double cpu;
  double memory;
  long long rx;
  long long tx;
};

struct DrData {
  long id;
  long sub_id;
  std::string partition;
  std::string src_device;
  std::string src_topic;
  SubMsgData data;
};

struct DwData {
  long id;
  long pub_id;
  std::string partition;
  std::string dst_device;
  std::string dst_topic;
  long pub_msg_count;
  std::vector<double> latency;
};

struct MeasureData {
  std::string partition;
  long pub_id;
  long dw_id;
  std::string dst_device;
  long send_sec;
  long send_nanosec;
};

struct MonitorCpuData {
  unsigned long long user;
  unsigned long long user_low;
  unsigned long long sys;
  unsigned long long idle;
};

struct MonitorData {
  MonitorCpuData cpu;
  double ram;
  long long rx;
  long long tx;
};

struct Duration {
  long sec;
  unsigned long nanosec;
};

struct UserDataQos {
  std::string data;
};

struct TopicDataQos {
  std::string data;
};

struct GroupDataQos {
  std::string data;
};

struct EntityFactoryQos {
  bool autoenable_created_entities;
};

struct TransportPriorityQos {
  long value;
};

struct LifespanQos {
  Duration duration;
};

struct DurabilityQos {
  long kind;
};  // kind： (default, 0)VOLATILE < (1)TRANSIENT_LOCAL < (2)TRANSIENT <
    // (3)PERSISTENT

struct DeadlineQos {
  Duration period;
};

struct LatencyBudgetQos {
  Duration duration;
};

struct OwnershipQos {
  long kind;
};  // kind: (default, 0)SHARED < (1)EXCLUSIVE

struct OwnershipStrengthQos {
  long value;
};

struct LivelinessQos {
  long kind;
  Duration lease_duration;
};  // kind: (default, 0)AUTOMATIC, (1)MANUAL_BY_PARTICIPANT, (2)MANUAL_BY_TOPIC

struct ReliabilityQos {
  long kind;
  Duration max_blocking_time;
};  // kind: (default, 0)BEST_EFFORT, (1)RELIABLE

struct DestinationOrderQos {
  long kind;
};  // kind: (default, 0)BY_RECEPTION_TIMESTAMP, (1)BY_SOURCE_TIMESTAMP

struct HistoryQos {
  long kind;
  long depth;
};  // kind: (default, 0)KEEP_LAST, (1)KEEP_ALL

struct ResourceLimitsQos {
  long max_samples;
  long max_instances;
  long max_samples_per_instance;
};

struct DurabilityServiceQos {
  Duration service_cleanup_delay;
  long kind;
  long depth;
  long max_samples;
  long max_instances;
  long max_samples_per_instance;
};  // kind: (default, 0)KEEP_LAST, (1)KEEP_ALL

struct PresentationQos {
  long kind;
  bool coherent_access;
  bool ordered_access;
};  // kind: (default, 0)INSTANCE, (1)TOPIC, (2)GROUP

struct WriterDataLifecycleQos {
  bool autodispose_unregistered_instances;
  Duration autopurge_suspended_samples_delay;
  Duration autounregister_instance_delay;
};

struct TimeBasedFilterQos {
  Duration minimum_separation;
};

struct ReaderDataLifecycleQos {
  Duration autopurge_nowriter_samples_delay;
  Duration autopurge_disposed_samples_delay;
  bool autopurge_dispose_all;
  long kind;
};  // kind: (0)NO_INVALID_SAMPLES, (default, 1)MINIMUM_INVALID_SAMPLES,
    // (2)ALL_INVALID_SAMPLES

struct DrQos {
  UserDataQos user_data;
  DurabilityQos durability;
  DeadlineQos deadline;
  LatencyBudgetQos latency_budget;
  OwnershipQos ownership;
  LivelinessQos liveliness;
  TimeBasedFilterQos time_based_filter;
  ReliabilityQos reliability;
  DestinationOrderQos destination_order;
  HistoryQos history;
  ResourceLimitsQos resource_limits;
  ReaderDataLifecycleQos reader_data_lifecycle;
};

struct DataReader {
  long id;
  std::string src_topic;
  DrQos qos;
};

struct SubQos {
  GroupDataQos group_data;
  PresentationQos presentation;
  EntityFactoryQos entity_factory;
};

struct Subscriber {
  long id;  // measure id = 0
  SubQos qos;
  std::vector<DataReader> readers;
};

struct DwQos {
  UserDataQos user_data;
  TransportPriorityQos transport_priority;
  LifespanQos lifespan;
  DurabilityQos durability;
  DeadlineQos deadline;
  LatencyBudgetQos latency_budget;
  OwnershipQos ownership;
  OwnershipStrengthQos ownership_strength;
  LivelinessQos liveliness;
  ReliabilityQos reliability;
  DestinationOrderQos destination_order;
  HistoryQos history;
  ResourceLimitsQos resource_limits;
  WriterDataLifecycleQos writer_data_lifecycle;
};

struct DataWriter {
  long id;
  std::string dst_topic;
  DwQos qos;
  unsigned long size;
  unsigned long cycletime;
};

struct PubQos {
  GroupDataQos group_data;
  PresentationQos presentation;
  EntityFactoryQos entity_factory;
};

struct Publisher {
  long id;  // measure id = 0
  PubQos qos;
  std::vector<DataWriter> writers;
};

struct Partition {
  std::string name;
  std::vector<Publisher> pubs;
  std::vector<Subscriber> subs;
};

struct TopicQos {
  TopicDataQos topic_data;
  TransportPriorityQos transport_priority;
  LifespanQos lifespan;
  DurabilityQos durability;
  DeadlineQos deadline;
  LatencyBudgetQos latency_budget;
  OwnershipQos ownership;
  LivelinessQos liveliness;
  ReliabilityQos reliability;
  DestinationOrderQos destination_order;
  HistoryQos history;
  ResourceLimitsQos resource_limits;
  DurabilityServiceQos durability_service;
};

struct Topic {
  std::string name;
  TopicQos qos;
};

struct DomainQos {
  UserDataQos user_data;
  EntityFactoryQos entity_factory;
};

struct Domain {
  DomainQos qos;
  std::vector<Topic> topics;
  std::vector<Partition> partitions;
};

struct Device {
  std::string name;
  long experiment_time;
  long measure_count;
  Domain domain;
};

#endif
