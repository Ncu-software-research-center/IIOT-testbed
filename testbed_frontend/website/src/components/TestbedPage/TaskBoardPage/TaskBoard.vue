<template>
  <div class="col-lg-12">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex justify-content-between align-items-center">
        <h6 class="m-0 font-weight-bold text-primary">Tasks</h6>
      </div>
      <div class="card-body">
        <table class="table table-borderless table-hover">
          <thead>
            <tr>
              <th scope="col">DSAL</th>
              <th scope="col">Progress</th>
              <th scope="col">Status</th>
              <th scope="col">Report Name</th>
              <th scope="col">Emulation Time</th>
              <th scope="col">Operation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in emulationTasks" :key="task.emulationTaskId">
              <td class="td-dsal-filename">{{ task.dsalFilename }}</td>
              <td class="td-progress-bar">
                <div class="progress">
                  <div
                    class="progress-bar progress-bar-striped progress-bar-animated"
                    role="progressbar"
                    style="width: 100%"
                    aria-valuenow="100"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    :class="task.progressBarColor"
                  ></div>
                </div>
              </td>
              <td class="td-status">{{ task.status }}</td>
              <td class="td-report-name">{{ task.reportName }}</td>
              <td class="td-emulation-time">&asymp; {{ task.emulationTime }}</td>
              <td class="td-delete-button">
                <button
                  class="btn btn-danger btn-icon-split btn-sm"
                  @click="deleteTask(task.emulationTaskId)"
                >
                  <span class="icon text-white-50">
                    <i class="fas fa-power-off"></i>
                  </span>
                  <span class="text">{{ task.deleteButton }}</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["tasks"],
  data() {
    return {
      emulationStatus: {
        INIT: "0",
        START: "1",
        END: "2",
        EXCEPTION: "3",
        ABORT: "4"
      }
    };
  },
  computed: {
    emulationTasks() {
      return this.tasks
        .filter(t => t.emulationTaskId !== "0")
        .map(t => {
          const taskObj = {
            ...t,
            emulationTime: this.formatEmultaionTime(t.emulationTime),
            progressBarColor: this.getProgressBarColor(t),
            status: this.getStatus(t),
            deleteButton: this.getDeleteButton(t)
          };
          return taskObj;
        });
    }
  },
  methods: {
    getProgressBarColor(task) {
      if (task.emulationStatus) {
        if (task.emulationStatus === this.emulationStatus.INIT) {
          return "bg-info";
        } else if (task.emulationStatus === this.emulationStatus.START) {
          return "";
        } else if (task.emulationStatus === this.emulationStatus.ABORT) {
          return "bg-danger";
        } else {
          return "bg-success";
        }
      } else {
        return "bg-warning";
      }
    },
    getStatus(task) {
      const status = task.emulationStatus;
      if (status === this.emulationStatus.INIT) {
        return "DDS Initialization";
      } else if (status === this.emulationStatus.START) {
        return "Emulation Executing";
      } else if (status === this.emulationStatus.END) {
        return "Processing Report";
      } else if (status === this.emulationStatus.ABORT) {
        return "Stoping Task";
      } else {
        return "Pending";
      }
    },
    getDeleteButton(task) {
      if (task.emulationStatus) {
        return "ABORT";
      } else {
        return "CANCEL";
      }
    },
    formatEmultaionTime(time) {
      const hours = Math.floor(time / 60 / 60);
      const minutes = Math.floor(time / 60);
      const seconds = time % 60;
      return `${this.paddingZero(hours)}:${this.paddingZero(
        minutes
      )}:${this.paddingZero(seconds)}`;
    },
    paddingZero(num) {
      return ("0" + num).slice(-2);
    },
    deleteTask(taskId) {
      this.$emit("delete-task", taskId);
    }
  }
};
</script>

<style lang="sass" scoped>
table
  table-layout: fixed

th
  color: #666

th, td
  v

th:not(:nth-child(2)), td:not(:nth-child(2))
  width: 200px
  max-width: 200px

.table-hover tbody tr:hover
  background: #4e73df1a

</style>
