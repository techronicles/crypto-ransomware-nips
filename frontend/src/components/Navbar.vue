<template>
  <header class="mb-8 flex items-center justify-between rounded-3xl border border-white/10 bg-white/[0.03] px-6 py-5 backdrop-blur-xl">
    <div class="flex items-center gap-4">
      <!-- Hamburger toggle -->
      <button
        @click="$emit('toggle-sidebar')"
        class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04] text-slate-400 transition hover:bg-white/[0.08] hover:text-white"
        title="Toggle sidebar"
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>

      <div>
        <div class="flex items-center gap-3">
          <h2 class="text-2xl font-bold tracking-tight text-white">{{ pageTitle }}</h2>
          <span class="hidden md:inline-flex rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-medium text-sky-300">
            Security Console
          </span>
        </div>
        <p class="mt-2 text-sm text-slate-400">{{ pageDescription }}</p>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

defineEmits(['toggle-sidebar']);

const route = useRoute();

const pageMap = {
  '/dashboard':    { title: 'Security Dashboard',  description: 'Real-time crypto-ransomware detection and prevention' },
  '/alerts':       { title: 'Security Alerts',      description: 'Threat monitoring and incident response management' },
  '/traffic':      { title: 'Traffic Monitor',      description: 'Captured network traffic and AI predictions' },
  '/blocked_ips':  { title: 'Blocked IPs',          description: 'Automatically and manually blocked hosts' },
  '/model_status': { title: 'Model Status',         description: 'Machine learning engine and detection metrics' },
  '/simulator':    { title: 'Attack Simulator',     description: 'Generate and test simulated ransomware traffic' },
  '/register':     { title: 'Add New User',         description: 'Create a user account for AI-NIPS console access' },
};

const pageTitle    = computed(() => pageMap[route.path]?.title       || 'AI-NIPS');
const pageDescription = computed(() => pageMap[route.path]?.description || 'AI-driven network intrusion prevention system');
</script>