<template>
  <div class="row">
    <div class="col-md-4 mb-4">
      <div class="card border-left-primary h-100 py-2 shadow">
        <div class="card-body">
          <div class="row no-gutters align-items-center">
            <div class="col mr-2">
              <div
                class="d-flex flex-row align-items-center text-xs font-weight-bold text-primary mb-1"
              >
                Available Device
                <Tooltip
                  tooltip="The number of your backend machine which is connecting to frontend."
                />
              </div>
              <div class="h5 mb-0 font-weight-bold text-gray-800">{{ availableDeviceNum }}</div>
            </div>
            <div class="col-auto">
              <i class="fas fa-desktop fa-2x text-gray-300"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4 mb-4">
      <div class="card border-left-info h-100 py-2 shadow">
        <div class="card-body">
          <div class="row no-gutters align-items-center">
            <div class="col mr-2">
              <div
                class="d-flex flex-row align-items-center text-xs font-weight-bold text-info mb-1"
              >
                Pending Tasks
                <Tooltip tooltip="The number of tasks which is pending to execute." />
              </div>
              <div class="row no-gutters align-items-center">
                <div class="col-auto">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">{{ taskNum }}</div>
                </div>
              </div>
            </div>
            <div class="col-auto">
              <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4 mb-4">
      <div class="card border-left-warning h-100 py-2 shadow">
        <div class="card-body">
          <div class="row no-gutters align-items-center">
            <div class="col mr-2">
              <div
                class="d-flex flex-row align-items-center text-xs font-weight-bold text-warning mb-1"
              >
                Tasks Remaining Time
                <Tooltip tooltip="The remaining time of emulation." />
              </div>
              <div class="row no-gutters align-items-center">
                <div class="col-auto">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">{{ taskRemainingTime }}</div>
                </div>
              </div>
            </div>
            <div class="col-auto">
              <i class="fas fa-clock fa-2x text-gray-300"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Tooltip from "../../common/Tooltip";

export default {
  components: { Tooltip },
  props: ["availableDevice", "tasks"],
  computed: {
    availableDeviceNum() {
      if (this.availableDevice.error) {
        return this.availableDevice.error;
      }

      if (this.availableDevice.availableDevice) {
        return this.availableDevice.availableDevice.length;
      }
      return 0;
    },
    taskNum() {
      if (this.tasks.error) {
        return this.tasks.error;
      }
      return this.tasks.filter(t => t.emulationTaskId !== "0").length;
    },
    taskRemainingTime() {
      if (this.tasks.error) {
        return this.tasks.error;
      }
      const remainingTime = this.tasks.reduce(
        (remaingTime, task) => remaingTime + task.emulationTime,
        0
      );
      const hours = Math.floor(remainingTime / 60 / 60);
      const minutes = Math.floor(remainingTime / 60);
      const seconds = remainingTime % 60;
      return `${this.paddingZero(hours)}:${this.paddingZero(
        minutes
      )}:${this.paddingZero(seconds)}`;
    }
  },
  methods: {
    paddingZero(num) {
      return ("0" + num).slice(-2);
    }
  }
};
</script>

<style>
</style>
