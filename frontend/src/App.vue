<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 flex">
    <Sidebar />

    <main class="flex-1 p-6">
      <Navbar />
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from "./components/Sidebar.vue";
import Navbar from "./components/Navbar.vue";
</script>