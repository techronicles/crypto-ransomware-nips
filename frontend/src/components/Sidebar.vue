<template>
  <aside class="w-72 min-h-screen bg-slate-950 border-r border-slate-800 p-5">
    <div class="mb-10">
      <h1 class="text-2xl font-bold text-white">AI-NIPS</h1>
      <p class="text-sm text-slate-400">Crypto-Ransomware Defense</p>
    </div>

    <nav class="space-y-2">
      <RouterLink
        v-for="item in links"
        :key="item.path"
        :to="item.path"
        class="block px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-800 hover:text-white transition"
        active-class="bg-blue-600 text-white"
      >
        {{ item.name }}
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup>
const links = [
  { name: "Dashboard", path: "/" },
  { name: "Alerts", path: "/alerts" },
  { name: "Traffic Monitor", path: "/traffic" },
  { name: "Blocked IPs", path: "/blocked-ips" },
  { name: "Model Status", path: "/model-status" },
];
</script>