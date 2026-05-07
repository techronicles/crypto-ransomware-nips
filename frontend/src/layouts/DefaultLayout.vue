<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 flex">
    <Sidebar v-model:collapsed="sidebarCollapsed" />

    <div class="flex-1 flex flex-col min-w-0">
      <div class="p-6 flex flex-col flex-1">
        <Navbar @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
        <main class="flex-1 overflow-y-auto">
          <RouterView />
        </main>
        <footer class="mt-4">
          <p class="text-center text-sm text-slate-500">
            &copy; 2026 AI-NIPS. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import Navbar from '@/components/Navbar.vue';

const sidebarCollapsed = ref(false);
</script>