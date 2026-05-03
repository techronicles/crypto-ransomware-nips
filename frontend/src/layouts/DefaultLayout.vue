<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 flex">
    <Sidebar />
    <div class="flex-1 p-6 flex flex-col">
      <Navbar />
      <main class="flex-1 overflow-y-auto p-6">
          <RouterView />
        </main>
        <div class="footer">
            <p class="text-center text-sm text-slate-500 mt-4">
                &copy; 2026 AI-NIPS. All rights reserved.
            </p>
        </div>
    </div>
</div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue';
import Navbar from '@/components/Navbar.vue';
</script>