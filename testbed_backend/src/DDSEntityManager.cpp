/**
 * LOGICAL_NAME:    DDSEntityManager.cpp
 * FUNCTION:        Manage OpenSplice DDS Entities and QoS Policies.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "DDSEntityManager.hpp"
#include "dds_debug.hpp"

using namespace std;

namespace {

void octet_append(DDS::octSeq &seq, string value) {
  for (unsigned int i = 0; i < value.length(); ++i) {
    unsigned long len = seq.length();
    seq.length(len + 1);
    seq[len] = static_cast<unsigned char>(value[i]);
  }
}

void assign_entity_factory_to_dds(DDS::EntityFactoryQosPolicy &qos,
                                  EntityFactoryQos setting) {
  qos.autoenable_created_entities = setting.autoenable_created_entities;
}

void assign_user_data_to_dds(DDS::UserDataQosPolicy &qos, UserDataQos setting) {
  octet_append(qos.value, setting.data);
}

void assign_topic_data_to_dds(DDS::TopicDataQosPolicy &qos,
                              TopicDataQos setting) {
  octet_append(qos.value, setting.data);
}

void assign_group_data_to_dds(DDS::GroupDataQosPolicy &qos,
                              GroupDataQos setting) {
  octet_append(qos.value, setting.data);
}
void assign_partition_to_dds(DDS::PartitionQosPolicy &qos,
                             string partition_name) {
  qos.name.length(1);
  qos.name[0] = partition_name.c_str();
}

void assign_durability_to_dds(DDS::DurabilityQosPolicy &qos,
                              DurabilityQos setting) {
  qos.kind = static_cast<DDS::DurabilityQosPolicyKind>(setting.kind);
}

void assign_durability_service_to_dds(DDS::DurabilityServiceQosPolicy &qos,
                                      DurabilityServiceQos setting) {
  qos.service_cleanup_delay.sec = setting.service_cleanup_delay.sec;
  qos.service_cleanup_delay.nanosec = setting.service_cleanup_delay.nanosec;
  qos.history_kind = static_cast<DDS::HistoryQosPolicyKind>(setting.kind);
  qos.history_depth = setting.depth;
  qos.max_samples = setting.max_samples;
  qos.max_instances = setting.max_instances;
  qos.max_samples_per_instance = setting.max_samples_per_instance;
}

void assign_deadline_to_dds(DDS::DeadlineQosPolicy &qos, DeadlineQos setting) {
  qos.period.sec = setting.period.sec;
  qos.period.nanosec = setting.period.nanosec;
}

void assign_latency_budget_to_dds(DDS::LatencyBudgetQosPolicy &qos,
                                  LatencyBudgetQos setting) {
  qos.duration.sec = setting.duration.sec;
  qos.duration.nanosec = setting.duration.nanosec;
}

void assign_liveliness_to_dds(DDS::LivelinessQosPolicy &qos,
                              LivelinessQos setting) {
  qos.kind = static_cast<DDS::LivelinessQosPolicyKind>(setting.kind);
  qos.lease_duration.sec = setting.lease_duration.sec;
  qos.lease_duration.nanosec = setting.lease_duration.nanosec;
}

void assign_reliability_to_dds(DDS::ReliabilityQosPolicy &qos,
                               ReliabilityQos setting) {
  qos.kind = static_cast<DDS::ReliabilityQosPolicyKind>(setting.kind);
  qos.max_blocking_time.sec = setting.max_blocking_time.sec;
  qos.max_blocking_time.nanosec = setting.max_blocking_time.nanosec;
}

void assign_destination_order_to_dds(DDS::DestinationOrderQosPolicy &qos,
                                     DestinationOrderQos setting) {
  qos.kind = static_cast<DDS::DestinationOrderQosPolicyKind>(setting.kind);
}

void assign_history_to_dds(DDS::HistoryQosPolicy &qos, HistoryQos setting) {
  qos.kind = static_cast<DDS::HistoryQosPolicyKind>(setting.kind);
  qos.depth = setting.depth;
}

void assign_resource_limits_to_dds(DDS::ResourceLimitsQosPolicy &qos,
                                   ResourceLimitsQos setting) {
  qos.max_samples = setting.max_samples;
  qos.max_instances = setting.max_instances;
  qos.max_samples_per_instance = setting.max_samples_per_instance;
}

void assign_transport_priority_to_dds(DDS::TransportPriorityQosPolicy &qos,
                                      TransportPriorityQos setting) {
  qos.value = setting.value;
}

void assign_lifespan_to_dds(DDS::LifespanQosPolicy &qos, LifespanQos setting) {
  qos.duration.sec = setting.duration.sec;
  qos.duration.nanosec = setting.duration.nanosec;
}

void assign_ownership_to_dds(DDS::OwnershipQosPolicy &qos,
                             OwnershipQos setting) {
  qos.kind = static_cast<DDS::OwnershipQosPolicyKind>(setting.kind);
}

void assign_ownership_strength_to_dds(DDS::OwnershipStrengthQosPolicy &qos,
                                      OwnershipStrengthQos setting) {
  qos.value = setting.value;
}

void assign_presentation_to_dds(DDS::PresentationQosPolicy &qos,
                                PresentationQos setting) {
  qos.access_scope =
      static_cast<DDS::PresentationQosPolicyAccessScopeKind>(setting.kind);
  qos.coherent_access = setting.coherent_access;
  qos.ordered_access = setting.ordered_access;
}

void assign_writer_data_lifecycle_to_dds(DDS::WriterDataLifecycleQosPolicy &qos,
                                         WriterDataLifecycleQos setting) {
  qos.autodispose_unregistered_instances =
      setting.autodispose_unregistered_instances;
  qos.autopurge_suspended_samples_delay.sec =
      setting.autopurge_suspended_samples_delay.sec;
  qos.autopurge_suspended_samples_delay.nanosec =
      setting.autopurge_suspended_samples_delay.nanosec;
  qos.autounregister_instance_delay.sec =
      setting.autounregister_instance_delay.sec;
  qos.autounregister_instance_delay.nanosec =
      setting.autounregister_instance_delay.nanosec;
}

void assign_time_based_filter_to_dds(DDS::TimeBasedFilterQosPolicy &qos,
                                     TimeBasedFilterQos setting) {
  qos.minimum_separation.sec = setting.minimum_separation.sec;
  qos.minimum_separation.nanosec = setting.minimum_separation.nanosec;
}

void assign_reader_data_lifecycle_to_dds(DDS::ReaderDataLifecycleQosPolicy &qos,
                                         ReaderDataLifecycleQos setting) {
  qos.autopurge_nowriter_samples_delay.sec =
      setting.autopurge_nowriter_samples_delay.sec;
  qos.autopurge_nowriter_samples_delay.nanosec =
      setting.autopurge_nowriter_samples_delay.nanosec;
  qos.autopurge_disposed_samples_delay.sec =
      setting.autopurge_disposed_samples_delay.sec;
  qos.autopurge_disposed_samples_delay.nanosec =
      setting.autopurge_disposed_samples_delay.nanosec;
  qos.invalid_sample_visibility.kind =
      static_cast<DDS::InvalidSampleVisibilityQosPolicyKind>(setting.kind);
}

void set_topic_qos(DDS::TopicQos &qos, TopicQos setting) {
  assign_topic_data_to_dds(qos.topic_data, setting.topic_data);
  assign_durability_to_dds(qos.durability, setting.durability);
  assign_durability_service_to_dds(qos.durability_service,
                                   setting.durability_service);
  assign_deadline_to_dds(qos.deadline, setting.deadline);
  assign_latency_budget_to_dds(qos.latency_budget, setting.latency_budget);
  assign_liveliness_to_dds(qos.liveliness, setting.liveliness);
  assign_reliability_to_dds(qos.reliability, setting.reliability);
  assign_destination_order_to_dds(qos.destination_order,
                                  setting.destination_order);
  assign_history_to_dds(qos.history, setting.history);
  assign_resource_limits_to_dds(qos.resource_limits, setting.resource_limits);
  assign_transport_priority_to_dds(qos.transport_priority,
                                   setting.transport_priority);
  assign_lifespan_to_dds(qos.lifespan, setting.lifespan);
  assign_ownership_to_dds(qos.ownership, setting.ownership);
}

void set_publisher_qos(DDS::PublisherQos &qos, PubQos setting,
                       string partition_name) {
  assign_partition_to_dds(qos.partition, partition_name);
  assign_group_data_to_dds(qos.group_data, setting.group_data);
  assign_presentation_to_dds(qos.presentation, setting.presentation);
  assign_entity_factory_to_dds(qos.entity_factory, setting.entity_factory);
}

void set_data_writer_qos(DDS::DataWriterQos &qos, DwQos setting) {
  assign_user_data_to_dds(qos.user_data, setting.user_data);
  assign_transport_priority_to_dds(qos.transport_priority,
                                   setting.transport_priority);
  assign_lifespan_to_dds(qos.lifespan, setting.lifespan);
  assign_durability_to_dds(qos.durability, setting.durability);
  assign_deadline_to_dds(qos.deadline, setting.deadline);
  assign_latency_budget_to_dds(qos.latency_budget, setting.latency_budget);
  assign_ownership_to_dds(qos.ownership, setting.ownership);
  assign_ownership_strength_to_dds(qos.ownership_strength,
                                   setting.ownership_strength);
  assign_liveliness_to_dds(qos.liveliness, setting.liveliness);
  assign_reliability_to_dds(qos.reliability, setting.reliability);
  assign_destination_order_to_dds(qos.destination_order,
                                  setting.destination_order);
  assign_history_to_dds(qos.history, setting.history);
  assign_resource_limits_to_dds(qos.resource_limits, setting.resource_limits);
  assign_writer_data_lifecycle_to_dds(qos.writer_data_lifecycle,
                                      setting.writer_data_lifecycle);
}

void set_subscriber_qos(DDS::SubscriberQos &qos, SubQos setting,
                        string partition_name) {
  assign_partition_to_dds(qos.partition, partition_name);
  assign_group_data_to_dds(qos.group_data, setting.group_data);
  assign_presentation_to_dds(qos.presentation, setting.presentation);
  assign_entity_factory_to_dds(qos.entity_factory, setting.entity_factory);
}

void set_data_reader_qos(DDS::DataReaderQos &qos, DrQos setting) {
  assign_user_data_to_dds(qos.user_data, setting.user_data);
  assign_durability_to_dds(qos.durability, setting.durability);
  assign_deadline_to_dds(qos.deadline, setting.deadline);
  assign_latency_budget_to_dds(qos.latency_budget, setting.latency_budget);
  assign_ownership_to_dds(qos.ownership, setting.ownership);
  assign_liveliness_to_dds(qos.liveliness, setting.liveliness);
  assign_time_based_filter_to_dds(qos.time_based_filter,
                                  setting.time_based_filter);
  assign_reliability_to_dds(qos.reliability, setting.reliability);
  assign_destination_order_to_dds(qos.destination_order,
                                  setting.destination_order);
  assign_history_to_dds(qos.history, setting.history);
  assign_resource_limits_to_dds(qos.resource_limits, setting.resource_limits);
  assign_reader_data_lifecycle_to_dds(qos.reader_data_lifecycle,
                                      setting.reader_data_lifecycle);
}

#define HISTORY_KIND_KEEP_ALL 1
#define RELIABILITY_KIND_RELIABLE 1
#define DURABILITY_KIND_TRANSIENT 2

Topic get_measure_topic(string topic_name) {
  Topic measure;
  measure.name = topic_name;
  measure.qos.topic_data = {EMPTY_DATA};
  measure.qos.transport_priority = {VALUE_MIN};
  measure.qos.reliability = {
      RELIABILITY_KIND_RELIABLE,
      {DEFAULT_BLOCK_TIME_SEC, DEFAULT_BLOCK_TIME_NANOSEC}};  // RELIABLE
  measure.qos.durability = {DURABILITY_KIND_TRANSIENT};       // TRANSIENT
  measure.qos.lifespan = {DURATION_MAX, DURATION_MAX};
  measure.qos.deadline = {DURATION_MAX, DURATION_MAX};
  measure.qos.latency_budget = {DURATION_MIN, DURATION_MIN};
  measure.qos.ownership = {DEFAULT_KIND};
  measure.qos.liveliness = {DEFAULT_KIND, {DURATION_MAX, DURATION_MAX}};
  measure.qos.destination_order = {DEFAULT_KIND};
  measure.qos.history = {HISTORY_KIND_KEEP_ALL, DEPTH_MIN};
  measure.qos.resource_limits = {VALUE_MAX, VALUE_MAX, VALUE_MAX};
  measure.qos.durability_service = {{DURATION_MIN, DURATION_MIN},
                                    HISTORY_KIND_KEEP_ALL,
                                    DEPTH_MIN,
                                    VALUE_MAX,
                                    VALUE_MAX,
                                    VALUE_MAX};
  return measure;
}

Publisher get_measure_publisher(string dst_topic) {
  DwQos dw_qos;
  dw_qos.user_data = {EMPTY_DATA};
  dw_qos.transport_priority = {VALUE_MIN};
  dw_qos.lifespan = {DURATION_MAX, DURATION_MAX};
  dw_qos.durability = {DURABILITY_KIND_TRANSIENT};  // TRANSIENT
  dw_qos.deadline = {DURATION_MAX, DURATION_MAX};
  dw_qos.latency_budget = {DURATION_MIN, DURATION_MIN};
  dw_qos.ownership = {DEFAULT_KIND};
  dw_qos.ownership_strength = {VALUE_MIN};
  dw_qos.liveliness = {DEFAULT_KIND, {DURATION_MAX, DURATION_MAX}};
  dw_qos.reliability = {
      RELIABILITY_KIND_RELIABLE,
      {DEFAULT_BLOCK_TIME_SEC, DEFAULT_BLOCK_TIME_NANOSEC}};  // RELIABLE
  dw_qos.destination_order = {DEFAULT_KIND};
  dw_qos.history = {HISTORY_KIND_KEEP_ALL, DEPTH_MIN};
  dw_qos.resource_limits = {VALUE_MAX, VALUE_MAX, VALUE_MAX};
  dw_qos.writer_data_lifecycle = {
      false, {DURATION_MAX, DURATION_MAX}, {DURATION_MAX, DURATION_MAX}};
  DataWriter dw = {0, dst_topic, dw_qos, 0, 0};
  Publisher measure;
  measure.id = 0;
  measure.writers.push_back(dw);
  measure.qos.group_data = {EMPTY_DATA};
  measure.qos.entity_factory = {true};
  measure.qos.presentation = {DEFAULT_KIND, false, false};
  return measure;
}

Subscriber get_measure_subscriber(string src_topic) {
  DrQos dr_qos;
  dr_qos.user_data = {EMPTY_DATA};
  dr_qos.durability = {DURABILITY_KIND_TRANSIENT};  // TRANSIENT
  dr_qos.deadline = {DURATION_MAX, DURATION_MAX};
  dr_qos.latency_budget = {DURATION_MIN, DURATION_MIN};
  dr_qos.ownership = {DEFAULT_KIND};
  dr_qos.liveliness = {DEFAULT_KIND, {DURATION_MAX, DURATION_MAX}};
  dr_qos.time_based_filter = {DURATION_MIN, DURATION_MIN};
  dr_qos.reliability = {
      RELIABILITY_KIND_RELIABLE,
      {DEFAULT_BLOCK_TIME_SEC, DEFAULT_BLOCK_TIME_NANOSEC}};  // RELIABLE
  dr_qos.destination_order = {DEFAULT_KIND};
  dr_qos.history = {HISTORY_KIND_KEEP_ALL, DEPTH_MIN};
  dr_qos.resource_limits = {VALUE_MAX, VALUE_MAX, VALUE_MAX};
  dr_qos.reader_data_lifecycle = {{DURATION_MAX, DURATION_MAX},
                                  {DURATION_MAX, DURATION_MAX},
                                  false,
                                  DEFAULT_READER_DATA_LIFECYCLE_KIND};
  DataReader dr = {0, src_topic, dr_qos};
  Subscriber measure;
  measure.id = 0;
  measure.readers.push_back(dr);
  measure.qos.group_data = {EMPTY_DATA};
  measure.qos.entity_factory = {true};
  measure.qos.presentation = {0, false, false};
  return measure;
}

}  // namespace

void DDSEntityManager::init(Device device) {
  measure_count = device.measure_count;
  create_participant(device);
  register_message_type();
  create_topics(device.domain);
  create_partitions(device.domain, device.name);
}

map<string, DDS::Topic_var> DDSEntityManager::get_topics() { return topics; }

vector<DDS::Publisher_var> DDSEntityManager::get_pubs() { return publishers; }

vector<DDS::Subscriber_var> DDSEntityManager::get_subs() { return subscribers; }

vector<DDS::DataWriter_var> DDSEntityManager::get_writers() { return writers; }

vector<DDS::DataReader_var> DDSEntityManager::get_readers() { return readers; }

vector<Receiver *> DDSEntityManager::get_receivers() { return receivers; }

vector<Sender *> DDSEntityManager::get_senders() { return senders; }

MeasureSender *DDSEntityManager::get_measure_sender() { return measure_sender; }

MeasureReceiver *DDSEntityManager::get_measure_receiver() {
  return measure_receiver;
}

DDSEntityManager::~DDSEntityManager() {
  this->factory->delete_contained_entities();
}

static EmulationData::MsgTypeSupport_var msg_type_support;
static EmulationData::ProbMsgTypeSupport_var measure_msg_type_support;

void DDSEntityManager::register_message_type() {
  DDS::ReturnCode_t status;
  // register normal message type
  msg_type_support = new EmulationData::MsgTypeSupport();
  this->msg_type_name = msg_type_support->get_type_name();
  status = msg_type_support->register_type(this->participant,
                                           this->msg_type_name.c_str());
  _check_status(
      status,
      DEBUG_MSG("EmulationData::MsgTypeSupport::register_type() failed"));

  // register meassure message type
  measure_msg_type_support = new EmulationData::ProbMsgTypeSupport();
  this->measure_msg_type_name = measure_msg_type_support->get_type_name();
  status = measure_msg_type_support->register_type(
      this->participant, this->measure_msg_type_name.c_str());
  _check_status(
      status,
      DEBUG_MSG("EmulationData::ProbMsgTypeSupport::register_type() failed"));
}

void DDSEntityManager::create_participant(Device device) {
  // get domain participant factory
  this->factory = DDS::DomainParticipantFactory::get_instance();
  _check_handle(
      factory,
      DEBUG_MSG("DDS::DomainParticipantFactory::get_instance() failed"));

  // set domain participant qos
  DDS::DomainParticipantQos p_qos = PARTICIPANT_QOS_DEFAULT;
  assign_user_data_to_dds(p_qos.user_data, device.domain.qos.user_data);
  assign_entity_factory_to_dds(p_qos.entity_factory,
                               device.domain.qos.entity_factory);

  // create domain participant
  this->participant = factory->create_participant(DDS::DOMAIN_ID_DEFAULT, p_qos,
                                                  NULL, DDS::STATUS_MASK_NONE);
  _check_handle(
      participant,
      DEBUG_MSG("DDS::DomainParticipantFactory::create_participant() failed"));
}

void DDSEntityManager::create_topics(Domain domain) {
  // create measure topic
  create_topic(get_measure_topic(this->measure_topic_name),
               this->measure_msg_type_name);
  // create topic
  for (auto const &topic : domain.topics)
    create_topic(topic, this->msg_type_name);
}

void DDSEntityManager::create_topic(Topic topic, string msg_type_name) {
  DDS::ReturnCode_t status;
  DDS::Topic_var topic_var;
  DDS::TopicQos t_qos;
  // get default topic qos
  status = this->participant->get_default_topic_qos(t_qos);
  _check_status(
      status,
      DEBUG_MSG("DDS::DomainParticipant::get_default_topic_qos() failed"));
  // set topic qos
  set_topic_qos(t_qos, topic.qos);
  // create topic
  topic_var =
      this->participant->create_topic(topic.name.c_str(), msg_type_name.c_str(),
                                      t_qos, NULL, DDS::STATUS_MASK_NONE);
  _check_handle(topic_var,
                DEBUG_MSG("DDS::DomainParticipant::create_topic() failed"));
  this->topics[topic.name] = topic_var;
}

void DDSEntityManager::create_partitions(Domain domain, string device_name) {
  // create measure publisher and measure sender
  create_publisher(get_measure_publisher(this->measure_topic_name), device_name,
                   this->measure_partition_name);
  // create measure subscriber and measure receiver
  create_subscriber(get_measure_subscriber(this->measure_topic_name),
                    device_name, this->measure_partition_name);
  for (auto const &partition : domain.partitions) {
    // create publishers
    for (auto const &pub : partition.pubs)
      create_publisher(pub, device_name, partition.name);
    // create subscribers
    for (auto const &sub : partition.subs)
      create_subscriber(sub, device_name, partition.name);
  }
}

void DDSEntityManager::create_publisher(Publisher pub, string device_name,
                                        string partition_name) {
  DDS::ReturnCode_t status;
  DDS::Publisher_var pub_var;
  DDS::PublisherQos p_qos;
  // get default publisher qos
  status = this->participant->get_default_publisher_qos(p_qos);
  _check_status(
      status,
      DEBUG_MSG("DDS::DomainParticipant::get_default_publisher_qos() failed"));
  // set publisher qos
  set_publisher_qos(p_qos, pub.qos, partition_name);
  // create publisher
  pub_var =
      this->participant->create_publisher(p_qos, NULL, DDS::STATUS_MASK_NONE);
  _check_handle(pub_var,
                DEBUG_MSG("DDS::DomainParticipant::create_publisher() failed"));
  this->publishers.push_back(pub_var);
  // create data_writers and senders
  for (auto const &dw : pub.writers) {
    DDS::DataWriter_var dw_var = create_data_writer(pub_var, dw);
    if (partition_name != measure_partition_name)
      create_sender(dw_var, dw.id, pub.id, device_name, partition_name,
                    dw.dst_topic, dw.size, dw.cycletime);
    else {
      // create measure sender
      create_measure_sender(dw_var, device_name);
    }
  }
}

DDS::DataWriter_var DDSEntityManager::create_data_writer(DDS::Publisher_var pub,
                                                         DataWriter dw) {
  DDS::ReturnCode_t status;
  DDS::DataWriter_var dw_var;
  DDS::DataWriterQos dw_qos;
  DDS::Topic_var topic = this->topics[dw.dst_topic];
  DDS::TopicQos t_qos;
  // get default data writer qos
  status = pub->get_default_datawriter_qos(dw_qos);
  _check_status(
      status, DEBUG_MSG("DDS::Publisher::get_default_datawriter_qos() failed"));
  // get topic qos
  status = topic->get_qos(t_qos);
  _check_status(status, DEBUG_MSG("DDS::Topic::get_qos() failed"));
  // copy qos from topic qos
  status = pub->copy_from_topic_qos(dw_qos, t_qos);
  _check_status(status,
                DEBUG_MSG("DDS::Publisher::copy_from_topic_qos() failed"));
  // set data writer qos
  set_data_writer_qos(dw_qos, dw.qos);
  // create data writer
  dw_var = pub->create_datawriter(topic, dw_qos, NULL, DDS::STATUS_MASK_NONE);
  _check_handle(dw_var,
                DEBUG_MSG("DDS::Publisher::create_datawriter() failed"));
  writers.push_back(dw_var);
  return dw_var;
}

void DDSEntityManager::create_subscriber(Subscriber sub, string device_name,
                                         string partition_name) {
  DDS::ReturnCode_t status;
  DDS::Subscriber_var sub_var;
  DDS::SubscriberQos s_qos;
  // get default subscriber qos
  status = this->participant->get_default_subscriber_qos(s_qos);
  _check_status(
      status,
      DEBUG_MSG("DDS::DomainParticipant::get_default_subscriber_qos() failed"));
  // set subscriber qos
  set_subscriber_qos(s_qos, sub.qos, partition_name);
  // create subscriber
  sub_var =
      this->participant->create_subscriber(s_qos, NULL, DDS::STATUS_MASK_NONE);
  _check_handle(
      sub_var, DEBUG_MSG("DDS::DomainParticipant::create_subscriber() failed"));
  this->subscribers.push_back(sub_var);
  // create data readers and receivers
  for (auto const &dr : sub.readers) {
    DDS::DataReader_var dr_var = create_data_reader(sub_var, dr);
    if (partition_name != measure_partition_name)
      create_receiver(dr_var, dr.id, sub.id, device_name, partition_name,
                      dr.src_topic);
    else {
      // create measure receiver
      create_measure_receiver(dr_var, device_name);
    }
  }
}

DDS::DataReader_var DDSEntityManager::create_data_reader(
    DDS::Subscriber_var sub, DataReader dr) {
  DDS::ReturnCode_t status;
  DDS::DataReader_var dr_var;
  DDS::DataReaderQos dr_qos;
  DDS::Topic_var topic = this->topics[dr.src_topic];
  DDS::TopicQos t_qos;
  // get default data reader qos
  status = sub->get_default_datareader_qos(dr_qos);
  _check_status(
      status,
      DEBUG_MSG("DDS::Subscriber::get_default_datareader_qos() failed"));
  // get topic qos
  status = topic->get_qos(t_qos);
  _check_status(status, DEBUG_MSG("DDS::Topic::get_qos() failed"));
  // copy qos from topic qos
  status = sub->copy_from_topic_qos(dr_qos, t_qos);
  _check_status(status,
                DEBUG_MSG("DDS::Subscriber::copy_from_topic_qos() failed"));
  // set data reader qos
  set_data_reader_qos(dr_qos, dr.qos);
  // create data reader
  dr_var = sub->create_datareader(topic, dr_qos, NULL, DDS::STATUS_MASK_NONE);
  _check_handle(dr_var,
                DEBUG_MSG("DDS::Subscriber::create_datareader() failed"));
  readers.push_back(dr_var);
  return dr_var;
}

void DDSEntityManager::create_receiver(DDS::DataReader_var dr_var, long id,
                                       long sub_id, string device,
                                       string partition, string topic) {
  Receiver *receiver =
      new Receiver(measure_sender, id, sub_id, device, topic, partition);
  receiver->set_data_reader(dr_var);
  receivers.push_back(receiver);
}

void DDSEntityManager::create_sender(DDS::DataWriter_var dw_var, long id,
                                     long pub_id, std::string device,
                                     std::string partition, std::string topic,
                                     long msg_size,
                                     unsigned long msg_cycletime) {
  Sender *sender =
      new Sender(measure_receiver, id, pub_id, device, topic, partition,
                 measure_count, msg_size, msg_cycletime);
  sender->set_data_writer(dw_var);
  senders.push_back(sender);
}

void DDSEntityManager::create_measure_receiver(DDS::DataReader_var dr_var,
                                               std::string device) {
  measure_receiver = new MeasureReceiver(device);
  measure_receiver->set_data_reader(dr_var);
}

void DDSEntityManager::create_measure_sender(DDS::DataWriter_var dw_var,
                                             string device) {
  measure_sender = new MeasureSender(device);
  measure_sender->set_data_writer(dw_var);
}
