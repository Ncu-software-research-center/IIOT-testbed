<template>
  <div class="row">
    <div class="col-lg-12">
      <div class="card mb-4 shadow">
        <div class="card-header py-3 d-flex align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold">Step 3: Set emulation time and start emulation</h6>
        </div>
        <div class="card-body">
          <div v-if="dsal">
            <p>Report Name (The default is the time of emulation execution.)</p>
            <div class="input-group pl-0 mb-4">
              <input
                type="text"
                class="form-control border-right-radius"
                placeholder="ex: report-1"
                v-model="reportName"
                :class="{'is-invalid': !isValidedReportName}"
              />
              <div class="invalid-feedback">Please enter a report name.</div>
            </div>
            <p>Emulation time (Please fill with emulation time in seconds.)</p>
            <div class="input-group pl-0">
              <input
                type="number"
                min="1"
                class="form-control"
                placeholder="ex: 10"
                v-model="emulationTime"
                :class="{'is-invalid': !isValidedEmulationTime}"
              />
              <div class="input-group-append">
                <button
                  class="btn btn-primary border-right-radius"
                  type="button"
                  @click="startEmulation()"
                >
                  <i class="fas fa-running"></i>
                </button>
              </div>
              <div class="invalid-feedback">The emulation time should be larger than 0.</div>
            </div>
          </div>
          <div v-else>
            <p>Please select a DSAL.</p>
          </div>
        </div>
      </div>
    </div>
    <modal msg="A new emulation task is generated." />
    <ModalErrorMsg :error-msg="errorMsg" />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config";
import modal from "@/components/common/ModalMsg";
import ModalErrorMsg from "@/components/common/ModalErrorMsg";

export default {
  props: ["dsal", "dataSetting", "availableDeviceNum"],
  components: {
    modal,
    ModalErrorMsg
  },
  data() {
    return {
      reportName: "",
      emulationTime: 10,
      isValidedReportName: true,
      isValidedEmulationTime: true,
      isValidedDeviceNum: true,
      errorMsg: ""
    };
  },
  methods: {
    validateReportName() {
      if (this.reportName.length === 0) {
        this.isValidedReportName = false;
      } else {
        this.isValidedReportName = true;
      }
    },
    validateEmulationTime() {
      if (this.emulationTime <= 0) {
        this.isValidedEmulationTime = false;
      } else {
        this.isValidedEmulationTime = true;
      }
    },
    validateDeviceNum() {
      if (this.availableDeviceNum < this.dataSetting.device.length) {
        this.isValidedDeviceNum = false;
      } else {
        this.isValidedDeviceNum = true;
      }
    },
    async startEmulation() {
      this.validateReportName();
      this.validateEmulationTime();
      this.validateDeviceNum();

      if (this.isValidedReportName && this.isValidedEmulationTime) {
        if (this.isValidedDeviceNum) {
          const task = {
            task: {
              dsalFilename: this.dsal.dsalFilename,
              dataSetting: this.dataSetting,
              reportName: this.reportName,
              emulationTime: this.emulationTime
            }
          };
          await axios.post(`${ApiHost}/emulations`, task);
          // eslint-disable-next-line
          $("#msg-modal").modal("show");
        } else {
          this.errorMsg = `The number of available devices should larger than ${this.dataSetting.device.length}.`;
          // eslint-disable-next-line
          $("#error-msg-modal").modal("show");
        }
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.border-right-radius
  border-top-right-radius: 0.3rem !important
  border-bottom-right-radius: 0.3rem !important
</style>
