import Vue from "vue";
import Router from "vue-router";
import UserLoginPage from "@/pages/UserLoginPage";
import TestbedPage from "@/pages/TestbedPage/index";
import DsalPage from "@/pages/TestbedPage/DsalPage";
import DsalFiles from "@/components/TestbedPage/DsalPage/DsalFiles";
import DsalViewer from "@/components/TestbedPage/DsalPage/DsalViewer";
import DsalNewFile from "@/components/TestbedPage/DsalPage/DsalNewFile";
import DsalEditor from "@/components/TestbedPage/DsalPage/DsalEditor";
import EmulationPage from "@/pages/TestbedPage/EmulationPage";
import ReportPage from "@/pages/TestbedPage/ReportPage";
import TaskBoardPage from "@/pages/TestbedPage/TaskBoardPage";
import QosOptimizationPage from "@/pages/TestbedPage/QosOptimizationPage";
import Cookies from "js-cookie";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/login",
      name: "login",
      component: UserLoginPage
    },
    {
      path: "/",
      name: "TestbedPage",
      component: TestbedPage,
      children: [
        {
          path: "dsal",
          component: DsalPage,
          children: [
            {
              path: "files",
              name: "dsal files",
              component: DsalFiles
            },
            {
              path: "new",
              name: "New File",
              component: DsalNewFile
            },
            {
              path: "files/:filename",
              name: "DSAL Viwer",
              component: DsalViewer
            },
            {
              path: "edit/:filename",
              name: "Edit File",
              component: DsalEditor
            }
          ]
        },
        {
          path: "emulation",
          name: "emulation",
          component: EmulationPage
        },
        {
          path: "report",
          name: "report",
          component: ReportPage
        },
        {
          path: "task-board",
          name: "task board",
          component: TaskBoardPage
        },
        {
          path: "qos-Optimization",
          name: "qos Optimization",
          component: QosOptimizationPage
        }
      ]
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (Cookies.get("accessToken")) {
    if (to.path === "/login") {
      next(from.path);
    } else {
      next();
    }
  } else {
    if (to.path === "/login") {
      next();
    } else {
      next("/login");
    }
  }
});

export default router;
