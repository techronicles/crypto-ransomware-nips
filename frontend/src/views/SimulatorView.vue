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
        :disabled="loading"
        class="bg-green-600 hover:bg-green-700 transition rounded-2xl p-6 text-left disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <h3 class="text-xl font-bold text-white">Simulate Benign Traffic</h3>
        <p class="text-green-100 mt-2 text-sm">
          Normal TCP traffic to public DNS.
        </p>
      </button>

      <button
        @click="simulateTraffic('suspicious')"
        :disabled="loading"
        class="bg-yellow-600 hover:bg-yellow-700 transition rounded-2xl p-6 text-left disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <h3 class="text-xl font-bold text-white">Simulate Suspicious Traffic</h3>
        <p class="text-yellow-100 mt-2 text-sm">
          High-volume TCP traffic pattern.
        </p>
      </button>

      <button
        @click="simulateTraffic('ransomware')"
        :disabled="loading"
        class="bg-red-600 hover:bg-red-700 transition rounded-2xl p-6 text-left disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <h3 class="text-xl font-bold text-white">Simulate Ransomware Attack</h3>
        <p class="text-red-100 mt-2 text-sm">
          SMB traffic pattern likely to trigger blocking.
        </p>
      </button>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="text-slate-400 mb-4">
      Running simulation... This may take a few seconds.
    </div>

    <!-- Error Message -->
    <div
      v-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6"
    >
      {{ error }}
    </div>

    <!-- Simulation Result -->
    <div
      v-if="result"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-6"
    >
      <h3 class="text-xl font-bold text-white mb-4">Simulation Result</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Prediction</p>
          <p class="text-2xl font-bold mt-1" :class="predictionClass(result.prediction)">
            {{ result.prediction || 'Unknown' }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Confidence</p>
          <p class="text-2xl font-bold mt-1">
            {{ formatConfidence(result.confidence) }}%
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Threat Type</p>
          <p class="text-white mt-1">
            {{ result.threat_type || '—' }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Traffic Log ID</p>
          <p class="text-white mt-1">
            {{ result.traffic_log_id || '—' }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">Alert Created</p>
          <p class="mt-1" :class="result.alert_created ? 'text-yellow-400' : 'text-slate-400'">
            {{ result.alert_created ? 'Yes' : 'No' }}
          </p>
        </div>

        <div class="border-b border-slate-800 pb-3">
          <p class="text-slate-400 text-sm">IP Blocked</p>
          <p class="mt-1" :class="result.blocked_ip_created ? 'text-red-400' : 'text-slate-400'">
            {{ result.blocked_ip_created ? 'Yes' : 'No' }}
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
          to="/blocked_ips"
          class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl transition"
        >
          View Blocked IPs
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const result = ref(null);
const router = useRouter();

// --- Predefined traffic samples ---
const samples = {
  benign: {
    source_ip: '192.168.1.80',
    destination_ip: '8.8.8.8',
    protocol: 'TCP',
    packet_size: 500,
  },
  suspicious: {
    source_ip: '192.168.1.150',
    destination_ip: '10.0.0.20',
    protocol: 'TCP',
    packet_size: 1300,
  },
  ransomware: {
    source_ip: '192.168.1.200',
    destination_ip: '10.0.0.5',
    protocol: 'SMB',
    packet_size: 1500,
  },
};

// --- Helper: Format confidence (ensure it's a number) ---
const formatConfidence = (confidence) => {
  if (confidence === undefined || confidence === null) return '0';
  const num = typeof confidence === 'number' ? confidence : parseFloat(confidence);
  return isNaN(num) ? '0' : Math.round(num * 100);
};

// --- Prediction text color class ---
const predictionClass = (prediction) => {
  if (prediction === 'Malicious') return 'text-red-400';
  if (prediction === 'Suspicious') return 'text-yellow-400';
  return 'text-green-400';
};

// --- Auth & redirect helper (stores warning for login page) ---
const clearAuthAndRedirect = (reason) => {
  sessionStorage.setItem('authWarning', reason);
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    router.push('/login');
  }, 1500);
};

// --- Simulate traffic ---
const simulateTraffic = async (type) => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';
  result.value = null;

  try {
    const response = await api.post('/api/v1/predict', samples[type]);
    const data = response.data;

    // Validate and set result with safe defaults
    result.value = {
      prediction: data.prediction || 'Unknown',
      confidence: typeof data.confidence === 'number' ? data.confidence : 0,
      threat_type: data.threat_type || 'None',
      traffic_log_id: data.traffic_log_id || null,
      alert_created: data.alert_created ?? false,
      blocked_ip_created: data.blocked_ip_created ?? false,
    };
  } catch (err) {
    console.error('Simulation error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired. Please log in again.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = `Simulation failed: ${err.response?.data?.detail || err.message || 'Unknown error'}`;
    }
  } finally {
    loading.value = false;
  }
};
</script>