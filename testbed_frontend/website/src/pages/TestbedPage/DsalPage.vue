<template>
  <transition name="fade" mode="out-in">
    <router-view :key="$route.fullPath" />
  </transition>
</template>

<script>
export default {};
</script>

<style lang="sass">
.fade-enter-active, .fade-leave-active
  transition: opacity .3s

.fade-enter, .fade-leave-to
  opacity: 0

.vue-codemirror, .CodeMirror
  font-size: 14px
  border-radius: 0.3rem

.CodeMirror-gutters
  background: #fff

.CodeMirror-gutter
  padding-left: 14px
  background: #fff

.CodeMirror-linenumber
  padding-left: 24px

.CodeMirror-line
  padding-left: 20px !important
</style>
