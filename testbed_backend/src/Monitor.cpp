/**
 * LOGICAL_NAME:    Monitor.cpp
 * FUNCTION:        Monitor cpu usage, memory consumption and network bandwidth.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Monitor.hpp"
#include <ifaddrs.h>
#include <sys/sysinfo.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <fstream>

using namespace std;

Monitor::Monitor() { get_interface(); }

void Monitor::run() {
  sleep(1);
  data.push_back({get_cpu(), get_ram(), get_rx(), get_tx()});
}

vector<MonitorData> Monitor::get_data() { return data; }

MonitorCpuData Monitor::get_cpu() {
  unsigned long long user, user_low, sys, idle;
  FILE *file;
  file = fopen("/proc/stat", "r");
  int ret =
      fscanf(file, "cpu %llu %llu %llu %llu", &user, &user_low, &sys, &idle);
  fclose(file);
  if (ret < 4) return {0, 0, 0, 0};
  return {user, user_low, sys, idle};
}

double Monitor::get_ram() {
  struct sysinfo memInfo;
  sysinfo(&memInfo);
  double totalVirtualMem = memInfo.totalram;
  // Add other values in next statement to avoid int overflow on right hand
  // side...
  totalVirtualMem += memInfo.totalswap;
  totalVirtualMem *= memInfo.mem_unit;

  double virtualMemUsed = memInfo.totalram - memInfo.freeram;
  // Add other values in next statement to avoid int overflow on right hand
  // side...
  virtualMemUsed += memInfo.totalswap - memInfo.freeswap;
  virtualMemUsed *= memInfo.mem_unit;

  return virtualMemUsed / totalVirtualMem * 100;
}

long long Monitor::get_rx() { return get_bandwidth("rx_bytes"); }

long long Monitor::get_tx() { return get_bandwidth("tx_bytes"); }

long long Monitor::get_bandwidth(string bandwidth) {
  string bw;
  ifstream bw_file(
      string("/sys/class/net/" + interface + "/statistics/" + bandwidth));
  if (bw_file.good() == 1) {
    if (bw_file.is_open()) {
      while (!bw_file.eof()) bw_file >> bw;
    }
  }
  bw_file.close();
  return stoll(bw);
}

void Monitor::get_interface() {
  struct ifaddrs *ifaddr(NULL), *ifhead(NULL);
  getifaddrs(&ifaddr);
  ifhead = ifaddr;
  while (ifaddr != NULL) {
    if (strcmp(ifaddr->ifa_name, "lo") == 0)
      ifaddr = ifaddr->ifa_next;
    else {
      interface = string(ifaddr->ifa_name);
      break;
    }
  }
  freeifaddrs(ifhead);
}
