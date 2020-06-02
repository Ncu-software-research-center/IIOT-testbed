/**
 * LOGICAL_NAME:    Loader.hpp
 * FUNCTION:        Load configuration file.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_LOADER_
#define TESTBED_BACKEND_LOADER_

#include <jsoncpp/json/json.h>
#include <string>
#include "Data.hpp"

class Loader {
 private:
  void parse_device(Device &device, Json::Value json);
  void parse_domain(Domain &domain, Json::Value json);
  void parse_domain_qos(DomainQos &qos, Json::Value json);
  void parse_topic(Domain &domain, Json::Value json);
  void parse_topic_qos(TopicQos &qos, Json::Value json);
  void parse_partition(Domain &domain, Json::Value json);
  void parse_publisher(Partition &partition, Json::Value json);
  void parse_publisher_qos(PubQos &qos, Json::Value json);
  void parse_data_writer(Publisher &pub, Json::Value json);
  void parse_data_writer_qos(DwQos &qos, Json::Value json);
  void parse_subscriber(Partition &partition, Json::Value json);
  void parse_subscriber_qos(SubQos &qos, Json::Value json);
  void parse_data_reader(Subscriber &sub, Json::Value json);
  void parse_data_reader_qos(DrQos &qos, Json::Value json);

 public:
  Device load(std::string path);
};

#endif