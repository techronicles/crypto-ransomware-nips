import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import AlertsView from "../views/AlertsView.vue";
import TrafficView from "../views/TrafficView.vue";
import BlockedIPsView from "../views/BlockedIPsView.vue";
import ModelStatusView from "../views/ModelStatusView.vue";

const routes = [
  { path: "/", name: "dashboard", component: DashboardView },
  { path: "/alerts", name: "alerts", component: AlertsView },
  { path: "/traffic", name: "traffic", component: TrafficView },
  { path: "/blocked-ips", name: "blocked-ips", component: BlockedIPsView },
  { path: "/model-status", name: "model-status", component: ModelStatusView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;