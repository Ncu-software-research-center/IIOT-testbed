<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3 d-flex align-items-center justify-content-between">
      <h6 class="m-0 py-2 font-weight-bold text-primary">Report File</h6>
      <button
        class="d-none d-sm-inline-block btn btn-sm btn-danger shadow-sm border-0"
        @click="deleteReport()"
        v-if="selectedReport"
      >
        <i class="far fa-trash-alt"></i> Delete Report (csv)
      </button>
    </div>
    <div class="card-body">
      <!-- File Link -->
      <div class="d-flex flex-wrap mb-4">
        <div
          class="file-link shodow-sm"
          v-for="(reportName) in reportNames"
          :key="reportName"
          @click="selectedReport=reportName"
          :class="{'active': selectedReport==reportName}"
        >
          <div class="border file-link-content">
            <i class="fas fa-file-alt mr-3"></i>
            {{ reportName }}
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="row">
        <div class="col-sm-12 col-md-5">
          <div
            class="d-flex align-items-center mt-3"
          >Showing {{ showingStartNum }} to {{ showingEndNum }} of {{ totalNum }} entries</div>
        </div>
        <div class="col-sm-12 col-md-7 d-flex justify-content-end">
          <div class="paging_simple_numbers">
            <ul class="pagination">
              <li
                class="paginate_button page-item previous"
                :class="{disabled: pagination.currentPage==1}"
              >
                <button class="page-link" @click="pagination.currentPage-=1">Previous</button>
              </li>
              <li class="paginate_button page-item" v-for="i in totalPage" :key="i">
                <button class="page-link" @click="pagination.currentPage=i">{{ i }}</button>
              </li>
              <li
                class="paginate_button page-item next"
                :class="{disabled: pagination.currentPage==totalPage}"
              >
                <button class="page-link" @click="pagination.currentPage+=1">Next</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import * as testReport from './test_report.json'
import axios from "axios";
import { ApiHost } from "@/config.js";

export default {
  data() {
    return {
      selectedReport: "",
      pagination: {
        currentPage: 1
      },
      reports: []
    };
  },
  mounted() {
    this.loadReports();
  },
  methods: {
    async loadReports() {
      const res = await axios.get(`${ApiHost}/reports`);
      this.reports = res.data;
    },
    async deleteReport() {
      this.reports = this.reports.filter(
        r => r.reportName !== this.selectedReport
      );
      await axios.delete(`${ApiHost}/reports/${this.selectedReport}`);
      this.selectedReport = "";
    }
  },
  computed: {
    reportNames() {
      return this.reports
        .map(r => r.reportName)
        .slice(this.showingStartNum - 1, this.showingEndNum);
    },
    totalNum() {
      return this.reports.length;
    },
    showingStartNum() {
      return (this.pagination.currentPage - 1) * 12 + 1;
    },
    showingEndNum() {
      let endNum = (this.pagination.currentPage - 1) * 12 + 12;
      if (endNum > this.totalNum) {
        endNum = this.totalNum;
      }
      return endNum;
    },
    totalPage() {
      return Math.ceil(this.reports.length / 12);
    }
  },
  watch: {
    selectedReport(reportName) {
      const r = this.reports.find(r => r.reportName === reportName);
      this.$emit("set-report", r);
    }
  }
};
</script>

<style lang="sass">
.file-link
  cursor: pointer
  width: calc(100%/6)
  box-sizing: border-box
  .file-link-content
    border-radius: 5px
    padding: 12px
    margin: 8px

.file-link.active
  .file-link-content
    background-color: #e8f0fe
    color: #1967d2
</style>
