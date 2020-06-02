<template>
  <modal id="confirm-save-dsal-modal">
    <template v-slot:title>Confirm to save DSAL</template>
    <template v-slot:body>
      <p
        class="mt-4"
      >Someone has changed the dsal {{ dsalFilename }}. Do you want to save {{ dsalFilename }} ?</p>
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button>
      <button type="button" class="btn btn-primary" @click="save()">Yes</button>
    </template>
  </modal>
</template>

<script>
import modal from "@/components/common/modal";

export default {
  props: ["save", "dsalFilename"],
  components: {
    modal
  },
  methods: {
    closeModalAndReset() {
      // eslint-disable-next-line
      $("#confirm-save-dsal-modal").modal("hide");
    }
  }
};
</script>

<style lang="sass" scoped>
</style>
