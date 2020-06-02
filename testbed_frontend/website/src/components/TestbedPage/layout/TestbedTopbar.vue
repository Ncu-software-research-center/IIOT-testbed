<template>
  <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top">
    <!-- Topbar Navbar -->
    <ul class="navbar-nav ml-auto mr-4">
      <!-- Nav Item - User Information -->
      <li class="nav-item no-arrow">
        <button type="button" class="btn btn-link" @click="logout()">Logout</button>
      </li>
    </ul>
  </nav>
</template>

<script>
import Cookies from "js-cookie";

export default {
  methods: {
    logout() {
      Cookies.remove("accessToken");
      Cookies.remove("refreshToken");
      this.$router.push("/login");
    }
  }
};
</script>

<style lang="sass" scoped>
</style>
