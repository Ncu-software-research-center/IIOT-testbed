<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3 d-flex align-items-center justify-content-between">
      <h6 class="m-0 py-2 font-weight-bold text-primary">
        Report Chart
        <span class="ml-2" v-if="reportName">
          <i class="far fa-file"></i>
          {{ reportName }}
        </span>
      </h6>
    </div>
    <div class="card-body">
      <h5 class="text-center" v-if="!report">You didn't select a performance report.</h5>
      <vue-chart :chart-labels="chartLabels" :chart-data="chartData" v-else />
    </div>
  </div>
</template>

<script>
import VueChart from "@/components/common/VueChart";

export default {
  components: {
    VueChart
  },
  props: ["report"],
  data() {
    return {
      chartLabels: [],
      chartData: []
    };
  },
  computed: {
    reportName() {
      if (this.report) {
        return this.report.reportName;
      } else {
        return "";
      }
    }
  },
  watch: {
    report(val) {
      if (val) {
        this.chartLabels = Array.from(
          { length: val.reportContent.report.length },
          (v, i) => 1 + i
        );
        this.chartData = [
          {
            label: "Loss rate",
            backgroundColor: "#f87979",
            data: val.reportContent.report.map(report => report.lossRate)
          }
        ];
      }
    }
  }
};
</script>

<style lang="sass" scoped>
canvas
  height: 400px !important
</style>
