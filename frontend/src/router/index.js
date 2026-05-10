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
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { roles: ['admin', 'analyst', 'viewer'] },
      },

      {
        path: 'traffic',
        name: 'traffic',
        component: () => import('@/views/TrafficView.vue'),
        meta: { roles: ['admin', 'analyst', 'viewer'] },
      },

      {
        path: 'alerts',
        name: 'alerts',
        component: () => import('@/views/AlertsView.vue'),
        meta: { roles: ['admin', 'analyst'] },
      },

      {
        path: 'blocked_ips',
        name: 'blocked_ips',
        component: () => import('@/views/BlockedIPsView.vue'),
        meta: { roles: ['admin', 'analyst'] },
      },

      {
        path: 'model_status',
        name: 'model_status',
        component: () => import('@/views/ModelStatusView.vue'),
        meta: { roles: ['admin', 'analyst', 'viewer'] },
      },

      {
        path: 'simulator',
        name: 'simulator',
        component: () => import('@/views/SimulatorView.vue'),
        meta: { roles: ['admin', 'analyst'] },
      },

      {
        path: 'register',
        name: 'register',
        component: () => import('@/views/RegisterView.vue'),
        meta: { roles: ['admin'] },
      },
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
  const role = localStorage.getItem('user_role') || 'viewer';

  // not logged in
  if (to.path !== '/login' && !token) {
    sessionStorage.setItem(
      'authWarning',
      'Please login before accessing the dashboard.'
    );

    next('/login');
    return;
  }

  // already logged in
  if (to.path === '/login' && token) {
    next('/dashboard');
    return;
  }

  // role protection
  const allowedRoles = to.meta?.roles;

  if (allowedRoles && !allowedRoles.includes(role)) {
    sessionStorage.setItem(
      'authWarning',
      'Access denied. You do not have permission to access that page.'
    );

    next('/dashboard');
    return;
  }

  next();
});

export default router;