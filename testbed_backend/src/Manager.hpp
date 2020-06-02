/**
 * LOGICAL_NAME:    Manager.hpp
 * FUNCTION:        Manage lifecycle of emulation.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_MANAGER_
#define TESTBED_BACKEND_MANAGER_

#include <vector>
#include "DDSEntityManager.hpp"
#include "Data.hpp"
#include "Loader.hpp"
#include "Monitor.hpp"
#include "Saver.hpp"

#define DATA_SETTING_DIR \
  "{TOPdir}/testbed/datasetting/dds_descriptive_file.json"
#define REPORT_DIR "{TOPdir}/testbed/report/"
#define READY_PATH "{TOPdir}/testbed/ready"
#define START_PATH "{TOPdir}/testbed/start"

class Manager {
 private:
  DDSEntityManager dds;
  Monitor monitor;
  Saver saver;
  Loader loader;
  Device device;
  std::vector<Sender*> senders;
  std::vector<Receiver*> receivers;
  MeasureReceiver* measure_receiver;
  MeasureSender* measure_sender;

  void wait_start();

 public:
  void load();   // load arguments with loader
  void init();   // initialize entities with dds
  void ready();  // wait to start emulating
  void run();    // start emulating
  void save();   // save device report
};

#endif