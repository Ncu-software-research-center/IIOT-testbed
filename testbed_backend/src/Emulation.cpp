/**
 * LOGICAL_NAME:    Emulation.cpp
 * FUNCTION:        Run the emulation with user's arguments.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Manager.hpp"
#include "ccpp_dds_dcps.h"

using namespace std;

/* entry point exported and demangled so symbol can be found in shared library
 */
extern "C" {
OS_API_EXPORT
int emulation(int argc, char *argv[]);
}

/* Main wrapper to allow embedded usage of the Publisher application. */
int main(int argc, char *argv[]) { return emulation(argc, argv); }

int emulation(int argc, char *argv[]) {
  Manager manager;
  manager.load();   // load user arguments from file
  manager.init();   // initialize DDS Entity
  manager.ready();  // submit ready
  manager.run();    // start emulating
  manager.save();   // save device report
  return 0;
}
