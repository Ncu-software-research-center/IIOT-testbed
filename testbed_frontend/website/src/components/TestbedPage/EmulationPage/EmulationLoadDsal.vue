<template>
  <div class="row">
    <div class="col-lg-12">
      <div class="card mb-4 shadow">
        <div class="card-header py-3 d-flex align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold">Step 1: Load DSAL</h6>
        </div>
        <div class="card-body">
          <div class="input-group">
            <div class="dropdown">
              <div
                class="dropdown-button col-12 border rounded p-2 d-flex justify-content-between align-items-center"
                data-toggle="dropdown"
                v-bind:class="{'is-invalid': inValid}"
              >
                {{ dropdownMsg }}
                <i class="fa fa-chevron-down"></i>
              </div>
              <div class="col-12 dropdown-menu p-2">
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text">
                      <i class="fas fa-search"></i>
                    </span>
                  </div>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="DSAL keyword"
                    v-model="dsalFilterKeyword"
                  />
                </div>
                <div class="dropdown-item-group">
                  <button
                    class="dropdown-item py-2"
                    v-for="filename in dsalFilenames"
                    v-bind:key="filename"
                    @click="selectedDsal=filename"
                  >{{ filename }}</button>
                </div>
              </div>
            </div>
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" @click="loadDsal()">Load</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <ModalErrorMsg :errorMsg="errorMsg" />
  </div>
</template>

<script>
import axios from "axios";
import { ApiHost } from "@/config";
import ModalErrorMsg from "@/components/common/ModalErrorMsg";

export default {
  components: {
    ModalErrorMsg
  },
  data() {
    return {
      dsals: [],
      dsalFilterKeyword: "",
      selectedDsal: "",
      inValid: false,
      errorMsg: ""
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    dropdownMsg() {
      if (this.selectedDsal) {
        return this.selectedDsal;
      } else {
        return "Please select a DSAL";
      }
    },
    dsalFilenames() {
      return this.dsals
        .map(d => d.dsalFilename)
        .filter(filename => filename.indexOf(this.dsalFilterKeyword) !== -1);
    },
    isSeletedFile() {
      return this.selectedDsal.length > 0;
    }
  },
  methods: {
    async init() {
      const dsals = await this.loadDsals();
      this.dsals = dsals;
    },
    async loadDsals() {
      const res = await axios.get(`${ApiHost}/dsals`);
      return res.data;
    },
    validateSelectedDsal() {
      if (!this.isSeletedFile) {
        this.inValid = true;
        throw new Error("Please select a dsal.");
      } else {
        this.inValid = false;
      }
    },
    loadDsal() {
      try {
        this.validateSelectedDsal();
        const dsal = this.dsals.find(d => d.dsalFilename === this.selectedDsal);
        this.$emit("set-dsal", dsal);
      } catch (err) {
        this.errorMsg = err;
        // eslint-disable-next-line
        $("#error-msg-modal").modal("show");
      }
    },
    processResponseData(res) {
      this.$emit("visualize-dsal", res.data);
      this.closeModalAndReset();
    },
    closeModalAndReset() {
      this.inValid = false;
      // eslint-disable-next-line
      $("#upload-dsal-modal").modal("hide");
    }
  }
};
</script>

<style lang="sass" scoped>
.dropdown
  flex-grow: 1
  width: 1%

.dropdown-button
  cursor: pointer
  border-top-right-radius: 0 !important
  border-bottom-right-radius: 0 !important

.dropdown-item-group
  max-height: 400px
  overflow: auto

.dropdown-item
  &:hover
    background-color: #4e73df1a

.is-invalid
  border-color: #dc3545 !important
</style>
