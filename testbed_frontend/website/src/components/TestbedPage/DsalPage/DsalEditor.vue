<template>
  <div class="row">
    <div class="col-md-12 mb-4 transition-div">
      <div class="code-card card shadow">
        <div class="card-header py-2 d-flex align-items-center justify-content-between">
          <div class="d-flex flex-row align-items-center">{{ dsalFilename }}</div>
        </div>
        <div class="card-body p-0">
          <codemirror v-model="dsal.dsalContent" :options="cmOptions"></codemirror>
        </div>
      </div>
    </div>
    <div class="col-md-12 mb-4 transition-div">
      <div class="card shadow">
        <div class="card-body p-0">
          <div class="row justify-content-between p-4 mx-2">
            <section class="success-section row align-items-center" v-if="validDsal">
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
    <ModalErrorMsg :errorMsg="errorMsg" />
    <ModalSaveDasl :dsalFilename="dsal.dsalFilename" :save="save" />
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
import ModalSaveDasl from "./Modal/ModalSaveDasl";

export default {
  name: "Editor",
  components: {
    codemirror,
    ModalErrorMsg,
    ModalSaveDasl
  },
  data() {
    return {
      dsal: {},
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true
      },
      errorMsg: "",
      validDsal: true
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    dsalFilename() {
      return this.$route.params.filename;
    }
  },
  methods: {
    async init() {
      await this.loadDsal();
    },
    async loadDsal() {
      const res = await axios.get(`${ApiHost}/dsals/${this.dsalFilename}`);
      this.dsal = res.data;
    },
    async validateDsalContent() {
      const dsalContent = this.dsal.dsalContent;
      if (!dsalContent) {
        throw new Error("The dsal content may not be blank");
      } else {
        const params = { dsalContent };
        const res = await axios.post(`${ApiHost}/data-setting`, params);
        if (res.data.error) {
          this.validDsal = false;
          throw new Error(res.data.error);
        } else {
          this.validDsal = true;
        }
      }
    },
    async dsalHasNoChanged() {
      const res = await axios.get(`${ApiHost}/dsals/${this.dsal.dsalFilename}`);
      return this.dsal.dsalHash === res.data.dsalHash;
    },
    async save() {
      const dsalContent = this.dsal.dsalContent;
      const params = { dsalContent };
      // eslint-disable-next-line
      $("#confirm-save-dsal-modal").modal("hide");
      await axios.patch(`${ApiHost}/dsals/${this.dsal.dsalFilename}`, params);
      this.$router.push(`/dsal/files/${this.dsal.dsalFilename}`);
    },
    async saveDsal() {
      try {
        await this.validateDsalContent();
        const dsalHasNoChanged = await this.dsalHasNoChanged();
        if (dsalHasNoChanged) {
          this.save();
        } else {
          // eslint-disable-next-line
          $("#confirm-save-dsal-modal").modal("show");
        }
      } catch (err) {
        this.errorMsg = err;
        // eslint-disable-next-line
        $("#error-msg-modal").modal("show");
      }
    }
  },
  watch: {}
};
</script>

<style lang="sass">
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
