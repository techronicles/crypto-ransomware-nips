<template>
  <section>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-white">Security Alerts</h2>
      <p class="text-slate-400">
        Detected ransomware and suspicious network activities
      </p>
    </div>

    <div v-if="loading" class="text-slate-400">
      Loading alerts...
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
      <div class="flex items-center justify-between mb-5">
        <h3 class="text-lg font-semibold text-white">All Alerts</h3>

        <span
          class="px-4 py-2 rounded-xl text-sm bg-red-500/20 text-red-400"
        >
          {{ alerts.length }} alerts
        </span>
      </div>

      <div v-if="alerts.length === 0" class="text-slate-400">
        No alerts found.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-800 text-slate-300">
            <tr>
              <th class="text-left p-4">Time</th>
              <th class="text-left p-4">Source IP</th>
              <th class="text-left p-4">Destination IP</th>
              <th class="text-left p-4">Threat</th>
              <th class="text-left p-4">Severity</th>
              <th class="text-left p-4">Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="alert in alerts"
              :key="alert.id"
              class="border-t border-slate-800 hover:bg-slate-800/50 transition"
            >
              <td class="p-4">{{ alert.timestamp }}</td>
              <td class="p-4 font-medium text-slate-200">
                {{ alert.sourceIp }}
              </td>
              <td class="p-4">{{ alert.destinationIp }}</td>
              <td class="p-4">{{ alert.threatType }}</td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="severityClass(alert.severity)"
                >
                  {{ alert.severity }}
                </span>
              </td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="statusClass(alert.status)"
                >
                  {{ alert.status }}
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
const error = ref("");
const alerts = ref([]);

const severityClass = (severity) => {
  if (severity === "High") return "bg-red-500/20 text-red-400";
  if (severity === "Medium") return "bg-yellow-500/20 text-yellow-400";
  return "bg-green-500/20 text-green-400";
};

const statusClass = (status) => {
  if (status === "Blocked") return "bg-red-500/20 text-red-400";
  if (status === "Monitoring") return "bg-yellow-500/20 text-yellow-400";
  return "bg-blue-500/20 text-blue-400";
};

const loadAlerts = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await api.get("/api/alerts");
    alerts.value = response.data;
  } catch (err) {
    error.value = "Failed to fetch alerts. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadAlerts);
</script>