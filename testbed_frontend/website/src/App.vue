<template>
  <div id="app">
    <transition name="page" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style lang="sass">
#app
  font-family: 'Lato', Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale

.page-enter-active, .page-leave-active
  transition: .5s

.page-enter, .page-leave-to
  opacity: 0
</style>
