/**
 * LOGICAL_NAME:    Saver.cpp
 * FUNCTION:        Output report file.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#include "Saver.hpp"
#include <jsoncpp/json/json.h>
#include <fstream>
#include "debug.hpp"

using namespace std;
using namespace Json;

void Saver::save(string device, string path) {
  Value json;
  Value data_writers;
  Value data_readers;
  Value resource;
  for (DwData dw : data_writer_data) {
    Value data;
    Value latency;
    data["id"] = static_cast<int>(dw.id);
    data["pub_id"] = static_cast<int>(dw.pub_id);
    data["partition"] = dw.partition;
    data["dst_device"] = dw.dst_device;
    data["dst_topic"] = dw.dst_topic;
    data["pub_msg_count"] = static_cast<int>(dw.pub_msg_count);
    for (double dw_latency : dw.latency) latency.append(dw_latency);
    data["latency"] = latency;
    data_writers.append(data);
  }
  for (DrData dr : data_reader_data) {
    Value data;
    Value sub_msg_id;
    data["id"] = static_cast<int>(dr.id);
    data["sub_id"] = static_cast<int>(dr.sub_id);
    data["partition"] = dr.partition;
    data["src_device"] = dr.src_device;
    data["src_topic"] = dr.src_topic;
    data["sub_msg_count"] = static_cast<int>(dr.data.msg_count);
    for (double dr_sub_msg_id : dr.data.msg_id)
      sub_msg_id.append(dr_sub_msg_id);
    data["sub_msg_id"] = sub_msg_id;
    data_readers.append(data);
  }
  for (ResourceData rd : resource_data) {
    resource["cpu"].append(rd.cpu);
    resource["memory"].append(rd.memory);
    resource["rx"].append(rd.rx);
    resource["tx"].append(rd.tx);
  }
  json["name"] = device;
  json["data_writers"] = data_writers;
  json["data_readers"] = data_readers;
  json["resource"] = resource;
  ofstream file(path + "/" + device + ".json");
  file << json;
  file.close();
}

void Saver::append_pub(string partition, string dst_topic, long pub_id,
                       long dw_id, long pub_msg_count,
                       map<string, vector<double>> latency) {
  for (auto it : latency) {
    data_writer_data.push_back({dw_id, pub_id, partition, it.first, dst_topic,
                                pub_msg_count, it.second});
  }
}

void Saver::append_sub(string partition, string src_topic, long sub_id,
                       long dr_id, map<string, SubMsgData> data) {
  for (auto it : data) {
    data_reader_data.push_back(
        {dr_id, sub_id, partition, it.first, src_topic, it.second});
  }
}

void Saver::append_resource(vector<MonitorData> data) {
  // cpu: 1 - 0
  // ram: 1
  // rx: 1 - 0
  // tx: 1 - 0
  for (unsigned int i = 1; i < data.size(); ++i) {
    // cpu
    double cpu = compute_cpu_load(data[i].cpu, data[i - 1].cpu);
    if (cpu < 0) continue;
    double memory = data[i].ram;
    long long rx = data[i].rx - data[i - 1].rx;
    long long tx = data[i].tx - data[i - 1].tx;
    resource_data.push_back({cpu, memory, rx, tx});
  }
}

double Saver::compute_cpu_load(MonitorCpuData val, MonitorCpuData last_val) {
  double percent;
  unsigned long long total;
  if (val.user < last_val.user || val.user_low < last_val.user_low ||
      val.sys < last_val.sys || val.idle < last_val.idle) {
    // overflow detection. just skip this value.
    percent = -1.0;
  } else {
    total = (val.user - last_val.user) + (val.user_low - last_val.user_low) +
            (val.sys - last_val.sys);
    percent = total;
    total += (val.idle - last_val.idle);
    percent /= total;
    percent *= 100;
  }
  return percent;
}

long long Saver::compute_bandwidth(long long val, long long last_val) {
  return val - last_val;
}
