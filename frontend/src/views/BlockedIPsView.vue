<template>
  <section>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-white">Blocked IPs</h2>
        <p class="text-slate-400">
          Malicious IP addresses blocked by the prevention module
        </p>
      </div>

      <button
        @click="showForm = !showForm"
        class="bg-blue-600 hover:bg-blue-700 transition px-5 py-3 rounded-xl font-medium"
      >
        Add Manual Block
      </button>
    </div>

    <div
      v-if="showForm"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-6"
    >
      <h3 class="text-lg font-bold text-white mb-4">Add Manual IP Block</h3>

      <form @submit.prevent="submitBlockIp" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="form.ipAddress"
          type="text"
          placeholder="IP Address e.g. 192.168.1.100"
          class="bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-blue-500"
          required
        />

        <input
          v-model="form.reason"
          type="text"
          placeholder="Reason for blocking"
          class="bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-blue-500"
          required
        />

        <button
          type="submit"
          :disabled="submitting"
          class="bg-red-600 hover:bg-red-700 disabled:opacity-50 transition px-5 py-3 rounded-xl font-medium"
        >
          {{ submitting ? "Blocking..." : "Block IP" }}
        </button>
      </form>
    </div>

    <div v-if="loading" class="text-slate-400">
      Loading blocked IPs...
    </div>

    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <div
      v-else
      class="bg-slate-900 border border-slate-800 rounded-2xl p-6"
    >
      <div class="mb-5">
        <span class="bg-red-500/20 text-red-400 px-4 py-2 rounded-xl text-sm">
          {{ blockedIps.length }} blocked IPs
        </span>
      </div>

      <div v-if="blockedIps.length === 0" class="text-slate-400">
        No blocked IPs found.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-800 text-slate-300">
            <tr>
              <th class="text-left p-4">IP Address</th>
              <th class="text-left p-4">Reason</th>
              <th class="text-left p-4">Blocked At</th>
              <th class="text-left p-4">Mode</th>
              <th class="text-left p-4">Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="ip in blockedIps"
              :key="ip.id"
              class="border-t border-slate-800 hover:bg-slate-800/50"
            >
              <td class="p-4 font-medium text-slate-200">
                {{ ip.ipAddress }}
              </td>
              <td class="p-4">{{ ip.reason }}</td>
              <td class="p-4">{{ ip.blockedAt }}</td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs"
                  :class="modeClass(ip.mode)"
                >
                  {{ ip.mode }}
                </span>
              </td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs"
                  :class="statusClass(ip.status)"
                >
                  {{ ip.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";

const loading = ref(true);
const submitting = ref(false);
const error = ref("");
const showForm = ref(false);

const blockedIps = ref([]);

const form = ref({
  ipAddress: "",
  reason: "",
});

const modeClass = (mode) => {
  if (mode === "Auto") return "bg-purple-500/20 text-purple-400";
  return "bg-blue-500/20 text-blue-400";
};

const statusClass = (status) => {
  if (status === "Active") return "bg-red-500/20 text-red-400";
  return "bg-slate-500/20 text-slate-400";
};

const loadBlockedIps = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await api.get("/api/blocked-ips");
    blockedIps.value = response.data;
  } catch (err) {
    error.value = "Failed to fetch blocked IPs. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const submitBlockIp = async () => {
  try {
    submitting.value = true;
    error.value = "";

    const response = await api.post("/api/blocked-ips", form.value);

    blockedIps.value.unshift(response.data);

    form.value = {
      ipAddress: "",
      reason: "",
    };

    showForm.value = false;
  } catch (err) {
    error.value = "Failed to block IP address.";
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

onMounted(loadBlockedIps);
</script>