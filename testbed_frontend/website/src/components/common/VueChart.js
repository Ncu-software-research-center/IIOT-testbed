import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  props: {
    chartLabels: Array,
    chartData: Array
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  mounted() {
    this.renderVueChart();
  },
  methods: {
    renderVueChart() {
      this.renderChart(
        {
          labels: this.chartLabels,
          datasets: this.chartData
        },
        { responsive: true, maintainAspectRatio: false }
      );
    }
  },
  watch: {
    chartData() {
      this.$data._chart.destroy();
      this.renderVueChart();
    },
    deep: true
  }
};
