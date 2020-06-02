<template>
  <div class="bg-gradient-primary">
    <div class="login-container container">
      <!-- Outer Row -->
      <div class="d-flex justify-content-center">
        <div class="card o-hidden border-0 shadow-lg my-5 col-6">
          <div class="card-body p-0">
            <!-- Nested Row within Card Body -->
            <div class="p-5">
              <div class="text-center">
                <h1 class="h4 text-gray-900 mb-4">Welcome Back!</h1>
              </div>
              <form class="user" v-on:submit.prevent="login()">
                <div class="form-group">
                  <input
                    type="text"
                    class="form-control form-control-user"
                    placeholder="Enter Username..."
                    v-model="username"
                    required
                  />
                </div>
                <div class="form-group">
                  <input
                    type="password"
                    class="form-control form-control-user"
                    placeholder="Password"
                    v-model="password"
                    required
                  />
                </div>
                <p class="text-danger" v-if="invalid">{{ invalidMessage }}</p>
                <button class="btn btn-primary btn-user btn-block" type="submit">Login</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import Cookies from "js-cookie";
import { ApiHost } from "@/config.js";

export default {
  data() {
    return {
      username: "",
      password: "",
      invalid: false,
      invalidMessage: ""
    };
  },
  methods: {
    getToken() {
      let user = {
        username: this.username,
        password: this.password
      };
      console.log(`${ApiHost}/token`, user);
      return new Promise((resolve, reject) => {
        axios
          .post(`${ApiHost}/token`, user)
          .then(res => {
            resolve(res.data);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    errorHandle(err) {
      if (err === "Network error") {
        this.invalidMessage = "API failed to connect.";
      } else {
        this.invalidMessage = "Invalid Login or password.";
      }
    },
    async login() {
      try {
        const token = await this.getToken();
        this.saveTokenInCookie(token);
        this.$router.push("/dsal/files");
      } catch (err) {
        this.invalid = true;
        this.errorHandle(err);
      }
    },
    saveTokenInCookie(token) {
      // The access token will expire after 10 minutes.
      var accessTokenExpireTime = new Date(
        new Date().getTime() + 10 * 60 * 1000
      );
      Cookies.set("accessToken", token["access"], {
        expires: accessTokenExpireTime
      });
      // The refresh token will expire after 1 day.
      Cookies.set("refreshToken", token["refresh"], { expires: 1 });
    }
  }
};
</script>

<style lang="sass">
body, #app
  height: 100vh
  >div
    height: 100vh

.login-container
  height: calc(100vh - 200px)
</style>
