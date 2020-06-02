<template>
  <!-- Sidebar -->
  <ul class="navbar-nav sidebar accordion shadow" id="accordionSidebar">
    <!-- Sidebar - Brand -->
    <span class="sidebar-brand d-flex align-items-center justify-content-center">
      <img src="@/assets/img/logo.png" width="100%" />
    </span>

    <!-- Divider -->
    <hr class="sidebar-divider my-0" />

    <!-- Heading -->
    <div class="sidebar-heading mt-2">Pages</div>

    <!-- Nav Item - Emulation -->
    <li class="nav-item" :class="{active: page=='dsal files'}" @click="page='dsal files'">
      <router-link class="nav-link" to="/dsal/files">
        <span class="nav-icon">
          <i class="fas fa-file"></i>
        </span>
        <span>DSAL Files</span>
      </router-link>
    </li>
    <!-- Nav Item - Emulation -->
    <li class="nav-item" :class="{active: page=='emulation'}" @click="page='emulation'">
      <router-link class="nav-link" to="/emulation">
        <span class="nav-icon">
          <i class="fas fa-cloud"></i>
        </span>
        <span>Emulation</span>
      </router-link>
    </li>
    <!-- Nav Item - Emulation -->
    <li class="nav-item" :class="{active: page=='task board'}" @click="page='task board'">
      <router-link class="nav-link" to="/task-board">
        <span class="nav-icon">
          <i class="fas fa-tasks"></i>
        </span>
        <span>Taskboard</span>
      </router-link>
    </li>
    <!-- Nav Item - Tables -->
    <li class="nav-item" :class="{active: page=='report'}" @click="page='report'">
      <router-link class="nav-link" to="/report">
        <span class="nav-icon">
          <i class="fas fa-fw fa-table"></i>
        </span>
        <span>Performance Report</span>
      </router-link>
    </li>
    <!-- Nav Item - Tables -->
    <!-- <li
      class="nav-item"
      :class="{active: page=='qos optimization'}"
      @click="page='qos optimization'"
    >
      <router-link class="nav-link" to="/qos-optimization">
        <span class="nav-icon">
          <i class="fas fa-sliders-h"></i>
        </span>
        <span>QoS Optimization</span>
      </router-link>
    </li> -->

    <!-- Sidebar Toggler (Sidebar) -->
    <div class="sidebar-toggle text-center d-none d-md-inline mt-2">
      <button class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>
  </ul>
</template>

<script>
export default {
  data() {
    return {
      page: this.$route.name
    };
  },
  mounted() {},
  methods: {}
};
</script>

<style lang="sass" scoped>
.sidebar
  &shadow
    box-shadow: 1px 0px 20px rgba(0, 0, 0, 0.08) !important

.sidebar hr.sidebar-divider
  border: 2px solid #f8f9fc
  margin: 0 !important

.nav-icon
  text-align: center
  display: inline-block !important
  width: 30px

.nav-item
  &.active
    background-color:  #4e73df1a
    border-right: 4px solid var(--primary)

    a
      font-weight: 400 !important
    a, i
      color: var(--primary) !important
  a, i
    color: #858796 !important

.sidebar-toggle
  .rounded-circle
    background-color: #F5F7FB
</style>
