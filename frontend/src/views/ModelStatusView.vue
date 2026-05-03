<template>
  <section>
    <!-- Header with Refresh Button -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <p class="text-slate-400">
          ML Model Status > Detection model performance and deployment status
        </p>
      </div>
      <button
        @click="loadModelStatus"
        :disabled="loading"
        class="bg-slate-800 hover:bg-slate-700 transition px-5 py-3 rounded-xl font-medium disabled:opacity-50"
      >
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <!-- Loading State (initial only) -->
    <div v-if="loading && !modelLoaded" class="text-slate-400">
      Loading model status...
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
      <!-- Performance Metrics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Accuracy</p>
          <h3 class="text-3xl font-bold mt-2 text-green-400">
            {{ model.performance.accuracy }}%
          </h3>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Precision</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.performance.precision }}%
          </h3>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Recall</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.performance.recall }}%
          </h3>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">F1 Score</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.performance.f1_score }}%
          </h3>
        </div>
      </div>

      <!-- Model Information -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 class="text-xl font-bold mb-5">Current Model Information</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <InfoRow label="Model Name" :value="model.model_name" />
          <InfoRow label="Version" :value="model.version" />
          <InfoRow label="Dataset" :value="model.dataset" />

          <div class="flex justify-between border-b border-slate-800 pb-3">
            <span class="text-slate-400">Status / Active</span>
            <span class="text-green-400">{{ model.status }} / {{ model.active ? 'Active' : 'Inactive' }}</span>
          </div>

          <InfoRow label="Last Trained" :value="formatTimestamp(model.last_trained)" />

          <div class="flex justify-between border-b border-slate-800 pb-3">
            <span class="text-slate-400">Prediction Mode</span>
            <span class="text-yellow-400">{{ model.prediction_mode }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref, h, defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

// --- State ---
const loading = ref(false);
const error = ref('');
const modelLoaded = ref(false);   // tracks if we have ever loaded data
let refreshInterval = null;

// Router for redirect
const router = useRouter();

// --- Model data structure with defaults ---
const model = ref({
  model_name: '—',
  version: '—',
  dataset: '—',
  performance: {
    accuracy: 0,
    precision: 0,
    recall: 0,
    f1_score: 0,
  },
  last_trained: null,
  status: 'Unknown',
  active: false,
  prediction_mode: 'Unknown',
});

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

// --- Auth Handling with Message for Login Page ---
const clearAuthAndRedirect = (reason) => {
  sessionStorage.setItem('authWarning', reason);
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');

  error.value = `${reason} Redirecting to login...`;

  setTimeout(() => {
    router.push('/login');
  }, 1500);
};

// --- InfoRow Component (for model info display) ---
const InfoRow = defineComponent({
  props: {
    label: String,
    value: [String, Number],
  },
  setup(props) {
    return () =>
      h('div', { class: 'flex justify-between border-b border-slate-800 pb-3' }, [
        h('span', { class: 'text-slate-400' }, props.label),
        h('span', { class: 'text-white' }, props.value ?? '—'),
      ]);
  },
});

// --- Fetch Model Status ---
const loadModelStatus = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/api/v1/ml_model/info');
    const data = response.data;

    // Validate and assign with safe defaults
    model.value = {
      model_name: data.model_name || '—',
      version: data.version || '—',
      dataset: data.dataset || '—',
      performance: {
        accuracy: data.performance?.accuracy ?? 0,
        precision: data.performance?.precision ?? 0,
        recall: data.performance?.recall ?? 0,
        f1_score: data.performance?.f1_score ?? 0,
      },
      last_trained: data.last_trained || null,
      status: data.status || 'Unknown',
      active: data.active ?? false,
      prediction_mode: data.prediction_mode || 'Unknown',
    };
    modelLoaded.value = true;
  } catch (err) {
    console.error('Model status error:', err);

    if (err.response?.status === 401) {
      clearAuthAndRedirect('Your session has expired. Please log in again.');
    } else if (err.response?.status === 403) {
      clearAuthAndRedirect('Access forbidden. Your token may be invalid or you lack permissions.');
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to backend. Is the server running?';
    } else {
      error.value = 'Failed to fetch model status. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

// --- Polling (every 60 seconds – model changes rarely) ---
const startPolling = () => {
  if (refreshInterval) clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    if (!loading.value && !error.value?.includes('Redirecting')) {
      loadModelStatus();
    }
  }, 60000);
};

// --- Lifecycle ---
onMounted(() => {
  loadModelStatus();
  startPolling();
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>