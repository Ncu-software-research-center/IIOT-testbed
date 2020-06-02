<template>
  <div>
    <!-- Information -->
    <emulation-info :availableDevice="availableDevice" :tasks="tasks" />

    <!-- Emulation Step -->
    <!-- Step 1: Load DSAL -->
    <emulation-load-dsal v-on:set-dsal="setDsal($event)" />
    <!-- Step 2: DSAL visualization -->
    <emulation-dsal-visualization v-bind:dsal="dsal" v-bind:data-setting="dataSetting" />
    <!-- Step 3: Start Emulation -->
    <emulation-start
      v-bind:dsal="dsal"
      v-bind:data-setting="dataSetting"
      :available-device-num="availableDeviceNum"
    />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config";
import EmulationInfo from "@/components/TestbedPage/EmulationPage/EmulationInfo.vue";
import EmulationLoadDsal from "@/components/TestbedPage/EmulationPage/EmulationLoadDsal.vue";
import EmulationDsalVisualization from "@/components/TestbedPage/EmulationPage/EmulationDsalVisualization.vue";
import EmulationStart from "@/components/TestbedPage/EmulationPage/EmulationStart.vue";

export default {
  components: {
    EmulationInfo,
    EmulationDsalVisualization,
    EmulationLoadDsal,
    EmulationStart
  },
  data() {
    return {
      intervalController: null,
      dsal: null,
      dataSetting: "",
      availableDevice: [],
      tasks: []
    };
  },
  beforeDestroy() {
    clearInterval(this.intervalController);
  },
  mounted() {
    this.getInfo();
  },
  computed: {
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
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async getInfo() {
      try {
        Promise.all([this.getAvailableDevice(), this.getTasks()]).then(
          async () => {
            await this.sleep(2000);
            this.getInfo();
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    async getAvailableDevice() {
      let res = await axios.get(`${ApiHost}/available-device`);
      this.availableDevice = res.data;
    },
    async getTasks() {
      const res = await axios.get(`${ApiHost}/emulations`);
      this.tasks = res.data;
    },
    setDsal(dsal) {
      this.dsal = dsal;
      this.convertDsal();
    },
    /**
     * Convert the dsal to data setting
     */
    async convertDsal() {
      const res = await axios.get(
        `${ApiHost}/dsals/${this.dsal.dsalFilename}/data-setting`
      );
      this.dataSetting = res.data;
    }
  }
};
</script>

<style lang="sass">
</style>
