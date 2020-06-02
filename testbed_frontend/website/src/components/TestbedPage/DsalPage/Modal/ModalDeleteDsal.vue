<template>
  <modal id="delete-dsal-modal">
    <template v-slot:title>Delete DSAL</template>
    <template v-slot:body>
      <p class="mt-4">Do you really want to delete {{ dsalFilename }} ?</p>
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
      <button type="button" class="btn btn-danger" @click="deleteDsal()">Delete</button>
    </template>
  </modal>
</template>

<script>
import modal from "@/components/common/modal";

export default {
  props: ["dsalFilename"],
  components: {
    modal
  },
  methods: {
    async deleteDsal() {
      this.$emit("delete-dsal");
      this.closeModalAndReset();
    },
    closeModalAndReset() {
      // eslint-disable-next-line
      $("#delete-dsal-modal").modal("hide");
    }
  }
};
</script>

<style lang="sass" scoped>
</style>
