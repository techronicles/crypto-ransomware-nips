<template>
  <section>
    <div class="mb-6 flex justify-between items-center">
      <p class="text-slate-400">Traffic Monitor > Captured network traffic and ML predictions</p>
      <button
        @click="loadTraffic"
        :disabled="loading"
        class="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-xl text-sm transition disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <!-- Loading State (only on initial load) -->
    <div v-if="loading && trafficRecords.length === 0" class="text-slate-400">
      Loading traffic records...
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <!-- Data Display -->
    <div v-else>
      <!-- Summary Cards -->
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
          <h3 class="text-3xl font-bold mt-2 text-red-400">{{ maliciousCount }}</h3>
        </div>
      </div>

      <!-- Traffic Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-800 text-slate-300">
              <tr>
                <th scope="col" class="text-left p-4">Time</th>
                <th scope="col" class="text-left p-4">Source IP</th>
                <th scope="col" class="text-left p-4">Destination IP</th>
                <th scope="col" class="text-left p-4">Protocol</th>
                <th scope="col" class="text-left p-4">Packet Size</th>
                <th scope="col" class="text-left p-4">Prediction</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="traffic in trafficRecords"
                :key="traffic.id"
                class="border-t border-slate-800 hover:bg-slate-800/50"
              >
                <td class="p-4">{{ formatTimestamp(traffic.timestamp) }}</td>
                <td class="p-4">
                    {{ traffic.sourceIp || traffic.source_ip || '—' }}
                  </td>

                  <td class="p-4">
                    {{ traffic.destinationIp || traffic.destination_ip || '—' }}
                  </td>

                  <td class="p-4">
                    {{ traffic.protocol || '—' }}
                  </td>

                  <td class="p-4">
                    {{ traffic.packetSize ?? traffic.packet_size ?? '—' }} bytes
                  </td>
                                  <td class="p-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs font-medium"
                    :class="predictionClass(traffic.prediction)"
                  >
                    {{ traffic.prediction || 'Unknown' }}
                  </span>
                </td>
              </tr>
              <tr v-if="trafficRecords.length === 0">
                <td colspan="6" class="text-center p-4 text-slate-400">
                  No traffic records found.
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
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // optional – install vue-router if not already
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const trafficRecords = ref([]);
let refreshInterval = null;

// Router instance (undefined if not using Vue Router)
const router = useRouter();

// --- Computed: Summary Stats (safe) ---
const tcpCount = computed(() =>
  trafficRecords.value.filter(item => item?.protocol === 'TCP').length
);
const udpCount = computed(() =>
  trafficRecords.value.filter(item => item?.protocol === 'UDP').length
);
const maliciousCount = computed(() =>
  trafficRecords.value.filter(item => item?.prediction === 'Malicious').length
);

// --- Helper: Prediction Styling ---
const predictionClass = (prediction) => {
  const classes = {
    Malicious: 'bg-red-500/20 text-red-400',
    Suspicious: 'bg-yellow-500/20 text-yellow-400',
    Benign: 'bg-green-500/20 text-green-400',
    Normal: 'bg-green-500/20 text-green-400',
  };
  return classes[prediction] || 'bg-gray-500/20 text-gray-400';
};

// --- Helper: Format Timestamp ---
const formatTimestamp = (isoString) => {
  if (!isoString) return '—';
  try {
    return new Intl.DateTimeFormat(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(new Date(isoString));
  } catch {
    return isoString;
  }
};

// --- Clear authentication data (customise based on your storage) ---
const clearAuthAndRedirect = (reason) => {
  // Remove token from localStorage/sessionStorage
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
  // If you use Vuex/Pinia, also clear auth state
  // e.g., authStore.logout();

  error.value = `${reason} Redirecting to login...`;

  // Give user a moment to read the message
  setTimeout(() => {
    if (router) {
      router.push('/login');
    } else {
      window.location.href = '/login';
    }
  }, 1500);
};

// --- Main Data Fetching ---
const loadTraffic = async () => {
  if (loading.value) return;

  loading.value = true;
  // Don't clear existing traffic on background refresh – keeps UI responsive
  // Only clear error if we succeed
  const previousError = error.value;
  error.value = '';

  try {
    const response = await api.get('/api/v1/traffic');
    const data = response.data;

    // Validate response
    trafficRecords.value = Array.isArray(data) ? data : [];
    // Clear any previous error on success
    if (previousError) error.value = '';
  } catch (err) {
    console.error('Traffic fetch error:', err);

    // Handle authentication/authorization errors (401 OR 403)
    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch traffic records. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

// --- Polling (every 30 seconds) ---
const startPolling = () => {
  if (refreshInterval) clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    if (!loading.value && !error.value?.includes('Redirecting')) {
      loadTraffic();
    }
  }, 30000);
};

// --- Lifecycle ---
onMounted(() => {
  loadTraffic();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>