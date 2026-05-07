<template>
  <section class="space-y-6">
   

    <!-- Error -->
    <div
      v-if="error"
      class="rounded-2xl border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-300"
    >
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading && !dashboardLoaded"
      class="rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-slate-400"
    >
      Loading dashboard data...
    </div>

    <div v-else>
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
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
          :subtitle="summary.modelName"
          statusClass="text-green-400"
        />
      </div>

      <!-- System strip -->
      <div class="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-4">
        <div class="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-4">
          <p class="text-xs text-slate-400">Backend</p>
          <p class="mt-1 font-semibold text-emerald-300">Online</p>
        </div>

        <div class="rounded-2xl border border-sky-400/20 bg-sky-400/10 p-4">
          <p class="text-xs text-slate-400">Database</p>
          <p class="mt-1 font-semibold text-sky-300">Connected</p>
        </div>

        <div class="rounded-2xl border border-purple-400/20 bg-purple-400/10 p-4">
          <p class="text-xs text-slate-400">Detection Engine</p>
          <p class="mt-1 font-semibold text-purple-300">Active</p>
        </div>

        <div class="rounded-2xl border border-yellow-400/20 bg-yellow-400/10 p-4">
          <p class="text-xs text-slate-400">Prevention Mode</p>
          <p class="mt-1 font-semibold text-yellow-300">Log Only</p>
        </div>
      </div>

      <!-- Recent Alerts -->
      <div class="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6">
        <div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 class="text-xl font-bold text-white">
              Recent Alerts
            </h3>
            <p class="mt-1 text-sm text-slate-400">
              Latest suspicious network activities detected by the system.
            </p>
          </div>

          <span class="rounded-2xl border border-red-400/20 bg-red-400/10 px-4 py-2 text-sm font-medium text-red-300">
            {{ alerts.length }} alerts
          </span>
        </div>

        <div v-if="alerts.length === 0" class="rounded-2xl border border-white/10 p-6 text-center text-slate-400">
          No recent alerts.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-900/80 text-slate-300">
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
                class="border-t border-white/10 hover:bg-white/[0.03]"
              >
                <td class="p-4 text-slate-400">
                  {{ formatTimestamp(alert.timestamp) }}
                </td>

                <td class="p-4 font-medium text-slate-200">
                  {{ alert.sourceIp || '—' }}
                </td>

                <td class="p-4">
                  {{ alert.threatType || '—' }}
                </td>

                <td class="p-4">
                  <span
                    class="rounded-full px-3 py-1 text-xs font-medium"
                    :class="severityClass(alert.severity)"
                  >
                    {{ alert.severity || 'Unknown' }}
                  </span>
                </td>

                <td class="p-4">
                  <span
                    class="rounded-full px-3 py-1 text-xs font-medium"
                    :class="statusClass(alert.status)"
                  >
                    {{ alert.status || 'New' }}
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
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import StatCard from '../components/StatCard.vue';
import api from '../services/api';

const router = useRouter();

const loading = ref(false);
const error = ref('');
const dashboardLoaded = ref(false);
const alerts = ref([]);

const summary = ref({
  totalTraffic: 0,
  suspiciousTraffic: 0,
  blockedIps: 0,
  modelAccuracy: 0,
  modelName: 'N/A',
});

let refreshInterval = null;

const normalizeSummary = (data) => {
  return {
    totalTraffic: data.totalTraffic ?? data.total_traffic ?? 0,
    suspiciousTraffic: data.suspiciousTraffic ?? data.suspicious_traffic ?? 0,
    blockedIps: data.blockedIps ?? data.blocked_ips ?? 0,
    modelAccuracy: data.modelAccuracy ?? data.model_accuracy ?? 0,
    modelName: data.modelName ?? data.model_name ?? 'N/A',
  };
};

const normalizeAlert = (alert) => {
  return {
    id: alert.id,
    timestamp: alert.timestamp,
    sourceIp: alert.sourceIp ?? alert.source_ip,
    threatType: alert.threatType ?? alert.threat_type,
    severity: alert.severity,
    status: alert.status,
  };
};

const formatTimestamp = (value) => {
  if (!value) return '—';

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

const severityClass = (severity) => {
  if (severity === 'High') return 'bg-red-500/20 text-red-400';
  if (severity === 'Medium') return 'bg-yellow-500/20 text-yellow-400';
  if (severity === 'Low') return 'bg-green-500/20 text-green-400';
  return 'bg-slate-500/20 text-slate-400';
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

const clearAuthAndRedirect = (message) => {
  sessionStorage.setItem('authWarning', message);
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');

  router.push('/login');
};

const loadDashboard = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const [summaryResponse, alertsResponse] = await Promise.all([
      api.get('/api/v1/dashboard/summary'),
      api.get('/api/v1/alerts'),
    ]);

    summary.value = normalizeSummary(summaryResponse.data);

    const alertsData = Array.isArray(alertsResponse.data)
      ? alertsResponse.data
      : [];

    alerts.value = alertsData.map(normalizeAlert);

    dashboardLoaded.value = true;
  } catch (err) {
    console.error('Dashboard load error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired. Please log in again.');
      return;
    }

    if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Please log in again.');
      return;
    }

    if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
      return;
    }

    error.value = 'Failed to fetch dashboard data. Please try again later.';
  } finally {
    loading.value = false;
  }
};

const startPolling = () => {
  refreshInterval = setInterval(() => {
    if (!loading.value) {
      loadDashboard();
    }
  }, 30000);
};

onMounted(() => {
  loadDashboard();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
</script>