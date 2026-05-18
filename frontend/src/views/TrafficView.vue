<template>
  <section>
    <div class="mb-6 flex justify-between items-center">
      <p class="text-slate-400">
        Traffic Monitor > Captured network traffic and ML predictions
      </p>

      <button
        @click="refreshTraffic"
        :disabled="loading"
        class="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-xl text-sm transition disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <!-- Loading State -->
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
          <h3 class="text-3xl font-bold mt-2 text-red-400">
            {{ maliciousCount }}
          </h3>
        </div>
      </div>

      <!-- Traffic Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <!-- Search + Filters -->
          <div class="mb-5 grid grid-cols-1 gap-4 lg:grid-cols-3">
            <!-- Search -->
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search source or destination IP..."
              class="w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-sky-400"
            />

            <!-- Protocol -->
            <select
              v-model="protocolFilter"
              class="w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-sky-400"
            >
              <option value="All">All Protocols</option>
              <option value="TCP">TCP</option>
              <option value="UDP">UDP</option>
            </select>

            <!-- Prediction -->
            <select
              v-model="predictionFilter"
              class="w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-sky-400"
            >
              <option value="All">All Predictions</option>
              <option value="Malicious">Malicious</option>
              <option value="Suspicious">Suspicious</option>
              <option value="Benign">Benign</option>
              <option value="Normal">Normal</option>
            </select>
          </div>

        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">Traffic Records</h3>
            <p class="mt-1 text-sm text-slate-400">
              Page {{ pagination.page }} of {{ pagination.pages }}
            </p>
          </div>

          <span
            class="px-4 py-2 rounded-xl text-sm bg-sky-500/20 text-sky-400"
          >
            {{ filteredTraffic.length }} shown / {{ pagination.total }} total
          </span>
        </div>

        <div v-if="filteredTraffic.length === 0" class="text-slate-400">
          No traffic records found.
        </div>

        <div v-else class="overflow-x-auto">
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
                v-for="traffic in filteredTraffic"
                :key="traffic.id"
                class="border-t border-slate-800 hover:bg-slate-800/50"
              >
                <td class="p-4">
                  {{ formatTimestamp(traffic.timestamp) }}
                </td>

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
            </tbody>
          </table>

          <!-- Backend Pagination Controls -->
          <div
            v-if="pagination.pages > 1"
            class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
          >
            <p class="text-sm text-slate-400">
              Showing {{ filteredTraffic.length }} records on page
              {{ pagination.page }} of {{ pagination.pages }}
              · Total {{ pagination.total }}
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
const trafficRecords = ref([]);

const searchQuery = ref('');
const protocolFilter = ref('All');
const predictionFilter = ref('All');
const currentPage = ref(1);
const itemsPerPage = ref(10);

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0,
  pages: 1,
});

let refreshInterval = null;

const router = useRouter();

//search
const filteredTraffic = computed(() => {
  return trafficRecords.value.filter((traffic) => {
    const sourceIp = String(
      traffic.sourceIp || traffic.source_ip || ''
    ).toLowerCase();

    const destinationIp = String(
      traffic.destinationIp || traffic.destination_ip || ''
    ).toLowerCase();

    const protocol = String(
      traffic.protocol || ''
    ).toLowerCase();

    const prediction = String(
      traffic.prediction || ''
    ).toLowerCase();

    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      sourceIp.includes(query) ||
      destinationIp.includes(query);

    const matchesProtocol =
      protocolFilter.value === 'All' ||
      traffic.protocol === protocolFilter.value;

    const matchesPrediction =
      predictionFilter.value === 'All' ||
      traffic.prediction === predictionFilter.value;

    return (
      matchesSearch &&
      matchesProtocol &&
      matchesPrediction
    );
  });
});


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

// --- Computed: Summary Stats for current page ---
const tcpCount = computed(() =>
  trafficRecords.value.filter((item) => item?.protocol === 'TCP').length
);

const udpCount = computed(() =>
  trafficRecords.value.filter((item) => item?.protocol === 'UDP').length
);

const maliciousCount = computed(() =>
  trafficRecords.value.filter((item) => item?.prediction === 'Malicious').length
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

// --- Auth Redirect ---
const clearAuthAndRedirect = (reason) => {
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');

  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    router.push('/login');
  }, 1500);
};

// --- Main Data Fetching using backend pagination ---
const loadTraffic = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/api/v1/traffic', {
      params: {
        page: currentPage.value,
        limit: itemsPerPage.value,
      },
    });

    const responseData = response.data;

    // Backend pagination shape:
    // { data: [...], pagination: { page, limit, total, pages } }
    trafficRecords.value = Array.isArray(responseData?.data)
      ? responseData.data
      : Array.isArray(responseData)
        ? responseData
        : [];

    pagination.value = responseData?.pagination || {
      page: currentPage.value,
      limit: itemsPerPage.value,
      total: trafficRecords.value.length,
      pages: 1,
    };

    currentPage.value = pagination.value.page || currentPage.value;
  } catch (err) {
    console.error('Traffic fetch error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect(
        'Access forbidden. Your token may be invalid or you lack permissions.'
      );
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch traffic records. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

const refreshTraffic = async () => {
  currentPage.value = 1;
  await loadTraffic();
};

const goToPage = async (page) => {
  if (
    page < 1 ||
    page > pagination.value.pages ||
    page === pagination.value.page
  ) {
    return;
  }

  currentPage.value = page;
  await loadTraffic();
};

// --- Polling ---
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