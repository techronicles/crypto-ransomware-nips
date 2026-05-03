<template>
  <section>
    <!-- Header with Refresh Button -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <p class="text-slate-400">
          Dashboard > Real‑time network security overview
        </p>
      </div>
      <button
        @click="loadDashboard"
        :disabled="loading"
        class="bg-slate-800 hover:bg-slate-700 transition px-5 py-3 rounded-xl font-medium disabled:opacity-50"
      >
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <!-- Loading State (initial only) -->
    <div v-if="loading && !dashboardLoaded" class="text-slate-400">
      Loading dashboard data...
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5 mb-8">
        <StatCard
          title="Total Traffic"
          :value="summary.total_traffic"
          subtitle="Packets analyzed"
        />
        <StatCard
          title="Suspicious Traffic"
          :value="summary.suspicious_traffic"
          subtitle="Requires attention"
          statusClass="text-yellow-400"
        />
        <StatCard
          title="Blocked IPs"
          :value="summary.blocked_ips"
          subtitle="Active blocks"
          statusClass="text-red-400"
        />
        <StatCard
          title="Model Accuracy"
          :value="summary.model_accuracy + '%'"
          :subtitle="summary.model_name"
          statusClass="text-green-400"
        />
      </div>

      <!-- Recent Alerts Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 class="text-xl font-bold text-white mb-2">Recent Alerts</h3>
        <p class="text-slate-400 mb-5">Latest suspicious network activities</p>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-800 text-slate-300">
              <tr>
                <th scope="col" class="text-left p-4">Time</th>
                <th scope="col" class="text-left p-4">Source IP</th>
                <th scope="col" class="text-left p-4">Threat</th>
                <th scope="col" class="text-left p-4">Severity</th>
                <th scope="col" class="text-left p-4">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="alert in alerts"
                :key="alert.id"
                class="border-t border-slate-800 hover:bg-slate-800/50"
              >
                <td class="p-4">{{ formatTimestamp(alert.timestamp) }}</td>
                <td class="p-4">{{ alert.source_ip || '—' }}</td>
                <td class="p-4">{{ alert.threat_type || '—' }}</td>
                <td class="p-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs font-medium"
                    :class="severityClass(alert.severity)"
                  >
                    {{ alert.severity || 'Unknown' }}
                  </span>
                </td>
                <td class="p-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs font-medium"
                    :class="statusClass(alert.status)"
                  >
                    {{ alert.status || 'New' }}
                  </span>
                </td>
              </tr>
              <tr v-if="alerts.length === 0">
                <td colspan="5" class="text-center p-4 text-slate-400">
                  No recent alerts.
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
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import StatCard from '../components/StatCard.vue';
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const dashboardLoaded = ref(false);  // tracks if we have ever loaded data
const summary = ref({
  total_traffic: 0,
  suspicious_traffic: 0,
  blocked_ips: 0,
  model_accuracy: 0,
  model_name: '',
});
const alerts = ref([]);
let refreshInterval = null;

const router = useRouter();

// --- Helpers ---
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

const severityClass = (severity) => {
  if (severity === 'High') return 'bg-red-500/20 text-red-400';
  if (severity === 'Medium') return 'bg-yellow-500/20 text-yellow-400';
  if (severity === 'Low') return 'bg-green-500/20 text-green-400';
  return 'bg-gray-500/20 text-gray-400';
};

const statusClass = (status) => {
  const classes = {
    Blocked: 'bg-red-500/20 text-red-400',
    Monitoring: 'bg-yellow-500/20 text-yellow-400',
    Reviewed: 'bg-blue-500/20 text-blue-400',
    Resolved: 'bg-green-500/20 text-green-400',
    'False Positive': 'bg-slate-500/20 text-slate-300',
  };
  return classes[status] || 'bg-slate-500/20 text-slate-400';
};

// --- Auth Handling with Message for Login Page ---
const clearAuthAndRedirect = (reason) => {
  // Store the warning message so login page can display it
  sessionStorage.setItem('authWarning', reason);
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');

  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    router.push('/login');
  }, 1500);
};

// --- Load Dashboard Data ---
const loadDashboard = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const [summaryResponse, alertsResponse] = await Promise.all([
      api.get('/api/v1/dashboard/summary'),
      api.get('/api/v1/alerts'),
    ]);

    // Validate and set summary
    const summaryData = summaryResponse.data;
    summary.value = {
      total_traffic: summaryData.total_traffic ?? 0,
      suspicious_traffic: summaryData.suspicious_traffic ?? 0,
      blocked_ips: summaryData.blocked_ips ?? 0,
      model_accuracy: summaryData.model_accuracy ?? 0,
      model_name: summaryData.model_name ?? 'N/A',
    };

    // Ensure alerts is an array
    alerts.value = Array.isArray(alertsResponse.data) ? alertsResponse.data : [];
    dashboardLoaded.value = true;
  } catch (err) {
    console.error('Dashboard load error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired. Please log in again.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch dashboard data. Please try again later.';
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
      loadDashboard();
    }
  }, 30000);
};

// --- Lifecycle ---
onMounted(() => {
  loadDashboard();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>