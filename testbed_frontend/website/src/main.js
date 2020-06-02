// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import Cookies from "js-cookie";
import axios from "axios";
import { ApiHost } from "@/config";

Vue.config.productionTip = false;

async function getRefreshToken() {
  const refreshToken = { refresh: Cookies.get("refreshToken") };
  const res = await axios.post(`${ApiHost}/tokenrefresh`, refreshToken);
  return res.data["access"];
}

// http request intercpetor
axios.interceptors.request.use(
  config => {
    if (Cookies.get("accessToken")) {
      config.headers.Authorization = `Bearer ${Cookies.get("accessToken")}`;
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);

// http response interceptors
axios.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;
    if (error.message === "Network Error") {
      return Promise.reject(error.message);
    } else if (error.response.status === 401 && !originalRequest._retry) {
      if (Cookies.get("refreshToken")) {
        originalRequest._retry = true;
        const refreshToken = await getRefreshToken();

        // The access token will expire after 10 minutes.
        const accessTokenExpireTime = new Date(
          new Date().getTime() + 10 * 60 * 1000
        );
        Cookies.set("accessToken", refreshToken, {
          expires: accessTokenExpireTime
        });

        return axios(originalRequest);
      } else {
        router.push("/login");
      }
      return Promise.reject(error.response.data);
    } else {
      return Promise.reject(error.response.data);
    }
  }
);

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});
