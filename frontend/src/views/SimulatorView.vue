<template>
  <section>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-white">Attack Simulator</h2>
      <p class="text-slate-400">
        Simulate network traffic and test AI-driven ransomware detection.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
      <button
        @click="simulateTraffic('benign')"
        class="bg-green-600 hover:bg-green-700 transition rounded-2xl p-6 text-left"
      >
        <h3 class="text-xl font-bold text-white">Simulate Benign Traffic</h3>
        <p class="text-green-100 mt-2 text-sm">
          Normal TCP traffic to public DNS.
        </p>
      </button>

      <button
        @click="simulateTraffic('suspicious')"
        class="bg-yellow-600 hover:bg-yellow-700 transition rounded-2xl p-6 text-left"
      >
        <h3 class="text-xl font-bold text-white">Simulate Suspicious Traffic</h3>
        <p class="text-yellow-100 mt-2 text-sm">
          High-volume TCP traffic pattern.
        </p>
      </button>

      <button
        @click="simulateTraffic('ransomware')"
        class="bg-red-600 hover:bg-red-700 transition rounded-2xl p-6 text-left"
      >
        <h3 class="text-xl font-bold text-white">Simulate Ransomware Attack</h3>
        <p class="text-red-100 mt-2 text-sm">
          SMB traffic pattern likely to trigger blocking.
        </p>
      </button>
    </div>

    <div v-if="loading" class="text-slate-400">
      Running simulation...
    </div>

    <div
      v-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6"
    >
      {{ error }}
    </div>

    <div
      v-if="result"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-6"
    >
      <h3 class="text-xl font-bold text-white mb-4">Simulation Result</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Prediction</p>
          <p class="text-2xl font-bold mt-1" :class="predictionClass(result.prediction)">
            {{ result.prediction }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Confidence</p>
          <p class="text-2xl font-bold mt-1">
            {{ Math.round(result.confidence * 100) }}%
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Threat Type</p>
          <p class="text-white mt-1">
            {{ result.threatType }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Traffic Log ID</p>
          <p class="text-white mt-1">
            {{ result.trafficLogId }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Alert Created</p>
          <p class="mt-1" :class="result.alertCreated ? 'text-yellow-400' : 'text-slate-400'">
            {{ result.alertCreated ? 'Yes' : 'No' }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">IP Blocked</p>
          <p class="mt-1" :class="result.blockedIpCreated ? 'text-red-400' : 'text-slate-400'">
            {{ result.blockedIpCreated ? 'Yes' : 'No' }}
          </p>
        </div>
      </div>

      <div class="mt-6 flex flex-wrap gap-3">
        <RouterLink
          to="/traffic"
          class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl transition"
        >
          View Traffic Logs
        </RouterLink>

        <RouterLink
          to="/alerts"
          class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl transition"
        >
          View Alerts
        </RouterLink>

        <RouterLink
          to="/blocked-ips"
          class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl transition"
        >
          View Blocked IPs
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";

const loading = ref(false);
const error = ref("");
const result = ref(null);

const samples = {
  benign: {
    sourceIp: "192.168.1.80",
    destinationIp: "8.8.8.8",
    protocol: "TCP",
    packetSize: 500,
  },
  suspicious: {
    sourceIp: "192.168.1.150",
    destinationIp: "10.0.0.20",
    protocol: "TCP",
    packetSize: 1300,
  },
  ransomware: {
    sourceIp: "192.168.1.200",
    destinationIp: "10.0.0.5",
    protocol: "SMB",
    packetSize: 1500,
  },
};

const simulateTraffic = async (type) => {
  try {
    loading.value = true;
    error.value = "";
    result.value = null;

    const response = await api.post("/api/predict", samples[type]);
    result.value = response.data;
  } catch (err) {
    error.value = "Simulation failed. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const predictionClass = (prediction) => {
  if (prediction === "Malicious") return "text-red-400";
  if (prediction === "Suspicious") return "text-yellow-400";
  return "text-green-400";
};
</script>