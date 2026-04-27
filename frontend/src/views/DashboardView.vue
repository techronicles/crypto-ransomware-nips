<template>
  <section>
    <div v-if="loading" class="text-slate-400">
      Loading dashboard data...
    </div>

    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5 mb-8">
        <StatCard
          title="Total Traffic"
          :value="summary.totalTraffic"
          subtitle="Packets analyzed"
        />

        <StatCard
          title="Suspicious Traffic"
          :value="summary.suspiciousTraffic"
          subtitle="Requires attention"
          statusClass="text-yellow-400"
        />

        <StatCard
          title="Blocked IPs"
          :value="summary.blockedIps"
          subtitle="Active blocks"
          statusClass="text-red-400"
        />

        <StatCard
          title="Model Accuracy"
          :value="summary.modelAccuracy + '%'"
          subtitle="Random Forest"
          statusClass="text-green-400"
        />
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 class="text-xl font-bold text-white mb-2">Recent Alerts</h3>
        <p class="text-slate-400 mb-5">Latest suspicious network activities</p>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-800 text-slate-300">
              <tr>
                <th class="text-left p-4">Time</th>
                <th class="text-left p-4">Source IP</th>
                <th class="text-left p-4">Threat</th>
                <th class="text-left p-4">Severity</th>
                <th class="text-left p-4">Status</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="alert in alerts"
                :key="alert.id"
                class="border-t border-slate-800"
              >
                <td class="p-4">{{ alert.timestamp }}</td>
                <td class="p-4">{{ alert.sourceIp }}</td>
                <td class="p-4">{{ alert.threatType }}</td>
                <td class="p-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs"
                    :class="severityClass(alert.severity)"
                  >
                    {{ alert.severity }}
                  </span>
                </td>
                <td class="p-4">{{ alert.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div
      v-if="error"
      class="mt-4 bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import StatCard from "../components/StatCard.vue";
import api from "../services/api";

const loading = ref(true);
const error = ref("");

const summary = ref({
  totalTraffic: 0,
  suspiciousTraffic: 0,
  blockedIps: 0,
  modelAccuracy: 0,
});

const alerts = ref([]);

const severityClass = (severity) => {
  if (severity === "High") return "bg-red-500/20 text-red-400";
  if (severity === "Medium") return "bg-yellow-500/20 text-yellow-400";
  return "bg-green-500/20 text-green-400";
};

const loadDashboard = async () => {
  try {
    loading.value = true;

    const [summaryResponse, alertsResponse] = await Promise.all([
      api.get("/api/dashboard/summary"),
      api.get("/api/alerts"),
    ]);

    summary.value = summaryResponse.data;
    alerts.value = alertsResponse.data;
  } catch (err) {
    error.value = "Failed to fetch dashboard data. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadDashboard);
</script>