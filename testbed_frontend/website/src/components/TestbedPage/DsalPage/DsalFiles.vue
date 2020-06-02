<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3 d-flex align-items-center justify-content-between">
      <h6 class="d-flex flex-row align-items-center m-0 font-weight-bold text-primary">
        Files
        <Tooltip
          tooltip=" DSAL is a language used to define DDS QoS policies, define DDS entities, define DDS communication structures, and reuse defined DDS QoS policies, as well as DDS entities."
        />
      </h6>
      <div class="row">
        <router-link
          class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-2"
          to="new"
        >
          <span class="icon text-white-50">
            <i class="fas fa-plus"></i>
          </span>
          <span class="text">New...</span>
        </router-link>
      </div>
    </div>
    <div class="card-body">
      <table class="table table-hover table-borderless">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Filename</th>
            <th scope="col">Last update</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(dsal, i) in dsalList"
            :key="dsal.dsalFilename"
            @click="$router.push(dsal.fileLink)"
          >
            <td scope="row">{{ i+1 }}</td>
            <td>
              <router-link :to="dsal.fileLink">{{ dsal.dsalFilename }}</router-link>
            </td>
            <td>{{ dsal.dsalUpdated | date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

import { ApiHost } from "@/config";
import Tooltip from "../../common/Tooltip";

export default {
  components: {
    Tooltip
  },
  data() {
    return {
      dsals: [],
      selectedDsal: ""
    };
  },

  mounted() {
    this.init();
  },
  filters: {
    date(d) {
      return moment(d).format("YYYY-MM-DD hh:mm:ss");
    }
  },
  computed: {
    dsalFilenames() {
      return this.dsals.map(d => d.dsalFilename);
    },
    dsalList() {
      return this.dsals.map(d => {
        d["fileLink"] = this.$route.path + "/" + d.dsalFilename;
        return d;
      });
    }
  },
  methods: {
    async init() {
      console.log("init");
      await this.sleep(100);
      const dsals = await this.loadDsals();
      // this.dsals = Object.assign({}, this.dsals, dsals)
      this.dsals = dsals;
    },
    async loadDsals() {
      const res = await axios.get(`${ApiHost}/dsals`);
      return res.data;
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  }
};
</script>

<style lang="sass" scoped>
.table-hover tbody tr:hover
  background: #4e73df1a

th
  color:  #666

tr
  &:hover
    cursor: pointer
  th, td
    text-align: center
  a
    color: #858796
</style>
