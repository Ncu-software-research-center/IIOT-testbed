<template>
  <div class="row">
    <div class="col-lg-12">
      <div class="card mb-4 shadow">
        <div class="card-header py-2 d-flex align-items-center justify-content-between">
          <div class="d-flex flex-row align-items-center">
            <h6 class="m-0 font-weight-bold">
              Step 2: DSAL visualization
              <span class="ml-2" v-if="dsalFilename">
                <i class="far fa-file"></i>
                {{ dsalFilename }}
              </span>
            </h6>
          </div>
          <div>
            <button
              class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"
              data-toggle="modal"
              data-target="#dsal-viewer"
              @click="showDsalViewer()"
              :disabled="!dsal"
            >
              <span class="icon text-white">
                <i class="fas fa-code"></i>
              </span>
              <span class="text">DSAL</span>
            </button>
          </div>
        </div>
        <div class="card-body">
          <div class="visualization" v-if="dsal">
            <visualization :data-setting="dataSetting" />
          </div>
          <div v-else>
            <p>Please select a DSAL.</p>
          </div>
        </div>
      </div>
    </div>
    <modal-dsal-viewer v-bind:dsal="dsal" />
  </div>
</template>

<script>
import ModalDsalViewer from "./Modal/ModalDsalViewer";
import Visualization from "@/components/visualization/Visualization";

export default {
  components: {
    ModalDsalViewer,
    Visualization
  },
  props: ["dsal", "dataSetting"],
  computed: {
    dsalFilename() {
      if (this.dsal) {
        return this.dsal.dsalFilename;
      }
    }
  },
  methods: {
    showDsalViewer() {
      setTimeout(() => {
        this.$children[0].$children[0].refresh();
      }, 200);
    }
  },
  watch: {
    dataSetting() {
      console.log(this.dataSetting);
    }
  }
};
</script>

<style lang="sass">
.visualization
  width: 100%
  height: 500px
  overflow: auto
</style>
