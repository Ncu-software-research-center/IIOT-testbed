<template>
  <div class="col-md-12 mb-4 transition-div">
    <div class="card shadow">
      <div class="card-header py-2 d-flex align-items-center justify-content-between">
        <div class="d-flex flex-row align-items-center">
          <h6 class="m-0 font-weight-bold text-primary">Dsal Visualization</h6>
        </div>
        <button
          class="d-none d-sm-inline-block btn btn-sm btn-light shadow-sm"
          @click="$emit('edit-dsal')"
        >
          <span class="icon text-gray-600">
            <i class="fas fa-code"></i>
          </span>
          <span class="text">Editor</span>
        </button>
      </div>
      <div class="card-body">
        <img src="https://i.imgur.com/bg3nA6H.jpg" alt="demo" />
        {{ dsal }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["dsal"]
};
</script>

<style>
</style>
