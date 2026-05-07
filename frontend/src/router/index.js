import { createRouter, createWebHistory } from 'vue-router';
import DefaultLayout from '@/layouts/DefaultLayout.vue';
import BlankLayout from '@/layouts/BlankLayout.vue';

const routes = [
  {
    path: '/login',
    component: BlankLayout,
    children: [
      {
        path: '',
        name: 'login',
        component: () => import('@/views/LoginView.vue'),
      },
    ],
  },
  {
    path: '/',
    component: DefaultLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'traffic',   name: 'traffic',   component: () => import('@/views/TrafficView.vue') },
      { path: 'alerts',    name: 'alerts',    component: () => import('@/views/AlertsView.vue') },
      { path: 'blocked_ips',  name: 'blocked_ips',  component: () => import('@/views/BlockedIPsView.vue') },
      { path: 'model_status', name: 'model_status', component: () => import('@/views/ModelStatusView.vue') },
      { path: 'simulator', name: 'simulator', component: () => import('@/views/SimulatorView.vue') },
      { path: 'register',  name: 'register',  component: () => import('@/views/RegisterView.vue') },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');

  if (to.path !== '/login' && !token) {
    sessionStorage.setItem('authWarning', 'Please login before accessing the dashboard.');
    next('/login');
    return;
  }

  if (to.path === '/login' && token) {
    next('/dashboard');
    return;
  }

  next();
});

export default router;