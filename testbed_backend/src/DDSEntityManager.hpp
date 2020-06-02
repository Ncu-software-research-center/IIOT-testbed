/**
 * LOGICAL_NAME:    DDSEntityManager.hpp
 * FUNCTION:        Manage OpenSplice DDS Entities and QoS Policies.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_DDS_ENRITY_MANAGER_
#define TESTBED_BACKEND_DDS_ENRITY_MANAGER_

#include <map>
#include <string>
#include <vector>
#include "Data.hpp"
#include "MeasureReceiver.hpp"
#include "MeasureSender.hpp"
#include "Receiver.hpp"
#include "Sender.hpp"
#include "ccpp_dds_dcps.h"

class DDSEntityManager {
 private:
  DDS::DomainParticipantFactory_var factory;
  DDS::DomainParticipant_var participant;
  std::map<std::string, DDS::Topic_var> topics;
  std::vector<DDS::Publisher_var> publishers;
  std::vector<DDS::Subscriber_var> subscribers;
  std::vector<DDS::DataWriter_var> writers;
  std::vector<DDS::DataReader_var> readers;
  std::vector<Receiver*> receivers;
  std::vector<Sender*> senders;
  MeasureSender* measure_sender;
  MeasureReceiver* measure_receiver;
  std::string measure_topic_name = "measure";
  std::string measure_partition_name = "measure";
  std::string msg_type_name;
  std::string measure_msg_type_name;
  long measure_count;

  void create_participant(Device device);
  void create_topics(Domain domain);
  void create_topic(Topic topic, std::string msg_type_name);
  void create_partitions(Domain domain, std::string device_name);
  void create_publisher(Publisher pub, std::string device_name,
                        std::string partition_name);
  DDS::DataWriter_var create_data_writer(DDS::Publisher_var pub_var,
                                         DataWriter dw);
  void create_subscriber(Subscriber sub, std::string device_name,
                         std::string partition_name);
  DDS::DataReader_var create_data_reader(DDS::Subscriber_var sub,
                                         DataReader dr);
  void create_receiver(DDS::DataReader_var dr_var, long id, long sub_id,
                       std::string device, std::string partition,
                       std::string topic);
  void create_sender(DDS::DataWriter_var dw_var, long id, long pub_id,
                     std::string device, std::string partition,
                     std::string topic, long msg_size,
                     unsigned long msg_cycletime);
  void create_measure_receiver(DDS::DataReader_var dr_var, std::string device);
  void create_measure_sender(DDS::DataWriter_var dw_var, std::string device);
  void register_message_type();

 public:
  ~DDSEntityManager();

  void init(Device device);

  std::map<std::string, DDS::Topic_var> get_topics();
  std::vector<DDS::Publisher_var> get_pubs();
  std::vector<DDS::Subscriber_var> get_subs();
  std::vector<DDS::DataWriter_var> get_writers();
  std::vector<DDS::DataReader_var> get_readers();
  std::vector<Receiver*> get_receivers();
  std::vector<Sender*> get_senders();
  MeasureSender* get_measure_sender();
  MeasureReceiver* get_measure_receiver();
};

#endif