<template>
  <aside class="w-72 min-h-screen bg-slate-950 border-r border-slate-800 p-5 flex flex-col">
    <div class="mb-10">
      <h1 class="text-2xl font-bold text-white">AI-NIPS</h1>
      <p class="text-sm text-slate-400">Crypto-Ransomware Defense</p>
    </div>

    <nav class="space-y-2 flex-1">
      <RouterLink
        v-for="item in links"
        :key="item.path"
        :to="item.path"
        :class="[
          'block px-4 py-3 rounded-xl transition',
          isActive(item.path)
            ? 'bg-blue-600 text-white'
            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
        ]"
      >
        {{ item.name }}
      </RouterLink>
      <!-- Logout button at the bottom -->
      <button
        @click="handleLogout"
        class="w-full px-4 py-3 rounded-xl text-red-400 hover:bg-red-600 hover:text-white transition self-start text-left">Logout
      </button>
    </nav>

  </aside>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const router = useRouter();

const links = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Alerts", path: "/alerts" },
  { name: "Traffic Monitor", path: "/traffic" },
  { name: "Blocked IPs", path: "/blocked_ips" },
  { name: "Model Status", path: "/model_status" },
  { name: "Attack Simulator", path: "/simulator" },
];

const handleLogout = () => {
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
  sessionStorage.setItem('authWarning', 'You have been logged out.');
  router.push('/login');
};

const isActive = (path) => {
  return route.path === path;
};
</script>