<template>
  <modal id="msg-modal">
    <template v-slot:title>
      <h5 class="text-primary">Message</h5>
    </template>
    <template v-slot:body>{{ msg }}</template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" data-dismiss="modal">Ok</button>
    </template>
  </modal>
</template>

<script>
import modal from "@/components/common/modal";

export default {
  components: {
    modal
  },
  props: ["msg"]
};
</script>

<style lang="sass">
</style>
