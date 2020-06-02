/**
 * LOGICAL_NAME:    Loader.cpp
 * FUNCTION:        Load configuration file.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Loader.hpp"
#include <jsoncpp/json/json.h>
#include <fstream>
#include <string>
#include "Data.hpp"

using namespace std;
using namespace Json;

Device Loader::load(string path) {
  Device device;
  ifstream file(path);
  Value json;
  file >> json;
  file.close();
  parse_device(device, json);
  return device;
}

void Loader::parse_device(Device &device, Value json) {
  device.name = json["name"].asString();
  device.experiment_time = json["experiment_time"].asInt();
  device.measure_count = json["measure_count"].asInt();
  parse_domain(device.domain, json["domain"]);
}

void Loader::parse_domain(Domain &domain, Value json) {
  parse_domain_qos(domain.qos, json["domain_qos"]);
  parse_topic(domain, json["topic"]);
  parse_partition(domain, json["partition"]);
}

void Loader::parse_domain_qos(DomainQos &qos, Value json) {
  qos.user_data = {json["user_data"].get("data", EMPTY_DATA).asString()};
  qos.entity_factory = {
      json["entity_factory"].get("autoenable_created_entities", true).asBool()};
}

void Loader::parse_topic(Domain &domain, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    Topic topic;
    topic.name = json[i]["name"].asString();
    parse_topic_qos(topic.qos, json[i]["topic_qos"]);
    domain.topics.push_back(topic);
  }
}

void Loader::parse_topic_qos(TopicQos &qos, Value json) {
  qos.topic_data = {json["topic_data"].get("data", EMPTY_DATA).asString()};
  qos.transport_priority = {
      json["transport_priority"].get("value", VALUE_MIN).asInt()};
  qos.lifespan = {
      {json["lifespan"]["duration"].get("sec", DURATION_MAX).asInt(),
       json["lifespan"]["duration"].get("nanosec", DURATION_MAX).asUInt()}};
  qos.durability = {json["durability"].get("kind", DEFAULT_KIND).asInt()};
  qos.deadline = {
      {json["deadline"]["period"].get("sec", DURATION_MAX).asInt(),
       json["deadline"]["period"].get("nanosec", DURATION_MAX).asUInt()}};
  qos.latency_budget = {
      {json["latency_budget"]["duration"].get("sec", DURATION_MIN).asInt(),
       json["latency_budget"]["duration"]
           .get("nanosec", DURATION_MIN)
           .asUInt()}};
  qos.ownership = {json["ownership"].get("kind", DEFAULT_KIND).asInt()};
  qos.liveliness = {
      json["liveliness"].get("kind", DEFAULT_KIND).asInt(),
      {json["liveliness"]["lease_duration"].get("sec", DURATION_MAX).asInt(),
       json["liveliness"]["lease_duration"]
           .get("nanosec", DURATION_MAX)
           .asUInt()}};
  qos.reliability = {json["reliability"].get("kind", DEFAULT_KIND).asInt(),
                     {json["reliability"]["max_blocking_time"]
                          .get("sec", DEFAULT_BLOCK_TIME_SEC)
                          .asInt(),
                      json["reliability"]["max_blocking_time"]
                          .get("nanosec", DEFAULT_BLOCK_TIME_NANOSEC)
                          .asUInt()}};
  qos.destination_order = {
      json["destination_order"].get("kind", DEFAULT_KIND).asInt()};
  qos.history = {json["history"].get("kind", DEFAULT_KIND).asInt(),
                 json["history"].get("depth", DEPTH_MIN).asInt()};
  qos.resource_limits = {
      json["resource_limits"].get("max_samples", VALUE_UNLIMIT).asInt(),
      json["resource_limits"].get("max_instances", VALUE_UNLIMIT).asInt(),
      json["resource_limits"]
          .get("max_samples_per_instance", VALUE_UNLIMIT)
          .asInt()};
  qos.durability_service = {
      {json["durability_service"]["service_cleanup_delay"]
           .get("sec", DURATION_MIN)
           .asInt(),
       json["durability_service"]["service_cleanup_delay"]
           .get("nanosec", DURATION_MIN)
           .asUInt()},
      json["durability_service"].get("kind", DEFAULT_KIND).asInt(),
      json["durability_service"].get("depth", DEPTH_MIN).asInt(),
      json["durability_service"].get("max_samples", VALUE_UNLIMIT).asInt(),
      json["durability_service"].get("max_instances", VALUE_UNLIMIT).asInt(),
      json["durability_service"]
          .get("max_samples_per_instance", VALUE_UNLIMIT)
          .asInt(),
  };
}

void Loader::parse_partition(Domain &domain, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    Partition partition;
    partition.name = json[i]["name"].asString();
    parse_publisher(partition, json[i]["publisher"]);
    parse_subscriber(partition, json[i]["subscriber"]);
    domain.partitions.push_back(partition);
  }
}

void Loader::parse_publisher(Partition &partition, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    Publisher pub;
    pub.id = json[i]["id"].asInt();
    parse_publisher_qos(pub.qos, json[i]["pub_qos"]);
    parse_data_writer(pub, json[i]["data_writer"]);
    partition.pubs.push_back(pub);
  }
}

void Loader::parse_publisher_qos(PubQos &qos, Value json) {
  qos.group_data = {json["group_data"].get("data", EMPTY_DATA).asString()};
  qos.entity_factory = {
      json["entity_factory"].get("autoenable_created_entities", true).asBool()};
  qos.presentation = {
      json["presentation"].get("kind", DEFAULT_KIND).asInt(),
      json["presentation"].get("coherent_access", false).asBool(),
      json["presentation"].get("ordered_access", false).asBool()};
}

void Loader::parse_data_writer(Publisher &pub, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    DataWriter dw;
    dw.id = json[i]["id"].asInt();
    dw.dst_topic = json[i]["dst_topic"].asString();
    dw.size = json[i]["size"].asUInt();
    dw.cycletime = json[i]["cycletime"].asUInt();
    parse_data_writer_qos(dw.qos, json[i]["dw_qos"]);
    pub.writers.push_back(dw);
  }
}

void Loader::parse_data_writer_qos(DwQos &qos, Value json) {
  qos.user_data = {json["user_data"].get("data", EMPTY_DATA).asString()};
  qos.transport_priority = {
      json["transport_priority"].get("value", VALUE_MIN).asInt()};
  qos.lifespan = {
      {json["lifespan"]["duration"].get("sec", DURATION_MAX).asInt(),
       json["lifespan"]["duration"].get("nanosec", DURATION_MAX).asUInt()}};
  qos.durability = {json["durability"].get("kind", DEFAULT_KIND).asInt()};
  qos.deadline = {
      {json["deadline"]["period"].get("sec", DURATION_MAX).asInt(),
       json["deadline"]["period"].get("nanosec", DURATION_MAX).asUInt()}};
  qos.latency_budget = {
      {json["latency_budget"]["duration"].get("sec", DURATION_MIN).asInt(),
       json["latency_budget"]["duration"]
           .get("nanosec", DURATION_MIN)
           .asUInt()}};
  qos.ownership = {json["ownership"].get("kind", DEFAULT_KIND).asInt()};
  qos.ownership_strength = {
      json["ownership_strength"].get("value", VALUE_MIN).asInt()};
  qos.liveliness = {
      json["liveliness"].get("kind", DEFAULT_KIND).asInt(),
      {json["liveliness"]["lease_duration"].get("sec", DURATION_MAX).asInt(),
       json["liveliness"]["lease_duration"]
           .get("nanosec", DURATION_MAX)
           .asUInt()}};
  qos.reliability = {
      json["reliability"].get("kind", DEFAULT_DW_RELIABILITY_KIND).asInt(),
      {json["reliability"]["max_blocking_time"]
           .get("sec", DEFAULT_BLOCK_TIME_SEC)
           .asInt(),
       json["reliability"]["max_blocking_time"]
           .get("nanosec", DEFAULT_BLOCK_TIME_NANOSEC)
           .asUInt()}};
  qos.destination_order = {
      json["destination_order"].get("kind", DEFAULT_KIND).asInt()};
  qos.history = {json["history"].get("kind", DEFAULT_KIND).asInt(),
                 json["history"].get("depth", DEPTH_MIN).asInt()};
  qos.resource_limits = {
      json["resource_limits"].get("max_samples", VALUE_UNLIMIT).asInt(),
      json["resource_limits"].get("max_instances", VALUE_UNLIMIT).asInt(),
      json["resource_limits"]
          .get("max_samples_per_instance", VALUE_UNLIMIT)
          .asInt()};
  qos.writer_data_lifecycle = {
      json["writer_data_lifecycle"]
          .get("autodispose_unregistered_instances", true)
          .asBool(),
      {json["writer_data_lifecycle"]["autopurge_suspended_samples_delay"]
           .get("sec", DURATION_MAX)
           .asInt(),
       json["writer_data_lifecycle"]["autopurge_suspended_samples_delay"]
           .get("nanosec", DURATION_MAX)
           .asUInt()},
      {json["writer_data_lifecycle"]["autounregister_instance_delay"]
           .get("sec", DURATION_MAX)
           .asInt(),
       json["writer_data_lifecycle"]["autounregister_instance_delay"]
           .get("nanosec", DURATION_MAX)
           .asUInt()}};
}

void Loader::parse_subscriber(Partition &partition, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    Subscriber sub;
    sub.id = json[i]["id"].asInt();
    parse_subscriber_qos(sub.qos, json[i]["sub_qos"]);
    parse_data_reader(sub, json[i]["data_reader"]);
    partition.subs.push_back(sub);
  }
}

void Loader::parse_subscriber_qos(SubQos &qos, Value json) {
  qos.group_data = {json["group_data"].get("data", EMPTY_DATA).asString()};
  qos.entity_factory = {
      json["entity_factory"].get("autoenable_created_entities", true).asBool()};
  qos.presentation = {
      json["presentation"].get("kind", DEFAULT_KIND).asInt(),
      json["presentation"].get("coherent_access", false).asBool(),
      json["presentation"].get("ordered_access", false).asBool()};
}

void Loader::parse_data_reader(Subscriber &sub, Value json) {
  for (unsigned int i = 0; i < json.size(); ++i) {
    DataReader dr;
    dr.id = json[i]["id"].asInt();
    dr.src_topic = json[i]["src_topic"].asString();
    parse_data_reader_qos(dr.qos, json[i]["dr_qos"]);
    sub.readers.push_back(dr);
  }
}

void Loader::parse_data_reader_qos(DrQos &qos, Value json) {
  qos.user_data = {json["user_data"].get("data", EMPTY_DATA).asString()};
  qos.durability = {json["durability"].get("kind", DEFAULT_KIND).asInt()};
  qos.deadline = {
      {json["deadline"]["period"].get("sec", DURATION_MAX).asInt(),
       json["deadline"]["period"].get("nanosec", DURATION_MAX).asUInt()}};
  qos.latency_budget = {
      {json["latency_budget"]["duration"].get("sec", DURATION_MIN).asInt(),
       json["latency_budget"]["duration"]
           .get("nanosec", DURATION_MIN)
           .asUInt()}};
  qos.ownership = {json["ownership"].get("kind", DEFAULT_KIND).asInt()};
  qos.liveliness = {
      json["liveliness"].get("kind", DEFAULT_KIND).asInt(),
      {json["liveliness"]["lease_duration"].get("sec", DURATION_MAX).asInt(),
       json["liveliness"]["lease_duration"]
           .get("nanosec", DURATION_MAX)
           .asUInt()}};
  qos.time_based_filter = {{json["time_based_filter"]["minimum_separation"]
                                .get("sec", DURATION_MIN)
                                .asInt(),
                            json["time_based_filter"]["minimum_separation"]
                                .get("nanosec", DURATION_MIN)
                                .asUInt()}};
  qos.reliability = {json["reliability"].get("kind", DEFAULT_KIND).asInt(),
                     {json["reliability"]["max_blocking_time"]
                          .get("sec", DEFAULT_BLOCK_TIME_SEC)
                          .asInt(),
                      json["reliability"]["max_blocking_time"]
                          .get("nanosec", DEFAULT_BLOCK_TIME_NANOSEC)
                          .asUInt()}};
  qos.destination_order = {
      json["destination_order"].get("kind", DEFAULT_KIND).asInt()};
  qos.history = {json["history"].get("kind", DEFAULT_KIND).asInt(),
                 json["history"].get("depth", DEPTH_MIN).asInt()};
  qos.resource_limits = {
      json["resource_limits"].get("max_samples", VALUE_UNLIMIT).asInt(),
      json["resource_limits"].get("max_instances", VALUE_UNLIMIT).asInt(),
      json["resource_limits"]
          .get("max_samples_per_instance", VALUE_UNLIMIT)
          .asInt()};
  qos.reader_data_lifecycle = {
      {json["reader_data_lifecycle"]["autopurge_nowriter_samples_delay"]
           .get("sec", DURATION_MAX)
           .asInt(),
       json["reader_data_lifecycle"]["autopurge_nowriter_samples_delay"]
           .get("nanosec", DURATION_MAX)
           .asUInt()},
      {json["reader_data_lifecycle"]["autopurge_disposed_samples_delay"]
           .get("sec", DURATION_MAX)
           .asInt(),
       json["reader_data_lifecycle"]["autopurge_disposed_samples_delay"]
           .get("nanosec", DURATION_MAX)
           .asUInt()},
      json["reader_data_lifecycle"]
          .get("autopurge_dispose_all", false)
          .asBool(),
      json["reader_data_lifecycle"].get("kind", DEFAULT_KIND).asInt()};
}
