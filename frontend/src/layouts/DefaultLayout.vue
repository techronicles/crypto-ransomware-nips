<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <!-- Mobile overlay -->
    <div
      v-if="mobileSidebarOpen"
      @click="mobileSidebarOpen = false"
      class="fixed inset-0 z-40 bg-black/60 lg:hidden"
    ></div>

    <div class="flex min-h-screen">
      <!-- Desktop sidebar -->
      <div class="hidden lg:block">
        <Sidebar v-model:collapsed="sidebarCollapsed" />
      </div>

      <!-- Mobile sidebar drawer -->
      <div
        :class="[
          'fixed inset-y-0 left-0 z-50 transition-transform duration-300 lg:hidden',
          mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <Sidebar
          v-model:collapsed="mobileSidebarCollapsed"
          @click="mobileSidebarOpen = false"
        />
      </div>

      <!-- Main content -->
      <div class="flex min-w-0 flex-1 flex-col">
        <div class="flex flex-1 flex-col p-4 sm:p-5 lg:p-6">
          <Navbar @toggle-sidebar="handleSidebarToggle" />

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
  </div>
</template>

<script setup>
import { ref } from 'vue';

import Sidebar from '@/components/Sidebar.vue';
import Navbar from '@/components/Navbar.vue';

const sidebarCollapsed = ref(false);
const mobileSidebarOpen = ref(false);
const mobileSidebarCollapsed = ref(false);

const handleSidebarToggle = () => {
  if (window.innerWidth < 1024) {
    mobileSidebarOpen.value = !mobileSidebarOpen.value;
    mobileSidebarCollapsed.value = false;
    return;
  }

  sidebarCollapsed.value = !sidebarCollapsed.value;
};
</script>