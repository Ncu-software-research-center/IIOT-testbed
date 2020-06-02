<template>
  <div>
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex align-items-center justify-content-between">
        <h6 class="m-0 py-2 font-weight-bold text-primary">QoS Optimization</h6>
      </div>

      <div class="card-body mx-2" valign="top" v-if="optimization.reliabilityOptimization">
        <h5>Reliability QoS Suggestion:</h5>
        <div class="alert alert-danger" role="alert" v-if="raliabilityWarning">
          <b>
            Warning:
            DDS won't guarantee that all selected links will give 0% loss rate. But all the selected links will get the loss rate reduced.
          </b>
        </div>
        <div v-for="suggestion in reliabilitySuggestions" :key="suggestion.entity">
          <p>{{ suggestion.entity }}</p>
          <codemirror v-model="suggestion.qos" :options="cmOptions"></codemirror>
        </div>
      </div>

      <div class="card-body mx-2" valign="top" v-if="optimization.timelinessOptimization">
        <h5>Timeliness QoS Suggestion:</h5>
        <div class="alert alert-danger" role="alert" v-if="timelinessWarning">
          <b>
            Warning:
            DDS won't guarantee that all selected links will give 0% loss rate. But all the selected links will get the loss rate reduced.
          </b>
        </div>
        <div v-for="suggestion in timelinessSuggestions" :key="suggestion.entity">
          <p>{{ suggestion.entity }}</p>
          <codemirror v-model="suggestion.qos" :options="cmOptions"></codemirror>
        </div>
      </div>

      <!-- emulation block -->
      <div class="card-footer">
        <h5>You can re-run emulation based on QoS suggestion.</h5>
        <form v-on:submit.prevent="runEmulation">
          <p class="mt-4">Report Name (The default is the time of emulation execution.)</p>
          <div class="input-group pl-0 mb-4">
            <input
              type="text"
              class="form-control border-right-radius"
              placeholder="ex: report-1"
              v-model="reportName"
              :class="{'is-invalid': !isValidedReportName}"
              required
            />
            <div class="invalid-feedback">Please enter a report name.</div>
          </div>
          <p>Emulation time (Please fill with emulation time in seconds.)</p>
          <div class="input-group pl-0 mb-4">
            <input
              type="number"
              min="1"
              class="form-control"
              placeholder="ex: 10"
              v-model="emulationTime"
              :class="{'is-invalid': !isValidedEmulationTime}"
              required
            />
            <div class="invalid-feedback">The emulation time should be larger than 0.</div>
          </div>
          <button class="btn btn-primary mt-2" type="submit">run emulation</button>
        </form>
      </div>
    </div>
    <modal id="run-emulation-modal" msg="A new emulation task is generated." />
    <ModalErrorMsg :error-msg="errorMsg" />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config.js";
import YAML from "yaml";
import modal from "@/components/common/ModalMsg";
import ModalErrorMsg from "@/components/common/ModalErrorMsg";

// require component
import { codemirror } from "vue-codemirror";

// require styles
import "codemirror/lib/codemirror.css";

// language js
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/yaml/yaml.js";

export default {
  components: {
    codemirror,
    modal,
    ModalErrorMsg
  },
  props: ["optimization", "optimizationTopics", "report"],
  data() {
    return {
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true,
        readOnly: "nocursor"
      },
      reportName: "",
      emulationTime: 10,
      availableDevice: null,
      errorMsg: ""
    };
  },
  computed: {
    reliabilitySuggestions() {
      if (
        this.optimization &&
        this.optimization.reliabilityOptimization !== undefined
      ) {
        return this.optimization.reliabilityOptimization.suggestion.map(
          suggestion => ({
            ...suggestion,
            qos: YAML.stringify(suggestion.qos)
          })
        );
      }

      return [];
    },
    raliabilityWarning() {
      if (
        this.optimization &&
        this.optimization.reliabilityOptimization !== undefined
      ) {
        return this.optimization.reliabilityOptimization.warning;
      }
    },
    timelinessSuggestions() {
      if (this.optimization && this.optimization.timelinessOptimization) {
        return this.optimization.timelinessOptimization.suggestion.map(
          suggestion => ({
            ...suggestion,
            qos: YAML.stringify(suggestion.qos)
          })
        );
      }

      return [];
    },
    timelinessWarning() {
      if (this.optimization && this.optimization.timelinessOptimization) {
        return this.optimization.timelinessOptimization.warning;
      }
    },
    isValidedReportName() {
      return this.reportName.length !== 0;
    },
    isValidedEmulationTime() {
      return this.emulationTime > 0;
    },
    /**
     * Check if the alive device is anought to run emulation.
     */
    availableDeviceNum() {
      if (this.availableDevice.error) {
        return this.availableDevice.error;
      }

      if (this.availableDevice.availableDevice) {
        return this.availableDevice.availableDevice.length;
      }
      return 0;
    }
  },
  methods: {
    toCamel(s) {
      return s.replace(/([-_][a-z])/gi, $1 => {
        return $1
          .toUpperCase()
          .replace("-", "")
          .replace("_", "");
      });
    },
    async getAvailableDevice() {
      const res = await axios.get(`${ApiHost}/available-device`);
      this.availableDevice = res.data;
    },
    setReliabilityToDataSetting(dataSetting) {
      if (this.optimization.reliabilityOptimization === undefined) return;

      const reliabilitySuggestions = this.optimization.reliabilityOptimization
        .suggestion;
      const optimizationTopcis = Object.keys(
        this.optimizationTopics
      ).filter(t => ["reliability"].indexOf(this.optimizationTopics[t]));

      reliabilitySuggestions.forEach(({ entity, qos }) => {
        if (entity === "Selected topics") {
          dataSetting.topic
            .filter(topic => {
              return optimizationTopcis.indexOf(topic.name);
            })
            .forEach(topic => {
              Object.keys(qos.qos).forEach(qosKey => {
                topic.topicQos[qosKey] = qos.qos[qosKey];
              });
            });
        } else if (entity === "Data writers") {
          dataSetting.device.forEach(({ domain }) => {
            domain[0].partition.forEach(({ publisher }) => {
              if (!Array.isArray(publisher)) return;

              publisher.forEach(({ dataWriter }) => {
                dataWriter
                  .filter(({ dstTopic }) =>
                    optimizationTopcis.indexOf(dstTopic)
                  )
                  .forEach(dw => {
                    Object.keys(qos.qos).forEach(qosKey => {
                      dw.dwQos[this.toCamel(qosKey)] = qos.qos[qosKey];
                    });
                  });
              });
            });
          });
        } else if (entity === "Data Readers") {
          dataSetting.device.forEach(({ domain }) => {
            domain[0].partition.forEach(({ subscriber }) => {
              if (!Array.isArray(subscriber)) return;

              subscriber.forEach(({ dataReader }) => {
                dataReader
                  .filter(({ srcTopic }) =>
                    optimizationTopcis.indexOf(srcTopic)
                  )
                  .forEach(dr => {
                    Object.keys(qos.qos).forEach(qosKey => {
                      dr.drQos[this.toCamel(qosKey)] = qos.qos[qosKey];
                    });
                  });
              });
            });
          });
        }
      });
    },
    setTimelinessToDataSetting(dataSetting) {
      if (this.optimization.timelinessOptimization === undefined) return;

      const timelinessSuggestions = this.optimization.timelinessOptimization
        .suggestion;
      const optimizationTopcis = Object.keys(
        this.optimizationTopics
      ).filter(t => ["timeliness"].indexOf(this.optimizationTopics[t]));

      timelinessSuggestions.forEach(({ entity, qos }) => {
        if (entity === "Selected topics") {
          dataSetting.topic
            .filter(topic => {
              return optimizationTopcis.indexOf(topic.name);
            })
            .forEach(topic => {
              Object.keys(qos.qos).forEach(qosKey => {
                topic.topicQos[qosKey] = qos.qos[qosKey];
              });
            });
        } else if (entity === "Data writers") {
          dataSetting.device.forEach(({ domain }) => {
            domain[0].partition.forEach(({ publisher }) => {
              if (!Array.isArray(publisher)) return;

              publisher.forEach(({ dataWriter }) => {
                dataWriter
                  .filter(({ dstTopic }) =>
                    optimizationTopcis.indexOf(dstTopic)
                  )
                  .forEach(dw => {
                    Object.keys(qos.qos).forEach(qosKey => {
                      dw.dwQos[this.toCamel(qosKey)] = qos.qos[qosKey];
                    });
                  });
              });
            });
          });
        } else if (entity === "Data Readers") {
          dataSetting.device.forEach(({ domain }) => {
            domain[0].partition.forEach(({ subscriber }) => {
              if (!Array.isArray(subscriber)) return;

              subscriber.forEach(({ dataReader }) => {
                dataReader
                  .filter(({ srcTopic }) =>
                    optimizationTopcis.indexOf(srcTopic)
                  )
                  .forEach(dr => {
                    Object.keys(qos.qos).forEach(qosKey => {
                      dr.drQos[this.toCamel(qosKey)] = qos.qos[qosKey];
                    });
                  });
              });
            });
          });
        }
      });
    },
    async runEmulation() {
      const daslFilename = this.report.dsal;
      const res = await axios.get(
        `${ApiHost}/dsals/${daslFilename}/data-setting`
      );
      const dataSetting = res.data;

      await this.getAvailableDevice();
      if (this.availableDeviceNum < dataSetting.device.length) {
        this.errorMsg = `The number of available devices should larger than ${dataSetting.device.length}.`;
        // eslint-disable-next-line
        $("#error-msg-modal").modal("show");
        return;
      }

      this.setReliabilityToDataSetting(dataSetting);
      this.setTimelinessToDataSetting(dataSetting);
      console.log(dataSetting);
      const task = {
        task: {
          dsalFilename: daslFilename,
          dataSetting: dataSetting,
          reportName: this.reportName,
          emulationTime: this.emulationTime
        }
      };
      await axios.post(`${ApiHost}/emulations`, task);
      // eslint-disable-next-line
      $("#run-emulation-modal").modal("show");
    }
  },
  watch: {
    optimization(val) {
      console.log(val);
    }
  }
};
</script>

<style lang="sass">
.vue-codemirror
  border: 1px solid #d6d6d6

.vue-codemirror, .CodeMirror
  font-size: 14px
  border-radius: 0.3rem

.CodeMirror-gutters
  background: #fff !important

.CodeMirror-gutter
  padding-left: 14px
  background: #fff

.CodeMirror-linenumber
  padding-left: 24px

.CodeMirror-line
  padding-left: 20px !important

.code-card
  height: 100%

.card-body
  & /deep/ .vue-CodeMirror
    height: 100%
  & /deep/ .CodeMirror
    height: 100%
</style>
