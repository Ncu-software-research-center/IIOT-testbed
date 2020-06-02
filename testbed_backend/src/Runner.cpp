/**
 * LOGICAL_NAME:    Runner.cpp
 * FUNCTION:        Maintain lifecycle of a thread.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Runner.hpp"

using namespace std;

void Runner::run() {}

void Runner::do_run() {
  do {
    run();
  } while (!is_stop);
}

void Runner::before_join() {}
void Runner::after_stop() {}

void Runner::start() { loop = thread(&Runner::do_run, this); }

void Runner::stop() {
  is_stop = true;
  before_join();
  loop.join();
  after_stop();
}
