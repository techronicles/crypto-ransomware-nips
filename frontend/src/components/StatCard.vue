<template>
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
    <p class="text-sm text-slate-400">{{ title }}</p>
    <h3 class="text-3xl font-bold text-white mt-2">{{ value }}</h3>
    <p class="text-xs mt-2" :class="statusClass">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  statusClass: {
    type: String,
    default: "text-slate-400",
  },
});
</script>