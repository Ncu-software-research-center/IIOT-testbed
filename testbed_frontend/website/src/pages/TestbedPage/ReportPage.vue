<template>
  <div>
    <!-- Report File -->
    <ReportFile v-on:set-report="report=$event" />

    <!-- Report Chart-->
    <ReportChart :report="report" />

    <!-- Report detail-->
    <ReportDetail :report="report" @setOptimizationResult="setOptimizationResult" />

    <ReportOptimization
      :report="report"
      :optimization="optimization"
      :optimizationTopics="optimizationTopics"
      v-if="optimization"
    />
  </div>
</template>

<script>
import ReportFile from "@/components/TestbedPage/ReportPage/ReportFile";
import ReportChart from "@/components/TestbedPage/ReportPage/ReportChart";
import ReportDetail from "@/components/TestbedPage/ReportPage/ReportDetail";
import ReportOptimization from "@/components/TestbedPage/ReportPage/ReportOptimization";

export default {
  components: {
    ReportFile,
    ReportChart,
    ReportDetail,
    ReportOptimization
  },
  data() {
    return {
      report: null,
      optimization: null,
      optimizationTopics: null
    };
  },
  methods: {
    setOptimizationResult(result) {
      this.optimization = result.optimization;
      this.optimizationTopics = result.optimizationTopics;
    }
  },
  watch: {
    report(val, oldVal) {
      if (val !== oldVal) {
        this.optimization = null;
        this.optimizationTopics = null;
      }
    }
  }
};
</script>

<style lang="sass">
</style>
