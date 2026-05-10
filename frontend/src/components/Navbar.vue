<template>
  <header
    class="mb-8 flex items-center justify-between rounded-3xl border border-white/10 bg-white/[0.03] px-6 py-5 backdrop-blur-xl"
  >
    <!-- LEFT -->
    <div class="flex items-center gap-4">
      <!-- Hamburger -->
      <button
        @click="$emit('toggle-sidebar')"
        class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04] text-slate-400 transition hover:bg-white/[0.08] hover:text-white"
        title="Toggle sidebar"
      >
        <svg
          class="h-5 w-5"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
          />
        </svg>
      </button>

      <div>
        <div class="flex items-center gap-3">
          <h2 class="text-2xl font-bold tracking-tight text-white">
            {{ pageTitle }}
          </h2>

          <span
            class="hidden md:inline-flex rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-medium text-sky-300"
          >
            Security Console
          </span>
        </div>

        <p class="mt-2 text-sm text-slate-400">
          {{ pageDescription }}
        </p>
      </div>
    </div>

    <!-- RIGHT -->
    <!-- RIGHT -->
<div class="flex items-center gap-4">
  <!-- Date / Time -->
  <div
    class="hidden sm:flex items-center gap-3 rounded-2xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-2"
  >

    <div>
    <div class="flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
      <span class="text-xs font-medium text-emerald-300">System Online</span>
    </div>
    <p class="mt-1 text-xs text-slate-400">Monitoring The Network</p>
  </div>
    <div class="text-right">
      <p class="text-xs font-semibold text-emerald-300">
        {{ currentDate }}
      </p>
      <p class="text-xs text-slate-400">
        {{ currentTime }}
      </p>
    </div>
  </div>

  
</div>
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';

defineEmits(['toggle-sidebar']);

const route = useRoute();

/* =========================
   LIVE DATE / TIME
========================= */
const now = ref(new Date());
let clockTimer = null;

const currentDate = computed(() => {
  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(now.value);
});

const currentTime = computed(() => {
  return new Intl.DateTimeFormat('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(now.value);
});

onMounted(() => {
  clockTimer = setInterval(() => {
    now.value = new Date();
  }, 1000);
});

onUnmounted(() => {
  if (clockTimer) {
    clearInterval(clockTimer);
  }
});

/* =========================
   PAGE TITLES
========================= */
const pageMap = {
  '/dashboard': {
    title: 'Security Dashboard',
    description: 'Real-time crypto-ransomware detection and prevention',
  },

  '/alerts': {
    title: 'Security Alerts',
    description: 'Threat monitoring and incident response management',
  },

  '/traffic': {
    title: 'Traffic Monitor',
    description: 'Captured network traffic and AI predictions',
  },

  '/blocked_ips': {
    title: 'Blocked IPs',
    description: 'Automatically and manually blocked hosts',
  },

  '/model_status': {
    title: 'Model Status',
    description: 'Machine learning engine and detection metrics',
  },

  '/simulator': {
    title: 'Attack Simulator',
    description: 'Generate and test simulated ransomware traffic',
  },

  '/register': {
    title: 'Manage Users',
    description: 'Create and manage AI-NIPS user accounts',
  },
};

const pageTitle = computed(() => {
  return pageMap[route.path]?.title || 'AI-NIPS';
});

const pageDescription = computed(() => {
  return (
    pageMap[route.path]?.description ||
    'AI-driven network intrusion prevention system'
  );
});

/* =========================
   USER INFO
========================= */
const userRole = computed(() => {
  return localStorage.getItem('user_role') || 'viewer';
});

const username = computed(() => {
  try {
    const token = localStorage.getItem('access_token');

    if (!token) return 'Administrator';

    const payload = JSON.parse(atob(token.split('.')[1]));

    return payload.sub || payload.username || 'Administrator';
  } catch {
    return 'Administrator';
  }
});

const initials = computed(() => {
  return username.value
    .split(' ')
    .map((word) => word[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
});

/* =========================
   ROLE COLORS
========================= */
const roleTextClass = computed(() => {
  if (userRole.value === 'admin') {
    return 'text-red-300';
  }

  if (userRole.value === 'analyst') {
    return 'text-sky-300';
  }

  return 'text-emerald-300';
});

const roleDotClass = computed(() => {
  if (userRole.value === 'admin') {
    return 'bg-red-400';
  }

  if (userRole.value === 'analyst') {
    return 'bg-sky-400';
  }

  return 'bg-emerald-400';
});
</script>