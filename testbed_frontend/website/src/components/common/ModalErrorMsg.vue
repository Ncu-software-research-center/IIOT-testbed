<template>
  <div class="modal fade" tabindex="-1" role="dialog" id="error-msg-modal" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <h5 class="text-danger">Error Message</h5>
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <span id="error-msg"></span>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" data-dismiss="modal">Ok</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["errorMsg"],
  watch: {
    errorMsg() {
      document.getElementById("error-msg").innerHTML = this.errorMsg;
    }
  }
};
</script>

<style lang="sass">
</style>
