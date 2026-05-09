<template>
  <section>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <p class="text-slate-400">
          Alerts > Detected ransomware and suspicious network activities
        </p>
      </div>

      <button
        @click="refreshAlerts"
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
        <div>
          <h3 class="text-lg font-semibold text-white">All Alerts</h3>
          <p class="mt-1 text-sm text-slate-400">
            Page {{ pagination.page }} of {{ pagination.pages }}
          </p>
        </div>

        <span
          class="px-4 py-2 rounded-xl text-sm bg-red-500/20 text-red-400"
        >
          {{ pagination.total }} alerts
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

        <!-- Backend Pagination Controls -->
        <div
          v-if="pagination.pages > 1"
          class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
        >
          <p class="text-sm text-slate-400">
            Showing {{ alerts.length }} records on page {{ pagination.page }}
            of {{ pagination.pages }} · Total {{ pagination.total }}
          </p>

          <div class="flex items-center gap-2">
            <button
              @click="goToPage(pagination.page - 1)"
              :disabled="pagination.page === 1 || loading"
              class="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:bg-white/[0.08] disabled:opacity-40"
            >
              Previous
            </button>

            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :disabled="loading"
              :class="[
                'rounded-xl border px-4 py-2 text-sm transition disabled:opacity-40',
                page === pagination.page
                  ? 'border-sky-400/30 bg-sky-400 text-slate-950'
                  : 'border-white/10 bg-white/[0.04] text-slate-300 hover:bg-white/[0.08]'
              ]"
            >
              {{ page }}
            </button>

            <button
              @click="goToPage(pagination.page + 1)"
              :disabled="pagination.page === pagination.pages || loading"
              class="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:bg-white/[0.08] disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
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
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const successMessage = ref('');
const alerts = ref([]);
const updatingAlertId = ref(null);

const currentPage = ref(1);
const itemsPerPage = ref(10);

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0,
  pages: 1,
});

let refreshInterval = null;
let successTimeout = null;

const router = useRouter();

// --- Visible page buttons ---
const visiblePages = computed(() => {
  const total = pagination.value.pages || 1;
  const current = pagination.value.page || 1;
  const range = [];

  const start = Math.max(1, current - 1);
  const end = Math.min(total, current + 1);

  for (let page = start; page <= end; page += 1) {
    range.push(page);
  }

  return range;
});

// --- Helper: Format Timestamp ---
const formatTimestamp = (isoString) => {
  if (!isoString) return '—';

  const date = new Date(isoString);

  if (Number.isNaN(date.getTime())) {
    return isoString;
  }

  return new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date);
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
    router.push('/login');
  }, 1500);
};

// --- Fetch Alerts using backend pagination ---
const loadAlerts = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/api/v1/alerts', {
      params: {
        page: currentPage.value,
        limit: itemsPerPage.value,
      },
    });

    const responseData = response.data;

    // Backend pagination shape:
    // { data: [...], pagination: { page, limit, total, pages } }
    alerts.value = Array.isArray(responseData?.data)
      ? responseData.data
      : Array.isArray(responseData)
        ? responseData
        : [];

    pagination.value = responseData?.pagination || {
      page: currentPage.value,
      limit: itemsPerPage.value,
      total: alerts.value.length,
      pages: 1,
    };

    currentPage.value = pagination.value.page || currentPage.value;
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

const refreshAlerts = async () => {
  currentPage.value = 1;
  await loadAlerts();
};

const goToPage = async (page) => {
  if (page < 1 || page > pagination.value.pages || page === pagination.value.page) {
    return;
  }

  currentPage.value = page;
  await loadAlerts();
};

// --- Update Alert Status ---
const updateStatus = async (alertId, status) => {
  if (updatingAlertId.value === alertId) return;

  updatingAlertId.value = alertId;
  error.value = '';
  successMessage.value = '';

  if (successTimeout) clearTimeout(successTimeout);

  try {
    const response = await api.patch(`/api/v1/alerts/${alertId}/status`, { status });

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

// --- Polling ---
const startPolling = () => {
  if (refreshInterval) clearInterval(refreshInterval);

  refreshInterval = setInterval(() => {
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