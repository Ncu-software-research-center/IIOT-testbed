<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3 d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center">
        <h6 class="m-0 py-2 mr-4 font-weight-bold text-primary">
          Performance Report
          <span class="ml-2" v-if="reportName">
            <i class="far fa-file"></i>
            {{ reportName }}
          </span>
        </h6>
        <div class="custom-control custom-checkbox small d-flex align-items-center">
          <input type="checkbox" class="custom-control-input" id="customCheck" v-model="showDetail" />
          <label class="custom-control-label" for="customCheck">Show Detail</label>
        </div>
      </div>

      <div class="d-flex align-items-center" v-if="$route.name == 'report'">
        <button
          class="d-none d-sm-inline-block btn btn-sm btn-danger shadow-sm mr-2"
          :disabled="!isOptimizable"
          @click="optimizeQoS()"
        >
          <i class="fas fa-sliders-h fa-sm text-white-50"></i> Optimization
        </button>
        <button
          class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"
          @click="downloadReport()"
          :disabled="!reportDownloadLink"
        >
          <i class="fas fa-download fa-sm text-white-50"></i> Download Report (csv)
        </button>
      </div>
    </div>
    <div class="card-body report-table mx-2 text-center" valign="top">
      <h5 v-if="!reportRawData">You didn't select a performance report.</h5>
      <table class="table" v-else>
        <thead>
          <tr>
            <th>Optimized selection</th>
            <th>Topic</th>
            <th>Partition</th>
            <th>Publisher</th>
            <th>Publisher CPU Usage</th>
            <th>Subscriber</th>
            <th>Publisher CPU Usage</th>
            <th>Loss rate</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rowData, i) in reportRawData" :key="i">
            <template v-if="'rowSpan' in rowData">
              <td :rowspan="rowData.rowSpan">
                <select v-model="optimizationTopics[rowData.topic]">
                  <option value="default">default</option>
                  <option value="reliability">reliability</option>
                  <option value="timeliness">timeliness</option>
                </select>
              </td>
              <td :rowspan="rowData['rowSpan']">{{ rowData.topic }}</td>
            </template>
            <td>{{ rowData.partition }}</td>
            <td>{{ rowData.publisher }}</td>
            <td>{{ rowData.pubCpuUsgae }}</td>
            <td>{{ rowData.subscriber }}</td>
            <td>{{ rowData.subCpuUsgae }}</td>
            <td>{{ rowData.lossRate | keepTwoNum }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <ModalMsg msg="download report file" />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config";
import ModalMsg from "@/components/common/ModalMsg";

export default {
  components: {
    ModalMsg
  },
  props: ["report"],
  filters: {
    keepTwoNum(value) {
      if (typeof value === "number") {
        return value.toFixed(4);
      }
      return value;
    }
  },
  data() {
    return {
      showDetail: false,
      reportProperties: [
        "partition",
        "topic",
        "publisher",
        "subscriber",
        "letency",
        "lossRate"
      ],
      optimizationTopics: {}
    };
  },
  computed: {
    reportName() {
      if (this.report) {
        return this.report.reportName;
      } else {
        return "";
      }
    },
    reportRawData() {
      if (this.report) {
        this.initOptimizationDict();

        const reportData = this.report.reportContent.report;
        for (let i = 0; i < reportData.length; i++) {
          let count = 1;
          const currentTopicName = reportData[i].topic;
          for (let j = i + 1; j < reportData.length; j++) {
            if (currentTopicName === reportData[j].topic) {
              count++;
            } else {
              break;
            }
          }

          reportData[i]["rowSpan"] = count;
          i += count - 1;
        }

        return reportData;
      } else {
        return "";
      }
    },
    reportDownloadLink() {
      if (this.report) {
        return `${ApiHost}/reports/file/${this.reportName}.csv`;
      } else {
        return "";
      }
    },
    isOptimizable() {
      let numOfOptimizedTopics = 0;
      Object.keys(this.optimizationTopics).forEach(key => {
        if (
          ["reliability", "timeliness"].indexOf(
            this.optimizationTopics[key]
          ) !== -1
        ) {
          numOfOptimizedTopics += 1;
        }
      });

      return numOfOptimizedTopics > 0;
    }
  },
  methods: {
    downloadReport() {
      axios({
        url: this.reportDownloadLink,
        method: "GET",
        responseType: "blob"
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "report.csv");
        document.body.appendChild(link);
        link.click();
      });
    },
    initOptimizationDict() {
      const reportData = this.report.reportContent.report;
      const dict = {};
      reportData.forEach(report => {
        if (report.topic in dict === false) {
          dict[report.topic] = "default";
        }
      });
      this.optimizationTopics = dict;
    },
    calculateNumOfDevices() {
      const reportData = this.report.reportContent.report;
      const deviceNames = new Set();
      reportData.forEach(report => {
        deviceNames.add(report.publisher);
        deviceNames.add(report.subscriber);
      });
      return deviceNames.size;
    },
    /**
     * reliability optimization
     */
    optimizeQoSByTopicNum(kind) {
      const numOfTopics = Object.keys(this.optimizationTopics).length;

      let numOfOptimizedTopics = 0;
      Object.keys(this.optimizationTopics).forEach(key => {
        if (this.optimizationTopics[key] === kind) {
          numOfOptimizedTopics += 1;
        }
      });

      if (numOfOptimizedTopics === 0) return;

      if (numOfOptimizedTopics < numOfTopics) {
        return {
          warning:
            "DDS won't guarantee that all selected links will give 0% loss rate. But all the selected links will get the loss rate reduced.",
          suggestion: [
            {
              entity: "Selected topics",
              qos: {
                qos: {
                  history: {
                    kind: "keep_all",
                    depth: 1
                  }
                }
              }
            }
          ]
        };
      } else {
        return {
          warning:
            "Sent Packets from data writers may reduced due to the QoS Recommendation",
          suggestion: [
            {
              entity: "Data writers",
              qos: {
                qos: {
                  history: {
                    kind: "keep_all",
                    depth: 1
                  },
                  resource_limits: {
                    max_samples: kind === "timeliness" ? 200 : 1,
                    max_instances: -1,
                    max_samples_per_instance: -1
                  },
                  reliability: {
                    kind: "reliable",
                    max_blocking_time: {
                      sec: 5,
                      nanosec: 0
                    }
                  }
                }
              }
            },
            {
              entity: "Data Readers",
              qos: {
                qos: {
                  history: {
                    kind: "keep_all",
                    depth: 1
                  },
                  resource_limits: {
                    max_samples: kind === "timeliness" ? 200 : 1,
                    max_instances: -1,
                    max_samples_per_instance: -1
                  }
                }
              }
            }
          ]
        };
      }
    },
    optimizeOneDeviceQoS(kind) {
      const cpuUsage = this.report.reportContent.report[0].pubCpuUsgae;

      let numOfOptimizedTopics = 0;
      Object.keys(this.optimizationTopics).forEach(key => {
        if (this.optimizationTopics[key] === kind) {
          numOfOptimizedTopics += 1;
        }
      });
      if (numOfOptimizedTopics === 0) return;

      if (cpuUsage < 80) {
        return {
          warning: "",
          suggestion: [
            {
              entity: "Selected topics",
              qos: {
                qos: {
                  history: {
                    kind: "keep_all",
                    depth: 1
                  }
                }
              }
            }
          ]
        };
      } else {
        return this.optimizeQoSByTopicNum(kind);
      }
    },
    optimizeMultiDeviceQoS(kind = "") {
      return this.optimizeQoSByTopicNum(kind);
    },
    getRaliabilityOptimization() {
      let optimization = null;
      const numOfDevices = this.calculateNumOfDevices();
      if (numOfDevices === 1) {
        optimization = this.optimizeOneDeviceQoS("reliability");
      } else {
        optimization = this.optimizeMultiDeviceQoS("reliability");
      }

      return optimization;
    },
    getTimelinessOptimization() {
      let optimization = null;

      const numOfDevices = this.calculateNumOfDevices();
      if (numOfDevices === 1) {
        optimization = this.optimizeOneDeviceQoS("timeliness");
      } else {
        optimization = this.optimizeMultiDeviceQoS("timeliness");
      }

      return optimization;
    },
    optimizeQoS() {
      let reliabilityOptimization = this.getRaliabilityOptimization();
      let timelinessOptimization = this.getTimelinessOptimization();

      const optimization = { reliabilityOptimization, timelinessOptimization };

      this.$emit("setOptimizationResult", {
        optimization,
        optimizationTopics: this.optimizationTopics
      });
    }
  },
  watch: {
    showDetail(val) {
      let defaultProperties = [
        "topic",
        "partition",
        "publisher",
        "subscriber",
        "letency",
        "lossRate"
      ];
      if (val) {
        defaultProperties = [
          "partition",
          "topic",
          "publisher",
          "pubCpuUsgae",
          "pubMemoryUsgae",
          "pubBandwidthReceive",
          "pubBandwidthTransmit",
          "letency",
          "lossRate",
          "subscriber",
          "subCpuUsgae",
          "subMemoryUsgae",
          "subBandwidthReceive",
          "subBandwidthTransmit"
        ];
      }

      this.reportProperties = defaultProperties;
    }
  }
};
</script>

<style lang="sass">
.report-table
  overflow: auto
  font-size: 14px

table
  border-collapse: collapse

tbody [rowspan],
tbody [rowspan] ~ th,
tbody [rowspan] ~ td,
  border-top: 1px solid #d8d8d8

th, td
  vertical-align: middle !important
  background: transparent

tbody tr:hover
  background: transparent
</style>
