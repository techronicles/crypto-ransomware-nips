<template>
  <section>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <p class="text-slate-400">
          Alerts > Detected ransomware and suspicious network activities
        </p>
      </div>

      <button
        @click="loadAlerts"
        :disabled="loading"
        class="bg-slate-800 hover:bg-slate-700 transition px-5 py-3 rounded-xl font-medium disabled:opacity-50"
      >
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <!-- Loading State (initial only) -->
    <div v-if="loading && alerts.length === 0" class="text-slate-400">
      Loading alerts...
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <!-- Data Display -->
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
              <th scope="col" class="text-left p-4">Time</th>
              <th scope="col" class="text-left p-4">Source IP</th>
              <th scope="col" class="text-left p-4">Destination IP</th>
              <th scope="col" class="text-left p-4">Threat</th>
              <th scope="col" class="text-left p-4">Severity</th>
              <th scope="col" class="text-left p-4">Status</th>
              <th scope="col" class="text-left p-4">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="alert in alerts"
              :key="alert.id"
              class="border-t border-slate-800 hover:bg-slate-800/50 transition"
            >
              <td class="p-4">{{ formatTimestamp(alert.timestamp) }}</td>
             <td class="p-4 font-medium text-slate-200">
                {{ alert.sourceIp || alert.source_ip || '—' }}
              </td>

              <td class="p-4">
                {{ alert.destinationIp || alert.destination_ip || '—' }}
              </td>

              <td class="p-4">
                {{ alert.threatType || alert.threat_type || '—' }}
              </td>
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
              <td class="p-4">
                <div class="flex flex-wrap gap-2">
                  <button
                    @click="updateStatus(alert.id, 'Reviewed')"
                    :disabled="updatingAlertId === alert.id"
                    class="px-3 py-2 rounded-lg text-xs bg-blue-600 hover:bg-blue-700 transition disabled:opacity-50"
                  >
                    Review
                  </button>

                  <button
                    @click="updateStatus(alert.id, 'Resolved')"
                    :disabled="updatingAlertId === alert.id"
                    class="px-3 py-2 rounded-lg text-xs bg-green-600 hover:bg-green-700 transition disabled:opacity-50"
                  >
                    Resolve
                  </button>

                  <button
                    @click="updateStatus(alert.id, 'False Positive')"
                    :disabled="updatingAlertId === alert.id"
                    class="px-3 py-2 rounded-lg text-xs bg-slate-700 hover:bg-slate-600 transition disabled:opacity-50"
                  >
                    False +
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Success Message -->
    <div
      v-if="successMessage"
      class="mt-4 bg-green-500/10 border border-green-500/30 text-green-400 p-4 rounded-xl"
    >
      {{ successMessage }}
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // optional – install if not already
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const successMessage = ref('');
const alerts = ref([]);
const updatingAlertId = ref(null); // prevent concurrent updates on same alert
let refreshInterval = null;
let successTimeout = null;

// Router (if using Vue Router, otherwise undefined)
const router = useRouter();

// --- Helper: Format Timestamp (ISO → readable) ---
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

// --- Styling Helpers ---
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

// --- Authentication & Redirect ---
const clearAuthAndRedirect = (reason) => {
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');

  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    if (router) {
      router.push('/login');
    } else {
      window.location.href = '/login';
    }
  }, 1500);
};

// --- Fetch Alerts ---
const loadAlerts = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/api/v1/alerts');
    const data = response.data;
    alerts.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Load alerts error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch alerts. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

// --- Update Alert Status ---
const updateStatus = async (alertId, status) => {
  // Prevent multiple updates on the same alert
  if (updatingAlertId.value === alertId) return;

  updatingAlertId.value = alertId;
  error.value = '';
  successMessage.value = '';

  // Clear any existing success timeout
  if (successTimeout) clearTimeout(successTimeout);

  try {
    const response = await api.patch(`/api/v1/alerts/${alertId}/status`, { status });

    // Update alert in the list
    alerts.value = alerts.value.map((alert) =>
      alert.id === alertId ? response.data : alert
    );

    successMessage.value = `Alert marked as ${status}.`;
    successTimeout = setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (err) {
    console.error('Update status error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      const detail = err.response?.data?.detail || err.message;
      error.value = `Failed to update alert status: ${detail}`;
    }
  } finally {
    updatingAlertId.value = null;
  }
};

// --- Polling (every 30 seconds) ---
const startPolling = () => {
  if (refreshInterval) clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    // Don't poll during update or redirect
    if (!loading.value && !updatingAlertId.value && !error.value?.includes('Redirecting')) {
      loadAlerts();
    }
  }, 30000);
};

// --- Lifecycle ---
onMounted(() => {
  loadAlerts();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
  if (successTimeout) clearTimeout(successTimeout);
});
</script>