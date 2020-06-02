/**
 * LOGICAL_NAME:    Runner.hpp
 * FUNCTION:        Maintain lifecycle of a thread.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_RUNNER_
#define TESTBED_BACKEND_RUNNER_

#include <thread>

class Runner {
 private:
  bool is_stop = false;
  std::thread loop;
  void do_run();
  virtual void run();
  virtual void before_join();
  virtual void after_stop();

 public:
  void start();
  void stop();
};

#endif