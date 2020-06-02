<template>
  <div class="row">
    <TaskBoard :tasks="tasks" @delete-task="deleteTask($event)" />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config";
import TaskBoard from "@/components/TestbedPage/TaskBoardPage/TaskBoard.vue";

export default {
  components: {
    TaskBoard
  },
  data() {
    return {
      intervalController: null,
      tasks: []
    };
  },
  beforeDestroy() {
    clearInterval(this.intervalController);
  },
  mounted() {
    this.intervalController = setInterval(() => {
      this.getEmulationTasks();
    }, 1000);
  },
  methods: {
    async getEmulationTasks() {
      const res = await axios.get(`${ApiHost}/emulations`);
      this.tasks = res.data;
    },
    async deleteTask(taskId) {
      await axios.delete(`${ApiHost}/emulations/${taskId}`);
    }
  }
};
</script>

<style>
</style>
