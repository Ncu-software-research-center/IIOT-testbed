<template>
  <div class="row">
    <div class="col-md-12 mb-4 transition-div">
      <div class="card shadow">
        <div class="card-header py-2 d-flex align-items-center justify-content-between">
          <div class="d-flex flex-row align-items-center">{{ dsalFilename }}</div>
          <div class="row">
            <button
              class="d-none d-sm-inline-block btn btn-sm btn-light shadow-sm mr-2"
              @click="editDsal()"
            >
              <span class="icon text-white-90">
                <i class="far fa-edit"></i>
              </span>
              <span class="text">Edit</span>
            </button>
            <button
              class="d-none d-sm-inline-block btn btn-sm btn-danger shadow-sm mr-2"
              @click="displayConfirmModal()"
            >
              <span class="icon text-white-90">
                <i class="fas fa-trash-alt"></i>
              </span>
              <span class="text">Delete</span>
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <codemirror v-model="dsal.dsalContent" :options="cmOptions"></codemirror>
        </div>
      </div>
    </div>
    <ModalDeleteDsal :dsal-filename="dsal.dsalFilename" @delete-dsal="deleteDsal()" />
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
import ModalDeleteDsal from "./Modal/ModalDeleteDsal";

export default {
  components: {
    codemirror,
    ModalDeleteDsal
  },
  data() {
    return {
      dsal: {},
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true,
        readOnly: "nocursor"
      }
    };
  },
  mounted() {
    this.init();
    this.$forceUpdate();
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
    editDsal() {
      this.$router.push(`/dsal/edit/${this.dsalFilename}`);
    },
    displayConfirmModal() {
      // eslint-disable-next-line
      $("#delete-dsal-modal").modal("show");
    },
    deleteDsal() {
      axios.delete(`${ApiHost}/dsals/${this.dsalFilename}`);
      this.$router.push("/dsal/files");
    }
  }
};
</script>

<style lang="sass" scoped>
.code-card
  height: 100%

.card-body
  & /deep/ .vue-CodeMirror
    height: 100%
  & /deep/ .CodeMirror
    height: 100%

.success-tag
  width: 40px
  height: 40px
  display: flex
  justify-content: center
  align-items: center

.invalid-tag
  font-size: 36px
</style>
