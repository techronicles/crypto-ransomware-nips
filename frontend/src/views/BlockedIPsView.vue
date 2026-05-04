<template>
  <section>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <p class="text-slate-400">
          Blocked IPs > Malicious IP addresses blocked by the prevention module
        </p>
      </div>

      <div class="flex gap-3">
        <button
          @click="loadBlockedIps"
          :disabled="loading"
          class="bg-slate-700 hover:bg-slate-600 transition px-5 py-3 rounded-xl font-medium disabled:opacity-50"
        >
          {{ loading ? "Refreshing..." : "Refresh" }}
        </button>
        <button
          @click="showForm = !showForm"
          class="bg-blue-600 hover:bg-blue-700 transition px-5 py-3 rounded-xl font-medium"
        >
          Add Manual Block
        </button>
      </div>
    </div>

    <!-- Add Form -->
    <div
      v-if="showForm"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-6"
    >
      <h3 class="text-lg font-bold text-white mb-4">Add Manual IP Block</h3>

      <form @submit.prevent="submitBlockIp" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="form.ipAddress"
          type="text"
          placeholder="IP Address e.g. 192.168.1.100"
          class="bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-blue-500"
          required
        />

        <input
          v-model="form.reason"
          type="text"
          placeholder="Reason for blocking"
          class="bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-blue-500"
          required
        />

        <button
          type="submit"
          :disabled="submitting"
          class="bg-red-600 hover:bg-red-700 disabled:opacity-50 transition px-5 py-3 rounded-xl font-medium"
        >
          {{ submitting ? "Blocking..." : "Block IP" }}
        </button>
      </form>
    </div>

    <!-- Loading State (initial only) -->
    <div v-if="loading && blockedIps.length === 0" class="text-slate-400">
      Loading blocked IPs...
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
      <div class="mb-5">
        <span class="bg-red-500/20 text-red-400 px-4 py-2 rounded-xl text-sm">
          {{ blockedIps.length }} blocked IPs
        </span>
      </div>

      <div v-if="blockedIps.length === 0" class="text-slate-400">
        No blocked IPs found.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-800 text-slate-300">
            <tr>
              <th scope="col" class="text-left p-4">IP Address</th>
              <th scope="col" class="text-left p-4">Reason</th>
              <th scope="col" class="text-left p-4">Blocked At</th>
              <th scope="col" class="text-left p-4">Mode</th>
              <th scope="col" class="text-left p-4">Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="ip in blockedIps"
              :key="ip.id"
              class="border-t border-slate-800 hover:bg-slate-800/50"
            >
              <td class="p-4 font-medium text-slate-200">
                {{ ip.ip_address || '—' }}
              </td>
              <td class="p-4">{{ ip.reason || '—' }}</td>
              <td class="p-4">{{ formatTimestamp(ip.blocked_at) }}</td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="modeClass(ip.mode)"
                >
                  {{ ip.mode || 'Manual' }}
                </span>
              </td>
              <td class="p-4">
                <span
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="statusClass(ip.status)"
                >
                  {{ ip.status || 'Active' }}
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
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // optional – install if not already
import api from '../services/api';

// --- State ---
const loading = ref(false);
const submitting = ref(false);
const error = ref('');
const showForm = ref(false);
const blockedIps = ref([]);
let refreshInterval = null;

// Form state
const form = ref({
  ip_address: '',
  reason: '',
});

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
const modeClass = (mode) => {
  if (mode === 'Auto') return 'bg-purple-500/20 text-purple-400';
  return 'bg-blue-500/20 text-blue-400';
};

const statusClass = (status) => {
  if (status === 'Active') return 'bg-red-500/20 text-red-400';
  return 'bg-slate-500/20 text-slate-400';
};

// --- Authentication & Redirect ---
const clearAuthAndRedirect = (reason) => {
  // Clear stored tokens (adjust according to your auth implementation)
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
  // If you use Vuex/Pinia, also clear auth store here

  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    if (router) {
      router.push('/login');
    } else {
      window.location.href = '/login';
    }
  }, 1500);
};

// --- Fetch Blocked IPs ---
const loadBlockedIps = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/api/v1/blocked_ips');
    const data = response.data;
    // Ensure data is an array
    blockedIps.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Load blocked IPs error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch blocked IPs. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

// --- Submit New Block ---
const submitBlockIp = async () => {
  if (submitting.value) return;

  submitting.value = true;
  error.value = '';

  try {
    const response = await api.post('/api/v1/blocked_ips', {
      ipAddress: form.value.ipAddress,
      reason: form.value.reason,
    });

    // Prepend new block to the list
    blockedIps.value.unshift(response.data);

    // Reset form and hide it
    form.value = { ipAddress: '', reason: '' };
    showForm.value = false;
  } catch (err) {
    console.error('Submit block IP error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.response?.status === 400) {
      error.value = err.response.data?.message || 'Invalid IP address or missing data.';
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to block IP. Please try again later.';
    }
  } finally {
    submitting.value = false;
  }
};

// --- Polling (every 30 seconds) ---
const startPolling = () => {
  if (refreshInterval) clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    // Don't poll if we're already loading, submitting, or in a redirect state
    if (!loading.value && !submitting.value && !error.value?.includes('Redirecting')) {
      loadBlockedIps();
    }
  }, 30000);
};

// --- Lifecycle ---
onMounted(() => {
  loadBlockedIps();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>