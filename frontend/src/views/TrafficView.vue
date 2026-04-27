<template>
  <section>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-white">Traffic Monitor</h2>
      <p class="text-slate-400">Captured network traffic and ML predictions</p>
    </div>

    <div v-if="loading" class="text-slate-400">
      Loading traffic records...
    </div>

    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">TCP Traffic</p>
          <h3 class="text-3xl font-bold mt-2">{{ tcpCount }}</h3>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">UDP Traffic</p>
          <h3 class="text-3xl font-bold mt-2">{{ udpCount }}</h3>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Malicious Predictions</p>
          <h3 class="text-3xl font-bold mt-2 text-red-400">
            {{ maliciousCount }}
          </h3>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-800 text-slate-300">
              <tr>
                <th class="text-left p-4">Time</th>
                <th class="text-left p-4">Source IP</th>
                <th class="text-left p-4">Destination IP</th>
                <th class="text-left p-4">Protocol</th>
                <th class="text-left p-4">Packet Size</th>
                <th class="text-left p-4">Prediction</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="traffic in trafficRecords"
                :key="traffic.id"
                class="border-t border-slate-800 hover:bg-slate-800/50"
              >
                <td class="p-4">{{ traffic.timestamp }}</td>
                <td class="p-4">{{ traffic.sourceIp }}</td>
                <td class="p-4">{{ traffic.destinationIp }}</td>
                <td class="p-4">{{ traffic.protocol }}</td>
                <td class="p-4">{{ traffic.packetSize }} bytes</td>
                <td class="p-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs"
                    :class="predictionClass(traffic.prediction)"
                  >
                    {{ traffic.prediction }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import api from "../services/api";

const loading = ref(true);
const error = ref("");
const trafficRecords = ref([]);

const tcpCount = computed(() =>
  trafficRecords.value.filter((item) => item.protocol === "TCP").length
);

const udpCount = computed(() =>
  trafficRecords.value.filter((item) => item.protocol === "UDP").length
);

const maliciousCount = computed(() =>
  trafficRecords.value.filter((item) => item.prediction === "Malicious").length
);

const predictionClass = (prediction) => {
  if (prediction === "Malicious") return "bg-red-500/20 text-red-400";
  if (prediction === "Suspicious") return "bg-yellow-500/20 text-yellow-400";
  return "bg-green-500/20 text-green-400";
};

const loadTraffic = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await api.get("/api/traffic");
    trafficRecords.value = response.data;
  } catch (err) {
    error.value = "Failed to fetch traffic records. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadTraffic);
</script>