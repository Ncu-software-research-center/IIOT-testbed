<template>
  <div id="page-top">
    <!-- Page Wrapper -->
    <div id="wrapper">
      <!-- Testbed Sidebar component -->
      <testbed-sidebar />

      <!-- Content Wrapper -->
      <div id="content-wrapper" class="d-flex flex-column">
        <!-- Main Content -->
        <div id="content">
          <!-- Testbed Topbar component -->
          <testbed-topbar />

          <!-- Begin Page Content -->
          <div class="container-fluid">
            <!-- Page Heading -->
            <div class="d-sm-flex align-items-center justify-content-between mb-4">
              <h1 class="h3 mb-0 font-weight-bold text-primary">{{ $route.name | uppercase }}</h1>
            </div>

            <!-- Page Content -->
            <transition name="page" mode="out-in">
              <router-view />
            </transition>
          </div>
          <!-- /.container-fluid -->
        </div>
        <!-- End of Main Content -->

        <!-- Testbed footer component-->
        <testbed-footer />
      </div>
      <!-- End of Content Wrapper -->
    </div>
    <!-- End of Page Wrapper -->
  </div>
</template>

<script>
import TestbedTopbar from "@/components/TestbedPage/layout/TestbedTopbar.vue";
import TestbedSidebar from "@/components/TestbedPage/layout/TestbedSidebar.vue";
import TestbedFooter from "@/components/TestbedPage/layout/TestbedFooter.vue";

export default {
  components: {
    TestbedTopbar,
    TestbedSidebar,
    TestbedFooter
  },
  filters: {
    uppercase(v) {
      return v.toUpperCase();
    }
  }
};
</script>

<style lang="sass">
.page-enter-active, .page-leave-active
  transition: .5s

.page-enter, .page-leave-to
  opacity: 0

#wrapper #content-wrapper
  background-color: #F5F7FB

.card
  border: 0
  // border-color: #d7dfe3
  &.shadow
    box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05) !important

.card-header
  background-color: #fff !important
  border-bottom: 0
</style>
