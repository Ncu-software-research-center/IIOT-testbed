<template>
  <div class="col-lg-12">
    <div class="card shadow mb-4">
      <div class="card-body row justify-content-around align-items-center">
        <div
          id="step1"
          class="d-flex align-items-center justify-content-center"
          v-on:click="$emit('switch-step', 'load-dsal')"
        >
          <div class="d-flex flex-row">
            <div
              class="progress-circle d-flex justify-content-center align-items-center bg-primary rounded-circle"
            >
              <span class="text-white">1</span>
            </div>
            <p class="d-flex align-items-center ml-2 mb-0">Load DSAL</p>
          </div>
        </div>
        <div class="progress-line mr-4 ml-4"></div>
        <div
          id="step2"
          class="d-flex align-items-center"
          v-on:click="$emit('switch-step', 'visualization')"
        >
          <div class="d-flex flex-row">
            <div
              class="progress-circle d-flex justify-content-center align-items-center bg-primary rounded-circle"
            >
              <span class="text-white">2</span>
            </div>
            <p class="d-flex align-items-center ml-2 mb-0">DSAL visualization</p>
          </div>
        </div>
        <div class="progress-line mr-4 ml-4"></div>
        <div id="step3" class="align-items-center" v-on:click="$emit('switch-step', 'start')">
          <div class="d-flex flex-row">
            <div
              class="progress-circle d-flex justify-content-center align-items-center bg-primary rounded-circle"
            >
              <span class="text-white">3</span>
            </div>
            <p class="d-flex align-items-center ml-2 mb-0">Set emulation time and start emulation</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="sass">
#step1, #step2, #step3
  cursor: pointer
  flex-grow: 1
  p
    word-break: normal
    word-wrap: break-word

.progress-circle
  height: 30px
  width: 30px

.progress-line
  flex-grow: 1
  border-bottom: 1px solid #cacaca
  width: 130px
</style>
