<template>
  <div class="row">
    <div class="col-md-12 mb-4 transition-div">
      <div class="code-card card shadow">
        <div class="card-header py-2 d-flex align-items-center justify-content-between">
          <div class="d-flex flex-row align-items-center">
            <div class="input-group mr-2">
              <input
                type="text"
                class="form-control"
                placeholder="Dsal filename"
                v-model="newDsal.dsalFilename"
                :class="{'is-invalid': !newDsal.dsalFilenameIsValid}"
              />
            </div>
            <div class="dropdown">
              <button
                class="btn btn-light dropdown-toggle shadow-sm"
                type="button"
                data-toggle="dropdown"
              >Template</button>
              <div class="dropdown-menu">
                <button
                  class="dropdown-item"
                  v-for="t in templates"
                  :key="t.templateName"
                  @click="selectTemplate(t.templateContent)"
                >{{ t.templateName }}</button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <codemirror v-model.lazy="newDsal.dsalContent" :options="cmOptions" />
        </div>
      </div>
    </div>
    <div class="col-md-12 mb-4 transition-div">
      <div class="card shadow">
        <div class="card-body p-0">
          <div class="row justify-content-between p-4 mx-2">
            <section
              class="success-section row align-items-center"
              v-if="newDsal.dsalFilenameIsValid"
            >
              <div class="success-tag rounded-circle bg-success">
                <i class="fas fa-check text-white"></i>
              </div>
              <div class="ml-4">
                <h5 class="text-dark">Your dsal looks good!</h5>
                <p class="text-dark m-0">Save it, then you can use it to do emulation.</p>
              </div>
            </section>
            <section class="invalid-section row align-items-center" v-else>
              <div class="invalid-tag">
                <i class="fas fa-exclamation-triangle text-warning"></i>
              </div>
              <div class="ml-4">
                <h5 class="text-dark">Your dsal is invalid</h5>
                <p class="text-dark m-0">We’ve collect your error so you could fix them before save.</p>
              </div>
            </section>
            <div class="d-flex align-items-center">
              <button class="btn btn-success btn-icon-split" @click="saveDsal()">
                <span class="text">Save</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <ModalErrorMsg :errorMsg="newDsal.errorMsg" />
  </div>
</template>

<script>
// require component
import { codemirror } from "vue-codemirror";

// require styles
import "codemirror/lib/codemirror.css";

// language js
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/yaml/yaml.js";

import axios from "axios";
import { ApiHost } from "@/config.js";
import ModalErrorMsg from "@/components/common/ModalErrorMsg";

export default {
  name: "Editor",
  components: {
    codemirror,
    ModalErrorMsg
  },
  data() {
    return {
      dsals: [],
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true
      },
      newDsal: {
        dsalFilename: "",
        dsalContent: "",
        dsalFilenameIsValid: true,
        errorMsg: ""
      },
      templates: []
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    dsalFilenames() {
      return this.dsals.map(d => d.dsalFilename);
    }
  },
  methods: {
    async init() {
      await this.loadDsal();
      this.loadTemplates();
    },
    async loadDsal() {
      const res = await axios.get(`${ApiHost}/dsals`);
      this.dsals = res.data;
    },
    loadTemplates() {
      this.templates = [
        {
          templateName: "Template#1",
          templateContent:
            "# This is a sample configuration for DSAL.\n# Check our guides at ...\n# Only use spaces to indent your .yml configuration.\n# -----\ndsal:\n  version: 1.0.0\n  define_qos:\n    - name: qos1\n      qos:\n        reliability:\n          kind: best_effort\n          max_blocking_time:\n            sec: 10\n            nanosec: 100\n    - name: qos2\n      base: qos1\n      qos:\n        liveliness:\n          kind: automatic\n          lease_duration:\n            sec: 10\n            nanosec: 10\n  define_topic:\n    - name: topic1\n      qos: qos1\n    - name: topic2\n      qos: qos1\n  define_data_writer:\n    - name: dw_1\n      qos: qos1\n      dst_topic: topic1\n      msg_size: 12\n      msg_cycletime: 1\n    - name: dw_2\n      base: dw_1\n      qos: qos2\n      msg_size: 1\n    - name: dw_3\n      base: dw_2\n      msg_size: 11\n  define_data_reader:\n    - name: dr_1\n      qos: qos1\n      src_topic: topic1\n  profile_name: profile1\n  devices:\n    - name: device1\n      number: 80\n      domains:\n        - qos: qos1\n          partitions:\n            - name: part1\n              publishers:\n                - qos: qos1\n                  data_writers:\n                    - name: dw_1\n                    - name: dw_1\n                      qos: qos2\n                    - name: dw_1\n                      dst_topic: topic2\n                    - name: dw_1\n                      msg_size: 1024\n                      msg_cycletime: 1000\n              subscribers:\n                - qos: qos1\n                  data_readers:\n                    - name: dr_1"
        }
      ];
    },
    selectTemplate(sample) {
      this.newDsal.dsalContent = sample;
    },
    validateDsalFilename() {
      const newDsalFilename = this.newDsal.dsalFilename;
      if (!newDsalFilename) {
        this.newDsal.dsalFilenameIsValid = false;
        throw new Error("The dsal filename should not be empty.");
      } else if (this.dsalFilenames.includes(newDsalFilename)) {
        this.newDsal.dsalFilenameIsValid = false;
        throw new Error("The dsal filename already exist.");
      } else {
        this.newDsal.dsalFilenameIsValid = true;
      }
    },
    async validateDsalContent() {
      const newDsalContent = this.newDsal.dsalContent;
      if (!newDsalContent) {
        throw new Error("The dsal content may not be blank");
      } else {
        const params = {
          dsal_content: this.newDsal.dsalContent
        };
        const res = await axios.post(`${ApiHost}/data-setting`, params);
        if (res.data.error) {
          this.newDsal.dsalFilenameIsValid = false;
          throw new Error(res.data.error);
        } else {
          this.newDsal.dsalFilenameIsValid = true;
        }
      }
    },
    async saveDsal() {
      try {
        this.validateDsalFilename();
        await this.validateDsalContent();
        const data = {
          dsalFilename: this.newDsal.dsalFilename,
          dsalContent: this.newDsal.dsalContent
        };
        await axios.post(`${ApiHost}/dsals`, data);
        this.$router.push("/dsal/files");
      } catch (err) {
        this.newDsal.errorMsg = err;
        // eslint-disable-next-line
        $("#error-msg-modal").modal("show");
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.code-card
  height: 500px

.card-body
  & /deep/ .vue-CodeMirror
    height: 452px
  & /deep/ .CodeMirror
    height: 452px

.success-tag
  width: 40px
  height: 40px
  display: flex
  justify-content: center
  align-items: center

.invalid-tag
  font-size: 36px
</style>
